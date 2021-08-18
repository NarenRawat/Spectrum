import os
import threading
from io import BytesIO

from kivy.clock import mainthread
from kivy.core.image import Image as CoreImage
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, ListProperty
from mutagen import File

from libs import filemanager

KV_DIR = "libs/kv"

# Load all kv files from KV_DIR
for kv_file in os.listdir(KV_DIR):
    Builder.load_file(os.path.join(KV_DIR, kv_file))


class SpectrumApp(MDApp):
    now_playing = ListProperty() # Image, Title, Artists, Path
    def __init__(self, **kwargs):
        super(SpectrumApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = '800'

    def on_start(self):
        (self.root.ids.main_card.ids.music_screen.
            ids.music_screen_tabs.switch_tab(
                self.root.ids.main_card.ids.
                music_screen.ids.music_screen_tabs.
                get_tab_list()[1]))
        threading.Thread(target=self.populate_songs_tab, daemon=True).start()

    @mainthread
    def populate_songs_tab(self):
        all_songs = filemanager.extract_files('D:/Naren/Songs/BTS', 'mp3')
        for song_path in all_songs:
            title, artist, image_texture = self.get_song_details(song_path)
            self.root.ids.main_card.ids.music_screen.ids.songs_tab.ids.songs_tab_rv.data.append(
                {
                    'title': title,
                    'artist': artist,
                    'image_texture': image_texture,
                    'file_path': song_path
                }
            )
        self.root.ids.main_card.ids.music_screen.ids.songs_tab.ids.songs_tab_rv.data.sort(key=lambda x: x.get('title').capitalize())
    def get_song_details(self, file_path):
        detail = File(file_path)

        artist = 'Unknown Artist'
        title = None
        image_texture = None

        if 'TIT2' in detail:
            title = detail['TIT2'][0]
        else:
            title = os.path.basename(file_path)[:-4]
        if 'TPE1' in detail:
            artist = detail['TPE1'][0]
       
        if 'APIC:' in  detail:
            data = detail['APIC:'].data
            image_texture = CoreImage(BytesIO(data), ext='png').texture
        else:
            with open('assets/images/song.png', 'rb') as file:
                data = file.read()
            image_texture = CoreImage(BytesIO(data), ext='png').texture
        
        return title, artist, image_texture


    def on_pause(self):
        return True

    def toggle_theme_style(self, switch, value):
        if value:
            self.theme_cls.theme_style = 'Dark'
        else:
            self.theme_cls.theme_style = 'Light'


if __name__ == '__main__':
    SpectrumApp().run()
