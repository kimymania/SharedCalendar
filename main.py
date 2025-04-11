"""
MVP Version with Kivy
MainApp class
"""
from kivy.app import App

from cal_functions import MonthView

# kivy doesn't require def __init__() - uses build() instead
class MainApp(App):
    def build(self) -> MonthView:
        self.title = 'Calendar App'
        self.locale = 'en_US.UTF-8'
        return MonthView(locale=self.locale)

if __name__ == '__main__':
    MainApp().run()
