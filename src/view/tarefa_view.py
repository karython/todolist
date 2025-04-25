import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefas, listar_tarefas, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa  # Certifique-se de que o modelo se chama Tarefa
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text  # Importa text para consultas SQL textuais

# Widget customizado para representar uma tarefa
class Task(ft.Row):
    def __init__(self, task: Tarefa):
        super().__init__()
        self.task = task
        self.checkbox = ft.Row(
            controls=[
                ft.Checkbox(value=task.situacao, on_change=self.on_checkbox_change, fill_color=ft.Colors.GREEN_100),
            ]
        )
        # Text para exibir a descrição com limite de 30 caracteres
        descricao_limitada = task.descricao if len(task.descricao) <= 30 else task.descricao[:30] + "..."
        # Adiciona o traço no texto se a tarefa estiver concluída
        self.text_view = ft.Text(
            descricao_limitada,
            color=ft.Colors.AMBER_500,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH if task.situacao else ft.TextDecoration.NONE
            )  # Define o traço com base no status
        )
        # TextField para edição (inicialmente invisível)
        self.text_edit = ft.TextField(
            value=task.descricao,
            visible=False,
            color=ft.Colors.DEEP_ORANGE_900,
            width=150,  
            read_only=False  
        )
        # Botão para iniciar a edição
        self.edit_button = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=self.edit,
            icon_color=ft.Colors.AMBER_900
        )
        # Botão para salvar a edição (inicialmente invisível)
        self.save_button = ft.IconButton(icon=ft.Icons.SAVE, visible=False, on_click=self.save, icon_color=ft.Colors.GREEN_ACCENT_700)
        # Botão para excluir a tarefa
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            on_click=self.delete,
            icon_color=ft.Colors.RED_ACCENT_700
        )
        # Ajuste o espaçamento entre os botões usando um ft.Row
        self.button_row = ft.Row(
            controls=[self.edit_button, self.delete_button],
            spacing=5   
        )
        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.button_row,  # Substitui os botões individuais pelo ft.Row
            self.save_button,
        ]
    
    def edit(self, e):
        # Ativa o modo edição
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()
    
    def save(self, e):
        # Atualiza a tarefa no banco e na interface
        new_text = self.text_edit.value
        checkbox_value = self.checkbox.controls[0].value  
        result = editar_tarefa(self.task.id, new_text, checkbox_value)
        if "editada com sucesso" in result:
            self.task.descricao = new_text
            self.text_view.value = new_text
            # Atualiza o traço no texto com base no status
            self.text_view.style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH if checkbox_value else ft.TextDecoration.NONE,
                decoration_thickness=2.0 
            )
        self.edit_button.visible = True
        self.save_button.visible = False
        self.text_view.visible = True
        self.text_edit.visible = False
        self.update()
    
    def delete(self, e):
        # Exclui a tarefa do banco e remove o widget da interface
        excluir_tarefas(self.task.id)
        self.controls.clear()  
        self.visible = False  
        self.update()  
    
    def on_checkbox_change(self, e):
        # Atualiza o status da tarefa (checkbox)
        checkbox_value = self.checkbox.controls[0].value  
        result = editar_tarefa(self.task.id, self.task.descricao, checkbox_value)
        self.task.situacao = checkbox_value

        # Atualiza o traço no texto com base no status 
        self.text_view.style = ft.TextStyle(
            decoration=ft.TextDecoration.LINE_THROUGH if checkbox_value else ft.TextDecoration.NONE,
            decoration_thickness=2.0  
        )
        self.update()

    background_image = ft.Image(
        src="src/assets/images/system.jpg",
        fit=ft.ImageFit.COVER,
        expand=True,)
    

