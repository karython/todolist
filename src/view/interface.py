import flet as ft
import threading
from datetime import datetime, timedelta
from services.service import criar_tarefa, listar_tarefas, editar_tarefa, alternar_status_tarefa, deletar_tarefa

class TarefaUI(ft.Row):
    def __init__(self, tarefa, remover_callback, status_callback, lista_tarefas, modo_selecao=False):
        super().__init__()
        self.tarefa = tarefa
        self.remover_callback = remover_callback
        self.status_callback = status_callback
        self.modo_selecao = modo_selecao
        self.lista_tarefas = lista_tarefas  

        self.checkbox_status = ft.Checkbox(value=tarefa.status, on_change=self.alternar_status,)
        self.checkbox_status.fill_color = self.definir_cor_classe()

        self.checkbox_selecao = ft.Checkbox(value=False, visible=self.modo_selecao,)
        self.botao_editar = ft.IconButton(icon=ft.icons.EDIT, on_click=self.abrir_modal_edicao, visible=self.modo_selecao,)
        self.texto_nome = ft.GestureDetector(
            content=ft.Container(
                content=ft.Text(
                    tarefa.nome,
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.UNDERLINE,
                        decoration_color=self.definir_cor_prioridade(),
                        decoration_thickness=2.0
                    )
                ),
                padding=10,
                ink=True,
                border_radius=5,
                expand=True,
                bgcolor=ft.colors.TRANSPARENT
            ),
            on_tap=self.mostrar_detalhes
        )

        self.page = self.lista_tarefas.page



        self.controls = [self.checkbox_selecao, self.checkbox_status, self.texto_nome, self.botao_editar]

    def definir_cor_classe(self):
        return {
            'saude': 'blue',
            'casa': 'orange',
            'trabalho': 'green',
            'lazer': 'purple'
        }.get(self.tarefa.classe.value, 'gray')

    def definir_cor_prioridade(self):
        return {
            'alta': 'red',
            'media': 'yellow',
            'baixa': 'gray'
        }.get(self.tarefa.prioridade.value, 'gray')
    
    def abrir_modal_edicao(self, e):
        dialogo = self.lista_tarefas.dialogo_edicao(self.tarefa)
        self.page.dialog = dialogo
        self.page.overlay.append(dialogo)  
        expand=True
        dialogo.open = True
        self.page.update()

    def alternar_status(self, e):
        alternar_status_tarefa(self.tarefa.id, self.checkbox_status.value)
        self.status_callback()

    def mostrar_detalhes(self, e):
        print("[DEBUG] Mostrar detalhes da tarefa:", self.tarefa.nome)
        # Obter os detalhes da tarefa
        prioridade = self.tarefa.prioridade.value.capitalize()
        classe = self.tarefa.classe.value.capitalize()
        status = "Concluída" if self.tarefa.status else "Pendente"
        data_inicio = self.tarefa.data_inicio.strftime("%d/%m/%Y %H:%M")
        data_entrega = self.tarefa.data_entrega.strftime("%d/%m/%Y %H:%M")

        # Criar o conteúdo do diálogo
        conteudo = ft.Column([
            ft.Text(f"Nome: {self.tarefa.nome}", weight="bold"),
            ft.Text(f"Classe: {classe}"),
            ft.Text(f"Prioridade: {prioridade}"),
            ft.Text(f"Status: {status}"),
            ft.Text(f"Início: {data_inicio}"),
            ft.Text(f"Entrega: {data_entrega}"),
            ft.Text(f"Descrição:", size=13, weight="bold"),
            ft.Text(self.tarefa.descricao or "Sem descrição."),
        ], 
        scroll="auto", tight=True,expand=True)

        # Criar o diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text("Detalhes da tarefa"),
            content=conteudo,
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: self.fechar_dialogo())
            ],
            modal=False,  # Não modal
            expand=True
        )

        # Exibir o diálogo
        self.page.dialog = dialogo
        if dialogo not in self.page.overlay:
            self.page.overlay.append(dialogo)
        self.page.dialog.open = True
        self.page.update()

    def fechar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

