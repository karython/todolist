'''
/src/main.py
Este arquivo é o ponto de entrada do aplicativo Flet. Ele importa a função main do módulo home e executa o aplicativo.
'''

# Importando a biblioteca Flet e o módulo home.
import flet as ft
from view.home import main  # Importe a função main do arquivo home.pye

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")  # Executa o aplicativo Flet, passando a função main como alvo