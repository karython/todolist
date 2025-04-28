import flet as ft
from view.home import main  # Importe a função main do arquivo home.py

if __name__ == "__main__":
  ft.app(target=main, view=ft.WEB_BROWSER)    # Alterado para executar como uma janela nativa