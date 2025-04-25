import flet as ft
from view.tarefa_view import atualizar_lista_tarefas, Task  # Importa Task para configurar o tema

class Page2:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        page.theme = ft.Theme(font_family="MarioText")

    def construir(self):
        # Configurações iniciais da página
        self.page.title = "Listagem de Tarefas"
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.padding = 20
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.horizontal_alignment = ft.MainAxisAlignment.START

        
        # Primeira imagem de fundo
        background_image = ft.Container(
            content=ft.Image(
                src="/imgs/Underground.png" if self.page.theme_mode == ft.ThemeMode.DARK else "/imgs/Overworld.png",  # Caminho da imagem de fundo
                width=self.page.width,
                height=self.page.height,  # Aumenta ainda mais a altura da imagem de fundo
                fit=ft.ImageFit.COVER
            )
        )

        # Cabeçalho com as colunas da "tabela", usando containers expansíveis
        cabecalho = ft.Row(  # Alterado de ResponsiveRow para Row
            controls=[
            ft.Container(
                content=ft.Text(
                "Descrição", 
                weight="bold", 
                font_family="MarioText", 
                size=13, 
                color="#FFF8E1" if self.page.theme_mode == ft.ThemeMode.DARK else "#000000"
                ),
                expand=1,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Text(
                "Concluída", 
                weight="bold", 
                font_family="MarioText", 
                size=13, 
                color="#FFF8E1" if self.page.theme_mode == ft.ThemeMode.DARK else "#000000"
                ),
                expand=1,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Text(
                "Ações", 
                weight="bold", 
                font_family="MarioText", 
                size=13, 
                color="#FFF8E1" if self.page.theme_mode == ft.ThemeMode.DARK else "#000000"
                ),
                expand=1,
                alignment=ft.alignment.center
            )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        )

        # Container que abrigará a lista de tarefas (em modo ResponsiveRow)
        tarefas_list = ft.Column(
            expand=True,
            spacing=10
        )

        # Define o tema para as tarefas
        Task.theme_mode = self.page.theme_mode

        # Layout principal: Cabeçalho + lista de tarefas
        self.page.add(
            ft.Stack(
            [
                background_image, 
                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Image(
                                    src="/imgs/TituloListagem.png", 
                                    width=300, 
                                    height=50
                                )
                            ], 
                            alignment=ft.MainAxisAlignment.CENTER), 
                            cabecalho, 
                            tarefas_list
                            ]
                        ),
            ]
            )
        )

        # Atualiza a lista de tarefas ao carregar a página
        atualizar_lista_tarefas(tarefas_list)
        background_image.content.height = len(tarefas_list.controls)*1.8*(tarefas_list.spacing + self.page.padding)
        background_image.update()
        self.page.update()
