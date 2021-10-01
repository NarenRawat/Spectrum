import json
import os
from io import BytesIO
from math import ceil

from kivy import platform
from kivy._event import EventDispatcher
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivymd.app import MDApp

from libs.applibs import song_details
from libs.uix.baseclass.root import Root

if platform == 'android':
    from android.permissions import Permission, request_permissions
    from jnius import autoclass

# Import all kv files
KV_DIR = os.path.join("libs", "uix", "kv")
for kv_file in os.listdir(KV_DIR):
    if not os.path.isdir(file := os.path.join(KV_DIR, kv_file)):
        Builder.load_file(os.path.join(file))


class MediaPlayer(EventDispatcher):
    sound = None
    '''The loaded sound.
    '''

    length = NumericProperty(0)
    '''Length of currently loaded sound.
    '''
    title = StringProperty("No song is playing")
    artist = StringProperty(" ")
    image_texture = ObjectProperty()

    last_pos = NumericProperty(0)

    cur_pos = NumericProperty(0)

    data_source = StringProperty()

    is_playing = BooleanProperty(False)

    percent_played = NumericProperty(0)

    play_clock = None

    is_favorite = BooleanProperty(False)

    def __init__(self):
        self.play_clock = Clock.schedule_interval(self.played_percent_update,
                                                  0)
        self.play_clock.cancel()
        if platform == 'android':
            self.AndroidMediaPlayer = autoclass('android.media.MediaPlayer')

    def load(self, filething):
        if platform == 'win':
            if self.sound:
                self.sound.unload()
            self.sound = SoundLoader.load(filething)
            # self.length = self.sound.length
            self.last_pos = 0
        elif platform == 'android':
            if self.sound:
                self.sound.release()
            self.sound = self.AndroidMediaPlayer()
            self.last_pos = 0
            self.sound.setDataSource(filething)
            self.sound.prepare()
        self.data_source = filething
        self.play()

    def play(self):
        if platform == 'win':
            if self.sound:
                self.sound.play()
                self.is_playing = True
        elif platform == 'android':
            if self.sound:
                self.sound.start()
                self.is_playing = True
        Clock.create_trigger(self.play_clock, 0)()

    def seek(self, percentage):
        if platform == 'win':
            if self.sound:
                self.sound.seek(percentage * self.length)
        elif platform == 'android':
            if self.sound:
                self.sound.seekTo(percentage * (self.length * 1000))

    def pause(self):
        if platform == 'win':
            if self.sound:
                self.last_pos = self.sound.get_pos()
                self.is_playing = False
                self.play_clock.cancel()
                self.sound.stop()
        elif platform == 'android':
            if self.sound:
                self.last_pos = self.sound.getCurrentPosition() / 1000
                self.is_playing = False
                self.play_clock.cancel()
                self.sound.pause()

    def unpause(self):
        if platform == 'win':
            if self.sound:
                self.sound.play()
                self.sound.seek(self.last_pos)
                self.is_playing = True
                Clock.create_trigger(self.play_clock, 0)()
        elif platform == 'android':
            if self.sound:
                self.sound.start()
                self.is_playing = True
                Clock.create_trigger(self.play_clock, 0)()

    def played_percent_update(self, dt):
        if platform == 'win':
            self.cur_pos = self.sound.get_pos()
            self.percent_played = self.cur_pos / self.length
            if ceil(self.cur_pos) >= ceil(self.length):
                self.is_playing = False
                self.sound.stop()
                self.sound.unload()
                self.percent_played = 0
                self.cur_pos = 0
                self.play_clock.cancel()
                return False
        if platform == 'android':
            self.cur_pos = self.sound.getCurrentPosition() / 1000
            self.percent_played = self.cur_pos / self.length
            if ceil(self.cur_pos) >= ceil(self.length):
                self.is_playing = False
                self.sound.release()
                self.percent_played = 0
                self.cur_pos = 0
                self.play_clock.cancel()
                return False


class Spectrum(MDApp):

    media_player = MediaPlayer()

    if platform == 'win':
        sound_dir = os.path.realpath("D:/Naren/Songs/")
    elif platform == 'android':
        sound_dir = os.path.realpath('/storage/emulated/0/Music')
    """Path to search for sounds
    Path will be searched recursively for music
    """
    with open(os.path.join('assets', 'images', 'song.png'), 'rb') as file:
        default_song_texture = CoreImage(BytesIO(file.read()),
                                         ext='png').texture

    def __init__(self, **kwargs):
        super(Spectrum, self).__init__(**kwargs)
        Window.soft_input_mode = "below_target"
        self.title = "Spectrum"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "800"
        self.media_player.image_texture = self.default_song_texture
        Window.bind(on_keyboard=self.key_input)

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True

    def build(self):
        return Root()

    def on_pause(self):
        return True

    def on_start(self):
        if platform == 'android':
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

    def toggle_theme_style(self, switch, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def toggle_favorite(self, filething):
        if self.media_player.sound:
            if self.media_player.is_favorite:
                with open(os.path.join('assets', 'data',
                                       'favorites.json')) as fav:
                    favorites = json.load(fav)
                    favorites.remove(filething)
                    print(favorites)

                with open(os.path.join('assets', 'data', 'favorites.json'),
                          'w') as fav:
                    json.dump(favorites, fav, indent=4)
                self.media_player.is_favorite = False
            else:
                with open(os.path.join('assets', 'data',
                                       'favorites.json')) as fav:
                    favorites = json.load(fav)
                    favorites.append(filething)
                    print(favorites)
                with open(os.path.join('assets', 'data', 'favorites.json'),
                          'w') as fav:
                    json.dump(favorites, fav, indent=4)
                self.media_player.is_favorite = True


if __name__ == "__main__":
    Spectrum().run()
