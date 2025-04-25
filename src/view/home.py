import flet as ft  # Importa a biblioteca Flet, usada para criar a interface gráfica.
from view.Page import TodoApp  # Importa a classe TodoApp do arquivo view.py, que define a estrutura da aplicação de lista de tarefas.

def main(page: ft.Page):  # Define a função principal que é chamada para configurar e iniciar a aplicação.
    # Configura o título da página
    page.title = "To-Do App"  # Define o título da aba do navegador.

    # Configura o modo de tema da página
    page.theme_mode = ft.ThemeMode.LIGHT  # Define o tema como claro. Você pode mudar para ft.ThemeMode.DARK para o modo escuro.

    # Configura o alinhamento horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centraliza o conteúdo horizontalmente na página.

    # Configura o comportamento de rolagem da página
    page.scroll = "adaptive"  # Define o comportamento da rolagem. "adaptive" faz a rolagem ser ativada conforme necessário (ou seja, se o conteúdo exceder o tamanho da tela).

    # Define o preenchimento (padding) da página, ou seja, a distância entre o conteúdo e as bordas da tela
    page.padding = 20  # Aplica 20 pixels de espaço nas bordas da página.

    # Atualiza a página após todas as configurações
    page.update()  # Atualiza a página para aplicar as configurações feitas acima.

    # Cria a instância da aplicação TodoApp e adiciona à página
    app = TodoApp(page)  # Cria um objeto da classe TodoApp, que representa a aplicação de lista de tarefas.
    page.add(app)  # Adiciona a instância da aplicação (app) à página para ser exibida.