from PIL import Image
import io
import base64
import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefa, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa
import datetime

def encode_image_to_base64(path):
    img = Image.open(path)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

class TarefaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.image_src = encode_image_to_base64("src/assets/img/fundo.png")  # Codifica a imagem em base64
        self.page.image_fit = ft.ImageFit.COVER
        
        # Configuração da lista de tarefas com rolagem
        self.tarefas_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
            width=400  # Largura fixa para centralização
        )
        
        self.error_text = ft.Text(value="", color="red")
        self.editing_task_id = None
    
    def construir(self):
        self.page.clean()
        self.page.padding = 0
        self.page.spacing = 0
        
        # Elementos da UI
        background_image = ft.Image(
            src=self.page.image_src,  # Usa a imagem codificada em base64
            fit=ft.ImageFit.COVER,
            width=self.page.width,  # Faz a imagem ocupar toda a largura da página
            height=self.page.height,  # Faz a imagem ocupar toda a altura da página
            expand=True
        )

        # Botão para voltar à tela inicial
        back_button = ft.Container(
            width=120,  # Mesmo tamanho que o botão "Excluir"
            height=50,  # Mesmo tamanho que o botão "Excluir"
            alignment=ft.alignment.center,
            bgcolor="#6E6E6E",
            border=ft.border.all(1, "#5C5C5C"),
            border_radius=ft.border_radius.all(5),
            shadow=ft.BoxShadow(blur_radius=3, color="black", spread_radius=1),
            content=ft.ElevatedButton(
                content=ft.Row(
                    [ft.Text("Voltar", color="white", size=14)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                ),
                on_click=lambda e: self.page.go('/inicial'),
                bgcolor="transparent",
                color="white",
                elevation=0
            ),
            on_hover=lambda e: self._on_hover(e)
        )

        # Substitui o Container por um Column para suportar o botão "Voltar" e "Excluir"
        main_content = ft.Column(
            controls=[
                ft.Container(
                    content=self.tarefas_list,
                    height=self.page.height * 0.6,  # Mantém a altura da lista
                    alignment=ft.alignment.center,
                    margin=ft.margin.symmetric(horizontal=20, vertical=1),
                    border_radius=10,
                    padding=5
                ),
                self._create_footer(back_button)  # Passa o botão "Voltar" para o rodapé
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=2
        )
        
        # Adiciona apenas o main_content à página
        self.page.controls.clear()
        self.page.add(ft.Stack([background_image, main_content]))
        self.page.update()

        # Atualiza a lista de tarefas após adicionar o main_content
        self.atualizar_lista_tarefas()

        return ft.Stack([background_image, main_content])
    
    def _create_footer(self, back_button):
        """Cria o rodapé centralizado com os botões de excluir e voltar"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=120,
                        height=50,
                        alignment=ft.alignment.center,
                        bgcolor="#6E6E6E",
                        border=ft.border.all(1, "#5C5C5C"),
                        border_radius=ft.border_radius.all(5),
                        shadow=ft.BoxShadow(blur_radius=5, color="black", spread_radius=1),
                        content=ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Text("X", font_family="Mine 2", size=20, color="white"),
                                    ft.Text("Excluir", font_family="Mine", size=14, color="white")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5
                            ),
                            on_click=self.on_excluir_tarefa_click,
                            bgcolor="transparent",
                            color="white",
                            elevation=0
                        ),
                        on_hover=lambda e: self._on_hover(e)
                    ),
                    ft.Container(width=20),  # Espaçamento entre os botões
                    back_button  # Adiciona o botão "Voltar" ao rodapé
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=100)  # Move os botões mais para baixo
        )

    def _on_hover(self, e):
        """Função para lidar com o hover nos botões"""
        if e.data == "true":  # Quando o mouse está sobre o botão
            e.control.bgcolor = "#8A8A8A"  # Torna o botão mais claro
        else:  # Quando o mouse sai do botão
            e.control.bgcolor = "#6E6E6E"  # Retorna à cor original
        e.control.update()

    def atualizar_lista_tarefas(self, apenas_vencidas=False):
        """Atualiza a lista de tarefas centralizadas"""
        self.editing_task_id = None
        session = Session()
        
        try:
            self.tarefas_list.controls.clear()

            # Filtra as tarefas com base no parâmetro `apenas_vencidas`
            query = session.query(Tarefa).order_by(
                Tarefa.dt.is_(None),  # Coloca os valores NULL no final
                Tarefa.dt == "0000-00-00",  # Coloca as tarefas "Sem prazo" no final
                Tarefa.dt.asc()       # Ordena as datas em ordem crescente
            )
            todas_tarefas = query.all()

            for tarefa in todas_tarefas:
                def on_checkbox_change(e, tarefa_container):
                    tarefa_container.bgcolor = "#5A5A5A" if e.control.value else "#6E6E6E"
                    tarefa_container.update()

                # Converte a data para datetime.date se necessário
                if isinstance(tarefa.dt, str):
                    try:
                        tarefa.dt = datetime.datetime.strptime(tarefa.dt, "%Y-%m-%d").date()
                    except ValueError:
                        tarefa.dt = None

                # Define a cor do texto com base na data de vencimento
                if tarefa.dt == datetime.date(1, 1, 1):  # Data "0000-00-00" é interpretada como 0001-01-01
                    text_color = "white"
                    show_red_line = False
                    show_yellow_line = False
                    data_text = "Sem prazo"
                elif tarefa.dt and tarefa.dt < datetime.date.today():
                    text_color = "#FF0000"  # Vermelho para tarefas atrasadas
                    show_red_line = True
                    show_yellow_line = False
                    data_text = tarefa.dt.strftime('%d/%m/%Y')
                elif tarefa.dt and tarefa.dt == datetime.date.today():
                    text_color = "#FFFF00"  # Amarelo para tarefas com data igual à data corrente
                    show_red_line = False
                    show_yellow_line = True
                    data_text = tarefa.dt.strftime('%d/%m/%Y')
                else:
                    text_color = "white"
                    show_red_line = False
                    show_yellow_line = False
                    data_text = tarefa.dt.strftime('%d/%m/%Y') if tarefa.dt else "Sem prazo"

                # Container da tarefa centralizado
                tarefa_container = ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(
                                            f"{tarefa.descricao}",
                                            size=14,
                                            text_align="start",  # Alinha o texto à esquerda
                                            color=text_color,  # Cor do texto
                                            max_lines=2,  # Permite até 2 linhas para a descrição
                                            overflow="ellipsis",  # Adiciona reticências se o texto for muito longo
                                        ),
                                        on_click=lambda e, t=tarefa: self.abrir_edicao_tarefa(e, t),
                                        alignment=ft.alignment.center_left,  # Move o texto mais para a esquerda
                                        expand=True,  # Faz o texto ocupar o espaço disponível
                                        padding=ft.padding.only(left=5)  # Adiciona um pequeno padding à esquerda
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            data_text,  # Exibe a data ou "Sem prazo"
                                            size=14,
                                            text_align="center",  # Centraliza o texto
                                            color=text_color,  # Cor do texto
                                            no_wrap=True  # Garante que a data não quebre a linha
                                        ),
                                        # Desabilita a edição da data se a tarefa estiver vencida
                                        on_click=None if (tarefa.dt and tarefa.dt < datetime.date.today()) else lambda e, t=tarefa: self.abrir_edicao_data(e, t),
                                        alignment=ft.alignment.center,  # Centraliza o campo da data
                                        width=120  # Define uma largura fixa para a data
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Garante espaçamento entre os itens
                                expand=True  # Faz a linha ocupar toda a largura disponível
                            ),
                            # Adiciona uma linha vermelha ou amarela abaixo, se necessário
                            ft.Container(
                                height=2,
                                bgcolor="#FF0000" if show_red_line else "#FFFF00" if show_yellow_line else "transparent",
                                visible=show_red_line or show_yellow_line  # Exibe apenas para tarefas atrasadas ou com data corrente
                            )
                        ]
                    ),
                    padding=ft.padding.all(5),
                    bgcolor="#6E6E6E",  # Cinza para todas as caixas
                    border=ft.border.all(1, "#5C5C5C"),
                    border_radius=ft.border_radius.all(5),
                    shadow=ft.BoxShadow(blur_radius=5, color="black", spread_radius=1),
                    alignment=ft.alignment.center,
                    expand=True  # Faz o container ocupar toda a largura disponível
                )

                # Linha da tarefa centralizada
                tarefa_row = ft.Row(
                    [
                        ft.Checkbox(
                            value=False,
                            data=tarefa.id,
                            fill_color="#5A5A5A",
                            on_change=lambda e, tc=tarefa_container: on_checkbox_change(e, tc)
                        ),
                        tarefa_container
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Ajusta o alinhamento para exibir a checkbox
                )
                
                # Container para centralizar a linha da tarefa
                centered_row = ft.Container(
                    content=tarefa_row,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10)  # Reduz a margem horizontal
                )
                
                self.tarefas_list.controls.append(centered_row)

            self.tarefas_list.update()

        finally:
            session.close()

    def abrir_edicao_tarefa(self, e, tarefa):
        if self.editing_task_id is not None and self.editing_task_id != tarefa.id:
            return  # Impede abrir outro campo de edição se já houver um aberto

        self.editing_task_id = tarefa.id  # Define a tarefa atual como em edição
        descricao_input = ft.TextField(
            value=tarefa.descricao,
            expand=False,  # Remove o comportamento de expansão para alinhar melhor
            text_align="start",  # Alinha o texto à esquerda
            autofocus=True,  # Foca automaticamente no campo ao editar
            multiline=True,  # Permite múltiplas linhas
            max_lines=None  # Sem limite de linhas
        )
        error_text = ft.Text(value="", color="white", weight="bold")  # Alterado para branco

        def salvar_edicao(e):
            if descricao_input.value.strip() == "":
                error_text.value = "O CAMPO NÃO PODE SER VAZIO."
                error_text.update()  # Atualiza o texto de erro na tela
            else:
                # Chama a função de edição da tarefa
                resultado = editar_tarefa(tarefa.id, descricao_input.value)
                
                if isinstance(resultado, str) and resultado == "Tarefa já existe.":
                    error_text.value = "ERRO: TAREFA JÁ EXISTE."
                    error_text.update()  # Atualiza o texto de erro na tela
                elif "editada com sucesso" in resultado:
                    self.editing_task_id = None  # Libera a edição após salvar
                    self.atualizar_lista_tarefas()  # Atualiza a lista de tarefas
                else:
                    error_text.value = resultado  # Exibe qualquer outro erro retornado
                    error_text.update()

        def cancelar_edicao(e):
            self.editing_task_id = None  # Libera a edição ao cancelar
            self.atualizar_lista_tarefas()  # Atualiza a lista de tarefas
        
        tarefa_row = e.control.parent
        tarefa_row.controls.clear()  # Limpa os controles para adicionar os novos
        tarefa_row.controls.append(
            ft.Column(
                [
                    descricao_input,
                    error_text,  # Adiciona o texto de erro abaixo do campo de entrada
                    ft.Row(
                        [
                            ft.Container(
                                width=100,
                                height=40,  # Define altura menor para tornar o botão mais compacto
                                alignment=ft.alignment.center,  # Centraliza o conteúdo do botão
                                bgcolor="green",  # Define a cor de fundo do container
                                border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
                                content=ft.ElevatedButton(
                                    content=ft.Text("Salvar", font_family="Mine", size=12),  # Ícone de edição
                                    bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                                    color="white",
                                    elevation=0,  # Remove a elevação para alinhar com o container
                                    on_click=salvar_edicao  # Chama a função de salvar
                                )
                            ),
                            ft.Container(width=50),  # Adiciona um espaçamento fixo entre os botões
                            ft.Container(
                                width=100,
                                height=40,  # Define altura menor para tornar o botão mais compacto
                                alignment=ft.alignment.center,  # Centraliza o conteúdo do botão
                                bgcolor="red",  # Define a cor de fundo do container
                                border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
                                content=ft.ElevatedButton(
                                    content=ft.Text("Cancelar", font_family="Mine", size=12),  # Ícone de cancelar
                                    bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                                    color="white",
                                    elevation=0,  # Remove a elevação para alinhar com o container
                                    on_click=cancelar_edicao  # Chama a função de cancelar
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START  # Alinha os botões no início, com o espaçamento fixo
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER  # Centraliza o conteúdo verticalmente
            )
        )
        tarefa_row.update()

    def abrir_edicao_data(self, e, tarefa):
        """Abre o calendário para editar a data da tarefa"""
        def on_date_selected(e):
            if e.control.value:
                nova_data = e.control.value.strftime("%Y-%m-%d")
                self.atualizar_data_tarefa(tarefa.id, nova_data)

        self.page.open(
            ft.DatePicker(
                first_date=datetime.date.today(),
                last_date=datetime.date(2026, 12, 31),
                on_change=on_date_selected
            )
        )

    def atualizar_data_tarefa(self, tarefa_id, nova_data):
        """Atualiza a data da tarefa no banco de dados"""
        session = Session()
        try:
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
            if tarefa:
                tarefa.dt = datetime.datetime.strptime(nova_data, "%Y-%m-%d").date()
                session.commit()
                self.atualizar_lista_tarefas()
        except Exception as e:
            print(f"Erro ao atualizar a data da tarefa: {e}")
            session.rollback()
        finally:
            session.close()

    def on_excluir_tarefa_click(self, e):
        """Exclui as tarefas marcadas"""
        tarefas_marcadas = []
        for item in self.tarefas_list.controls:
            if isinstance(item.content, ft.Row):
                row = item.content
                for control in row.controls:
                    if isinstance(control, ft.Checkbox) and control.value:  # Verifica se a checkbox está marcada
                        tarefas_marcadas.append(control.data)

        if tarefas_marcadas:
            def confirmar_exclusao(e):
                erros = []
                for tarefa_id in tarefas_marcadas:
                    resultado = excluir_tarefa(tarefa_id)
                    if not isinstance(resultado, str) or "sucesso" not in resultado.lower():
                        erros.append(tarefa_id)

                self.fechar_dialog(dialog)

                if erros:
                    self.mostrar_dialogo_erro(f"Erro ao excluir as tarefas: {', '.join(map(str, erros))}")
                else:
                    self.atualizar_lista_tarefas()

            def cancelar_exclusao(e):
                self.fechar_dialog(dialog)

            # Criação do pop-up de confirmação
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("CONFIRMAR EXCLUSÃO", color="red", weight="bold"),
                content=ft.Text(f"Você tem certeza que deseja excluir {len(tarefas_marcadas)} tarefa(s) selecionada(s)?", weight="bold"),
                actions=[
                    ft.TextButton("SIM", on_click=confirmar_exclusao),
                    ft.TextButton("NÃO", on_click=cancelar_exclusao)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            # Abre o diálogo
            self.page.dialog = dialog
            dialog.open = True
            self.page.add(dialog)
            self.page.update()
        else:
            # Criação do pop-up de erro
            self.mostrar_dialogo_erro("Nenhuma tarefa selecionada. Por favor, selecione pelo menos uma tarefa para excluir.")

    def mostrar_dialogo_erro(self, mensagem):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("ERRO", color="red", weight="bold"),
            content=ft.Text(mensagem, weight="bold"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.fechar_dialog(dialog))
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.add(dialog)
        self.page.update()

    def fechar_dialog(self, dialog):
        dialog.open = False
        self.page.update()
