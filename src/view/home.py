import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas, on_excluir_tarefa_click
from connection import Session
from model.tarefa_model import Tarefa
from services.tarefa_service import editar_tarefa

class Task(ft.Row):
    def __init__(self, tarefa, tarefa_column, page):
        super().__init__()
        self.page = page  # Referência para a página
        self.tarefa = tarefa
        self.tarefa_column = tarefa_column

        # Campos para exibir a descrição e editar
        self.text_view = ft.Text(f"ID: {tarefa.id} - {tarefa.descricao} - {'Concluída' if tarefa.situacao else 'Pendente'}")
        self.text_edit = ft.TextField(value=tarefa.descricao, visible=False)

        # Botões de Editar e Salvar
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(icon=ft.icons.SAVE, visible=False, on_click=self.save)
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.delete)

        self.controls = [
            ft.Checkbox(value=tarefa.situacao), 
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
            self.delete_button
        ]

    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()

    def save(self, e):
        # Salva a edição da tarefa no banco de dados
        nova_descricao = self.text_edit.value
        nova_situacao = self.controls[0].value  # Valor do checkbox

        # Chama a função de editar tarefa no banco de dados
        resultado = editar_tarefa(self.tarefa.id, nova_descricao, nova_situacao)
        
        if resultado:  # Verifica se a edição foi bem-sucedida
            # Atualiza a descrição na interface
            self.text_view.value = nova_descricao
            self.text_view.visible = True
            self.text_edit.visible = False
            self.edit_button.visible = True
            self.save_button.visible = False

            # Garantir que a Task esteja adicionada antes de atualizar
            self.page.update()

            # Atualiza a lista de tarefas na tela
            atualizar_lista_tarefas(self.tarefa_column)
        else:
            print("Erro ao salvar a edição. A tarefa não foi atualizada.")

    def delete(self, e):
        # Exclui a tarefa do banco de dados
        on_excluir_tarefa_click(e, self.tarefa.id, self.tarefa_column)
        self.page.update()

# Função de edição ajustada:
def editar_tarefa(tarefa_id: int, nova_descricao: str, nova_situacao: bool):
    session = Session()
    try:
        # Busca a tarefa pelo ID
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        
        if tarefa:
            # Atualiza a descrição e a situação
            tarefa.descricao = nova_descricao
            tarefa.situacao = nova_situacao
            session.commit()  # Salva as alterações no banco
            return True
        else:
            print(f"Tarefa com ID {tarefa_id} não encontrada.")
            return False

    except Exception as e:
        session.rollback()
        print(f"Erro ao editar a tarefa: {e}")
        return False
    finally:
        session.close()

# Função principal da aplicação
def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)

    add_button = ft.ElevatedButton("Cadastrar Tarefa", on_click=lambda e: on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column))

    result_text = ft.Text()
    tarefas_column = ft.Column()

    def carregar_tarefas():
        session = Session()
        try:
            tarefas_column.controls.clear()
            todas_tarefas = session.query(Tarefa).all()

            for tarefa in todas_tarefas:
                # Adiciona a tarefa à lista com o componente `Task`
                tarefas_column.controls.append(Task(tarefa, tarefas_column, page))

            page.update()  # Atualiza a interface com as tarefas
        finally:
            session.close()

    def fechar_aplicativo(e):
        # Fecha o aplicativo
        page.window.close()  # Método correto para fechar a janela

    # Adicionando os componentes na interface
    page.add(
        descricao_input, situacao_input, add_button,
        result_text, tarefas_column
    )

    carregar_tarefas()

    # Adiciona um botão para fechar o aplicativo corretamente
    close_button = ft.ElevatedButton("Fechar", on_click=fechar_aplicativo)
    page.add(close_button)
