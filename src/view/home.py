import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = 'adaptive'


    # Define o tema da página corretamente
    page.theme = ft.Theme(
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                font_family="Heveltica",
                weight=ft.FontWeight.BOLD,
                italic=True
            )
        )
    )
    page.theme_mode = ft.ThemeMode.DARK  # Define o tema como escuro

    titulo = ft.Text( # Título da página
        "To do List",
        font_family="Heveltica",
        text_align="center",
        italic=True,
        weight=ft.FontWeight.BOLD,
        size=50,
        color=ft.Colors.AMBER_500
    )

    descricao_input = ft.TextField( # Campo de entrada para a descrição da tarefa
        label="Descrição da Tarefa",
        label_style=ft.TextStyle(color=ft.Colors.AMBER_500),
        autofocus=True,
        expand=True, 
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.AMBER_500,
        border_color=ft.Colors.DEEP_ORANGE_900,
        text_style=ft.TextStyle(color=ft.Colors.AMBER_500),
        max_length=30,
        keyboard_type=ft.KeyboardType.TEXT  
    )

    situacao_input = ft.Checkbox( # Checkbox para indicar se a tarefa está concluída
        label="Tarefa concluída",
        value=False,
        fill_color=ft.Colors.GREEN_100,
        label_style=ft.TextStyle(color=ft.Colors.AMBER_500)
    )

    add_button = ft.ElevatedButton( # Botão para adicionar a tarefa
        "Cadastrar Tarefa",
        on_click=lambda e: [
            on_add_tarefa_click(
                e,
                descricao_input,
                situacao_input,
                result_text_container.content,  
                tarefas_column
            ),
            setattr(descricao_input, "value", ""),
            descricao_input.update()
        ],
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )

    tarefas_column = ft.Column( # Coluna para exibir as tarefas cadastradas
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,  
        scroll=ft.ScrollMode.AUTO
    )

    result_text_container = ft.Container(  # Container para exibir mensagens de resultado
        content=ft.Text(
            color=ft.Colors.AMBER_500,
            font_family="Heveltica",
            italic=True,
            weight=ft.FontWeight.BOLD,
            expand=True 
        ),
        bgcolor=ft.Colors.WHITE,
        opacity=0.5,
        padding=ft.Padding(10, 10, 10, 10)  # Corrige o erro adicionando os quatro argumentos
    )

    refresh_page_button = ft.ElevatedButton( # Botão para atualizar a lista de tarefas
        "Atualizar Página",
        on_click=lambda e: atualizar_lista_tarefas(
            tarefas_column,
            result_text_container.content 
        ),
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )

    # Imagem de fundo via ft.Image
    fundo = ft.Container(
        content=ft.Image(
            src="https://i.postimg.cc/FHtV5J9S/system.jpg",
            fit=ft.ImageFit.COVER, 
            width=page.width,      
            height=page.height,   
        ),
        expand=True,
        opacity=0.5,  
    )

    conteudo = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [titulo],
                    alignment=ft.MainAxisAlignment.CENTER  # Alinha o título ao centro
                ),
                descricao_input,
                ft.Row(
                    [situacao_input, add_button],  # Checkbox e botão alinhados à esquerda
                    alignment=ft.MainAxisAlignment.START
                ),
                tarefas_column,
                ft.Row(
                    [refresh_page_button],
                    alignment=ft.MainAxisAlignment.CENTER  # Alinha o botão "Atualizar Página" ao centro
                ),
                result_text_container  
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True 
        ),
        margin=ft.Margin(20, 20, 20, 20)
    )

    page.add(
        ft.Stack(
            controls=[fundo, conteudo]
        )
    )

    def on_resize(e):
        # Atualiza o tamanho da imagem ao redimensionar a página
        fundo.content.width = page.width
        fundo.content.height = page.height
        page.update()

    page.on_resize = on_resize
    atualizar_lista_tarefas(tarefas_column, result_text_container.content)

