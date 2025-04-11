"""
MVP Version with Kivy
MainApp class
"""
from kivy.app import App

from cal_functions import CoreFunctions

# kivy doesn't require def __init__() - uses build() instead
class MainApp(App):
    def build(self) -> CoreFunctions:
        self.title = 'Calendar App'
        self.locale = 'en_US.UTF-8'
        return CoreFunctions(locale=self.locale)

if __name__ == '__main__':
    MainApp().run()
