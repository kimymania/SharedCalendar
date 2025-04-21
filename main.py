"""
MVP Version with Kivy
MainApp class
Written in Python 3.13.2
"""
from kivy.app import App

# from cal_functions import CoreFunctions
import gui_logic

class MainApp(App):
    def build(self):
        self.title = 'Calendar App'
        self.screen_manager = self.root.ids.calendar_screen_manager
        self.screen_manager.current = 'current_month_screen' # can't set first screen like this. why?
        return gui_logic
    
    def switch_screen(self, new_screen):
        self.screen_manager.current = new_screen

if __name__ == '__main__':
    MainApp().run()
