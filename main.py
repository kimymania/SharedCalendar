"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.3
"""
import locale

from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.config import Config
from kivy.properties import ListProperty

from cal_functions import CoreFunctions
from palette import (
    RED, background_colour, text_colour,
    line_colour, selected_colour, disabled_colour
)

class MainApp(App):
    locale = 'ko_KR.UTF-8'
    colour_background = ListProperty(background_colour)
    colour_text = ListProperty(text_colour)
    colour_lines = ListProperty(line_colour)
    colour_selected = ListProperty(selected_colour)
    colour_disabled = ListProperty(disabled_colour)
    colour_holiday = ListProperty(RED)
    def build(self) -> CoreFunctions:
        self.title = '캘린더'
        print(DEFAULT_FONT)
        return CoreFunctions(locale=self.locale)

if __name__ == '__main__':
    LabelBase.register(
        name='NanumSquareRound',
        fn_regular='./fonts/NanumSquareRoundL.ttf',
        fn_italic='./fonts/NanumSquareRoundR.ttf',
        fn_bold='./fonts/NanumSquareRoundB.ttf',
        fn_bolditalic='./fonts/NanumSquareRoundEB.ttf'
    )

    # Config.setdefault('kivy', 'default_font', [
    #     'NanumSquareRound',
    #     './fonts/NanumSquareRoundL.ttf',
    #     './fonts/NanumSquareRoundR.ttf', # italic
    #     './fonts/NanumSquareRoundB.ttf', # bold
    #     './fonts/NanumSquareRoundEB.ttf', # bold italic
    # ])

    # this is the only piece of code that actually matters when changing font:
    # don't know if italic, bold and bold italic is working as shown here
    # the Light version is too thin for my liking
    LabelBase.register(
        DEFAULT_FONT,
        # './fonts/NanumSquareRoundL.ttf',
        './fonts/NanumSquareRoundR.ttf', # italic
        './fonts/NanumSquareRoundB.ttf', # bold
        './fonts/NanumSquareRoundEB.ttf', # bold italic
    )

    # set locale value for use with datetime.strftime()
    locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')
    MainApp().run()
