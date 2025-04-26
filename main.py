"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.3
"""
from kivy.app import App
from kivy.properties import ListProperty

from cal_functions import CoreFunctions
import palette

# kivy doesn't require def __init__() - uses build() instead
class MainApp(App):
    colour_light_base = ListProperty(palette.LIGHT_BACKGROUND)
    colour_light_text = ListProperty(palette.LIGHT_TEXT)
    colour_light_blue = ListProperty(palette.LIGHT_BLUE)
    def build(self) -> CoreFunctions:
        self.title = 'Calendar App'
        self.locale = 'en_US.UTF-8'
        return CoreFunctions(locale=self.locale)

if __name__ == '__main__':
    MainApp().run()
