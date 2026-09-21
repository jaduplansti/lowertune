# Lowertune
**A YT Music Streaming App**

> **Warning:** This app is purely experimental and may break, use at your own risk.

# Features
- [x] Youtube Streaming
- [x] Basic Player
- [x] Music Searching 
- [ ] Full Playback Controls 
- [ ] History Management

# Building APK

``` 
git clone https://github.com/jaduplansti/lowertune 
pip install -r requirements.txt
flet build apk
``` 

>[!NOTE]
> Install all project requirements by pip install -r requirements.txt

# Android Player

This project does not use flet-audio as the package is currently facing issues, instead it uses pyjnius to interace with the android java sdk (**MediaPlayer**). You may encounter issues in building.
```
class AndroidPlayer:
    def __init__(self):
        self.__media_player_class = autoclass("android.media.MediaPlayer")
        self.__media_player = self.__media_player_class()

    def play(self, url):
        self.__media_player.reset()
        self.__media_player.setDataSource(url)
        self.__media_player.prepare()
        self.__media_player.start()
```
