import flet as ft
from view.tarefa_view import on_add_tarefa_click, on_excluir_tarefa_click, on_editar_tarefa_click
from model.tarefa_model import Tarefa
from connection import Session

def main(page: ft.Page):
    page.title = "Gerenciador de Tarefas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    page.theme = ft.Theme(font_family="Montserrat")

    def alternar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text(
            "Gerenciador de Tarefas",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE,
        ),
        center_title=True,
        bgcolor=ft.colors.BLUE_GREY_900,
        actions=[
            ft.IconButton(
                icon=ft.icons.BRIGHTNESS_6,
                tooltip="Alternar Tema",
                on_click=alternar_tema,
            )
        ],
    )

    descricao_input = ft.TextField(label="Descrição da Tarefa", width=300)

    situacao_input = ft.Checkbox(
        value=False,
        label="Concluída",
        scale=1.5,
    )

    result_text = ft.Text(
        "",
        size=14,
        color=ft.colors.RED_ACCENT,
        weight=ft.FontWeight.BOLD,
    )

    listar_result_text = ft.Text(
        "",
        size=14,
        color=ft.colors.RED_ACCENT,
        weight=ft.FontWeight.BOLD,
    )

    lista_tarefas = ft.Column(
        spacing=10,  # Espaçamento entre as linhas de tarefas
        scroll=ft.ScrollMode.AUTO,  # Adiciona rolagem para dispositivos móveis
    )

    def atualizar_tabela():
        lista_tarefas.controls.clear()  # Limpa a lista de tarefas
        session = Session()
        try:
            tarefas = session.query(Tarefa).all()
            for tarefa in tarefas:
                # Adiciona cada tarefa à lista
                lista_tarefas.controls.append(
                    ft.Row(
                        [
                            ft.Text(
                                tarefa.descricao,
                                size=16,
                                no_wrap=False,
                                max_lines=2,
                                overflow="ellipsis",
                                expand=True,
                            ),
                            ft.Text(
                                "Concluída" if tarefa.situacao else "Pendente",
                                size=14,
                                color=ft.colors.GREEN if tarefa.situacao else ft.colors.RED,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        tooltip="Editar Tarefa",
                                        icon_color=ft.colors.BLUE,
                                        icon_size=20,
                                        on_click=lambda e, tarefa_id=tarefa.id: on_editar_tarefa_click(
                                            e, tarefa_id, descricao_input, situacao_input, page, atualizar_tabela,listar_layout
                                        ),
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        tooltip="Excluir Tarefa",
                                        icon_color=ft.colors.RED,
                                        icon_size=20,
                                        on_click=lambda e, tarefa_id=tarefa.id: on_excluir_tarefa_click(
                                            e, tarefa_id, listar_result_text, lista_tarefas, atualizar_tabela
                                        ),
                                    ),
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
            lista_tarefas.update()  # Atualiza a lista de tarefas
        finally:
            session.close()

    add_button = ft.IconButton(
        icon=ft.icons.ADD,
        tooltip="Adicionar Tarefa",
        icon_size=32,
        bgcolor=ft.colors.GREEN,
        icon_color=ft.colors.WHITE,
        on_click=lambda e: on_add_tarefa_click(
            e, descricao_input, situacao_input, result_text, lista_tarefas, atualizar_tabela
        ),
    )

    cadastrar_layout = ft.Column(
        [
            descricao_input,
            ft.Row(
                [
                    situacao_input,
                    ft.Container(width=20),
                    add_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            result_text,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    listar_layout = ft.Column(
        [
            ft.Text("Listar Tarefas", size=28, weight=ft.FontWeight.BOLD),
            lista_tarefas,  # Substitui a tabela pela lista de tarefas
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,  # Adiciona rolagem para dispositivos móveis
        expand=True,  # Faz o layout ocupar o espaço disponível
    )

    def mudar_aba(e):
        aba_selecionada = e.control.selected_index

        # Limpa os controles da página
        page.controls.clear()

        # Adiciona o layout correto com base na aba selecionada
        if aba_selecionada == 0:
            page.add(cadastrar_layout)
        elif aba_selecionada == 1:
            page.add(listar_layout)
            atualizar_tabela()  # Atualiza a tabela de tarefas

        # Atualiza a página
        page.update()

    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.BLUE_GREY_900,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.LIGHT_BLUE_500,
        on_change=mudar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.ADD),
            ft.NavigationBarDestination(icon=ft.icons.LIST),
        ],
    )

    page.add(cadastrar_layout)