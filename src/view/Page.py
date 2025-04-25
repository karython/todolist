import flet as ft  # Importa a biblioteca Flet, usada para criar a interface gráfica
from services.services import adicionar_tarefa, excluir_tarefas_selecionadas  # Importa as funções de serviços para adicionar e excluir tarefas


class TodoApp(ft.Column):  # Classe que representa o aplicativo de tarefas, herdando de ft.Column (uma coluna, ou seja, itens dispostos verticalmente)
    def __init__(self, page: ft.Page):  # Construtor da classe, recebe uma instância da página
        super().__init__()  # Chama o construtor da classe pai (ft.Column), que organiza os controles verticalmente
        self.page = page  # Atribui a página à variável de instância para uso posterior

        # Cria um campo de texto para inserir novas tarefas
        self.new_task = ft.TextField(
            hint_text="O que precisa ser feito?",  # Texto de dica que aparece quando o campo está vazio
            expand=True,  # Expande o campo para ocupar todo o espaço disponível
        )

        # Cria um botão flutuante de adicionar tarefa
        self.add_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,  # Define o ícone do botão como um sinal de "+" (adicionar)
            on_click=self.add_clicked  # Define a função a ser chamada quando o botão for clicado
        )

        # Cria um botão de excluir tarefas selecionadas
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,  # Define o ícone como um ícone de excluir
            tooltip="Excluir tarefas selecionadas",  # Exibe uma dica quando o usuário passa o mouse sobre o botão
            on_click=self.delete_selected_tasks,  # Função chamada ao clicar no botão
        )

        # Cria um botão para alternar entre os modos claro e escuro do tema
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,  # Define o ícone do botão como um ícone de tema escuro
            tooltip="Alternar tema",  # Exibe uma dica ao passar o mouse sobre o botão
            on_click=self.toggle_theme,  # Função chamada ao clicar no botão
        )

        # Cria a lista de tarefas (usada para exibir as tarefas)
        self.tasks_list = ft.ListView(
            expand=True,  # Expande a lista para ocupar todo o espaço disponível
            spacing=10,  # Define o espaçamento entre os itens da lista
            padding=10,  # Define o preenchimento da lista
            auto_scroll=False,  # Desativa o rolar automático (pode ser ativado conforme necessidade)
        )

        # Organiza os controles da página (campo de texto, botões e a lista de tarefas) em uma estrutura de controles
        self.controls = [
            ft.Row([self.new_task], alignment=ft.MainAxisAlignment.CENTER),  # Organiza o campo de texto para inserir tarefas centralizado
            ft.ResponsiveRow(
                controls=[self.add_button, self.delete_button, self.theme_button],  # Organiza os botões em uma linha responsiva
                alignment=ft.MainAxisAlignment.START,  # Alinha os botões à esquerda
                run_spacing=10,  # Espaçamento entre os botões
                spacing=10,  # Espaçamento interno dos controles
            ),
            ft.Container(content=self.tasks_list, expand=True),  # Exibe a lista de tarefas em um container
        ]

        self.expand = True  # Define a propriedade de expandir a coluna para preencher o espaço disponível

    def add_clicked(self, e):  # Função chamada quando o botão de adicionar tarefa é clicado
        adicionar_tarefa(self.tasks_list, self.new_task.value, self.update)  # Adiciona a nova tarefa à lista
        self.new_task.value = ""  # Limpa o campo de entrada de tarefa após adicionar
        self.update()  # Atualiza a página para refletir as mudanças

    def delete_selected_tasks(self, e):  # Função chamada quando o botão de excluir tarefas selecionadas é clicado
        excluir_tarefas_selecionadas(self.tasks_list, self.update)  # Exclui as tarefas marcadas na lista

    def toggle_theme(self, e):  # Função chamada quando o botão de alternar tema é clicado
        if self.page.theme_mode == ft.ThemeMode.LIGHT:  # Se o tema atual for claro
            self.page.theme_mode = ft.ThemeMode.DARK  # Altera para o tema escuro
            self.theme_button.icon = ft.Icons.LIGHT_MODE  # Muda o ícone do botão para "modo claro"
        else:  # Caso contrário, se o tema for escuro
            self.page.theme_mode = ft.ThemeMode.LIGHT  # Altera para o tema claro
            self.theme_button.icon = ft.Icons.DARK_MODE  # Muda o ícone do botão para "modo escuro"
        self.page.update()  # Atualiza a página para aplicar a mudança de tema