# Função para verificar o estado das tarefas e exibir mensagens
def verificar_estado_tarefas(tasks_column, result_text_container):
    if not tasks_column.controls:
        result_text_container.value = "VOCÊ NÃO TEM TAREFAS. ADICIONE PARA QUE A FORÇA ESTEJA COM VOCÊ."
        result_text_container.font_family = "Heveltica"  # Define a fonte
        result_text_container.color = ft.Colors.DEEP_ORANGE_ACCENT_700
        result_text_container.visible = True
    elif all(isinstance(control, Task) and control.task.situacao for control in tasks_column.controls):
        result_text_container.value = "PARABÉNS VOCÊ CONCLUIU TODAS AS SUAS TAREFAS!"
        result_text_container.font_family = "Heveltica" 
        result_text_container.color = ft.Colors.GREEN_900
        result_text_container.visible = True
    else:
        result_text_container.value = ""  
        result_text_container.visible = False 
    result_text_container.update()

# Função para gerenciar a sessão do banco de dados
def get_session():
    try:
        session = Session()
        # Testa a conexão executando uma consulta simples
        session.execute(text("SELECT 1"))  
        return session
    except OperationalError:
        # Fecha a sessão e cria uma nova em caso de erro
        session.close()
        return Session()

# Função para atualizar a lista de tarefas na interface
def atualizar_lista_tarefas(tasks_column, result_text=None):
    session = get_session()  
    try:
        tasks_column.controls.clear()
        todas_tarefas = session.query(Tarefa).all()
        for task in todas_tarefas:
            tasks_column.controls.append(Task(task))
        tasks_column.update()
        if result_text:
            verificar_estado_tarefas(tasks_column, result_text) 
    finally:
        session.close()


# Função acionada ao clicar no botão de adicionar tarefa
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tasks_column):
    descricao = descricao_input.value.strip()  
    situacao = situacao_input.value 

    if not descricao:  # Verifica se a descrição está vazia
        result_text.value = "Erro: A descrição da tarefa não pode estar vazia."
        result_text.color = ft.Colors.RED
        result_text.update()
        return

    session = get_session() 
    try:
        tarefa_id = cadastrar_tarefa(descricao, situacao)
        if tarefa_id:
            result_text.value = f"Tarefa cadastrada com sucesso!"
            result_text.color = ft.Colors.AMBER_500
            atualizar_lista_tarefas(tasks_column, result_text)  
        else:
            result_text.value = "Erro ao cadastrar a tarefa"
            result_text.color = ft.Colors.AMBER_500
    except OperationalError as e:
        result_text.value = f"Erro ao cadastrar tarefa: {str(e)}"
        result_text.color = ft.Colors.RED
    finally:
        session.close()
    result_text.update()


def main(page: ft.Page):
    page.title = "Task Manager"
    
    # Coluna para exibir as tarefas
    tasks_column = ft.Column()
    
    # Componentes para cadastro de nova tarefa
    new_task_desc = ft.TextField(
        label="Descrição da Tarefa",
        color=ft.Colors.DEEP_ORANGE_900,
        expand=True  
    )
    new_task_status = ft.Checkbox(
        label="Tarefa concluída",
        value=False,
        fill_color=ft.Colors.GREEN_100,
        label_style=ft.TextStyle(color=ft.Colors.AMBER_500)
    )
    result_text = ft.Text(color=ft.Colors.ORANGE)
    
    add_button = ft.ElevatedButton(
        text="Adicionar Tarefa",
        on_click=lambda e: on_add_tarefa_click(e, new_task_desc, new_task_status, result_text, tasks_column),
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )
    
    refresh_button = ft.ElevatedButton(
        text="Atualizar Lista",
        on_click=lambda e: atualizar_lista_tarefas(tasks_column, result_text)
    )
    
    # Monta a interface
    page.add(
        ft.Column(
            [
                new_task_desc,
                ft.Row(
                    [new_task_status, add_button],
                    alignment=ft.MainAxisAlignment.START 
                ),
                result_text,
                refresh_button,
                ft.Divider(),
                tasks_column
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True
        )
    )
    
    # Carrega as tarefas existentes
    atualizar_lista_tarefas(tasks_column, result_text)

