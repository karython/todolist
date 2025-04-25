import flet as ft
from view.interface import ListaTarefas  


def main(page: ft.Page):
    # Configurações da página
    page.scroll = "always"  # Habilita scroll horizontal e vertical
    page.horizontal_alignment = ft.CrossAxisAlignment.START  # Alinha o conteúdo à esquerda
    page.vertical_alignment = ft.MainAxisAlignment.START  # Alinha o conteúdo ao topo
    page.padding = 20
    page.auto_scroll = True

    # Adiciona a aplicação principal
    app = ListaTarefas(page)
    page.add(app)

ft.app(target=main)