'''
/src/view/listagem.py

View Listagem para exibir as tarefas cadastradas.
'''

# Importando as bibliotecas necessárias.
import flet as ft
from model.tarefa_model import Tarefa
from datetime import datetime, timedelta
from services.tarefa_service import remover_tarefa, atualizar_tarefa, cadastrar_tarefa, query_tarefa
from enum import Enum

# Criando uma classe Enum para definir as cores usadas na interface.
# Uma classe Enum é uma maneira de definir um conjunto de constantes nomeadas.
class Cores(Enum):
    PRETO = "#000000"
    BRANCO = "#FFFFFF"
    VERMELHO_500 = "#F44336"
    AMARELO_500 = "#FFEB3B"
    TRANSPARENTE = "transparent"

# Função principal para exibir a tela de listagem de tarefas.
def exibir_listagem(page: ft.Page):
    # Configurações iniciais da página.
    page.clean()  # Limpa a página antes de adicionar novos elementos.
    page.title = "Listagem de Tarefas"  # Define o título da página.
    page.bgcolor = ft.Colors.with_opacity(0.9, Cores.PRETO.value)
    page.scroll = "auto"  # Permite rolagem automática.
    page.padding = 0  # Remove o preenchimento da página.
    page.theme_mode = ft.ThemeMode.DARK  # Define o tema como escuro.
    page.decoration = ft.BoxDecoration(  # Adiciona uma imagem de fundo.
        image=ft.DecorationImage(
            src="../assets/menu.png",  # Diretório da imagem de fundo.
            fit=ft.ImageFit.COVER,  # Faz a imagem cobrir a página inteira.
        ),
    )

    # Dicionário para armazenar as tarefas selecionadas.
    tarefas_selecionadas = {}

    def cor_prioridade(tarefa):
        try:
            # Verifica se a tarefa possui uma data e se ela é uma string
            if isinstance(tarefa.data, str):
                try:
                    tarefa_data = datetime.strptime(tarefa.data, '%Y-%m-%d %H:%M')
                except ValueError:
                    tarefa_data = datetime.now()
            else:
                tarefa_data = tarefa.data
            
            # Aqui você pode comparar a tarefa com a data de hoje ou definir uma lógica de cor
            if tarefa_data <= datetime.now():
                return Cores.VERMELHO_500.value  # Exemplo de cor para tarefas antigas ou urgentes
            else:
                return Cores.PRETO.value
        except Exception as e:
            # Caso ocorra algum outro erro, retorna uma cor padrão
            print(f"Erro ao processar a data da tarefa: {e}")
            return Cores.TRANSPARENTE.value

    # Função para atualizar a tela.
    def atualizar_tela():
        exibir_listagem(page)

    # Função para exibir uma mensagem na tela.
    def exibir_mensagem(mensagem):
        sn = ft.SnackBar(content=ft.Text(mensagem, weight="bold"), behavior="floating")
        page.open(sn)

    # Função para verificar a cor de fundo com base na data de expiração.
    def verificar_cor_expiracao(tarefa):
        if tarefa.data <= datetime.now():
            return Cores.VERMELHO_500.value
        elif tarefa.data <= datetime.now() + timedelta(days=1):
            return Cores.AMARELO_500.value
        return Cores.TRANSPARENTE.value

    # Função para alterar a cor do texto com base na data de expiração.
    def alterar_cor_texto_expiracao(tarefa):
        if tarefa.data <= datetime.now():
            return Cores.PRETO.value
        elif tarefa.data <= datetime.now() + timedelta(days=1):
            return Cores.PRETO.value
        return Cores.BRANCO.value

    # Função para abrir o modal de edição de uma tarefa.
    def abrir_modal_edicao(tarefa):
        descricao_campo = ft.TextField(label="Descrição", value=tarefa.descricao, border_color=Cores.BRANCO.value)
        descricao_campo.autofocus = True
        data_campo = ft.TextField(
            label="Data (YYYY-MM-DD HH:MM)",
            value=tarefa.data.strftime('%Y-%m-%d %H:%M'),
            border_color=Cores.BRANCO.value,
        )

        # Função para validar e salvar as alterações.
        def validar_e_salvar(e):
            descricao = descricao_campo.value.strip()
            data = data_campo.value.strip()

            # Caso a descrição esteja vazia, exibe mensagem de feedback.
            if len(descricao) > 25:
                exibir_mensagem("A descrição não pode ter mais de 25 caracteres.")
                return

            if verificar_descricao_existente(descricao):
                exibir_mensagem("Já existem três ou mais tarefas com essa descrição.")
                return

            try:
                datetime.strptime(data, '%Y-%m-%d %H:%M')
            except ValueError:
                exibir_mensagem("A data está em um formato inválido. Use o formato YYYY-MM-DD HH:MM.")
                return

            atualizar_tarefa(tarefa.id, descricao, data)
            atualizar_tela()
            page.close(dialogo)

        botao_salvar = ft.TextButton(
            "Salvar",
            icon="SAVE",
            on_click=validar_e_salvar,
        )

        dialogo = ft.AlertDialog(
            title=ft.Text("Editar Tarefa", color=Cores.BRANCO.value),
            content=ft.Column(
                [
                    ft.Divider(thickness=1, color=Cores.BRANCO.value),
                    descricao_campo,
                    data_campo,
                ],
                tight=True,
            ),
            adaptive=True,
            modal=True,
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            actions=[
                botao_salvar,
                ft.TextButton("Fechar", on_click=lambda e: page.close(dialogo)),
            ],
        )

        page.open(dialogo)

    # Função para remover uma tarefa.
    def remover_tarefa_por_id(tarefa_id):
        remover_tarefa(tarefa_id)
        atualizar_tela()

    # Função para atualizar a seleção de tarefas.
    def atualizar_selecao(tarefa_id, selecionada):
        tarefas_selecionadas[tarefa_id] = selecionada
        # Recalcular a visibilidade do botão
        botao_remover_selecionadas.visible = any(tarefas_selecionadas.values())
        page.update()  # Atualiza a interface

    # Função para remover as tarefas selecionadas.
    def remover_tarefas_selecionadas(e):
        # Desabilitar o botão para evitar múltiplos cliques
        botao_remover_selecionadas.disabled = True
        page.update()  # Atualiza a interface para refletir o estado desabilitado

        # Remover tarefas selecionadas
        tarefas_a_remover = [tarefa_id for tarefa_id, selecionada in tarefas_selecionadas.items() if selecionada]
        
        # Remover as tarefas do banco de dados ou do estado
        for tarefa_id in tarefas_a_remover:
            remover_tarefa(tarefa_id)
            del tarefas_selecionadas[tarefa_id]  # Remover do dicionário

        # Atualizar a tela
        atualizar_tela()

        # Reabilitar o botão após a operação
        botao_remover_selecionadas.disabled = False
        page.update()  # Atualiza a interface para refletir o estado habilitado novamente

    # Lista de painéis expansíveis para exibir as tarefas.
    lista_paineis_expansiveis = ft.ExpansionPanelList(
        elevation=4,
    )

    # Obtém as tarefas ordenadas por prioridade e data.
    tarefas = sorted(query_tarefa(), key=lambda t: (t.data, cor_prioridade(t)))

    # Itera sobre as tarefas para criar os painéis.
    for tarefa in tarefas:
        tarefas_selecionadas[tarefa.id] = False

        checkbox = ft.Checkbox(
            value=tarefas_selecionadas[tarefa.id],
            fill_color=Cores.BRANCO.value,
            on_change=lambda e, tid=tarefa.id: atualizar_selecao(tid, e.control.value),
            border_side=ft.BorderSide(width=2, color=Cores.PRETO.value),
        )

        lista_paineis_expansiveis.divider_color = alterar_cor_texto_expiracao(tarefa)
        lista_paineis_expansiveis.expanded_icon_color = alterar_cor_texto_expiracao(tarefa)

        painel = ft.ExpansionPanel(
            bgcolor=verificar_cor_expiracao(tarefa),
            header=ft.CupertinoContextMenu(
                enable_haptic_feedback=True,
                content=ft.ListTile(
                    leading=checkbox,
                    title=ft.Text(tarefa.descricao, weight="bold", style=ft.TextStyle(color=alterar_cor_texto_expiracao(tarefa))),
                    bgcolor=verificar_cor_expiracao(tarefa),
                ),
                actions=[
                    ft.CupertinoContextMenuAction(
                        text="Editar",
                        trailing_icon="EDIT",
                        on_click=lambda e, t=tarefa: abrir_modal_edicao(t),
                    ),
                    ft.CupertinoContextMenuAction(
                        text="Completar",
                        is_destructive_action=True,
                        trailing_icon="CHECK",
                        on_click=lambda e, tid=tarefa.id: remover_tarefa_por_id(tid),
                    ),
                ],
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon="ALARM",
                                icon_color=alterar_cor_texto_expiracao(tarefa),
                                disabled=True,
                            ),
                            ft.Text(f"Data: {tarefa.data.strftime('%Y-%m-%d %H:%M')}", weight="bold", height=20, color=alterar_cor_texto_expiracao(tarefa)),
                        ]
                    ),
                ]
            ),
        )

        lista_paineis_expansiveis.controls.append(painel)

    botao_remover_selecionadas = ft.ElevatedButton(
        text="Completar Selecionadas",
        icon="CHECK",
        style=ft.ButtonStyle(text_style=ft.TextStyle(weight="bold")),
        bgcolor=Cores.TRANSPARENTE.value,
        visible=True if len(tarefas_selecionadas) > 0 else False,
        on_click=lambda e: remover_tarefas_selecionadas(e),
        disabled=False  # Botão começa habilitado
    )

    # Adiciona os elementos à página.
    page.add(
        ft.Container(
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    botao_remover_selecionadas,
                    lista_paineis_expansiveis
                ]
            )
        )
    )

    # Função para verificar tarefas atrasadas ou próximas do vencimento e notificar o usuário.
    def verificar_tarefas_e_notificar():
        tarefas = query_tarefa()
        agora = datetime.now()

        tarefas_atrasadas = [tarefa for tarefa in tarefas if tarefa.data <= agora]
        tarefas_proximas = [tarefa for tarefa in tarefas if agora < tarefa.data <= agora + timedelta(days=1)]

        mensagens = []

        if tarefas_atrasadas:
            descricoes_atrasadas = ', '.join(tarefa.descricao for tarefa in tarefas_atrasadas)
            mensagens.append(f"Tarefas atrasadas: {descricoes_atrasadas}")

        if tarefas_proximas:
            descricoes_proximas = ', '.join(tarefa.descricao for tarefa in tarefas_proximas)
            horas_ate_vencimento = ', '.join(
                f"{int((tarefa.data - agora).total_seconds() // 3600)}h"
                for tarefa in tarefas_proximas
            )
            mensagens.append(f"Tarefas próximas do vencimento: {descricoes_proximas} (vencem em {horas_ate_vencimento})")

        if mensagens:
            exibir_mensagem('\n'.join(mensagens))

    verificar_tarefas_e_notificar()

# Função para adicionar uma nova tarefa.
def adicionar_tarefa(data, descricao):
    cadastrar_tarefa(data, descricao)

# Função para verificar se já existem três ou mais tarefas com a mesma descrição.
def verificar_descricao_existente(descricao):
    tarefas = query_tarefa()
    count = sum(1 for tarefa in tarefas if tarefa.descricao == descricao)
    return True if count >= 3 else False
