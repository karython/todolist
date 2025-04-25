import flet as ft

# Importe a função main do arquivo home.py
from view.home import main  

# Executa o aplicativo Flet, passando a função main como alvo
if __name__ == "__main__":
    ft.app(target=main)