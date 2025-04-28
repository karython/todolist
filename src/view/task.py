import flet as ft
from services.tarefa_service import editar_tarefa, excluir_tarefa

class Task(ft.Container):
    def __init__(self, tarefa, tarefa_column, page, atualizar_lista_tarefas, excluir_tarefa=None):
        super().__init__()
        self.page = page
        self.tarefa = tarefa
        self.tarefa_column = tarefa_column
        self.atualizar_lista_tarefas = atualizar_lista_tarefas
        self.excluir_tarefa = excluir_tarefa  # Adiciona o argumento excluir_tarefa

        # Componentes da interface
        self.checkbox = ft.Checkbox(value=tarefa.situacao, on_change=self.toggle_status)
        self.text_view = ft.Text(f"{tarefa.descricao} - {'Concluída' if tarefa.situacao else 'Pendente'}")
        self.text_edit = ft.TextField(value=tarefa.descricao, visible=False)

        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(icon=ft.icons.SAVE, visible=False, on_click=self.save)
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.delete)

        # Layout da tarefa
        self.content = ft.Row(
            [
                self.checkbox,  # Checkbox
                self.text_view,  # Texto da tarefa
                self.text_edit,  # Campo de edição (invisível por padrão)
                self.edit_button,  # Botão de editar
                self.save_button,  # Botão de salvar (invisível por padrão)
                self.delete_button,  # Botão de excluir
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos verticalmente
        )

    def edit(self, e):
        # Muda a visibilidade dos componentes para permitir a edição
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.page.update()

    def save(self, e):
        """Salva as alterações feitas na tarefa."""
        nova_descricao = self.text_edit.value.strip()  # Remove espaços em branco
        nova_situacao = self.checkbox.value

        # Validação da descrição
        if not nova_descricao:
            self.page.snack_bar = ft.SnackBar(ft.Text("A descrição não pode estar vazia."), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Chama a função de edição no serviço
        resultado = editar_tarefa(self.tarefa.id, nova_descricao, nova_situacao)
        if resultado:
            # Atualiza os valores na tarefa
            self.tarefa.descricao = nova_descricao
            self.tarefa.situacao = nova_situacao

            # Atualiza os componentes da interface
            self.text_view.value = f"{nova_descricao} - {'Concluída' if nova_situacao else 'Pendente'}"
            self.text_view.visible = True
            self.text_edit.visible = False
            self.edit_button.visible = True
            self.save_button.visible = False
            self.page.update()
        else:
            # Exibe uma mensagem de erro caso a edição falhe
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar a edição."), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()

    def delete(self, e):
        if self.excluir_tarefa:
            self.excluir_tarefa(self.tarefa)  # Chama a função de exclusão com confirmação
        else:
            resultado = excluir_tarefa(self.tarefa.id)
            if "sucesso" in resultado.lower():
                self.tarefa_column.controls.remove(self)
                self.page.update()
            else:
                print(resultado)

    def toggle_status(self, e):
        """Alterna o status de conclusão da tarefa."""
        nova_situacao = e.control.value
        resultado = editar_tarefa(self.tarefa.id, self.tarefa.descricao, nova_situacao)
        if resultado:
            self.tarefa.situacao = nova_situacao
            self.text_view.value = f"{self.tarefa.descricao} - {'Concluída' if nova_situacao else 'Pendente'}"
            self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar o status."), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()