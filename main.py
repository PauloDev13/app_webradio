from xml.dom import NoModificationAllowedErr

import flet as ft
import flet_audio as fa
# import requests



import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

LOGO_URL = "https://drive.google.com/uc?export=view&id=1t_Q8u_ouwmjctpgSGzDMFnYhe8x8DKEb"
STREAM_URL = 'https://usa13.fastcast4u.com/proxy/parqueverde?mp=/1'
JSON_URL = 'https://usa13.fastcast4u.com/rpc/parqueverde/streaminfo.get'

def main(page: ft.Page):

    page.title = 'Webrádio Parque Verde'
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.padding = 0

    # Player
    audio = fa.Audio(
        src=STREAM_URL,
    )

    page.overlay.append(audio)

    # wave = SoundWave(color=ft.Colors.GREEN, bar_count=8)

    def start_radio(e):
        audio.play()


    def pause_radio(e):
        audio.pause()

    def stop_radio(e):
        nonlocal audio
        audio.release()

        new_audio = fa.Audio(
            src=STREAM_URL,
        )
        page.overlay.append(new_audio)

        audio = new_audio


    # Componentes visuais
    title = ft.Text(
        value='Estação Parque Verde',
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    subtitle = ft.Text(
        value="WebRádio - Parnamirim/RN",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE70,
        text_align=ft.TextAlign.CENTER
    )

    logo = ft.Image(
        src=LOGO_URL,
        width=200,
        height=200,
    )

    control_row = ft.Row(
        [
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.PLAY_ARROW,
                    icon_color=ft.Colors.BLUE_900,
                    icon_size=40,
                    on_click=start_radio,
                ),
                bgcolor=ft.Colors.BLUE_400,
                shape=ft.BoxShape.CIRCLE,
            ),

            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.PAUSE,
                     icon_color=ft.Colors.BLUE_900,
                    icon_size=40,
                    on_click=pause_radio,
                ),
                bgcolor=ft.Colors.BLUE_400,
                shape=ft.BoxShape.CIRCLE,
            ),

            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.STOP,
                    icon_color=ft.Colors.BLUE_900,
                    icon_size=40,
                    on_click=stop_radio,
                ),
                bgcolor=ft.Colors.BLUE_400,
                shape=ft.BoxShape.CIRCLE,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )


    # Layout principal
    page.add(
        ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    "#0d47a1", "#1976d2", "#42a5f5"
                ]
            ),
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    title,
                    subtitle,
                    logo,
                    # wave,
                    control_row,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
        )
    )

ft.app(target=main)