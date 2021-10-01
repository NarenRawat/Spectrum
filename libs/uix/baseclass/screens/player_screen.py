from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock


class PlayerScreen(MDScreen):
    def __init__(self, **kw):
        super(PlayerScreen, self).__init__(**kw)
        self.app = MDApp.get_running_app()
        self.is_down = False
        

    def slider_down(self, slider, touch):
        if self.app.media_player.sound:
            if slider.children[0].collide_point(*touch.pos):
                self.app.media_player.play_clock.cancel()
                self.is_down = True
    def slider_up(self, slider, touch):
        # if slider.children[0].collide_point(*touch.pos):
        if self.app.media_player.sound:
            if self.is_down:
                Clock.create_trigger(self.app.media_player.play_clock, 0)()
                self.app.media_player.seek(slider.value / 100)
                self.is_down = False