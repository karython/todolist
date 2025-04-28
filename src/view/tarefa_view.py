# Importando as funções necessárias e bibliotecas externas
from services.tarefa_service import cadastrar_tarefa, excluir_tarefa, editar_tarefa, listar_tarefas
import flet as ft
from view.task import Task


# Função para atualizar a lista de tarefas na interface
def atualizar_lista_tarefas(tarefas_column):
    try:
        tarefas_column.controls.clear()
        todas_tarefas = listar_tarefas()  # Obtém as tarefas do serviço
        for tarefa in todas_tarefas:
            tarefas_column.controls.append(
                Task(
                    tarefa=tarefa,
                    tarefa_column=tarefas_column,
                    atualizar_lista_tarefas=atualizar_lista_tarefas,
                )
            )
        tarefas_column.update()
    except Exception as ex:
        print(f"Erro ao atualizar a lista de tarefas: {ex}")


# Função chamada ao clicar no botão de adicionar tarefa
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column, data_entrega):
    descricao = descricao_input.value.strip()
    situacao = situacao_input.value  # Acessando o valor do Checkbox aqui (True ou False)

    if not descricao:
        result_text.value = "A descrição da tarefa não pode estar vazia."
        result_text.color = ft.colors.RED
        e.page.update()
        return

    tarefa_cadastrada = cadastrar_tarefa(descricao, situacao, data_entrega)
    if tarefa_cadastrada:
        result_text.value = "Tarefa cadastrada com sucesso!"
        result_text.color = ft.colors.GREEN
        atualizar_lista_tarefas(tarefas_column)
        descricao_input.value = ""
        situacao_input.value = False  # Reseta o valor do Checkbox
    else:
        result_text.value = "Erro ao cadastrar a tarefa."
        result_text.color = ft.colors.RED

    e.page.update()





# Função chamada ao clicar no botão de excluir tarefa
def on_excluir_tarefa_click(e, tarefa_id, tarefas_column, result_text):
    try:
        if excluir_tarefa(tarefa_id):
            result_text.value = "Tarefa excluída com sucesso!"
            result_text.color = ft.colors.GREEN
            atualizar_lista_tarefas(tarefas_column)
        else:
            result_text.value = "Erro: Tarefa não encontrada."
            result_text.color = ft.colors.RED
    except Exception as ex:
        result_text.value = f"Erro ao excluir a tarefa: {ex}"
        result_text.color = ft.colors.RED
    e.page.update()


# Função para exibir um modal de edição de tarefa
def modal_editar(page, tarefa, tarefas_column, result_text):
    descricao_input = ft.TextField(label="Nova Descrição", value=tarefa["descricao"])
    situacao_input = ft.Checkbox(label="Concluída", value=tarefa["situacao"])

    def salvar_edicao(e):
        try:
            if editar_tarefa(tarefa["id"], descricao_input.value.strip(), situacao_input.value):
                result_text.value = "Tarefa editada com sucesso!"
                result_text.color = ft.colors.GREEN
                atualizar_lista_tarefas(tarefas_column)
            else:
                result_text.value = "Erro: Tarefa não encontrada."
                result_text.color = ft.colors.RED
        except Exception as ex:
            result_text.value = f"Erro ao editar a tarefa: {ex}"
            result_text.color = ft.colors.RED
        finally:
            page.dialog.open = False
            page.update()

    modal = ft.AlertDialog(
        title=ft.Text("Editar Tarefa"),
        content=ft.Column([descricao_input, situacao_input]),
        actions=[
            ft.TextButton("Salvar", on_click=salvar_edicao),
            ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(page)),
        ],
    )

    page.dialog = modal
    modal.open = True
    page.update()


# Função para fechar o modal
def fechar_modal(page):
    page.dialog.open = False
    page.update()