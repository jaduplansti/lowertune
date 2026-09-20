import flet as ft
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
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

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
            width = 330,
            height = 330,
            border_radius = 20,
            bgcolor = ft.Colors.GREY_900,
            clip_behavior = ft.ClipBehavior.HARD_EDGE,
            content = ft.Image(
                ref = self.thumbnail_ref,
                src = "icon.png",
                width = 330,
                height = 330,
                fit = ft.BoxFit.CONTAIN
            )
        )

    def createBlankInfo(self):
        return ft.Column(
            width = 330,
            horizontal_alignment = ft.CrossAxisAlignment.START,
            spacing = 4,
            controls = [
                ft.Text(
                    ref = self.music_name_ref,
                    value = "Title",
                    size = 24,
                    weight = ft.FontWeight.BOLD,
                    max_lines = 2,
                    overflow = ft.TextOverflow.ELLIPSIS
                ),
                ft.Text(
                    ref = self.artist_name_ref,
                    value = "Artist",
                    size = 16,
                    opacity = 0.6,
                    max_lines = 1,
                    overflow = ft.TextOverflow.ELLIPSIS
                )
            ]
        )

    def createBlankProgress(self):
        return ft.Column(
            width = 330,
            spacing = 5,
            controls = [
                ft.ProgressBar(
                    ref = self.progress_bar_ref,
                    value = 0,
                    height = 5
                ),
                ft.Row(
                    controls = [
                        ft.Text("0:00", size = 13, opacity = 0.6),
                        ft.Container(expand = True),
                        ft.Text(ref = self.duration_ref, value = "0:00", size = 13, opacity = 0.6)
                    ]
                )
            ]
        )

    def createBlankControls(self):
        return ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            spacing = 30,
            controls = [
                ft.IconButton(
                    icon = ft.Icons.FAST_REWIND,
                    icon_size = 38
                ),
                ft.IconButton(
                    icon = ft.Icons.PLAY_CIRCLE_FILL,
                    icon_size = 72,
                    on_click = self.mainButtonClicked
                ),
                ft.IconButton(
                    icon = ft.Icons.FAST_FORWARD,
                    icon_size = 38
                )
            ]
        )

    def createLayout(self):
        return ft.SafeArea(
            content = ft.Column(
                width = 330,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 24,
                controls = [
                    self.createBlankImage(),
                    self.createBlankInfo(),
                    self.createBlankProgress(),
                    self.createBlankControls()
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

        self.page.update()

        self.page.android_player.play(info["url"])

    def mainButtonClicked(self, e):
        button : ft.IconButton = e.control 
        state = self.page.android_player.getState()

        if state == "playing":
            button.icon = ft.Icons.PLAY_CIRCLE
            self.pause()
        elif state == "paused":
            button.icon = ft.Icons.PAUSE_CIRCLE
            self.play()
        self.page.update() 

    def play(self):
        self.page.android_player.resume()

    def pause(self):
        self.page.android_player.pause()

    def trackProgress(self): # TODO: FIX THIS
        while self.page.android_player:
            
            duration = self.page.android_player.getDuration()
            position = self.page.android_player.getPosition()

            if duration > 0:
                progress = position / duration
                self.progress_bar_ref.current.value = progress
            
            if self.page.android_player.isFinished():
                self.pause()
                self.play_button_ref.current.icon = ft.Icons.PLAY_CIRCLE

            self.page.update()

            time.sleep(0.5)
    
