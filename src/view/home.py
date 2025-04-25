from PIL import Image
import io
import base64
import datetime
import flet as ft
from view.tarefa_view import TarefaView
from services.tarefa_service import cadastrar_tarefa

def encode_image_to_base64(path):
    img = Image.open(path)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

class Home:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.image_src = encode_image_to_base64("src/assets/img/fundo.png")  # Codifica a imagem em base64
        self.page.image_fit = ft.ImageFit.COVER  # Ajusta a imagem para cobrir toda a janela
    
    def construir(self):
        self.page.clean()
        self.page.padding = 0  # Remove qualquer padding da página
        self.page.spacing = 0  # Remove espaçamento entre os elementos

        # Primeira imagem de fundo
        background_image = ft.Container(
            content=ft.Image(
                src=self.page.image_src,  # Usa a imagem codificada em base64
                fit=ft.ImageFit.COVER
            ),
            expand=True,  # Faz o container expandir para ocupar toda a janela
            width=self.page.width,  # Ajusta a largura para o tamanho da janela
            height=self.page.height * 2,  # Aumenta ainda mais a altura da imagem de fundo
        )

        # Campo de entrada para a descrição da tarefa
        result_text = ft.Text(color="white", weight="bold")
        error_text = ft.Text(value="", color="white", weight="bold")

        def limpar_mensagens(e):
            # Certifique-se de que os controles foram adicionados antes de atualizá-los
            if result_text not in self.page.controls:
                self.page.add(result_text)
            if error_text not in self.page.controls:
                self.page.add(error_text)
            descricao_input.value = "" 
            result_text.value = ""
            error_text.value = ""
            result_text.update()
            error_text.update()
            descricao_input.update()

        descricao_input = ft.TextField(
            label="Descrição da Tarefa",
            autofocus=True,
            width=300,
            on_focus=limpar_mensagens,  # Limpa as mensagens ao clicar no campo
            color="white",  # Texto branco
            bgcolor="black",  # Fundo preto
            border_color="white",  # Borda branca
            focused_border_color="white",  # Mantém a borda branca ao focar
            cursor_color="white",  # Define a cor do cursor como branco
            label_style=ft.TextStyle(color="white")  # Define a cor do texto do rótulo como branco
        )

        # Função para lidar com a mudança de data
        def handle_date_change(e):
            selected_date.value = f"Data selecionada: {e.control.value.strftime('%d/%m/%Y')}"
            selected_date.visible = True  # Torna o texto visível após a seleção
            selected_date.update()

        # Função para lidar com o fechamento do seletor de data
        def handle_date_dismissal(e):
            selected_date.visible = False  # Oculta o texto se nenhuma data for selecionada
            selected_date.update()

        # Botão para abrir o seletor de data
        date_picker_button = ft.ElevatedButton(
            "Selecionar Data",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime.now(),  # Começa no dia vigente
                    last_date=datetime.datetime(year=2026, month=12, day=31),  # Limite no final de 2026
                    on_change=handle_date_change,
                    on_dismiss=handle_date_dismissal
                )
            ),
        )

        # Texto para exibir a data selecionada (inicialmente invisível)
        selected_date = ft.Text(value="", color="white", visible=False)

        # Instância de TarefaView
        tarefa_view = TarefaView(self.page)
        
        # Botão para adicionar a tarefa
        add_button = ft.Container(
            width=150,  # Aumenta a largura do botão
            height=50,  # Define altura menor para tornar o botão retangular
            alignment=ft.alignment.center,
            bgcolor="#6E6E6E",  # Define a cor de fundo do botão
            border=ft.border.all(1, "#5C5C5C"),  # Define a cor da borda
            border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
            shadow=ft.BoxShadow(blur_radius=3, color="black", spread_radius=1),  # Adiciona sombra ao botão
            content=ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Text("Cadastrar", color="white", size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                ),
                on_click=lambda e: self._on_cadastrar_click(e, descricao_input, selected_date, result_text, error_text),
                bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                color="white",
                elevation=0  # Remove a elevação para alinhar com o container
            ),
            margin=ft.margin.only(top=40),  # Aumenta a margem superior para empurrar o botão mais para baixo
            on_hover=lambda e: self._on_hover(e)  # Adiciona o evento de hover
        )

        # Botão para voltar à tela inicial
        back_button = ft.Container(
            width=150,
            height=50,
            alignment=ft.alignment.center,
            bgcolor="#6E6E6E",
            border=ft.border.all(1, "#5C5C5C"),
            border_radius=ft.border_radius.all(5),
            shadow=ft.BoxShadow(blur_radius=3, color="black", spread_radius=1),
            content=ft.ElevatedButton(
                content=ft.Row(
                    [ft.Text("Voltar", color="white", size=14)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                ),
                on_click=lambda e: self.page.go('/inicial'),
                bgcolor="transparent",
                color="white",
                elevation=0
            ),
            margin=ft.margin.only(top=20),
            on_hover=lambda e: self._on_hover(e)
        )

        content_container = ft.Container(
            content=ft.Column(
                [
                    descricao_input,
                    date_picker_button,
                    selected_date,
                    add_button,
                    back_button,  # Adiciona o botão "Voltar"
                    result_text,
                    error_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos verticalmente
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centraliza os elementos horizontalmente
            ),
            expand=True,
            alignment=ft.alignment.center  # Centraliza o container na tela
        )
        
        # Retorna o Stack com o fundo e o conteúdo centralizado
        return ft.Stack(
            [
                background_image,  # Primeira imagem de fundo
                content_container  # Conteúdo centralizado
            ],
            expand=True  # Faz o Stack preencher toda a tela
        )

    def _on_cadastrar_click(self, e, descricao_input, selected_date, result_text, error_text):
        """Função chamada ao clicar no botão de cadastro"""
        descricao = descricao_input.value.strip()
        data = selected_date.value.replace("Data selecionada: ", "").strip()

        if not descricao:
            result_text.value = ""  # Limpa a mensagem de sucesso
            error_text.value = "O campo de descrição não pode estar vazio."
            result_text.update()
            error_text.update()
            return

        # Configura a data como "0000-00-00" se nenhuma data for selecionada
        if not data:
            data_formatada = "0000-00-00"
        else:
            # Converte a data para o formato aaaa-mm-dd
            try:
                data_formatada = datetime.datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                result_text.value = ""  # Limpa a mensagem de sucesso
                error_text.value = "Formato de data inválido."
                result_text.update()
                error_text.update()
                return

        resultado = cadastrar_tarefa(descricao, data_formatada)  # Passa a descrição e a data formatada
        if isinstance(resultado, str) and resultado == "Tarefa já existe.":
            result_text.value = ""  # Limpa a mensagem de sucesso
            error_text.value = "Erro: Tarefa já cadastrada."
        elif resultado:
            error_text.value = ""  # Limpa a mensagem de erro
            result_text.value = "Tarefa cadastrada com sucesso!"
            descricao_input.value = ""  # Limpa o campo de entrada
            selected_date.value = ""  # Reseta a data
            selected_date.visible = False  # Oculta o texto da data
        else:
            result_text.value = ""  # Limpa a mensagem de sucesso
            error_text.value = "Erro ao cadastrar a tarefa."

        # Atualiza os textos na tela
        result_text.update()
        error_text.update()
        descricao_input.update()
        selected_date.update()

    def _on_hover(self, e):
        if e.data == "true":  # Quando o mouse está sobre o botão
            e.control.bgcolor = "#8A8A8A"  # Torna o botão mais claro
        else:  # Quando o mouse sai do botão
            e.control.bgcolor = "#6E6E6E"  # Retorna à cor original
        e.control.update()
