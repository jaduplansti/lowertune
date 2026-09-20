import flet as ft 
import asyncio
from android_player import AndroidPlayer

from views.dashboard import Dashboard 
from views.player import Player
from user import User 

def createNavigationBar(change_fn):
    return ft.NavigationBar(
        destinations = [
            ft.NavigationBarDestination(icon = ft.Icons.HOME, label = "Home"),
            ft.NavigationBarDestination(icon = ft.Icons.MUSIC_NOTE, label = "Player"),
            ft.NavigationBarDestination(icon = ft.Icons.SETTINGS, label = "Settings")
        ],
        on_change = change_fn
    )

def loadAndroidPlayer(page):
    try:
        page.android_player = AndroidPlayer()
    except:
        page.android_player = None

def startProgressTracker(page, player):
    #if page.android_player:
    page.run_thread(player.trackProgress)

async def main(page : ft.Page):
    user = User() 
    progress_tracked = False 

    def route_changed():
        page.views.clear()
        nonlocal progress_tracked 

        if page.route == "/":
            page.views.append(dashboard)
        elif page.route == "/player":
            page.views.append(player)
            page.update()
            if progress_tracked is False:
                startProgressTracker(page, player)
                progress_tracked = True
        page.update()

        

    async def navigation_changed():
        if navbar.selected_index == 0:
            await page.push_route("/")
        elif navbar.selected_index == 1:
            await page.push_route("/player")

    async def player_launch(url):
        user.current_audio = url
        navbar.selected_index = 1
        await page.push_route("/player")
        await player.start()

    loadAndroidPlayer(page)

    page.player_launch = player_launch
    navbar = createNavigationBar(navigation_changed)
    dashboard = Dashboard(user, navigation_bar = navbar)
    player = Player(user, navigation_bar = navbar)

    page.on_route_change = route_changed
    await page.push_route("/")
    route_changed()


if __name__ == "__main__":
    ft.run(main)