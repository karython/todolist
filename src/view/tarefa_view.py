import flet as ft
from sqlalchemy.orm import sessionmaker
from connection import Session
from model.tarefa_model import Tarefa
import time

# Classe que representa uma tarefa na interface
class Task(ft.Row):
    def __init__(self, tarefa, tarefas_list):
        super().__init__()
        self.tarefa = tarefa
        self.tarefas_list = tarefas_list

        # Determina a cor com base no tema
        theme_color = '#FFF8E1' if Task.theme_mode == ft.ThemeMode.DARK else '#000000'

        # Controles de visualização (modo não edição)
        self.text_view = ft.Text(f"{tarefa.descricao}", font_family="MarioText", size=13, color=theme_color)
        self.text_situation = ft.Text("Sim" if tarefa.situacao else "Não", font_family="MarioText", size=13, color=theme_color)
        self.view_actions = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.EDIT_SHARP,
                    icon_color=theme_color,
                    tooltip="Editar",
                    on_click=lambda e, t=self: editar(e, t, tarefas_list)
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Excluir",
                    icon_color=theme_color,
                    on_click=lambda e, t=self: excluir(e, t, tarefas_list)
                )
            ],
            spacing=10
        )

        # Usando containers expansíveis para as colunas,
        # a ordem é: Descrição, Concluída e Ações
        self.col_desc_view = ft.Container(
            content=self.text_view,
            expand=1,
            alignment=ft.alignment.center_left
        )
        self.col_sit_view = ft.Container(
            content=self.text_situation,
            expand=1,
            alignment=ft.alignment.center
        )
        self.col_actions_view = ft.Container(
            content=self.view_actions,
            expand=1,
            alignment=ft.alignment.center
        )

        self.view_controls = [
            self.col_desc_view,
            self.col_sit_view,
            self.col_actions_view
        ]

        # Controles de edição
        self.descricao_input = ft.TextField(
            value=tarefa.descricao,
            label="Descrição",
            label_style=ft.TextStyle(size=13, color='#FFF8E1'),
            text_style=ft.TextStyle(color='#FFF8E1'),
            error_style=ft.TextStyle(size=8.5),
            border_color='#FFF8E1',
            expand=1
        )
        self.situacao_checkbox = ft.Checkbox(
            label="Concluída",
            active_color='#FFF8E1',
            label_style=ft.TextStyle(color='#FFF8E1'),
            value=tarefa.situacao
        )
        self.edit_actions = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Salvar",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TRANSPARENT,
                        color=ft.Colors.WHITE
                    ),
                    on_click=lambda ev: salvar_edicao(
                        ev, tarefa, self.descricao_input, self.situacao_checkbox, tarefas_list
                    )
                )
            ],
            spacing=10
        )

        self.col_desc_edit = ft.Container(
            content=self.descricao_input,
            expand=1,
            alignment=ft.alignment.center
        )
        self.col_sit_edit = ft.Container(
            content=self.situacao_checkbox,
            expand=1,
            alignment=ft.alignment.center
        )
        self.col_actions_edit = ft.Container(
            content=self.edit_actions,
            expand=1,
            alignment=ft.alignment.center
        )

        self.edit_controls = [
            self.col_desc_edit,
            self.col_sit_edit,
            self.col_actions_edit
        ]

# Função para fechar o modal de confirmação
def fechar_modal(e, page):
    page.dialog.open = False
    page.update()

# Função para atualizar a lista de tarefas na interface usando ResponsiveRow
def atualizar_lista_tarefas(tarefas_list):
    session = Session()
    try:
        # Limpa os controles existentes
        tarefas_list.controls.clear()
        # Para cada tarefa cadastrada, cria uma linha (simulando uma tabela)
        for tarefa in session.query(Tarefa).all():
            tar = Task(tarefa, tarefas_list)
            row = ft.Row(  # Alterado de ResponsiveRow para Row
                controls=tar.view_controls,
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            )
            tarefas_list.controls.append(row)
        tarefas_list.update()
    finally:
        session.close()

