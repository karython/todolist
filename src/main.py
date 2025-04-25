import flet as ft
from view.inicial import Home as Inicial
from view.home import Home
from view.tarefa_view import TarefaView
import random

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = None
    page.clean()
    page.padding = 0
    page.spacing = 0

    # Configuração global da fonte
    page.fonts = {
        "Mine": "/fonts/minecraftia/Minecraftia-Regular.ttf",
        "Mine 2": "/fonts/minedings/minedings.ttf",
        "Mine 3": "/fonts/minecraft-1-0/minecraft_10.ttf",
    }
    page.theme = ft.Theme(font_family="Mine")
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = True
    page.window_width = 360
    page.window_height = 640
    page.icon = "/assets/img/icon.ico"

    # Seleciona o vídeo aleatório uma vez
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

    def rotas(route):
        page.controls.clear()
        if route == '/inicial':
            tela = Inicial(page, video_escolhido)  # Passa o vídeo selecionado
        elif route == '/home':
            tela = Home(page)
        elif route == '/listagem':
            tela = TarefaView(page)
        else:
            tela = Inicial(page, video_escolhido)  # Passa o vídeo selecionado

        page.add(tela.construir())
        page.update()

    page.on_route_change = lambda e: rotas(e.route)
    page.go('/inicial')
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
