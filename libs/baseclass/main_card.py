from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivymd.uix.card import MDCard


class MainCard(MDCard):
    closed = BooleanProperty(True)
    anim_duration = 0.1

    def __init__(self, **kwargs):
        super(MainCard, self).__init__(**kwargs)

    def toggle(self):
        if self.closed:
            anim = Animation(
                size_hint_y=0.9,
                x=self.parent.ids.menu.right + 50,
                center_y=Window.height/2,
                duration=self.anim_duration
            )
            anim.start(self)
            self.closed = False
        else:
            anim = Animation(
                size_hint=(1, 1),
                pos=(0, 0),
                duration=self.anim_duration
            )
            anim.start(self)
            self.closed = True