class ListaTarefas(ft.Column):
    def __init__(self, page):
        super().__init__(scroll="auto", expand=True)

        self.page = page
        self.page.title = "Lista de Tarefas Inteligente"

        self.lista_tarefas = ft.Column()
        self.pesquisa = ft.TextField(hint_text="Pesquisar...", on_change=self.pesquisar_tarefas,expand=True)
        self.modo_edicao = False
        self.filtro_prioridade = ft.Dropdown(
            label="Prioridade",
            value="todas",
            on_change=self.filtrar_tarefas,
            expand=True,
            options=[
                ft.dropdown.Option("todas", "Todas"),
                ft.dropdown.Option("alta", "Alta"),
                ft.dropdown.Option("media", "Média"),
                ft.dropdown.Option("baixa", "Baixa"),
            ],
        )
        
        self.filtro_status = ft.Tabs(
            selected_index=0,
            on_change=self.filtrar_tarefas,
            tabs=[ft.Tab(text="ativas"), ft.Tab(text="completas"), ft.Tab(text="atrasadas")],
            expand=True,
        )

        self.calendario = ft.DatePicker(
            on_change=self.definir_data,
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2100, 12, 31),
            expand=True,
        )

        self.menu_lateral = ft.NavigationDrawer(controls=[
            ft.ListTile(title=ft.Text("Filtrar por Classe"), dense=True),
            ft.ListTile(title=ft.Text("Todas as Classes"),on_click=lambda e: self.aplicar_filtro_geral()),
            *[ft.ListTile(title=ft.Text(c.capitalize()), on_click=lambda e, c=c: self.filtrar_por_classe(c))
              for c in ["saude", "casa", "trabalho", "lazer"]],
            ft.Divider(),
            ft.ListTile(title=ft.Text("Personalizar Tema"), dense=True),
            ft.Switch(label="Modo Escuro", on_change=self.mudar_tema),
        ])
        self.filtro_classe_atual = None  # None = todas


        self.banner = ft.Banner(
            bgcolor="red",
            leading=ft.Icon(ft.icons.ERROR_OUTLINE, color="white"),
            content=ft.Text("Mensagem de erro aqui", color="white"),
            actions=[
                ft.TextButton("Fechar", on_click=self.fechar_banner)
            ],
        )
        self.page.banner = self.banner

        # Divisões de tarefas por vencimento
        self.tarefas_hoje = ft.Column()
        self.tarefas_semana = ft.Column()
        self.tarefas_depois = ft.Column()
        self.tarefas_agendadas = ft.Column() 

        # Seções visuais
        self.secao_hoje = ft.Container(content=ft.Column([
            ft.Text("Hoje", style=ft.TextStyle(weight="bold", size=16)),
            self.tarefas_hoje,
        ]))

        self.secao_semana = ft.Container(content=ft.Column([
            ft.Text("Essa Semana", style=ft.TextStyle(weight="bold", size=16)),
            self.tarefas_semana,
        ]))

        self.secao_depois = ft.Container(content=ft.Column([
            ft.Text("Depois", style=ft.TextStyle(weight="bold", size=16)),
            self.tarefas_depois,
        ]))

        self.secao_agendadas = ft.Container(content=ft.Column([
            ft.Text("Tarefas Agendadas", style=ft.TextStyle(weight="bold", size=16)),
            self.tarefas_agendadas,
        ]))


        self.tarefas_ativas = ft.Text("0 tarefas ativas")
        self.botao_limpar_concluidas = ft.OutlinedButton(text="Limpar concluídas", on_click=self.limpar_concluidas, visible=False,expand=True,)
        self.botao_excluir = ft.IconButton(icon=ft.icons.DELETE, on_click=self.confirmar_exclusao_selecionados, visible=self.modo_edicao,)
        self.botao_adicionar = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.abrir_formulario_tarefa)
        self.botao_editar_deletar = ft.IconButton(icon=ft.icons.EDIT, on_click=self.mostrar_selecao,)


        self.controls = [
            self.banner,
            ft.Row([ft.IconButton(icon=ft.icons.MENU, on_click=self.abrir_menu), self.pesquisa],expand=True,),
            ft.Container(height=10,expand=True,),
            self.filtro_prioridade, 
            self.filtro_status,
            self.lista_tarefas,
            self.secao_hoje,
            self.secao_semana,
            self.secao_depois,
            self.secao_agendadas,
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.tarefas_ativas,
                    self.botao_limpar_concluidas,
                ],expand=True,),
            self.calendario,
            self.botao_excluir,
            ft.Row([self.botao_editar_deletar,self.botao_adicionar], alignment=ft.MainAxisAlignment.END,expand=True,),
        ]

        self.carregar_tarefas()



    def fechar_banner(self, e):
        self.page.banner.open = False
        self.page.update()


    def abrir_menu(self, e):
        self.page.drawer = self.menu_lateral
        self.page.drawer.open = True
        self.page.update()

    def aplicar_filtro_geral(self):
        self.filtro_classe_atual = None
        self.filtro_prioridade.value = "todas"
        self.filtro_status.selected_index = 0
        self.filtrar_tarefas()


    def mudar_tema(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        self.page.update()

    def carregar_tarefas(self):
        self.lista_tarefas.controls.clear()
        tarefas = listar_tarefas()
        for tarefa in tarefas:
            ui = TarefaUI(tarefa, self.remover_tarefa, self.filtrar_tarefas, lista_tarefas=self)
            ui.page = self.page
            self.lista_tarefas.controls.append(ui)
        self.filtrar_tarefas()
        self.page.update()


    def dialogo_edicao(self, tarefa):
        campo_nome = ft.TextField(label="Nome da tarefa", value=tarefa.nome)
        campo_classe = ft.Dropdown(
            label="Classe da tarefa",
            value=tarefa.classe.value,
            options=[ft.dropdown.Option(c, c.capitalize()) for c in ["saude", "casa", "trabalho", "lazer"]],
        )
        campo_prioridade = ft.Dropdown(
            label="Prioridade",
            value=tarefa.prioridade.value,
            options=[ft.dropdown.Option(p, p.capitalize()) for p in ["alta", "media", "baixa"]],
        )
        campo_descricao = ft.TextField(label="Descrição detalhada", value=tarefa.descricao, multiline=True)

        # 🗓️ Inicializar datas
        data_inicio = tarefa.data_inicio
        data_entrega = tarefa.data_entrega

        btn_inicio = ft.TextButton()
        btn_entrega = ft.TextButton()

        def atualizar_texto_data():
            btn_inicio.text = f"Data início: {data_inicio.strftime('%d/%m/%Y')}"
            btn_entrega.text = f"Data entrega: {data_entrega.strftime('%d/%m/%Y')}"
            self.page.update()

        # ⚙️ Usar variáveis locais para manter o estado de datas dentro do diálogo
        tipo_data_em_edicao = {"value": None}

        def abrir_calendario(tipo):
            tipo_data_em_edicao["value"] = tipo
            self.calendario.open = True
            self.page.update()

        def definir_data(e):
            nonlocal data_inicio, data_entrega
            data = e.control.value
            if tipo_data_em_edicao["value"] == "inicio":
                data_inicio = data
            elif tipo_data_em_edicao["value"] == "entrega":
                data_entrega = data
            atualizar_texto_data()

        self.calendario.on_change = definir_data  # Conecta DatePicker ao diálogo de edição

        btn_inicio.on_click = lambda e: abrir_calendario("inicio")
        btn_entrega.on_click = lambda e: abrir_calendario("entrega")
        atualizar_texto_data()

        def salvar_edicao(e):
            editar_tarefa(
                tarefa.id,
                nome=campo_nome.value,
                classe=campo_classe.value,
                prioridade=campo_prioridade.value,
                data_inicio=data_inicio,
                data_entrega=data_entrega,
                descricao=campo_descricao.value
            )
            self.page.dialog.open = False
            self.banner.content = ft.Text("Tarefa atualizada!", color="white")
            self.banner.bgcolor = "green"
            self.page.banner.open = True
            self.carregar_tarefas()
            self.page.update()

        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Tarefa"),
            content=ft.Column([
                campo_nome,
                 ft.Row([campo_classe,campo_prioridade]),
                ft.Row([btn_inicio, btn_entrega]),
                campo_descricao
            ], scroll="auto"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
                ft.TextButton("Salvar", on_click=salvar_edicao)
            ]
        )

    def filtrar_tarefas(self, e=None):
        # Limpa os grupos
        self.tarefas_hoje.controls.clear()
        self.tarefas_semana.controls.clear()
        self.tarefas_depois.controls.clear()
        self.tarefas_agendadas.controls.clear()
        self.lista_tarefas.controls.clear()
        self.lista_tarefas.visible = True
        self.secao_hoje.visible = False
        self.secao_semana.visible = False
        self.secao_depois.visible = False
        self.secao_agendadas.visible = False

        prioridade = self.filtro_prioridade.value
        status = self.filtro_status.tabs[self.filtro_status.selected_index].text

        agora = datetime.now()
        hoje = agora.date()
        fim_da_semana = hoje + timedelta(days=(6 - hoje.weekday()))

        count_ativas = 0

        for tarefa in listar_tarefas():
            # Exibir tarefas agendadas apenas no filtro "ativas"
            if tarefa.data_inicio.date() > hoje:
                if status == "ativas":  # Apenas no filtro "ativas"
                    ui = TarefaUI(tarefa, self.remover_tarefa, self.filtrar_tarefas, lista_tarefas=self)
                    ui.page = self.page
                    self.tarefas_agendadas.controls.append(ui)
                    self.secao_agendadas.visible = True
                continue

            # Filtro de classe
            if self.filtro_classe_atual and tarefa.classe.value != self.filtro_classe_atual:
                continue

            # Prioridade
            if prioridade != "todas" and tarefa.prioridade.value != prioridade:
                continue

            # Filtro de status
            mostrar_tarefa = False
            if status == "completas" and tarefa.status:
                mostrar_tarefa = True
            elif status == "atrasadas" and not tarefa.status and tarefa.data_entrega < agora:
                mostrar_tarefa = True
            elif status == "ativas" and not tarefa.status and tarefa.data_entrega >= agora:
                mostrar_tarefa = True

            if not mostrar_tarefa:
                continue

            # Criar UI
            ui = TarefaUI(tarefa, self.remover_tarefa, self.filtrar_tarefas, lista_tarefas=self)
            ui.page = self.page

            # Tarefas ativas separadas por data
            if status == "ativas":
                count_ativas += 1
                self.lista_tarefas.visible = False
                if tarefa.data_entrega.date() == hoje:
                    self.tarefas_hoje.controls.append(ui)
                    self.secao_hoje.visible = True
                elif tarefa.data_entrega.date() <= fim_da_semana:
                    self.tarefas_semana.controls.append(ui)
                    self.secao_semana.visible = True
                else:
                    self.tarefas_depois.controls.append(ui)
                    self.secao_depois.visible = True
            else:
                self.lista_tarefas.controls.append(ui)

        # Atualiza o texto de tarefas ativas
        self.tarefas_ativas.value = f"{count_ativas} tarefa(s) ativa(s)"
        self.botao_limpar_concluidas.visible = (status == "completas" and len(self.lista_tarefas.controls) > 0)
        self.page.update()


    def filtrar_por_classe(self, classe):
        self.filtro_classe_atual = classe
        self.lista_tarefas.controls.clear()
        self.tarefas_hoje.controls.clear()
        self.tarefas_semana.controls.clear()
        self.tarefas_depois.controls.clear()

        tarefas = [t for t in listar_tarefas() if t.classe.value == classe]

        if not tarefas:
            self.banner.content = ft.Text(f"Nenhuma tarefa encontrada para '{classe}'. Retornando ao filtro geral.", color="white")
            self.banner.bgcolor = "orange"
            self.page.banner.open = True
            self.aplicar_filtro_geral()
            return

        # Exibir tarefas da classe (modo "plano", sem separação por datas)
        for tarefa in tarefas:
            ui = TarefaUI(tarefa, self.remover_tarefa, self.filtrar_tarefas, lista_tarefas=self, modo_selecao=self.modo_edicao)
            ui.page = self.page
            self.lista_tarefas.controls.append(ui)

        self.lista_tarefas.visible = True
        self.secao_hoje.visible = False
        self.secao_semana.visible = False
        self.secao_depois.visible = False
        self.page.update()


    def pesquisar_tarefas(self, e):
        termo = e.control.value.lower().strip()
        self.lista_tarefas.controls.clear()
        tarefas = [t for t in listar_tarefas() if termo in t.nome.lower()]
        for tarefa in tarefas:
            ui = TarefaUI(tarefa, self.remover_tarefa, self.filtrar_tarefas, lista_tarefas=self,modo_selecao=self.modo_edicao)
            ui.page = self.page
            self.lista_tarefas.controls.append(ui)

        if not tarefas:
            self.banner.content = ft.Text("Nenhuma tarefa encontrada.", color="white")
            self.banner.bgcolor = "orange"
            self.page.banner.open = True
        self.page.update()

    def abrir_formulario_tarefa(self, e):
        # 🟦 1. Campos básicos
        self.campo_nome = ft.TextField(label="Nome da tarefa", autofocus=True)
        self.campo_classe = ft.Dropdown(
            label="Classe da tarefa",
            options=[
                ft.dropdown.Option("saude", "Saúde"),
                ft.dropdown.Option("casa", "Casa"),
                ft.dropdown.Option("trabalho", "Trabalho"),
                ft.dropdown.Option("lazer", "Lazer"),
            ]
        )
        self.campo_prioridade = ft.Dropdown(
            label="Prioridade",
            options=[
                ft.dropdown.Option("alta", "Alta"),
                ft.dropdown.Option("media", "Média"),
                ft.dropdown.Option("baixa", "Baixa"),
            ],
            value="media"
        )
        # 🟩 2. Datas
        self.data_inicio = datetime.now()
        self.data_entrega = self.data_inicio + timedelta(days=1)
        self.botao_data_inicio = ft.TextButton(
            text=f"Data de início: {self.data_inicio.strftime('%d/%m/%Y')}",
            on_click=lambda e: self.abrir_calendario("inicio")
        )
        self.botao_data_entrega = ft.TextButton(
            text=f"Data de entrega: {self.data_entrega.strftime('%d/%m/%Y')}",
            on_click=lambda e: self.abrir_calendario("entrega")
        )
        # 🟨 3. Descrição detalhada
        self.campo_descricao = ft.TextField(
            label="Descrição detalhada",
            multiline=True,
            min_lines=3,
            max_lines=6
        )

        # 🔘 4. Função para fechar o diálogo
        def fechar_dialogo(e):
            self.dialogo_nova_tarefa.open = False
            self.page.update()
        # ✅ 6. Criar o diálogo após TODOS os campos estarem definidos
        self.dialogo_nova_tarefa = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nova Tarefa"),
            content=ft.Column([
                self.campo_nome,
                ft.Row([self.campo_classe,self.campo_prioridade]),
                ft.Row([self.botao_data_inicio, self.botao_data_entrega]),
                self.campo_descricao,
            ], 
            scroll="auto"),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Criar", on_click=self.criar_tarefa_dialog),
            ]
        )
        # Mostrar o diálogo
        self.page.dialog = self.dialogo_nova_tarefa
        self.page.overlay.append(self.dialogo_nova_tarefa)
        self.dialogo_nova_tarefa.open = True
        self.page.update()


    def abrir_calendario(self, tipo):
        self.tipo_data_em_edicao = tipo
        self.calendario.open = True
        self.page.update()

    def definir_data(self, e):
        data_selecionada = e.control.value
        if self.tipo_data_em_edicao == "inicio":
            self.data_inicio = data_selecionada
            self.botao_data_inicio.text = f"Data de início: {data_selecionada.strftime('%d/%m/%Y')}"
        elif self.tipo_data_em_edicao == "entrega":
            self.data_entrega = data_selecionada
            self.botao_data_entrega.text = f"Data de entrega: {data_selecionada.strftime('%d/%m/%Y')}"
        self.page.update()

    def criar_tarefa_dialog(self, e):
        # 1. Validação
        nome = self.campo_nome.value.strip()
        classe = self.campo_classe.value
        prioridade = self.campo_prioridade.value or "media"
        descricao = self.campo_descricao.value.strip()
        if not nome or not classe:
            self.banner.content = ft.Text("Campos obrigatórios não preenchidos: nome e classe.", color="white")
            self.banner.bgcolor = "orange"
            self.page.banner.open = True
            self.page.update()
            return
        # 2. Criar tarefa
        try:
            nova_tarefa = criar_tarefa(
                nome=nome,
                classe=classe,
                prioridade=prioridade,
                data_inicio=self.data_inicio,
                data_entrega=self.data_entrega,
                descricao=descricao,   
            )
            # 3. Adicionar à interface
            self.lista_tarefas.controls.append(
                TarefaUI(
                    nova_tarefa,
                    self.remover_tarefa,
                    self.filtrar_tarefas,
                    lista_tarefas=self
                )
            )
            # 4. Mensagem de sucesso
            self.banner.content = ft.Text("Tarefa criada com sucesso!", color="white")
            self.banner.bgcolor = "green"
            self.page.banner.open = True
            self.page.update()
            
        except Exception as err:
            print("[ERRO ao criar tarefa]", err)
            self.banner.content = ft.Text("ERRO ao criar tarefa", color="white")
            self.banner.bgcolor = "red"
            self.page.banner.open = True
            self.page.update()

        # 5. Fechar diálogo e atualizar interface
        self.dialogo_nova_tarefa.open = False
        self.filtrar_tarefas()
        self.page.update()
       
    def remover_tarefa(self, tarefa_ui):
        # Remove do banco de dados
        deletar_tarefa(tarefa_ui.tarefa.id)

        # Verifica e remove a tarefa de todos os grupos
        for grupo in [self.lista_tarefas, self.tarefas_hoje, self.tarefas_semana, self.tarefas_depois]:
            if tarefa_ui in grupo.controls:
                grupo.controls.remove(tarefa_ui)
                break  # Sai do loop após encontrar e remover a tarefa

        # Atualiza a interface
        self.banner.content = ft.Text("Tarefa removida", color="white")
        self.banner.bgcolor = "green"
        self.page.banner.open = True
        self.page.update()

    def limpar_concluidas(self, e):
        # Verifica se há tarefas concluídas
        concluidas = [tarefa_ui for tarefa_ui in self.lista_tarefas.controls if tarefa_ui.tarefa.status]
        if not concluidas:
            self.banner.content = ft.Text("Não há tarefas concluídas para limpar.", color="white")
            self.banner.bgcolor = "orange"
            self.page.banner.open = True
            self.page.update()
            return

        # Função para confirmar a exclusão
        def confirmar(e):
            for tarefa_ui in concluidas:
                self.remover_tarefa(tarefa_ui)
            self.page.dialog.open = False
            self.banner.content = ft.Text("Tarefas concluídas removidas com sucesso.", color="white")
            self.banner.bgcolor = "green"
            self.page.banner.open = True
            self.page.update()

        # Criar o diálogo de confirmação
        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar limpeza"),
            content=ft.Text(f"Tem certeza que deseja excluir {len(concluidas)} tarefa(s) concluída(s)?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
                ft.TextButton("Limpar", on_click=confirmar)
            ]
        )
        self.page.dialog = dialogo
        self.page.overlay.append(dialogo)
        dialogo.open = True
        self.page.update()

    def confirmar_exclusao_selecionados(self, e):
        selecionados = []

        for grupo in [self.lista_tarefas, self.tarefas_hoje, self.tarefas_semana, self.tarefas_depois]:
            selecionados.extend([t for t in grupo.controls if t.checkbox_selecao.value])

        if not selecionados:
            self.banner.content = ft.Text("Nenhuma tarefa selecionada.", color="white")
            self.banner.bgcolor = "orange"
            self.page.banner.open = True
            self.page.update()
            return

        def confirmar(e):
            for tarefa_ui in selecionados:
                self.remover_tarefa(tarefa_ui)
            self.fechar_dialogo()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir {len(selecionados)} tarefa(s)?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
                ft.TextButton("Excluir", on_click=confirmar)
            ]
        )
        self.page.dialog = dialog
        self.page.overlay.append(dialog)  
        dialog.open = True
        self.page.update()

    def fechar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

    def mostrar_selecao(self, e):
        self.modo_edicao = not self.modo_edicao

        def aplicar_modo(lista):
            for tarefa_ui in lista.controls:
                tarefa_ui.checkbox_selecao.visible = self.modo_edicao
                tarefa_ui.botao_editar.visible = self.modo_edicao
                tarefa_ui.update()

        # Atualiza todos os grupos de tarefas
        aplicar_modo(self.lista_tarefas)
        aplicar_modo(self.tarefas_hoje)
        aplicar_modo(self.tarefas_semana)
        aplicar_modo(self.tarefas_depois)

        # Atualiza botão excluir
        self.botao_excluir.visible = self.modo_edicao

        # Atualiza banner e página
        self.banner.content = ft.Text("Modo edição." if self.modo_edicao else "Modo visualização.", color="white")
        self.banner.bgcolor = "blue"
        self.page.banner.open = True
        self.page.update()




