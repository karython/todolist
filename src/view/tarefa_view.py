from services.tarefa_service import cadastrar_tarefa, listar_tarefas, atualizar_tarefa, excluir_tarefa_por_id
import flet as ft
from datetime import datetime

# Função para atualizar a lista de tarefas
def atualizar_lista_tarefas(tarefas_column, result_text, page):
    tarefas_column.controls.clear()

    # Calcula o progresso das tarefas
    tarefas = listar_tarefas()
    total_tarefas = len(tarefas)
    tarefas_concluidas = sum(1 for tarefa in tarefas if tarefa.situacao)
    progresso = tarefas_concluidas / total_tarefas if total_tarefas > 0 else 0

    # Barra de progresso
    tarefas_column.controls.append(
        ft.Column(
            controls=[
                ft.Text(f"Progresso: {tarefas_concluidas}/{total_tarefas} tarefas concluídas", size=14),
                ft.ProgressBar(value=progresso, width=400, height=10, color="green"),
            ],
            spacing=10,
        )
    )

    # Cabeçalho da tabela
    tarefas_column.controls.append(
        ft.Row(
            controls=[
                ft.Text("", expand=0),
                ft.Text("Status e Descrição", weight="bold", expand=4, text_align=ft.TextAlign.LEFT, size=14),
                ft.Text("Concluída", weight="bold", expand=2, text_align=ft.TextAlign.CENTER, size=14, no_wrap=True),
                ft.Text("Data Adicionada", weight="bold", expand=3, text_align=ft.TextAlign.CENTER, size=14),
                ft.Text("Data Conclusão", weight="bold", expand=3, text_align=ft.TextAlign.CENTER, size=14),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
            height=50,
        )
    )

    # Linhas da tabela
    for tarefa in tarefas:
        if not tarefa.situacao and tarefa.data_conclusao and tarefa.data_conclusao >= datetime.now():
            cor_bolinha = "yellow"
        elif tarefa.situacao:
            cor_bolinha = "green"
        else:
            cor_bolinha = "red"

        tarefas_column.controls.append(
            ft.Dismissible(
                key=f"tarefa-{tarefa.id}",
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=10,
                            height=10,
                            bgcolor=cor_bolinha,
                            border_radius=5,
                            alignment=ft.alignment.center,
                            margin=ft.Margin(0, 0, 10, 0),
                        ),
                        ft.Text(tarefa.descricao, expand=4, text_align=ft.TextAlign.LEFT, size=12),
                        ft.Text("Sim" if tarefa.situacao else "Não", expand=2, text_align=ft.TextAlign.CENTER, size=12, no_wrap=True),
                        ft.Text(
                            tarefa.data_adicionada.strftime("%d/%m/%Y") if tarefa.data_adicionada else "N/A",
                            expand=3,
                            text_align=ft.TextAlign.CENTER,
                            size=12,
                        ),
                        ft.Text(
                            tarefa.data_conclusao.strftime("%d/%m/%Y") if tarefa.data_conclusao else "N/A",
                            expand=3,
                            text_align=ft.TextAlign.CENTER,
                            size=12,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=10,
                    height=50,
                ),
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                background=ft.Container(
                    content=ft.Text("Editar", color="white", weight="bold", size=12),
                    bgcolor="blue",
                    alignment=ft.alignment.center_left,
                    padding=ft.Padding(20, 0, 0, 0),
                ),
                secondary_background=ft.Container(
                    content=ft.Text("Excluir", color="white", weight="bold", size=12),
                    bgcolor="red",
                    alignment=ft.alignment.center_right,
                    padding=ft.Padding(0, 0, 20, 0),
                ),
                on_dismiss=lambda e, tarefa=tarefa: handle_confirm_dismiss(e, tarefa, tarefas_column, result_text, page),
            )
        )

    if tarefas_column.page:
        tarefas_column.update()

def handle_confirm_dismiss(e, tarefa, tarefas_column, result_text, page):
    if e.direction == ft.DismissDirection.START_TO_END:
        abrir_edicao_tarefa(page, tarefa, tarefas_column, result_text)
    elif e.direction == ft.DismissDirection.END_TO_START:
        if excluir_tarefa_por_id(tarefa.id):
            result_text.value = "Tarefa excluída com sucesso!"
        else:
            result_text.value = "Erro ao excluir a tarefa."
        result_text.update()
        atualizar_lista_tarefas(tarefas_column, result_text, page)

