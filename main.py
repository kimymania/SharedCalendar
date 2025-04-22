"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.2
"""
from kivy.app import App

# from cal_functions import CoreFunctions
from gui_logic import GUI

class MainApp(App):
    def build(self):
        self.title = 'Calendar App'
        display = GUI
        self.screen_manager = display.ids.calendar_screen_manager
        self.month_screen_manager = display.ids.calendar_screen_manager.ids.month_screen_manager
        self.screen_manager.current = 'month_screen'
        self.month_screen_manager.current = 'current_month'
        return display

    # not implemented yet
    def switch_view(self, new_screen) -> None:
        self.screen_manager.current = new_screen

if __name__ == '__main__':
    MainApp().run()
