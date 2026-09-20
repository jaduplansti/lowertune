import flet as ft


class SearchResult(ft.Container):
    def __init__(self, name, artist, duration, cover, video_url, click_fn):
        super().__init__(
            alignment = ft.Alignment.CENTER,
            padding = 10,
            border_radius = 5,
            bgcolor = ft.Colors.GREY_400,
            on_click = click_fn,
            content = ft.Row(
                controls = [
                    self.coverImage(cover),
                    self.SongDetails(name, artist, duration)
                ]
            )
        )

        self.video_url = video_url

    def SongDetails(self, name, artist, duration):
        return ft.Column(
            controls = [
                ft.Text(name),
                ft.Text(f"{artist} > {duration}")
            ]
        )

    def coverImage(self, cover):
        return ft.Image(src = cover, height = 50, width = 50, fit = ft.BoxFit.CONTAIN)