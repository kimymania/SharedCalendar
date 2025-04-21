"""
This file contains all GUI logic for Kivy
"""
from datetime import datetime

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

from common_utils import LOCAL_CALENDAR, get_month

TODAY = datetime.today()

class CalendarScreens(ScreenManager):
    pass

class YearScreen(Screen):
    pass

class CurrentMonthScreen(Screen):
    """ Populate MonthView """
    def on_enter(self, *args) -> None:
        """ Delay load until widget tree is complete """
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, dt) -> None:
        self.ids.month_grid.clear_widgets()

        # placeholder values
        year: int = 2025
        month: int = 4

        self.ids.month_label.text = f"{LOCAL_CALENDAR.formatmonthname(
            theyear=year,
            themonth=month,
            width=0,
            withyear=True
        )}"

        for day in range(7):
            self.ids.month_grid.add_widget(Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                size_hint_y=0.15
            ))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.month_grid.add_widget(btn)
                else:
                    self.ids.month_grid.add_widget(Label(text=' '))
    
    def on_day_selected(self, day) -> None:
        """ Load DayView popup """
        print('dayview load')
        # day_view = DayView(selected_day=day)
        # day_view.open()

class PrevMonthScreen(Screen):
    """ Populate MonthView """
    def on_enter(self, *args) -> None:
        """ Delay load until widget tree is complete """
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, dt) -> None:
        self.ids.prev_month_grid.clear_widgets()

        # placeholder values
        year: int = 2025
        month: int = 4

        self.ids.prev_month_label.text = 'PreviousMonthView'

        for day in range(7):
            self.ids.prev_month_grid.add_widget(Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                size_hint_y=0.15
            ))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.prev_month_grid.add_widget(btn)
                else:
                    self.ids.prev_month_grid.add_widget(Label(text=' '))
    
    def on_day_selected(self, day) -> None:
        """ Load DayView popup """
        print('dayview load')
        # day_view = DayView(selected_day=day)
        # day_view.open()

class NextMonthScreen(Screen):
    """ Populate MonthView """
    def on_enter(self, *args) -> None:
        """ Delay load until widget tree is complete """
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, dt) -> None:
        self.ids.next_month_grid.clear_widgets()

        # placeholder values
        year: int = 2025
        month: int = 4

        self.ids.next_month_label.text = 'PreviousMonthView'

        for day in range(7):
            self.ids.next_month_grid.add_widget(Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                size_hint_y=0.15
            ))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.next_month_grid.add_widget(btn)
                else:
                    self.ids.next_month_grid.add_widget(Label(text=' '))
    
    def on_day_selected(self, day) -> None:
        """ Load DayView popup """
        print('dayview load')
        # day_view = DayView(selected_day=day)
        # day_view.open()

class WeekScreen(Screen):
    pass

Builder.load_file('main.kv')