import os
from kivymd.app import MDApp
from kivy.lang.builder import Builder

KV_DIR = "libs/kv"

# Load all kv files from KV_DIR
for kv_file in os.listdir(KV_DIR):
    Builder.load_file(os.path.join(KV_DIR, kv_file))


class SpectrumApp(MDApp):
    def __init__(self, **kwargs):
        super(SpectrumApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = '800'

    def on_pause(self):
        return True


if __name__ == '__main__':
    SpectrumApp().run()
