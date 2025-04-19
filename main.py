"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.2
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# from cal_functions import CoreFunctions

class CalendarScreens(ScreenManager):
    pass

class YearScreen(Screen):
    pass

class MonthScreen(Screen):
    pass

class WeekScreen(Screen):
    pass

GUI = Builder.load_file('main.kv')

class MainApp(App):
    def build(self):
        self.title = 'Calendar App'
        screen_manager = self.root.ids.calendar_screen_manager
        screen_manager.current = 'month_screen' # can't set first screen like this. why?
        return GUI

if __name__ == '__main__':
    MainApp().run()
