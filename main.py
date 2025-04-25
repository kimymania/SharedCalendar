"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.2
"""
# pylint: disable=attribute-defined-outside-init
from datetime import datetime

from kivy.app import App

from gui_logic import GUI

class MainApp(App):
    def build(self):
        self.title = 'Calendar App'
        display = GUI
        self.displayed_date = datetime.today()
        self.screen_manager = display.ids.calendar_screen_manager
        self.year_screen_manager = display.ids.calendar_screen_manager.ids.year_screen_manager
        self.month_screen_manager = display.ids.calendar_screen_manager.ids.month_screen_manager
        self.week_screen_manager = display.ids.calendar_screen_manager.ids.week_screen_manager
        self.screen_manager.current = 'month_screen'
        return display

    def get_date(self, date_string: str = None) -> datetime:
        """ String (YYYYMMDD) -> return datetime format """
        if date_string:
            self.displayed_date = datetime.strptime(date_string, '%Y%m%d')
        print(self.displayed_date)
        return self.displayed_date

    def switch_screen(self, new_screen: str) -> None:
        self.screen_manager.current = new_screen
        if new_screen == 'year_screen':
            self.year_screen_manager.current = 'year'
        elif new_screen == 'month_screen':
            self.month_screen_manager.current = 'month'
        else:
            self.week_screen_manager.current = 'week'

if __name__ == '__main__':
    MainApp().run()
