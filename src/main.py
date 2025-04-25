import flet as ft
from view.home import main  # Importe a função main do arquivo home.py

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = 'adaptive'

    # Adiciona um indicador de carregamento
    loading_indicator = ft.ProgressRing()
    page.add(loading_indicator)
    page.update()

    def on_resize(e):
        page.update()  # Atualiza a página ao redimensionar

    page.on_resize = on_resize  # Adiciona o evento de redimensionamento

    # Remove apenas o indicador de carregamento
    page.controls.remove(loading_indicator)
    page.update()

    # Chama a função main do arquivo home.py para carregar a interface
    from view.home import main as home_main
    home_main(page)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)  # Executa o aplicativo Flet, passando a função main como alvo

