from enum import EnumType

import flet as ft
import flet_audio as fa

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

STREAM_URL = 'https://usa13.fastcast4u.com/proxy/parqueverde?mp=/1'
# STREAM_URL = 'https://usa13.fastcast4u.com/proxy/parqueverde?mp=/1&type=mp3'
INSTAGRAM_URL = 'http://instagram.com/'
WHATSAPP_URL = 'http://wa.me/558497015547'
LOGO_URL = 'https://drive.google.com/uc?export=view&id=1t_Q8u_ouwmjctpgSGzDMFnYhe8x8DKEb'

def main(page: ft.Page):
    # ---------- Configurações básicas da página ----------
    page.title = 'Sua Web Radio'
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.window.bgcolor = ft.Colors.BLACK
    page.bgcolor = ft.Colors.TRANSPARENT
    page.fonts = {} # (opcional) adicione fontes customizadas aqui
    page.window.width = 360
    page.window.height = 640

    # ---------- Áudio: controlado por um componente não-visual ----------

    obj_audio = ft.Ref[ft.Audio]()
    # O controle Audio não é exibido; adicionamos no overlay e controlamos via código.

    audio = fa.Audio(
        src=STREAM_URL,
        autoplay=True,
        volume=1.0,
        # ref=obj_audio,
        # on_state_changed atualiza a UI conforme o estado do player
    )

    audio_new = fa.Audio(
        src=STREAM_URL,
        autoplay=True,
        volume=1.0,
        ref=obj_audio,
    )

    page.overlay.append(audio)

    # Estado simples do player para atualizar ícone/label
    is_playing = ft.Ref[bool]()
    is_playing.current = True # presume que iniciou tocando (autoplay)


    # botão dinâmico
    play_icon_button = ft.Ref[ft.IconButton]()

    # ---------- Handlers ----------
    def on_state_change(e):

        state = getattr(e, 'state', None)

        if state in (fa.AudioState.PAUSED, fa.AudioState.STOPPED, fa.AudioState.COMPLETED):
            print(f'State changed to {state} if do on_state_change')
            is_playing.current = False

            if play_icon_button.current:
                if play_icon_button.current:
                    play_icon_button.current.icon = ft.Icons.PLAY_ARROW_ROUNDED

        elif state == fa.AudioState.PLAYING:
            print(f'State changed to {state} no else do on_state_change')
            is_playing.current = True

            if play_icon_button.current:
                play_icon_button.current.icon = ft.Icons.PAUSE_ROUNDED

        page.update()

    audio.on_state_changed = on_state_change

    def toggle_play_pause(_):

        nonlocal audio
        """
        Alterna Play/Pause. Se o stream tiver sido interrompido,
        chamar play() novamente garante retomada.
        """
        try:

            # if is_playing.current:
            #     audio.pause()
            #
            # else:

            #     # Se estava pausado/completed/stopped, iniciar/reiniciar:
            #     audio.play()
            if is_playing.current:
                print('is_playing.curren')
                if fa.AudioState.PLAYING:
                    print('Playing stopped. A')
                    # audio.release()

                if obj_audio.current.on_state_changed == fa.AudioState.STOPPED:
                    print('Playing stopped. B')
                    # obj_audio.current.release()

            else:
                print('Entrou no else')
                if audio.on_state_changed == fa.AudioState.PLAYING:
                    print('Playing . A')
                    # page.overlay.append(obj_audio.current)
                    # obj_audio.current.play()
                    # audio_new = fa.Audio(src=STREAM_URL, autoplay=True, volume=1.0)
                    # audio = audio_new
                if obj_audio.current.on_state_changed == fa.AudioState.PLAYING:
                    print('Playing. A')
                    # page.overlay.append(audio)
                    # audio.play()

            audio.on_state_changed = toggle_play_pause

        except Exception as ex:
            # Em caso de falha de conexão, tentar reiniciar o stream.
            print(f'Erro ao alternar player: {ex}')
            audio.src = STREAM_URL
            audio.play()


    def toggle_stop(_):
        nonlocal audio

        is_playing.current = True

        audio.release()

        new_audio = fa.Audio(
            src=STREAM_URL,
        )
        page.overlay.append(new_audio)
        audio = new_audio


    # Abrir links externos (Instagram/WhatsApp) usando o launcher nativo
    def open_instagram(_):
        page.launch_url(INSTAGRAM_URL, web_window_name='_blank')

    def open_whatsapp(_):
        page.launch_url(WHATSAPP_URL, web_window_name='_blank')

    # Adiciona o player ao overlay da página.
    # page.overlay.append(audio)

    # ---------- UI: Gradiente de fundo ----------
    background = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.BLUE_600, ft.Colors.BLUE_800, ft.Colors.BLACK,
                ],
                tile_mode=ft.GradientTileMode.CLAMP
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=24),
        content=ft.Column(
            spacing=24,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                # ---------- Topo: Logomarca ----------
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Image(
                        src=LOGO_URL,
                        width=270,
                        height=270,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                    ),
                ),

                # ---------- Player: Botão Play/Pause estilizado ----------
                ft.Container(
                    padding=20,
                    content=ft.Column(
                        spacing=30,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=150,
                                height=50,
                                padding=ft.padding.only(left=5, right=5),
                                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                                border_radius=100,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                            padding=5,
                                            bgcolor=ft.Colors.BLUE_900,
                                            icon_size=30,
                                            ref=play_icon_button,
                                            on_click=toggle_play_pause,

                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.STOP_ROUNDED,
                                            padding=5,
                                            bgcolor=ft.Colors.BLUE_900,
                                            icon_size=30,
                                            on_click=toggle_stop,
                                        )
                                    ]
                                )

                            ),

                            # ---------- Título "Tocando agora" ----------
                            ft.Text(
                                value='Tocando agora',
                                color=ft.Colors.WHITE,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),

                            ft.Text(
                                value='Artista:',
                                color=ft.Colors.WHITE70,
                                size=12,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                value='Música:',
                                color=ft.Colors.WHITE70,
                                size=12,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
                # ---------- Espaçador para empurrar os botões sociais para o rodapé ----------
                ft.Container(expand=True),

                # ---------- Botões Sociais ----------
                ft.Container(
                    padding=ft.padding.only(bottom=8),
                    content=ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            ft.Container(
                                col=6,
                                content=ft.FilledTonalButton(
                                    icon=ft.Icons.CAMERA_ALT_ROUNDED, # ícone genérico para Instagram
                                    text='Instagram',
                                    on_click=open_instagram,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.with_opacity(0.18, ft.Colors.WHITE),
                                    ),
                                ),
                            ),
                            ft.Container(
                                col=6,
                                content=ft.FilledTonalButton(
                                    icon=ft.Icons.CHAT_ROUNDED,  # ícone genérico para WhatsApp
                                    text='WhatsApp',
                                    on_click=open_whatsapp,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.with_opacity(0.18, ft.Colors.WHITE),
                                    ),
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )
    # Compor tudo dentro do SafeArea
    # safe = ft.SafeArea(expand=True)
    safe = ft.SafeArea(content=background, expand=True)
    page.add(safe)

    # Se desejar garantir autoplay em alguns dispositivos, forçar um play() após o carregamento:
    try:
        audio.play()
    except Exception as ex:
        pass


# ft.app(target=main)
if __name__ == '__main__':
    ft.app(target=main,view=ft.AppView.FLET_APP)
    # Observação:
    # - Para Android, o empacotamento usa build de app nativo; ver instruções ao final.