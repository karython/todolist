import datetime
import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas

def main(page: ft.Page):
    page.title = "Gerenciador de Tarefas"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.SYSTEM

    # Variáveis globais para os controles
    descricao_input = ft.TextField(label="Descrição da Tarefa", expand=True)
    result_text = ft.Text(size=16, color="green")
    tarefas_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    data_conclusao = None

    # Função para lidar com a mudança de data
    def handle_date_change(e):
        nonlocal data_conclusao
        data_conclusao = e.control.value.strftime("%Y-%m-%d")
        result_text.value = f"Data selecionada: {data_conclusao}"
        result_text.update()

    # Tela inicial
    def tela_inicial():
        def entrar_no_aplicativo(e):
            page.controls.clear()
            page.add(adicionar_tarefa_view())
            page.navigation_bar.visible = True  # Exibe a NavigationBar
            page.update()

        return ft.Column(
            [
                ft.Image(
                    src="https://via.placeholder.com/150",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text(
                    "Bem-vindo ao Gerenciador de Tarefas!",
                    size=24,
                    weight="bold",
                    color="blue",
                    text_align=ft.TextAlign.CENTER,
                    animate_opacity=300,
                ),
                ft.Text(
                    "Organize suas tarefas de forma simples e eficiente.",
                    size=16,
                    color="gray",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    "Entrar no Aplicativo",
                    on_click=entrar_no_aplicativo,
                    style=ft.ButtonStyle(
                        bgcolor="blue",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding(20, 10, 20, 10),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    # Conteúdo da aba "Adicionar Tarefa"
    def adicionar_tarefa_view():
        return ft.Column(
            [
                ft.Text("Adicionar Nova Tarefa", size=24, weight="bold", color="blue"),
                descricao_input,
                ft.ElevatedButton(
                    "Selecionar Data de Conclusão",
                    icon=ft.icons.CALENDAR_MONTH,
                    on_click=lambda e: page.open(
                        ft.DatePicker(
                            first_date=datetime.datetime(year=2023, month=10, day=1),
                            last_date=datetime.datetime(year=2030, month=12, day=31),
                            on_change=handle_date_change,
                        )
                    ),
                ),
                ft.ElevatedButton(
                    "Cadastrar Tarefa",
                    icon=ft.icons.ADD,
                    on_click=lambda e: on_add_tarefa_click(
                        e, descricao_input, data_conclusao, result_text, tarefas_column
                    ),
                ),
                result_text,
            ],
            spacing=20,
        )

    # Conteúdo da aba "Tarefas Adicionadas"
    def tarefas_adicionadas_view():
        atualizar_lista_tarefas(tarefas_column, result_text, page)
        return ft.Column(
            [
                ft.Text("Tarefas Adicionadas", size=24, weight="bold", color="blue"),
                tarefas_column,
            ],
            spacing=20,
        )

    # Função para alternar entre as abas
    def on_navigation_change(e):
        page.controls.clear()
        if e.control.selected_index == 0:
            page.add(adicionar_tarefa_view())
        elif e.control.selected_index == 1:
            page.add(tarefas_adicionadas_view())
        page.update()

    # NavigationBar
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.ADD, label="Adicionar"),
            ft.NavigationBarDestination(icon=ft.icons.LIST, label="Tarefas"),
        ],
        on_change=on_navigation_change,
        visible=False,  # Oculta a NavigationBar inicialmente
    )

    # Exibe a tela inicial
    page.add(tela_inicial())
    page.update()