import json

from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import CardTransition, ScreenManager


class Root(ScreenManager):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.transition = CardTransition(duration=0.2, direction='up')
        Clock.schedule_once(self.add_screens)

    def add_screens(self, delta):
        """
        If you need to use more screens in your app,
        Create your screen files like below:
            1. Create screen_file.py in libs/uix/baseclass/
            2. Create screen_file.kv in libs/uix/kv/
            3. Add the screen details in screens.json like below:
                {
                    ...,
                    "screen_name": {
                        "import": "from libs.uix.baseclass.screen_py_file import ScreenObject",
                        "kv": "libs/uix/kv/screen_kv_file.kv",
                        "object": "ScreenObject()"
                    }
                }
                Note: In .JSON you must not use:
                        * Unneeded Commas
                        * Comments
        """
        with open("json/root_screens.json") as f:
            screens = json.load(f)

        for screen_name in screens.keys():
            screens_details = screens[screen_name]
            Builder.load_file(screens_details["kv"])
            exec(screens_details["import"])
            screen_object = eval(screens_details["object"])
            screen_object.name = screen_name
            self.add_widget(screen_object)
