"""
This file is used to create date/time selector UI in Kivy - only for MVP version
"""
import datetime

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
# from kivy.clock import Clock

from common_utils import LOCAL_CALENDAR, get_month

Builder.load_file('kivy_uis/selectors.kv')

class DateSelector(Popup):
    def __init__(self, current_day: datetime = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day = current_day or datetime.date.today()
        self.year: int = self.selected_day.year
        self.month: int = self.selected_day.month
        self.day: int = self.selected_day.day
        # Clock.schedule_once(self.build, 0)
        self.build()

    def build(self) -> None:
        self.ids.selector_calendar.clear_widgets()

        year = self.year
        month = self.month

        self.ids.selector_month.text = f"{LOCAL_CALENDAR.formatmonthname(
            theyear=year,
            themonth=month,
            width=0,
            withyear=True
        )}"

        for weekday in range(7):
            self.ids.selector_calendar.add_widget(Label(text=LOCAL_CALENDAR.formatweekday(day=weekday, width=2)))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.selector_calendar.add_widget(btn)
                else:
                    self.ids.selector_calendar.add_widget(Label(text=' '))

    def on_day_selected(self, selected_day: str) -> str:
        self.selected_day = selected_day

    def close_selector(self) -> None:
        self.ids.date_selector.height = 0

class TimeSelector(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self) -> None:
        for hour in range(12):
            btn_1 = Button(
                text=f'{hour}',
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.select_hour.add_widget(btn_1)
        for minute in range(0, 60):
            btn_2 = Button(
                text=f'{minute:02}',
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.select_minute.add_widget(btn_2)
