import flet as ft  # Importa o módulo flet, que é usado para criar interfaces gráficas

# Definindo a classe Task, que herda de ft.Row (uma linha de controles na interface gráfica)
class Task(ft.Row):
    def __init__(self, task_name):
        super().__init__()  # Chama o construtor da classe pai (ft.Row)
        
        # Cria um checkbox (caixa de seleção) para representar a tarefa
        self.checkbox = ft.Checkbox(label=task_name, value=False)
        
        # Cria um campo de texto invisível inicialmente, usado para editar o nome da tarefa
        self.edit_name = ft.TextField(value=task_name, expand=True, visible=False)

        # Cria o botão de edição da tarefa, que será usado para ativar a edição
        self.edit_button = ft.IconButton(
            icon=ft.Icons.EDIT,  # Define o ícone do botão (ícone de edição)
            tooltip="Editar tarefa",  # Tooltip que aparece ao passar o mouse sobre o botão
            on_click=self.enable_edit  # Ação que ocorre quando o botão é clicado
        )
        
        # Cria o botão de salvar as alterações da tarefa, que será visível após ativar a edição
        self.save_button = ft.IconButton(
            icon=ft.Icons.SAVE,  # Define o ícone do botão (ícone de salvar)
            tooltip="Salvar",  # Tooltip que aparece ao passar o mouse sobre o botão
            icon_color=ft.Colors.GREEN,  # Cor do ícone de salvar (verde)
            visible=False,  # Inicialmente invisível
            on_click=self.save_edit  # Ação que ocorre quando o botão é clicado
        )

        # Define a lista de controles que serão exibidos na linha da tarefa
        self.controls = [
            self.checkbox,  # Checkbox da tarefa
            self.edit_name,  # Campo de texto para edição do nome da tarefa
            ft.Row(controls=[self.edit_button, self.save_button])  # Linha com os botões de edição e salvar
        ]

        # Define o alinhamento dos controles dentro da linha
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN  # Espaçamento entre os controles
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER  # Alinhamento vertical ao centro

    # Método para verificar se a tarefa está selecionada (checkbox marcado)
    def is_selected(self):
        return self.checkbox.value  # Retorna o valor do checkbox (True ou False)

    # Método para habilitar a edição do nome da tarefa
    def enable_edit(self, e):
        # Quando o botão de edição for clicado, copia o nome da tarefa para o campo de edição
        self.edit_name.value = self.checkbox.label  
        
        # Torna o checkbox invisível e o campo de edição visível
        self.checkbox.visible = False
        self.edit_name.visible = True
        
        # Torna o botão de editar invisível e o de salvar visível
        self.edit_button.visible = False
        self.save_button.visible = True
        
        # Atualiza a interface para refletir as mudanças
        self.update()

    # Método para salvar as alterações feitas na edição da tarefa
    def save_edit(self, e):
        # Salva o novo nome da tarefa (valor do campo de edição) no checkbox
        self.checkbox.label = self.edit_name.value
        
        # Torna o checkbox visível e o campo de edição invisível
        self.checkbox.visible = True
        self.edit_name.visible = False
        
        # Torna o botão de editar visível novamente e o de salvar invisível
        self.edit_button.visible = True
        self.save_button.visible = False
        
        # Atualiza a interface para refletir as mudanças
        self.update()
