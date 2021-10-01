import json
import os
from threading import Thread

from kivy.clock import Clock, mainthread
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from libs.applibs.song_details import details
from libs.uix.baseclass.items import SongItem


class FavoritesScreen(MDScreen):
    def __init__(self, **kw):
        super(FavoritesScreen, self).__init__(**kw)
        Clock.schedule_once(self.thread_add)
        with open(os.path.join('assets', 'data', 'favorites.json')) as file:
            self.favorites = json.load(file)

    def thread_add(self, dt):
        Thread(target=self.add_items, daemon=True).start()

    @mainthread
    def add_items(self):
        for path in self.favorites:
            title, artist, album, image_texture, length = details(path)
            if not image_texture:
                image_texture = MDApp.get_running_app().default_song_texture

            self.ids.rv.data.append({
                "viewclass": "SongItem",
                "title": title,
                "artist": artist,
                "image_texture": image_texture,
                "path": path,
                "length": length,
                "is_favorite": True
            })
