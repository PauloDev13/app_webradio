import flet as ft
import flet_audio as fa
import requests
import asyncio

import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

STREAM_URL = 'https://usa13.fastcast4u.com/proxy/parqueverde?mp=/1'
JSON_URL = 'https://usa13.fastcast4u.com/rpc/parqueverde/streaminfo.get'
INSTAGRAM_URL = 'https://instagram.com/'
WHATSAPP_URL = 'https://wa.me/558487015547'
USE_LOCAL_ASSET = False
BACKGROUND_LOCAL = 'background.png'
BACKGROUND_URL = (
    BACKGROUND_LOCAL if USE_LOCAL_ASSET else 'https://drive.google.com/uc?export=view&id=1bU2-ZN55sF_V5FRnXY6DmsU_FcEctjnA'
)

def main(page: ft.Page):
    # ---------- Configurações básicas da página ----------
    page.title = 'Sua Web Radio'
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.window.bgcolor = ft.Colors.BLACK
    page.bgcolor = ft.Colors.TRANSPARENT
    page.fonts = {} # (opcional) adicione fontes customizadas aqui
    page.window.width = 400
    page.window.min_width = 400
    page.window.max_width = 400
    page.window.height = 700
    page.window.min_height = 700
    page.window.max_height = 720

    # --- Tela de carregamento (mostrada imediatamente) ---
    # splash_screen = ft.Container(
    #         alignment=ft.alignment.center,
    #         padding=0,
    #         content=
    #         ft.Column(
    #             [
    #                 ft.Image(src="assets/logo.png", width=150, height=150),
    #                 ft.ProgressRing(),
    #                 ft.Text("Carregando...", size=18, weight=ft.FontWeight.BOLD)
    #             ],
    #             alignment=ft.MainAxisAlignment.CENTER,
    #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #         )
    #
    # )

    # page.add(splash_screen)

    # def init_app():
    # ---------- Áudio: controlado por um componente não-visual ----------
    # O controle Audio não é exibido; adicionamos no overlay e controlamos via código.
    audio = fa.Audio(
        src=STREAM_URL,
        autoplay=True,
        volume=1.0,
        # on_state_changed atualiza a UI conforme o estado do player
    )

    # Estado simples do player para atualizar ícone/label
    is_playing = ft.Ref[bool]()
    is_playing.current = True # presume que iniciou tocando (autoplay)

    # botão dinâmico
    play_icon_button = ft.Ref[ft.IconButton]()

    # text_state_play = ft.Ref[ft.Text]()
    text_artist = ft.Ref[ft.Text]()
    text_music = ft.Ref[ft.Text]()

    # ---------- Handlers ----------
    def on_state_change(e):

        state = getattr(e, 'state', None)

        if state in (fa.AudioState.PAUSED, fa.AudioState.STOPPED, fa.AudioState.COMPLETED):
            # print(f'State changed to {state} if do on_state_change')
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
            if is_playing.current:
                audio.pause()

                new_audio = fa.Audio(
                    src=STREAM_URL,
                    volume=1.0
                )

                audio = new_audio
                page.overlay.append(audio)

                audio.on_state_changed = on_state_change
            else:
                # Se estava pausado/completed/stopped, iniciar/reiniciar:
                audio.play()


        except Exception as e:
            # Em caso de falha de conexão, tentar reiniciar o stream.
            print(f'Erro ao alternar player: {e}')
            audio.src = STREAM_URL
            audio.play()

    def update_song_info():
        try:
            # Busca dados na API
            response = requests.get(JSON_URL, timeout=(10, 15))
            response.raise_for_status()  # dispara erro HTTP se status != 200

            # Converte em JSON
            data = response.json()

            # Extrai track (se estrutura esperada existir)
            track = data.get("data", [{}])[0].get("track", {})

            # Extrai valores com fallback
            artist = track.get("artist")
            title = track.get("title")

            # Verificação final
            if not artist or not title:
                print("Aviso: JSON não contém 'artist' ou 'title'")
                return None, None

            # print("executou")
            return artist, title

        except requests.exceptions.Timeout:
            print("Erro: timeout na requisição")
        except requests.exceptions.ConnectionError:
            print("Erro: falha de conexão com o servidor")
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
        except ValueError:
            print("Erro: resposta não é JSON válido")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        # Retorno seguro em caso de erro
        return None, None

    async def loop_update():
        while True:
            artist, title = update_song_info()

            if artist and title:
                text_artist.current.value = f'Artista: {artist}'
                text_music.current.value = f'Musica: {title}'
            else:
                text_artist.current.value = 'Artista: Sem informações'
                text_music.current.value = 'Música: Sem informações'

            text_artist.current.update()
            text_music.current.update()

            await asyncio.sleep(10)

    # Abrir links externos (Instagram/WhatsApp) usando o launcher nativo
    def open_instagram(_):
        page.launch_url(INSTAGRAM_URL, web_window_name='_blank')

    def open_whatsapp(_):
        page.launch_url(WHATSAPP_URL, web_window_name='_blank')

    # Adiciona o player ao overlay da página.
    page.overlay.append(audio)

    # time.sleep(3)

    # ---------- UI ----------
    layout = ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=30, vertical=30),
            image=ft.DecorationImage(
                src=BACKGROUND_URL,
                fit=ft.ImageFit.COVER,
                alignment=ft.alignment.center,
                repeat=ft.ImageRepeat.NO_REPEAT,
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                        content=ft.Text(
                        value='Web Rádio',
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.alignment.center,
                        color=ft.Colors.with_opacity(0.8, '#00ebff'),
                        # ref=text_state_play
                    ),
                ),

                ft.Container(
                    padding=ft.padding.only(top=120),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=100,
                                height=100,
                                padding=ft.padding.only(left=5, right=5),
                                bgcolor=ft.Colors.with_opacity(0.3, '#00ebff'),
                                border_radius=100,
                                alignment=ft.alignment.center,
                                content= ft.IconButton(
                                    icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                    padding=5,
                                    bgcolor=ft.Colors.with_opacity(0.8,'#001c2b'),
                                    icon_size=60,
                                    ref=play_icon_button,
                                    on_click=toggle_play_pause,
                                ),
                            ),

                            ft.Container(expand=True, margin=30),

    #                         # ---------- Títulos "Tocando agora, Artista e M´suica" ----------
                            ft.Container(
                                width=350,
                                padding=ft.padding.only(top=20, bottom=20),
                                border_radius=20,
                                bgcolor=ft.Colors.with_opacity(0.3, '#000000'),
                                content=ft.Column(
                                    expand=True,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            value='Tocando agora',
                                            color='#00ebff',
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER,
                                        ),

                                        ft.Text(
                                            value='',
                                            color='#00ebff',
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER,
                                            ref=text_artist,
                                        ),

                                        ft.Text(
                                            value='',
                                            color='#00ebff',
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER,
                                            ref=text_music
                                        ),
                                    ],
                                ),
                            ),
                        ]
                    )
                ),

    #             # ---------- Espaçador para empurrar os botões sociais para o rodapé ----------
                ft.Container(expand=True),
                ft.Container(
                    padding=ft.padding.only(bottom=8),
                    content=ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            ft.Container(
                                col=6,
                                content=ft.FilledTonalButton(
                                    icon=ft.Icons.CAMERA_ALT_ROUNDED,  # ícone genérico para Instagram
                                    icon_color='#00ebff',
                                    text='Instagram',
                                    on_click=open_instagram,
                                    style=ft.ButtonStyle(
                                        color='#00ebff',
                                        bgcolor=ft.Colors.with_opacity(0.18, '#00ebff'),
                                    ),
                                ),
                            ),
                            ft.Container(
                                col=6,
                                content=ft.FilledTonalButton(
                                    icon=ft.Icons.CHAT_ROUNDED,  # ícone genérico para WhatsApp
                                    icon_color='#00ebff',
                                    text='WhatsApp',
                                    on_click=open_whatsapp,
                                    style=ft.ButtonStyle(
                                        color='#00ebff',
                                        bgcolor=ft.Colors.with_opacity(0.18, '#00ebff'),
                                    ),
                                ),
                            ),
                        ],
                    ),
                ),

            ]
        )
    )

    # page.controls.clear()
    safe = ft.SafeArea(content=layout, expand=True)
    page.add(safe)

    # Se desejar garantir autoplay em alguns dispositivos, forçar um play() após o carregamento:
    try:
        audio.play()
    except Exception as ex:
        print('Error', ex)

    page.run_task(loop_update)

    # threading.Thread(target=init_app, daemon=True).start()

# ft.app(target=main)
if __name__ == '__main__':
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP,
        assets_dir='assets'
    )
    # Observação:
    # - Para Android, o empacotamento usa build de app nativo; ver instruções ao final.