import flet as ft
from view.Page1 import Page1
from view.Page2 import Page2
from view.InitialPage import InitialPage


def main(page: ft.Page):
    page.title = "ToDo List"
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.fonts = {"MarioTitle": '/fonts/RetroMario.otf',
                  "MarioText": '/fonts/SMW_TextBox.ttf'}
    
    page.theme = ft.Theme(font_family="MarioText")

    # Função para construir a página com base na rota
    def cons_route(e):
        page.clean()  # Limpa os controles da página
        if page.route == "/inicio":
            initial_page = InitialPage(page)
            initial_page.construir()
        elif page.route == "/cadastro":
            page1 = Page1(page)
            page1.construir()
        elif page.route == "/listagem":
            page2 = Page2(page)
            page2.construir()
        else:
            page.go("/inicio")  # Redireciona para a rota padrão
        page.update()


    # Define a rota inicial e o callback para alteração de rota
    page.route = "/inicio"
    page.on_route_change = cons_route

    cons_route(None)
    page.update()