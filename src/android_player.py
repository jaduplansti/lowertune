from jnius import autoclass

import flet as ft


class AndroidPlayer:
    def __init__(self):
        self.__media_player_class = autoclass("android.media.MediaPlayer")
        self.__media_player = self.__media_player_class()

    def play(self, url):
        self.__media_player.reset()
        self.__media_player.setDataSource(url)
        self.__media_player.prepare()
        self.__media_player.start()

    def pause(self):
        if self.__media_player:
            if self.__media_player.isPlaying():
                self.__media_player.pause()

    def resume(self):
        if self.__media_player:
            if not self.__media_player.isPlaying():
                self.__media_player.start()

    def stop(self):
        if self.__media_player:
            self.__media_player.stop()

    def seek(self, position):
        if self.__media_player:
            self.__media_player.seekTo(position)

    def close(self):
        if self.__media_player:
            try:
                self.__media_player.stop()
            except Exception:
                pass

            self.__media_player.release()
            self.__media_player = None

    def getDuration(self):
        if self.__media_player:
            return self.__media_player.getDuration()

        return 0

    def getPosition(self):
        if self.__media_player:
            return self.__media_player.getCurrentPosition()

        return 0

    def isPlaying(self):
        if self.__media_player:
            return self.__media_player.isPlaying()

        return False

    def isFinished(self):
        if self.__media_player:
            duration = self.__media_player.getDuration()
            position = self.__media_player.getCurrentPosition()

            return duration > 0 and position >= duration

        return False

    def getState(self):
        if not self.__media_player:
            return "released"

        try:
            if self.__media_player.isPlaying():
                return "playing"

            position = self.__media_player.getCurrentPosition()
            duration = self.__media_player.getDuration()

            if duration > 0 and position >= duration:
                return "completed"
                
            if position > 0:
                return "paused"
            return "idle"

        except Exception:
            return "idle"