import flet as ft
from view.tarefa_view import on_add_tarefa_click

class Page1:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        page.theme = ft.Theme(font_family="MarioText")
    
    def construir(self):
        self.page.title = "Cadastro de Tarefa"
        self.page.padding = 20
        self.page.scroll = None
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.horizontal_alignment = ft.MainAxisAlignment.START

        def atualizar_layout(e=None):
            largura_disponivel = self.page.width
            descricao_input.width = largura_disponivel - btn_tema.width  # Ajuste para incluir o botão de tema
            background_image.content.width = self.page.width  # Atualiza largura da imagem
            background_image.content.height = self.page.height  # Atualiza altura da imagem
            self.page.update()
        
        # Primeira imagem de fundo
        background_image = ft.Container(
            content=ft.Image(
                src="/imgs/Underground.png" if self.page.theme_mode == ft.ThemeMode.DARK else "/imgs/Overworld.png",  # Caminho da imagem de fundo
                width=self.page.width,
                height=self.page.height,  # Aumenta ainda mais a altura da imagem de fundo
                fit=ft.ImageFit.COVER
            )
        )

        # Função para alternar entre as rotas
        def change_route(e):
            # Acessamos o índice selecionado pela instância da barra de navegação
            if self.page.navigation_bar.selected_index == 0:
                self.page.go("/cadastro")
            elif self.page.navigation_bar.selected_index == 1:
                self.page.go("/listagem")

        # Barra de navegação
        self.page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EDIT_OUTLINED, selected_icon=ft.Icons.EDIT_SHARP, label="Cadastro"),
                ft.NavigationBarDestination(icon=ft.Icons.VIEW_LIST_OUTLINED, selected_icon=ft.Icons.VIEW_LIST, label="Listagem"),
            ],
            on_change=change_route  # Define a função de troca de rota
        )

        descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300, border_color=ft.Colors.WHITE, label_style=ft.TextStyle(size=13))
        situacao_input = ft.Checkbox(label="Tarefa concluída", value=False, label_style=ft.TextStyle(size=13))
        
        def hover(e, container):
            if e.data == "true":
                img.visible = True
            else:
                img.visible = False
            self.page.update()

        img = ft.Image(src="/imgs/setaMario.png", width=15, height=15, visible=False)

        add_button = ft.Container(
            content=ft.Row(
                [
                    img,
                    ft.Text("Adicionar Tarefa", style=ft.TextStyle(size=13, font_family="MarioText")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=lambda e: on_add_tarefa_click(e, descricao_input, situacao_input, result_text),
            on_hover=lambda e: hover(e, add_button),
            bgcolor=ft.Colors.TRANSPARENT,
            width=200,
            height=50,
            border_radius=10,
            padding=10,
        )


        def alterar_tema(e):
            _ = e  # Access "e" to avoid the compile error
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
                btn_tema.icon = ft.Icons.WB_SUNNY_OUTLINED
                background_image.content.src = "/imgs/Underground.png"
                btn_tema.icon_color = ft.Colors.WHITE
                descricao_input.border_color = ft.Colors.WHITE
                if descricao_input.value:
                    descricao_input.text_style = ft.TextStyle(color=ft.Colors.WHITE)  # Update text style
                descricao_input.label_style.color = ft.Colors.WHITE
                situacao_input.label_style.color = ft.Colors.WHITE
                add_button.content.controls[1].style.color = ft.Colors.WHITE
            else:
                self.page.theme_mode = ft.ThemeMode.LIGHT
                btn_tema.icon = ft.Icons.NIGHTS_STAY_OUTLINED
                background_image.content.src = "/imgs/Overworld.png"
                btn_tema.icon_color = 'black'
                descricao_input.border_color = 'black'
                if descricao_input.value:
                    descricao_input.text_style = ft.TextStyle(color='black')  # Update text style
                descricao_input.label_style.color = 'black'
                situacao_input.label_style.color = 'black'
                add_button.content.controls[1].style.color = 'black'
            descricao_input.update()  # Explicitly update the TextField
            self.page.update()

        btn_tema = ft.IconButton(
            icon=ft.Icons.WB_SUNNY_OUTLINED,
            icon_color=ft.Colors.WHITE,
            tooltip="Alternar tema entre claro e escuro",
            on_click=lambda e: alterar_tema(e),
            width=50
        )
        
        result_text = ft.Text()

        self.page.add(ft.Stack(
            [
                background_image,  # Adicionado como fundo
                ft.ResponsiveRow(
                    [
                        ft.Image(src="/imgs/TituloCadastro.png", width=300, height=50),
                        ft.Row(
                            [
                                ft.Container(descricao_input, expand=True),
                                ft.Container(btn_tema, width=50),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(situacao_input),
                        ft.Container(add_button),
                        ft.Container(result_text),
                    ]
                ),
            ]
        ))

        self.page.on_resized = atualizar_layout
        atualizar_layout()
        self.page.update()