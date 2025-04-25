"""
This file contains all GUI logic for Kivy
"""
# pylint: disable=attribute-defined-outside-init
# pylint: disable=unused-argument
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

from common_utils import (
    LOCAL_CALENDAR, get_month,
    get_month_name, get_week_number, get_week_days
)

TODAY = datetime.today()

def get_selected_date(date_string: str | None = None) -> datetime:
    """ Take string value (YYYYMMDD) or none """
    date: datetime = App.get_running_app().get_date(date_string)
    return date

def switch_to(new_screen: str) -> None:
    App.get_running_app().switch_screen(new_screen)

class CalendarScreens(ScreenManager):
    """ Switches between different views - Up/Down (y axis) movement """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start_y = 0

    def on_touch_down(self, touch):
        self._touch_start_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dy = touch.y - self._touch_start_y
        if abs(dy) > 50:
            if dy > 0:
                direction = 'up'
            else:
                direction = 'down'
            self.transition.direction = direction
        return super().on_touch_up(touch)

class YearScreens(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start_x = 0

    def on_touch_down(self, touch):
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dx = touch.x - self._touch_start_x
        if abs(dx) > 50:
            if dx < 0:
                new_screen = self.next()
                self.transition.direction = 'left'
            else:
                new_screen = self.previous()
                self.transition.direction = 'right'
            self.current = new_screen
        return super().on_touch_up(touch)

class MonthScreens(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start_x = 0

    def on_touch_down(self, touch):
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dx = touch.x - self._touch_start_x
        if abs(dx) > 50:
            if dx < 0:
                new_screen = self.next()
                self.transition.direction = 'left'
            else:
                new_screen = self.previous()
                self.transition.direction = 'right'
            self.current = new_screen
        return super().on_touch_up(touch)

class WeekScreens(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start_x = 0

    def on_touch_down(self, touch):
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dx = touch.x - self._touch_start_x
        if abs(dx) > 50:
            if dx < 0:
                new_screen = self.next()
                self.transition.direction = 'left'
            else:
                new_screen = self.previous()
                self.transition.direction = 'right'
            self.current = new_screen
        return super().on_touch_up(touch)

class YearScreen(Screen):
    def on_pre_enter(self, *args) -> None:
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, _dt) -> None:
        self.ids.year_grid.clear_widgets()

        self.date: datetime = get_selected_date()
        year: int = self.date.year
        self.ids.year_label.text = f'{year}'

        for month in range(1, 13):
            month_name = get_month_name(month)
            btn = Button(text=month_name)
            btn.bind(on_release=lambda instance, m=month: self.on_month_selected(m))
            self.ids.year_grid.add_widget(btn)

    def on_month_selected(self, month: int) -> None:
        """ Load MonthView """
        date: str = f'{self.date.year}{month}{self.date.day}'
        get_selected_date(date)
        switch_to("month_screen")

class MonthScreen(Screen):
    def on_pre_enter(self, *args) -> None:
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, _dt) -> None:
        self.ids.month_grid.clear_widgets()

        date: datetime = get_selected_date()
        year: int = date.year
        month: int = date.month

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
        pass

class WeekScreen(Screen):
    def on_pre_enter(self, *args) -> None:
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, _dt) -> None:
        self.ids.week_days.clear_widgets()

        date: datetime = get_selected_date()
        year: int = date.year
        week: str = get_week_number(current_day=date)
        week_list: list = get_week_days(current_day=date)

        self.ids.week_label.text = f'{year}\nWeek {week}'

        for day in range(7):
            self.ids.week_days.add_widget(Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3)
            ))
        for date in week_list:
            self.ids.week_days.add_widget(Label(
                text=f'{date}', font_size=dp(13)
            ))

GUI = Builder.load_file('main.kv')
