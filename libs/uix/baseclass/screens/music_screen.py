import json
import os
from threading import Thread

# from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.clock import Clock, mainthread
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from libs.applibs.file_manager import extract_files
from libs.applibs.song_details import details
from libs.uix.baseclass.items import SongItem


class MusicScreen(MDScreen):
    progress_end_angle = NumericProperty(0)

    def __init__(self, **kw):
        super(MusicScreen, self).__init__(**kw)
        Clock.schedule_once(self.thread_add)
        with open(os.path.join('assets', 'data', 'favorites.json')) as file:
            self.favorites = json.load(file)

    def thread_add(self, dt):
        Thread(target=self.add_items, daemon=True).start()

    @mainthread
    def add_items(self):
        ls = extract_files(MDApp.get_running_app().sound_dir, "mp3")
        for path in ls:
            title, artist, album, image_texture, length = details(path)
            is_favorite = False
            if not image_texture:
                image_texture = MDApp.get_running_app().default_song_texture
            for fav in self.favorites:
                if os.path.samefile(os.path.realpath(path),
                                    os.path.realpath(fav)):
                    is_favorite = True
                    break
                else:
                    is_favorite = False

            self.ids.rv.data.append({
                "viewclass": "SongItem",
                "title": title,
                "artist": artist,
                "image_texture": image_texture,
                "path": path,
                "length": length,
                "is_favorite": is_favorite
            })
            self.ids.rv.data.sort(key=lambda x: x.get('title').capitalize())
        self.ids.rv.data.sort(key=lambda x: x.get('title').capitalize())
        self.ids.rv.data.append({
            "viewclass": "BoxLayout",
            "size_hint_y": None,
            "height": 70
            # "height": (self.ids.player.top -
            #            self.ids.bottom_navigation.ids.bottom_panel.top),
        })
