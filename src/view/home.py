import datetime
import flet as ft
from connection import Session
from model.tarefa_model import Tarefa


def main(page: ft.Page):
    page.title = "Organizador de Tarefas"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT  # Define o tema inicial como claro

    # Variável para armazenar a data selecionada
    data_entrega = None

    # Variável para armazenar a tarefa que está sendo editada
    tarefa_em_edicao = None

    # Texto para exibir mensagens de resultado
    result_text = ft.Text(
        color=ft.colors.RED,
        size=14,
        weight=ft.FontWeight.BOLD,
    )

    # Estatísticas
    total_tarefas = ft.Text("Total de Tarefas: 0", size=16, weight=ft.FontWeight.BOLD)
    tarefas_concluidas = ft.Text("Tarefas Concluídas: 0", size=16, weight=ft.FontWeight.BOLD)
    tarefas_pendentes = ft.Text("Tarefas Pendentes: 0", size=16, weight=ft.FontWeight.BOLD)
    progresso_barra = ft.ProgressBar(value=0, width=400, color=ft.colors.GREEN)

    # Função para atualizar as estatísticas
    def atualizar_estatisticas():
        session = Session()
        try:
            tarefas = session.query(Tarefa).all()
            total = len(tarefas)
            concluidas = len([t for t in tarefas if t.situacao])
            pendentes = total - concluidas

            # Atualiza os textos das estatísticas
            total_tarefas.value = f"Total de Tarefas: {total}"
            tarefas_concluidas.value = f"Tarefas Concluídas: {concluidas}"
            tarefas_pendentes.value = f"Tarefas Pendentes: {pendentes}"

            # Atualiza a barra de progresso
            progresso_barra.value = concluidas / total if total > 0 else 0
        finally:
            session.close()
        page.update()

    # Função para alternar o tema
    def alternar_tema(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            tema_button.icon = ft.icons.WB_SUNNY  # Ícone de sol para o tema escuro
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            tema_button.icon = ft.icons.DARK_MODE  # Ícone de lua para o tema claro
        page.update()

    # Botão para alternar o tema
    tema_button = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        on_click=alternar_tema,
        tooltip="Alternar Tema",
        bgcolor=ft.colors.BLUE,
        icon_color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    # Cabeçalho estilizado
    header = ft.Container(
        content=ft.Text(
            "Organizador de Tarefas",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.colors.BLUE, ft.colors.CYAN],
        ),
        border_radius=ft.border_radius.all(15),
        shadow=ft.BoxShadow(
            spread_radius=6,
            blur_radius=20,
            color=ft.colors.with_opacity(0.4, ft.colors.BLACK),
        ),
    )

    # Campo de entrada para descrição da tarefa
    descricao_input = ft.TextField(
        label="Descrição da Tarefa",
        hint_text="Digite a descrição da tarefa...",
        autofocus=True,
        width=400,
        border_color=ft.colors.BLUE,
    )

    # Checkbox para marcar a tarefa como concluída
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)

    # Funções para lidar com o DatePicker
    def handle_change(e):
        nonlocal data_entrega
        data_entrega = e.control.value.strftime('%Y-%m-%d')  # Armazena a data selecionada
        page.update()

    # Botão para abrir o DatePicker
    date_picker_button = ft.ElevatedButton(
        "Selecionar Data",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2025, month=1, day=1),
                last_date=datetime.datetime(year=2026, month=1, day=1),
                on_change=handle_change,
            )
        ),
    )

    # Função para determinar a cor da tarefa com base no status e na data de entrega
    def determinar_cor_tarefa(tarefa):
        if tarefa.situacao:  # Tarefa concluída
            return ft.colors.GREEN
        else:
            dias_para_vencimento = (datetime.datetime.strptime(tarefa.data_entrega, "%Y-%m-%d").date() - datetime.date.today()).days
            if dias_para_vencimento <= 3:  # Próxima do vencimento
                return ft.colors.AMBER
            else:
                return ft.colors.RED

    # Função para cadastrar ou editar uma tarefa
    def salvar_tarefa(e):
        nonlocal tarefa_em_edicao

        if not descricao_input.value:
            result_text.value = "Por favor, insira a descrição da tarefa."
            result_text.color = ft.colors.RED
            page.update()
            return

        if not data_entrega:
            result_text.value = "Por favor, selecione a data de entrega."
            result_text.color = ft.colors.RED
            page.update()
            return

        # Garantir que a data esteja no formato correto 'YYYY-MM-DD'
        try:
            data_entrega_formatada = datetime.datetime.strptime(data_entrega, "%Y-%m-%d").date()
        except Exception as ex:
            result_text.value = f"Erro ao formatar data: {str(ex)}"
            result_text.color = ft.colors.RED
            page.update()
            return

        session = Session()
        try:
            if tarefa_em_edicao:  # Se estiver editando uma tarefa existente
                tarefa_editada = session.query(Tarefa).filter(Tarefa.id == tarefa_em_edicao.id).first()
                if tarefa_editada:
                    tarefa_editada.descricao = descricao_input.value.strip()
                    tarefa_editada.situacao = situacao_input.value
                    tarefa_editada.data_entrega = data_entrega_formatada
                    session.commit()
                    result_text.value = "Tarefa editada com sucesso!"
                    result_text.color = ft.colors.GREEN
                else:
                    result_text.value = "Erro: Tarefa não encontrada."
                    result_text.color = ft.colors.RED
                tarefa_em_edicao = None  # Limpa a tarefa em edição
                salvar_button.text = "Cadastrar Tarefa"  # Volta o botão ao estado normal
            else:  # Se for uma nova tarefa
                nova_tarefa = Tarefa(
                    descricao=descricao_input.value.strip(),
                    situacao=situacao_input.value,
                    data_entrega=data_entrega_formatada,
                )
                session.add(nova_tarefa)
                session.commit()
                result_text.value = "Tarefa cadastrada com sucesso!"
                result_text.color = ft.colors.GREEN
        except Exception as ex:
            session.rollback()
            result_text.value = f"Erro ao salvar a tarefa: {str(ex)}"
            result_text.color = ft.colors.RED
        finally:
            session.close()

        # Atualizar a interface
        carregar_tarefas()
        descricao_input.value = ""
        situacao_input.value = False
        page.update()

    # Função para carregar as tarefas
    # Função para carregar as tarefas
    def carregar_tarefas():
        session = Session()
        try:
            tarefas_column.controls.clear()
            tarefas = session.query(Tarefa).all()
            for tarefa in tarefas:
                cor_tarefa = determinar_cor_tarefa(tarefa)
                nova_tarefa = ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        tarefa.descricao,
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_tarefa,
                                    ),
                                    ft.Text(
                                        f"Data de entrega: {tarefa.data_entrega}",
                                        size=14,
                                        color=cor_tarefa,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        tooltip="Editar Tarefa",
                                        on_click=lambda e, t=tarefa: exibir_edicao_tarefa(t),
                                        icon_color=ft.colors.ORANGE,
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        tooltip="Excluir Tarefa",
                                        on_click=lambda e, t=tarefa: excluir_tarefa_com_confirmacao(t),
                                        icon_color=ft.colors.RED,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os ícones
                                spacing=15,  # Espaçamento entre os ícones
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=15,
                    border_radius=ft.border_radius.all(10),
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=10,
                        color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                    ),
                    margin=ft.Margin(left=0, top=0, right=0, bottom=10),
                )
                tarefas_column.controls.append(nova_tarefa)
            tarefas_column.update()
        finally:
            session.close()
        atualizar_estatisticas()

    # Função para exibir a tela de edição de tarefa
    def exibir_edicao_tarefa(tarefa):
        nonlocal tarefa_em_edicao, data_entrega
        tarefa_em_edicao = tarefa
        descricao_input.value = tarefa.descricao
        situacao_input.value = tarefa.situacao
        data_entrega = tarefa.data_entrega

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Editar Tarefa",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE,
                        ),
                        ft.Row([descricao_input], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([situacao_input], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([date_picker_button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Salvar Alterações",
                                    on_click=salvar_edicao_tarefa,
                                    bgcolor=ft.colors.GREEN,
                                    color=ft.colors.WHITE,
                                    icon=ft.icons.SAVE,
                                ),
                                ft.ElevatedButton(
                                    "Cancelar",
                                    on_click=lambda e: exibir_listagem_tarefas(),
                                    bgcolor=ft.colors.RED,
                                    color=ft.colors.WHITE,
                                    icon=ft.icons.CANCEL,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        result_text,
                    ],
                    spacing=15,
                ),
                padding=20,
                border_radius=ft.border_radius.all(15),
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(
                    spread_radius=4,
                    blur_radius=15,
                    color=ft.colors.with_opacity(0.3, ft.colors.BLACK),
                ),
            )
        )
        page.update()

    # Função para salvar a edição da tarefa
    def salvar_edicao_tarefa(e):
        nonlocal tarefa_em_edicao

        if not descricao_input.value:
            result_text.value = "Por favor, insira a descrição da tarefa."
            result_text.color = ft.colors.RED
            page.update()
            return

        if not data_entrega:
            result_text.value = "Por favor, selecione a data de entrega."
            result_text.color = ft.colors.RED
            page.update()
            return

        session = Session()
        try:
            tarefa_editada = session.query(Tarefa).filter(Tarefa.id == tarefa_em_edicao.id).first()
            if tarefa_editada:
                tarefa_editada.descricao = descricao_input.value.strip()
                tarefa_editada.situacao = situacao_input.value
                tarefa_editada.data_entrega = data_entrega
                session.commit()
                result_text.value = "Tarefa editada com sucesso!"
                result_text.color = ft.colors.GREEN
            else:
                result_text.value = "Erro: Tarefa não encontrada."
                result_text.color = ft.colors.RED
        except Exception as ex:
            session.rollback()
            result_text.value = f"Erro ao salvar a tarefa: {str(ex)}"
            result_text.color = ft.colors.RED
        finally:
            session.close()

        tarefa_em_edicao = None
        exibir_listagem_tarefas()

    # Função para excluir uma tarefa com confirmação
    def excluir_tarefa_com_confirmacao(tarefa):
        def confirmar_exclusao(e):
            session = Session()
            try:
                tarefa_a_excluir = session.query(Tarefa).filter(Tarefa.id == tarefa.id).first()
                if tarefa_a_excluir:
                    session.delete(tarefa_a_excluir)
                    session.commit()
                    result_text.value = "Tarefa excluída com sucesso!"
                    result_text.color = ft.colors.GREEN
                else:
                    result_text.value = "Erro: Tarefa não encontrada."
                    result_text.color = ft.colors.RED
            except Exception as ex:
                session.rollback()
                result_text.value = f"Erro ao excluir a tarefa: {str(ex)}"
                result_text.color = ft.colors.RED
            finally:
                session.close()
                carregar_tarefas()
                page.close(dialog)
                page.update()

        def cancelar_exclusao(e):
            page.close(dialog)
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Tem certeza de que deseja excluir a tarefa '{tarefa.descricao}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_exclusao),
                ft.TextButton(
                    "Excluir",
                    on_click=confirmar_exclusao,
                    style=ft.ButtonStyle(bgcolor=ft.colors.RED, color=ft.colors.WHITE),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        page.open(dialog)
        page.update()

    # Botão "Salvar Tarefa"
    salvar_button = ft.ElevatedButton(
        "Cadastrar Tarefa",
        on_click=salvar_tarefa,
        bgcolor=ft.colors.GREEN,
        color=ft.colors.WHITE,
        icon=ft.icons.ADD_TASK,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            padding=ft.Padding(left=25, right=25, top=15, bottom=15),
            elevation=5,
        ),
    )

    # Coluna para exibir as tarefas
    tarefas_column = ft.Column(
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Função para exibir o menu inicial
    def exibir_menu_inicial():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "Bem-vindo ao Organizador de Tarefas!",
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.BLUE,
                            border_radius=ft.border_radius.all(15),
                            shadow=ft.BoxShadow(
                                spread_radius=4,
                                blur_radius=10,
                                color=ft.colors.with_opacity(0.3, ft.colors.BLACK),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=ft.Padding(left=20, right=20, top=20, bottom=20),
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.LIGHT_BLUE),
            )
        )
        page.update()

    # Função para exibir o cadastro de tarefas
    def exibir_cadastro_tarefas():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([descricao_input], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([situacao_input], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([date_picker_button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([salvar_button], alignment=ft.MainAxisAlignment.CENTER),
                        result_text,
                    ],
                    spacing=15,
                ),
                padding=20,
                border_radius=ft.border_radius.all(15),
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(
                    spread_radius=4,
                    blur_radius=15,
                    color=ft.colors.with_opacity(0.3, ft.colors.BLACK),
                ),
            )
        )
        page.update()

    # Função para exibir a listagem de tarefas
    def exibir_listagem_tarefas():
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Tarefas Cadastradas",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE,
                        ),
                        tarefas_column,
                    ],
                    spacing=15,
                ),
                padding=20,
                border_radius=ft.border_radius.all(15),
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.LIGHT_BLUE),
                shadow=ft.BoxShadow(
                    spread_radius=4,
                    blur_radius=15,
                    color=ft.colors.with_opacity(0.3, ft.colors.BLACK),
                ),
            )
        )
        carregar_tarefas()
        page.update()

    # Adicionando a barra de navegação
    def navegar(e):
        if e.control.selected_index == 0:
            exibir_menu_inicial()
        elif e.control.selected_index == 1:
            exibir_cadastro_tarefas()
        elif e.control.selected_index == 2:
            exibir_listagem_tarefas()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Início"),
            ft.NavigationBarDestination(icon=ft.icons.ADD, label="Cadastro"),
            ft.NavigationBarDestination(icon=ft.icons.LIST, label="Listagem"),
        ],
        on_change=navegar,
    )

    # Exibe o menu inicial ao iniciar o aplicativo
    exibir_menu_inicial()