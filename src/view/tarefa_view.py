from services.tarefa_service import cadastrar_tarefa, excluir_tarefa
import flet as ft
from connection import Session
from model.tarefa_model import Tarefa


def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tabela_tarefas, atualizar_tabela_tarefas):
    descricao = descricao_input.value.strip()  # Remove espaços em branco no início e no fim
    situacao = situacao_input.value

    # Validação: Verifica se a descrição está vazia
    if not descricao:
        result_text.value = "A descrição da tarefa não pode estar vazia."
        result_text.color = ft.colors.RED
        result_text.update()
        return

    tarefa_id = cadastrar_tarefa(descricao, situacao)

    if tarefa_id:
        descricao_input.value = ""
        descricao_input.update()

        situacao_input.value = False
        situacao_input.update()

        result_text.value = f"Tarefa cadastrada com sucesso!"
        result_text.color = ft.colors.GREEN
        result_text.update()

        atualizar_tabela_tarefas(tabela_tarefas)
    else:
        result_text.value = "Erro ao cadastrar a tarefa."
        result_text.color = ft.colors.RED
        result_text.update()


def on_excluir_tarefa_click(e, id_tarefa, result_text, tabela_tarefas, atualizar_tabela):
    def confirmar_exclusao(e):
        tarefa_excluida = excluir_tarefa(id_tarefa)

        if tarefa_excluida:
            result_text.value = f"Tarefa excluída com sucesso!"
            result_text.color = ft.colors.GREEN
            atualizar_tabela()
        else:
            result_text.value = f"Erro ao excluir tarefa."
            result_text.color = ft.colors.RED

        # Adiciona o result_text à página antes de chamar update()
        e.page.add(result_text)  # Garante que o result_text está na página
        result_text.update()  # Agora podemos atualizar o result_text sem erro
        e.page.close(cupertino_alert_dialog)  # Fecha o popup após a confirmação
        e.page.update()

    def cancelar_exclusao(e):
        e.page.close(cupertino_alert_dialog)  # Fecha o popup ao cancelar
        e.page.update()

    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza de que deseja excluir esta tarefa?"),
        actions=[
            ft.CupertinoDialogAction(
                text="Sim",
                is_destructive_action=True,
                on_click=confirmar_exclusao,
            ),
            ft.CupertinoDialogAction(
                text="Não",
                is_default_action=True,
                on_click=cancelar_exclusao,
            ),
        ],
    )

    e.page.open(cupertino_alert_dialog)


def on_editar_tarefa_click(e, id_tarefa, descricao_input, situacao_input, page, atualizar_tabela, listar_layout):
    # Obtém os valores atuais da tarefa
    session = Session()
    tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
    session.close()

    if not tarefa:
        page.snack_bar = ft.SnackBar(ft.Text("Erro: Tarefa não encontrada."), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()
        return

    # Cria os campos de edição
    descricao_editar = ft.TextField(label="Editar Descrição", value=tarefa.descricao, width=300)
    situacao_editar = ft.Checkbox(label="Concluída", value=tarefa.situacao)

    # Função para salvar as alterações
    def salvar_edicao(e):
        nova_descricao = descricao_editar.value
        nova_situacao = situacao_editar.value

        # Atualiza a tarefa no banco de dados
        session = Session()
        try:
            tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
            if tarefa:
                tarefa.descricao = nova_descricao
                tarefa.situacao = nova_situacao
                session.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Tarefa editada com sucesso!"), bgcolor=ft.colors.GREEN)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro: Tarefa não encontrada."), bgcolor=ft.colors.RED)
        except Exception as ex:
            session.rollback()
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao editar tarefa: {ex}"), bgcolor=ft.colors.RED)
        finally:
            session.close()
            fechar_pagina_edicao()

        atualizar_tabela()
        page.snack_bar.open = True
        fechar_pagina_edicao()

    # Função para cancelar a edição
    def cancelar_edicao(e):
        fechar_pagina_edicao()

    # Função para redirecionar para a tela de listagem
    def fechar_pagina_edicao():
        page.controls.clear()
        page.add(listar_layout)
        page.update()

    # Cria o layout da página de edição
    editar_layout = ft.Column(
        [
            ft.Text("Editar Tarefa", size=28, weight=ft.FontWeight.BOLD),
            descricao_editar,
            situacao_editar,
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.SAVE,
                        tooltip="Salvar Alterações",
                        icon_color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREEN,
                        on_click=salvar_edicao,
                    ),
                    ft.TextButton(
                        "Cancelar",
                        on_click=cancelar_edicao,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Redireciona para a página de edição
    page.controls.clear()
    page.add(editar_layout)
    page.update()
