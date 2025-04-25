from PIL import Image
import io
import base64
import datetime
import flet as ft
from view.tarefa_view import TarefaView
from services.tarefa_service import cadastrar_tarefa
import random  # Importa o módulo random

def encode_image_to_base64(path):
    img = Image.open(path)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

# Seleciona o vídeo aleatório apenas uma vez
video_escolhido = random.choice([
    "video/aids.mp4",
    "video/aids2.mp4",
    "video/aids3.mp4",
    "video/aids4.mp4",
    "video/aids5.mp4",
    "video/aids6.mp4",
    "video/aids7.mp4",
    "video/aids8.mp4"
])

class Home:
    def __init__(self, page: ft.Page, video_escolhido: str):
        self.page = page
        # Armazena o plano de fundo inicial na sessão, se ainda não estiver definido
        if not self.page.session.contains_key("selected_background"):
            self.page.session.set("selected_background", video_escolhido)

    def _on_hover(self, e):
        """Função para hover nos botões"""
        e.control.bgcolor = "#8A8A8A" if e.data == "true" else "#6E6E6E"
        e.control.update()

    def construir(self):
        self.page.clean()
        self.page.padding = 0
        self.page.spacing = 0

        # Função para atualizar a tela ao redimensionar
        def atualizar_tela(e):
            self.page.update()

        self.page.on_resize = atualizar_tela

        # Mapear opções para vídeos correspondentes
        video_map = {
            "Floresta": "video/aids.mp4",
            "Nevasca": "video/aids2.mp4",
            "Caverna": "video/aids3.mp4",
            "Deserto": "video/aids4.mp4",
            "Taiga": "video/aids5.mp4",
            "Cerejeira": "video/aids6.mp4",
            "Pântano": "video/aids7.mp4",
            "Oceano": "video/aids8.mp4",
        }

        # Função para recriar o vídeo local como fundo
        def atualizar_video(video_path):
            nonlocal video_background
            new_video = criar_video_background(video_path)  # Cria um novo componente de vídeo
            stack.controls[0] = new_video  # Substitui o vídeo no Stack
            video_background = new_video  # Atualiza a referência do vídeo
            self.page.update()  # Atualiza a página para refletir a mudança

        # Função para criar o vídeo local como fundo
        def criar_video_background(video_path):
            return ft.Video(
                expand=True,
                playlist=[ft.VideoMedia(video_path)],  # Define a playlist com o vídeo
                playlist_mode=ft.PlaylistMode.LOOP,
                fill_color=None,
                aspect_ratio=None,
                volume=0,
                autoplay=True,
                filter_quality=ft.FilterQuality.HIGH,
                muted=True,
                fit=ft.ImageFit.COVER,
                on_loaded=lambda e: e.control.play(),
            )

        # Recupera o plano de fundo selecionado da sessão
        selected_background = (
            self.page.session.get("selected_background")
            if self.page.session.contains_key("selected_background")
            else "video/aids.mp4"
        )

        # Inicializa o vídeo local como fundo com o plano de fundo selecionado
        video_background = criar_video_background(selected_background)

        # Determina a opção inicial selecionada no dropdown com base no plano de fundo selecionado
        initial_option = next(
            (key for key, value in video_map.items() if value == selected_background),
            None
        )

        # Imagem "tarefas.png" no início da tela
        imagem_tarefas = ft.Image(
            src=encode_image_to_base64("src/assets/img/tarefas.png"),
            fit=ft.ImageFit.CONTAIN,  # Ajusta a imagem para caber no espaço disponível
            width=min(self.page.width * 0.9, 600),  # Define a largura como 90% da largura da tela, com limite máximo de 600px
            height=min(self.page.height * 0.3, 300)  # Define a altura como 30% da altura da tela, com limite máximo de 300px
        )

        imagem_tarefas_container = ft.Container(
            content=imagem_tarefas,
            alignment=ft.alignment.top_center,  # Posiciona a imagem no início da tela
            padding=ft.padding.only(top=5),  # Adiciona um pequeno espaçamento superior
            expand=False
        )

        # Botão para abrir a tela de cadastro (Home)
        btn_cadastro = ft.Container(
            width=200,  # Aumenta a largura do botão
            height=50,  # Aumenta a altura do botão
            alignment=ft.alignment.center,
            bgcolor="#6E6E6E",
            border=ft.border.all(1, "#5C5C5C"),
            border_radius=ft.border_radius.all(5),
            shadow=ft.BoxShadow(blur_radius=3, color="black", spread_radius=1),
            content=ft.ElevatedButton(
                content=ft.Row(
                    [ft.Text("Abrir Cadastro", color="white", size=14)],  # Aumenta o tamanho do texto
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=7
                ),
                on_click=lambda e: self.page.go('/home'),
                bgcolor="transparent",
                color="white",
                elevation=0
            ),
            on_hover=self._on_hover
        )

        # Botão para abrir a tela de listagem (TarefaView)
        btn_listagem = ft.Container(
            width=200,  # Aumenta a largura do botão
            height=50,  # Aumenta a altura do botão
            alignment=ft.alignment.center,
            bgcolor="#6E6E6E",
            border=ft.border.all(1, "#5C5C5C"),
            border_radius=ft.border_radius.all(5),
            shadow=ft.BoxShadow(blur_radius=3, color="black", spread_radius=1),
            content=ft.ElevatedButton(
                content=ft.Row(
                    [ft.Text("Abrir Listagem", color="white", size=14)],  # Aumenta o tamanho do texto
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=7
                ),
                on_click=lambda e: self.page.go('/listagem'),
                bgcolor="transparent",
                color="white",
                elevation=0
            ),
            on_hover=self._on_hover
        )

        # Opções para o dropdown
        options = [
            {"name": "Floresta", "icon": lambda: ft.Text("v", font_family="Mine 2")},
            {"name": "Nevasca", "icon": lambda: ft.Icon(ft.Icons.DEVICE_THERMOSTAT)},
            {"name": "Caverna", "icon": lambda: ft.Text("g", font_family="Mine 3")},
            {"name": "Deserto", "icon": lambda: ft.Text("Z", font_family="Mine 3")},
            {"name": "Taiga", "icon": lambda: ft.Text("Q", font_family="Mine 3")},
            {"name": "Cerejeira", "icon": lambda: ft.Text("B", font_family="Mine 3")},
            {"name": "Pântano", "icon": lambda: ft.Text("V", font_family="Mine 3")},
            {"name": "Oceano", "icon": lambda: ft.Text("k", font_family="Mine 2")},
        ]

        def get_options():
            dropdown_options = []
            for option in options:
                dropdown_options.append(
                    ft.DropdownOption(
                        key=option["name"],
                        text=option["name"],
                        leading_icon=option["icon"]()  # Gera um novo ícone para cada opção
                    )
                )
            return dropdown_options

        # Função para atualizar o rótulo do dropdown e o plano de fundo do vídeo
        def on_option_change(e):
            selected_option = next(
                (opt for opt in options if opt["name"] == e.control.value), None
            )
            if selected_option:
                # Atualiza o plano de fundo na sessão
                self.page.session.set("selected_background", video_map[e.control.value])
                dropdown.value = e.control.value  # Atualiza o valor do dropdown
                dropdown.leading_icon = ft.Row(
                    [
                        ft.Container(
                            content=selected_option["icon"](),  # Gera um novo ícone para o rótulo
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=ft.Text(e.control.value, color="white", size=14),
                            padding=ft.padding.only(left=10)  # Adiciona espaçamento à esquerda
                        )
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                )
                # Atualiza o vídeo com o novo plano de fundo
                stack.controls[0] = criar_video_background(self.page.session.get("selected_background"))
                self.page.update()

        # Dropdown no canto superior esquerdo
        dropdown = ft.Dropdown(
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=False,
            label=None,  # Remove o texto inicial
            leading_icon=ft.Row(
                [
                    ft.Container(
                        content=next(
                            (opt["icon"]() for opt in options if opt["name"] == initial_option),
                            None
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text(initial_option, color="white", size=14),
                        padding=ft.padding.only(left=10)  # Adiciona espaçamento à esquerda
                    )
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.START
            ),
            options=get_options(),
            value=initial_option,  # Define a opção inicial selecionada
            width=150,  # Largura ajustada
            bgcolor="#6E6E6E",  # Fundo cinza
            border_radius=ft.border_radius.all(5),
            on_change=on_option_change,  # Chama a função ao alterar a opção
        )

        # Layout centralizado com rolagem automática
        content = ft.Column(
            [
                ft.Container(  # Adiciona o dropdown no canto superior esquerdo
                    content=dropdown,
                    alignment=ft.alignment.top_left,  # Posiciona o dropdown no canto superior esquerdo
                    padding=ft.padding.only(left=10, top=10),  # Adiciona espaçamento interno
                    expand=False  # Garante que o dropdown não bloqueie outros controles
                ),
                imagem_tarefas_container,  # Adiciona o container da imagem no início
                btn_cadastro,
                btn_listagem
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha os elementos ao início da tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,  # Aumenta o espaçamento entre os botões
            scroll=ft.ScrollMode.AUTO  # Permite rolagem automática em dispositivos móveis
        )

        # Stack principal
        stack = ft.Stack(
            [
                video_background,  # Vídeo como fundo
                ft.Container(
                    content=content,
                    expand=True,
                    alignment=ft.alignment.top_center,  # Alinha o conteúdo ao topo
                    padding=ft.padding.only(top=-0)  # Mantém os elementos mais para cima
                )
            ],
            expand=True
        )

        # Adiciona o Stack à página
        self.page.add(stack)

        # Retorna o Stack principal
        return stack
