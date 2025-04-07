from kivy.app import App
from event_controller import EventController
from calendar_logic import CalendarUI

class MainApp(App):
    def build(self):
        # load events on startup
        self.event_controller = EventController()
        self.calendar_ui = CalendarUI(controller=self.event_controller)
        return self.calendar_ui

if __name__ == '__main__':
    MainApp().run()