"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.2
"""
# pylint: disable=attribute-defined-outside-init
from datetime import datetime

from kivy.app import App

from common_utils import current_date
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
        self.month_screen_manager.current = 'current_month'
        return display

    def get_date(self, date_string: str = None) -> datetime:
        """ Get date in string format (YYYYMMDD) -> return datetime format """
        self.displayed_date = datetime.strptime(date_string=date_string, format='%Y%m%d')
        return self.displayed_date

    def switch_screen(self, *args, screen: str = None, view: str = None) -> None:
        """
        Switch screens

        [optional] Month value (int)

        'screen' = year/month/week screen

        'view' = next/previous year/month/week
        """
        if len(args) > 0:
            month: int = args[0]
            current_date(month=month)

        if screen:
            self.screen_manager.current = screen

        if view:
            if screen == 'year_screen':
                self.year_screen_manager.current = view
            elif screen == 'month_screen':
                self.month_screen_manager.current = view
            elif screen == 'week_screen':
                self.week_screen_manager.current = view

if __name__ == '__main__':
    MainApp().run()
