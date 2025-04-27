"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.3
"""
from kivy.app import App
from kivy.properties import ListProperty

from cal_functions import CoreFunctions
from palette import RED, background_colour, text_colour, selected_colour, disabled_colour

# kivy doesn't require def __init__() - uses build() instead
class MainApp(App):
    colour_background = ListProperty(background_colour)
    colour_text = ListProperty(text_colour)
    colour_selected = ListProperty(selected_colour)
    colour_disabled = ListProperty(disabled_colour)
    colour_holiday = ListProperty(RED)
    def build(self) -> CoreFunctions:
        self.title = 'Calendar App'
        self.locale = 'en_US.UTF-8'
        return CoreFunctions(locale=self.locale)

if __name__ == '__main__':
    MainApp().run()
