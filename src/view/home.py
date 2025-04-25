'''
/src/view/home.py

View Home para funcionamento do aplicativo To-Do List.
'''

# Importando as bibliotecas necessárias
import flet as ft
import view.listagem
import datetime
from enum import Enum

# Criando uma classe Enum para definir as cores usadas na interface.
# Uma classe Enum é uma maneira de definir um conjunto de constantes nomeadas.
class Cores(Enum):
    PRETO = "#000000"
    BRANCO = "#FFFFFF"
    VERMELHO_500 = "#F44336"
    AMARELO_500 = "#FFEB3B"
    VERDE_400 = "#66BB6A"
    TRANSPARENTE = "TRANSPARENT"

# --- "Setup" da página ---
def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"  # Título da página
    page.padding = 0  # Espaçamento interno do elemento
    page.bgcolor = ft.Colors.with_opacity(0.9, Cores.PRETO.value)
    page.theme_mode = ft.ThemeMode.DARK  # Tema da página
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",  # Link para a fonte Kanit, que vamos usar.
    }

    page.theme = ft.Theme(font_family="Kanit")  # Definindo a fonte padrão da página.

    # --- Snackbar ---
    '''
        Função para exibir mensagens coloridas de feedback ao usuário.
    '''
    def snackbar(message, color):
        sn = ft.SnackBar(content=ft.Text(message, color=color, weight="bold"))
        page.open(sn)

    # --- Imagem de fundo ---
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="../assets/menu.png",  # Diretório da imagem.
            fit=ft.ImageFit.COVER,  # Cobrir a página inteira.
        ),
    )

    # --- Barra de navegação ---
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home", selected_icon=ft.Icons.HOME),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_OUTLINED, label="Listagem", selected_icon=ft.Icons.LIST),
        ],
        selected_index=0,
        bgcolor=Cores.PRETO.value,  # Cor de fundo da barra de navegação.
        on_change=lambda e: on_nav_mudanca(page, e),  # Lambda para chamar a função de mudança de página.
    )

    # --- "Handler" da navegação ---
    def on_nav_mudanca(page, e):
        page.clean()  # Limpar página.
        if page.navigation_bar.selected_index == 0:
            main(page)  # Rodar a função main novamente, para voltar a página inicial.
            page.go("/")  # Ir para a página inicial (root).
        else:
            view.listagem.exibir_listagem(page)  # Rodar a função de listagem, para ir para a página de listagem.
            page.go("/listagem")  # Ir para a página de listagem..

    # --- Propriedades da Janela ---
    page.window.center()  # Centralizar a janela.
    page.window.width = 450  # Largura da janela.
    page.window.height = 800  # Altura da janela.
    page.window.full_screen = False  # Janela não em tela cheia.
    page.window.resizable = False  # Não redimensionável.
    page.window.icon = "../assets/icon.ico"  # Resgatar o ícone do aplicativo.
    page.on_error = lambda e: print("Page error:", e.data)  # Exibir erros no console, caso tenha um.

    # Localização do aplicativo para português brasileiro.
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("pt", "pt-BR"),
        ],
        current_locale=ft.Locale("pt", "pt-BR"),
    )

    # --- Controles do input ---
    # Campo de texto para o usuário digitar a descrição da tarefa.
    descricao_input = ft.TextField(
        label="Descrição da Tarefa",  # Texto que aparece como rótulo do campo.
        autofocus=True,  # Foco automático no campo ao abrir a página.
        width=280,  # Largura do campo de texto.
        label_style=ft.TextStyle(color=Cores.BRANCO.value),  # Estilo do texto do rótulo.
        multiline=False,  # Não permite múltiplas linhas no campo.
    )

    # Dicionário para armazenar a data selecionada.
    selecionada_data = {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  # Data e hora atuais como valor inicial.

    # Função para lidar com mudanças na data selecionada.
    def lidar_mudanca(e):
        selecionada_data["value"] = e.control.value.strftime('%Y-%m-%d %H:%M')  # Atualiza a data selecionada no dicionário.
        datebutton.text = f"Data: {selecionada_data['value']}"  # Atualiza o texto do botão com a nova data.
        datebutton.update()  # Atualiza o botão na interface.

    # Componente de seleção de data e hora no estilo Cupertino (iOS).
    cupertino_date_picker = ft.CupertinoDatePicker(
        first_date=datetime.datetime.now(),  # Data mínima permitida (hoje).
        last_date=datetime.datetime(2030, 10, 1, 23, 59),  # Data máxima permitida.
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,  # Permite selecionar data e hora.
        date_order=ft.CupertinoDatePickerDateOrder.DAY_MONTH_YEAR,  # Ordem dos campos de data (dia, mês, ano).
        on_change=lidar_mudanca,  # Chama a função lidar_mudanca ao alterar a data.
    )

    # Botão para abrir o seletor de data e hora.
    datebutton = ft.ElevatedButton(
        f"Data: {selecionada_data['value']}",  # Texto inicial do botão com a data atual.
        icon=ft.Icons.CALENDAR_MONTH,  # Ícone de calendário no botão.
        style=ft.ButtonStyle(text_style=ft.TextStyle(weight="bold")),  # Estilo do texto do botão.
        on_click=lambda e: page.open(  # Ao clicar, abre o seletor de data e hora.
            ft.CupertinoBottomSheet(  # Exibe o seletor em um "sheet" na parte inferior da tela.
                cupertino_date_picker,  # Componente de seleção de data e hora.
                height=216,  # Altura do "sheet".
                padding=ft.padding.only(top=6),  # Espaçamento no topo do "sheet".
            )
        ),
    )
    def quando_clicar_adicionar(e):
        add_button.disabled = True  # Desativa o botão
        add_button.update()

        try:
            descricao = descricao_input.value.strip()

            if not descricao:
                snackbar("A descrição não pode estar vazia.", Cores.VERMELHO_500.value)
                return

            if len(descricao) > 25:
                snackbar("A descrição é muito longa. Limite de 25 caracteres.", Cores.VERMELHO_500.value)
                return

            if not selecionada_data["value"]:
                snackbar("A data não pode estar vazia.", Cores.VERMELHO_500.value)
                return

            if view.listagem.verificar_descricao_existente(descricao):
                snackbar("Limite de três tarefas com a mesma descrição.", Cores.VERMELHO_500.value)
                return

            view.listagem.adicionar_tarefa(selecionada_data["value"], descricao)
            snackbar("Tarefa cadastrada com sucesso!", Cores.VERDE_400.value)

        finally:
            add_button.disabled = False  # Reativa o botão após finalizar a função
            add_button.update()

    # Botão para adicionar tarefa.
    # O botão chama a função on_add_click quando clicado.
    add_button = ft.ElevatedButton(
        "Cadastrar Tarefa",
        on_click=quando_clicar_adicionar,
    )

    # Botão de configurações.
    # O botão abre o dialog de configurações quando clicado.
    settings_button = ft.IconButton(
        icon="SETTINGS_OUTLINED",
        tooltip="Configurações",
        on_click=lambda e: page.open(config_dialog),
    )


    # --- Configurações do aplicativo ---
    # Função para alterar o tema do aplicativo, que pode ser claro (LIGHT) ou escuro (DARK).

    # Configuração do diálogo de configurações.
    config_dialog = ft.AlertDialog(
        title=ft.Text("Configurações", weight="bold"),  # Título do diálogo.
        adaptive=True,  # Ajusta o tamanho do diálogo automaticamente.
        actions=[
            ft.TextButton(
                "Fechar",  # Botão para fechar o diálogo.
                on_click=lambda e: page.close(config_dialog),
            ),
        ],
        modal=True,  # Define o diálogo como modal (não permite interação com outros elementos enquanto aberto).
        content=ft.Column(
            [
                ft.Divider(),  # Linha divisória.
                # Informações sobre o aplicativo.
                ft.Text("Versão do aplicativo: 1.0.3", size=14),
                ft.Text("Última atualização: 2025-25-04", size=14),
                ft.Text("Desenvolvedores: Thalita e Otávio", size=14),
            ], tight=True, spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # Adicionando os elementos à página principal.
    page.add(
    ft.Container(
        expand=True,  # Expande o container para ocupar todo o espaço disponível.
        padding=20,  # Espaçamento interno do container.
        content=ft.Column(
            controls=[
                # Linha com o botão de configurações e o título do aplicativo.
                ft.Row(controls=[settings_button, ft.Text("To-Do List", size=30, weight="bold", color="white")],),
                ft.Column(
                    controls=[
                        # Subtítulo e informações adicionais.
                        ft.Text("Gerenciador de Tarefas", size=20, weight="bold", color="white"),
                        ft.Text("Feito por: Thalita e Otávio", size=10, italic=True, color="white"),
                        ft.Divider(color="white", thickness=1),  # Linha divisória.
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                # Seção do formulário para cadastro de tarefas.
                ft.Container(
                    content=ft.Column(
                        controls=[
                            descricao_input,  # Campo de texto para descrição da tarefa.
                            datebutton,  # Botão para selecionar a data.
                            add_button,  # Botão para cadastrar a tarefa.
                        ],
                        spacing=10,  # Espaçamento entre os elementos.
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor = Cores.TRANSPARENTE,  # Fundo transparente.
                    padding=20,  # Espaçamento interno do container.
                    border_radius=10,  # Bordas arredondadas.
                    margin=ft.margin.only(top=20),  # Margem superior.
                ),
            ],
            spacing=30,  # Espaçamento entre as seções.
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
)