# Função para editar uma tarefa
def editar(e, tarefa, tarefas_list):
    session = Session()
    try:
        tarefa_db = session.query(Tarefa).filter_by(id=tarefa.tarefa.id).first()
        if tarefa_db:
            # Atualiza os controles de edição com os valores atuais
            tarefa_row = Task(tarefa_db, tarefas_list)
            tarefa_row.descricao_input.value = tarefa_db.descricao
            tarefa_row.situacao_checkbox.value = tarefa_db.situacao

            # Procura o índice do controle (Row) que contém a tarefa
            index = next(
                (i for i, row in enumerate(tarefas_list.controls)
                 if isinstance(row, ft.Row)
                 and hasattr(row.controls[0].content, "value")
                 and row.controls[0].content.value == tarefa.text_view.value),
                -1
            )
            if index != -1:
                # Substitui os controles da linha pela linha em modo de edição
                row = ft.Row(  # Alterado de ResponsiveRow para Row
                    controls=tarefa_row.edit_controls,
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START
                )
                tarefas_list.controls[index] = row
                tarefas_list.update()
                tarefa_row.descricao_input.focus()
        else:
            print("Tarefa não encontrada para edição.")
    except Exception as ex:
        print(f"Erro ao editar tarefa: {ex}")
    finally:
        session.close()

# Função para salvar a edição
def salvar_edicao(e, tarefa_db, descricao_input, situacao_checkbox, tarefas_list):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter_by(id=tarefa_db.id).first()
        if descricao_input.value.strip() == "":
            descricao_input.error_text = "Descrição não pode ser vazia!"
            descricao_input.update()
            time.sleep(1.5)
            descricao_input.error_text = ""
            descricao_input.update()
            descricao_input.focus()
            return
        if tarefa and descricao_input.value != '':
            tarefa.descricao = descricao_input.value
            tarefa.situacao = situacao_checkbox.value
            session.commit()
            atualizar_lista_tarefas(tarefas_list)
    except Exception as ex:
        print(f"Erro ao salvar edição da tarefa: {ex}")
    finally:
        session.close()
        e.page.update()

# Função para excluir uma tarefa
def excluir(e, tarefa, tarefas_list):
    def confirmar():
        session = Session()
        try:
            tarefa_db = session.query(Tarefa).filter_by(id=tarefa.tarefa.id).first()
            if tarefa_db:
                session.delete(tarefa_db)
                session.commit()
                atualizar_lista_tarefas(tarefas_list)
            else:
                print("Tarefa não encontrada para exclusão.")
        except Exception as ex:
            print(f"Erro ao excluir tarefa: {ex}")
        finally:
            session.close()
            e.page.update()
            fechar_modal(e, e.page)
    def cancelar():
        fechar_modal(e, e.page)

    # Cria um modal de confirmação
    modal = ft.AlertDialog(
        title=ft.Text("Confirmação"),
        content=ft.Text("Você tem certeza que deseja excluir esta tarefa?"),
        actions=[
            ft.ElevatedButton(
                text="Sim",
                on_click=lambda _: confirmar()
            ),
            ft.ElevatedButton(
                text="Não",
                on_click=lambda _: cancelar()
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    e.page.dialog = modal
    modal.open = True
    e.page.overlay.append(modal)
    e.page.update()
    # Atualiza a lista de tarefas
    atualizar_lista_tarefas(tarefas_list)
    e.page.update()

# Função para adicionar uma nova tarefa
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text):
    session = Session()
    try:
        if descricao_input.value.strip() == "":
            result_text.value = "Descrição da tarefa não pode ser vazia!"
            descricao_input.focus()
            e.page.update()
            time.sleep(1.5)
            result_text.value = ""
            e.page.update()
            return

        nova_tarefa = Tarefa(
            descricao=descricao_input.value,
            situacao=situacao_input.value
        )
        session.add(nova_tarefa)
        session.commit()

        descricao_input.value = ""
        situacao_input.value = False
        descricao_input.focus()
        result_text.value = "Tarefa cadastrada com sucesso!"
        e.page.update()
        time.sleep(1.5)
        result_text.value = ""
    except Exception as ex:
        result_text.value = f"Erro ao cadastrar tarefa: {ex}"
    finally:
        session.close()
        e.page.update()
