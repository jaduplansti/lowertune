import flet as ft


class SearchResult(ft.Container):
    def __init__(self, name, artist, duration, cover, video_url, click_fn):
        super().__init__(
            alignment = ft.Alignment.CENTER,
            padding = 10,
            border_radius = 12,
            bgcolor = ft.Colors.GREY_900,
            on_click = click_fn,
            content = ft.Row(
                spacing = 12,
                controls = [
                    self.coverImage(cover),
                    self.SongDetails(name, artist, duration)
                ]
            )
        )

        self.video_url = video_url

    def SongDetails(self, name, artist, duration):
        return ft.Column(
            expand = True,
            spacing = 3,
            alignment = ft.MainAxisAlignment.CENTER,
            controls = [
                ft.Text(name, size = 16, weight = ft.FontWeight.BOLD, max_lines = 1, overflow = ft.TextOverflow.ELLIPSIS),
                ft.Text(f"{artist} • {duration}", size = 13, opacity = 0.6, max_lines = 1, overflow = ft.TextOverflow.ELLIPSIS)
            ]
        )

    def coverImage(self, cover):
        return ft.Container(
            width = 55,
            height = 55,
            border_radius = 8,
            clip_behavior = ft.ClipBehavior.HARD_EDGE,
            content = ft.Image(src = cover, height = 55, width = 55, fit = ft.BoxFit.COVER)
        )