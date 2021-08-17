from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.properties import StringProperty, ObjectProperty


class SongItem(MDBoxLayout):
    title = StringProperty()
    artist = StringProperty()
    file_path = StringProperty()
    image_texture = ObjectProperty()

    def __init__(self, **kwargs):
        super(SongItem, self).__init__(**kwargs)


class SongItemRippleWidget(TouchRippleButtonBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super(SongItemRippleWidget, self).__init__(**kwargs)
