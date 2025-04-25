import flet as ft

class InitialPage:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        page.theme = ft.Theme(font_family="MarioText")
    
    def construir(self):
        self.page.title = "To Do List"
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        background_video = ft.Video(
            playlist=[ft.VideoMedia(resource='C:\\Users\\ead\\Documents\\Philipi\\Aulas\\Flet\\ToDoList\\src\\assets\\vids\\Super Mario World.mp4')],
            playlist_mode=ft.PlaylistMode.LOOP,
            show_controls=False,
            autoplay=True,
            width=self.page.width,
            height=self.page.height,
            fit=ft.ImageFit.COVER,
            on_loaded=lambda _: background_video.play(),
            on_error=lambda e: print(f"Error loading video: {e.data}")
        )

        def hover(e):
            if e.data == "true":
                img.visible = True
            else:
                img.visible = False
            self.page.update()

        img = ft.Image(src="/imgs/setaMario.png", width=15, height=15, visible=False)

        self.page.add(ft.Stack(
            controls=[
                background_video,
                ft.Column(
                    controls=[
                        ft.Image(
                            src="/imgs/TituloInicial.png",
                            width=300,
                            height=150,
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    img,
                                    ft.Text("Ir para Cadastro", style=ft.TextStyle(size=13, font_family="MarioText")),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            on_hover=lambda e: hover(e),
                            on_click=lambda _: self.page.go("/cadastro"),
                            bgcolor=ft.Colors.BLUE_300,
                            width=300,
                            height=50,
                            border_radius=10,
                            padding=10,
                        )
                    ],
                ),
            ]
        )
        )
        background_video.play()
        self.page.update()