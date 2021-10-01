import json

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout


class ClickableBoxLayout(ButtonBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super(ClickableBoxLayout, self).__init__(**kwargs)


# class MainCard(MDCard):
class MainCard(MDRelativeLayout, FakeRectangularElevationBehavior):
    closed = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(MainCard, self).__init__(**kwargs)
        Clock.schedule_once(self.add_screens)

    def add_screens(self, dt):
        with open("json/main_screens.json") as f:
            screens = json.load(f)

        for screen_name in screens.keys():
            screens_details = screens[screen_name]
            Builder.load_file(screens_details["kv"])
            exec(screens_details["import"])
            screen_object = eval(screens_details["object"])
            screen_object.name = screen_name
            self.ids.screen_manager.add_widget(screen_object)

    def toggle(self):
        if self.closed:
            Animation(size_hint_y=0.9,
                      x=self.parent.ids.menu.right + 50,
                      center_y=Window.height / 2,
                      duration=0.1).start(self)
            self.closed = False
        else:
            Animation(size_hint=(1, 1), pos=(0, 0), duration=0.1).start(self)
            self.closed = True
