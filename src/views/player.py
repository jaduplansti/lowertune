import flet as ft
import flet_audio as fta 
import asyncio
from youtube import Youtube

@ft.control
class Player(ft.View):
    def __init__(self, user, navigation_bar):
        super().__init__(navigation_bar = navigation_bar)
        self.user = user 

    def init(self):
        self.route = "/player"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER 

        self.thumbnail_ref = ft.Ref[ft.Image]()
        self.music_name_ref = ft.Ref[ft.Text]()
        self.artist_name_ref = ft.Ref[ft.Text]()
        self.duration_ref = ft.Ref[ft.Text]()

        self.progress_bar_ref = ft.Ref[ft.ProgressBar]()

        self.controls = [
            self.createLayout()
        ]

    def createBlankImage(self):
        return ft.Container(
            border_radius = 15,
            bgcolor = ft.Colors.GREY,
            content = ft.Image(
                fit = ft.BoxFit.CONTAIN,
                ref = self.thumbnail_ref, 
                height = 350,
                expand = True,
                src = "icon.png"
            )
        )

    def createBlankInfo(self):
        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 5,
            controls = [
                ft.Text(ref = self.music_name_ref, size = 24, value = "Title"),
                ft.Text(ref = self.artist_name_ref, size = 16, value = "Artist"),
            ]
        )

    def createBlankProgress(self):
        return ft.Column(
            expand = True, 
            controls = [
                ft.ProgressBar(ref = self.progress_bar_ref, expand = True),
                ft.Row(
                    controls = [
                        ft.Text("0:00", size = 16),
                        ft.Container(expand = True),
                        ft.Text(ref = self.duration_ref, value = "0:00", size = 16)
                    ]
                )
            ]
        )
    
    def createBlankControls(self):
        return ft.Row(
            alignment = ft.CrossAxisAlignment.CENTER,
            controls = [
                ft.IconButton(icon = ft.Icons.FAST_REWIND, icon_size = 48),
                ft.IconButton(icon = ft.Icons.PLAY_CIRCLE_FILL, icon_size = 60, on_click = self.play),
                ft.IconButton(icon = ft.Icons.FAST_FORWARD, icon_size = 48)
            ]
        )

    def createLayout(self):
        return ft.SafeArea(
            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 20,
                controls = [
                    self.createBlankImage(),
                    self.createBlankInfo(),
                    self.createBlankProgress(),
                    self.createBlankControls(),
                ]
            )
        )

  
    async def start(self):
        info = await asyncio.to_thread(
            Youtube.fetch,
            self.user.current_audio
        )

        self.thumbnail_ref.current.src = info["thumbnail"]
        self.music_name_ref.current.value = info["title"]
        self.artist_name_ref.current.value = info["artist"]
        self.duration_ref.current.value = info["duration"]
        self.page.audio.src = info["url"]
        self.page.update()

        await self.page.audio.play()
        

    async def play(self):
        pass
        #await self.page.audio_handler.play()
