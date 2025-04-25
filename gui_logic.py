"""
This file contains all GUI logic for Kivy
"""
# pylint: disable=attribute-defined-outside-init
# pylint: disable=unused-argument
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

from common_utils import (
    LOCAL_CALENDAR, current_date, get_month,
    get_month_name, get_week_number, get_week_days
)

def switch_to(*args, screen=None, view=None) -> None:
    App.get_running_app().switch_screen(*args, screen=screen, view=view)

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
                new_screen = self.next()
                self.transition.direction = 'up'
            else:
                new_screen = self.previous()
                self.transition.direction = 'down'
            self.current = new_screen
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

        year: int = 2025 # placeholder
        self.ids.year_label.text = f'{year}'

        for month in range(1, 13):
            month_name = get_month_name(month)
            btn = Button(text=month_name)
            btn.bind(on_release=lambda instance, m=month: self.on_month_selected(m))
            self.ids.year_grid.add_widget(btn)

    def on_month_selected(self, month: int) -> None:
        """ Load MonthView """
        switch_to(month, screen='month_screen', view='month')

class MonthScreen(Screen):
    def on_pre_enter(self, *args) -> None:
        Clock.schedule_once(self.update_label, 0)

    def update_label(self, _dt) -> None:
        self.ids.month_grid.clear_widgets()

        year: int = current_date().year
        month: int = current_date().month

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

        year: int = 2025
        current_day = datetime.today()
        week: str = get_week_number(current_day=current_day)
        week_list: list = get_week_days(current_day=current_day)

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
