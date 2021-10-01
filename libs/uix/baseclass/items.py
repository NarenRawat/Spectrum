from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivymd.uix.list import OneLineListItem


class SongItem(MDBoxLayout):
    title = StringProperty(' ')
    artist = StringProperty(' ')
    path = StringProperty()
    image_texture = ObjectProperty()
    length = NumericProperty(0)
    is_favorite = BooleanProperty()

    def __init__(self, **kwargs):
        super(SongItem, self).__init__(**kwargs)


class SongItemRippleWidget(TouchRippleButtonBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super(SongItemRippleWidget, self).__init__(**kwargs)