def abrir_edicao_tarefa(page, tarefa, tarefas_column, result_text):
    data_conclusao = tarefa.data_conclusao.strftime("%Y-%m-%d") if tarefa.data_conclusao else None

    def handle_date_change(ev):
        nonlocal data_conclusao
        data_conclusao = ev.control.value.strftime("%Y-%m-%d")
        result_text.value = f"Data selecionada: {data_conclusao}"
        if result_text.page:  # Verifica se result_text está associado à página
            result_text.update()

    descricao_input = ft.TextField(value=tarefa.descricao, label="Editar Descrição", expand=True)
    situacao_input = ft.Checkbox(value=tarefa.situacao, label="Concluída")
    date_picker_button = ft.ElevatedButton(
        "Selecionar Data de Conclusão",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda ev: page.open(
            ft.DatePicker(
                first_date=datetime(year=2023, month=10, day=1),
                last_date=datetime(year=2030, month=12, day=31),
                on_change=handle_date_change,
            )
        ),
    )
    salvar_button = ft.ElevatedButton(
        "Salvar",
        on_click=lambda ev: on_edit_tarefa_click(
            tarefa.id, descricao_input.value, situacao_input.value, data_conclusao, result_text, tarefas_column, page
        )
    )

    # Adiciona os controles de edição em duas linhas
    tarefas_column.controls.append(
        ft.Column(
            controls=[
                ft.Row([descricao_input, situacao_input], spacing=10),
                ft.Row([date_picker_button, salvar_button], spacing=10),
            ],
            spacing=10,
        )
    )
    tarefas_column.update()

def on_add_tarefa_click(e, descricao_input, data_conclusao, result_text, tarefas_column):
    descricao = descricao_input.value.strip()
    situacao = False
    data_adicionada = datetime.now()

    try:
        if isinstance(data_conclusao, str):
            data_conclusao = datetime.strptime(data_conclusao.strip(), "%Y-%m-%d")
        else:
            raise ValueError("Data de conclusão inválida.")
    except ValueError:
        result_text.value = "Data de conclusão inválida. Use o formato dd/mm/yyyy."
        result_text.color = "red"
        if result_text.page:  # Verifica se result_text está associado à página
            result_text.update()
        return

    if not descricao:
        result_text.value = "Por favor, escreva uma descrição para a tarefa."
        result_text.color = "red"
        if result_text.page:  # Verifica se result_text está associado à página
            result_text.update()
        return

    tarefa = cadastrar_tarefa(descricao, situacao, data_adicionada, data_conclusao)
    if tarefa:
        result_text.value = "Tarefa cadastrada com sucesso!"
        result_text.color = "green"
        descricao_input.value = ""
        descricao_input.update()
        atualizar_lista_tarefas(tarefas_column, result_text, None)
    else:
        result_text.value = "Erro ao cadastrar a tarefa."
        result_text.color = "red"

    if result_text.page:  # Verifica se result_text está associado à página
        result_text.update()

def on_edit_tarefa_click(tarefa_id, nova_descricao, nova_situacao, nova_data_conclusao, result_text, tarefas_column, page):
    try:
        nova_data_conclusao = datetime.strptime(nova_data_conclusao.strip(), "%Y-%m-%d")
    except ValueError:
        result_text.value = "Data de conclusão inválida. Use o formato dd/mm/yyyy."
        result_text.color = "red"
        if result_text.page:  # Verifica se result_text está associado à página
            result_text.update()
        return

    if atualizar_tarefa(tarefa_id, nova_descricao, nova_situacao, nova_data_conclusao):
        result_text.value = "Tarefa atualizada com sucesso!"
        result_text.color = "green"
    else:
        result_text.value = "Erro ao atualizar a tarefa."
        result_text.color = "red"

    if result_text.page:  # Verifica se result_text está associado à página
        result_text.update()
    atualizar_lista_tarefas(tarefas_column, result_text, page)
