"""
This file is used to create date/time selector UI in Kivy - only for MVP version
"""
from datetime import datetime, date

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

from common_utils import LOCAL_CALENDAR, get_month

Builder.load_file('kivy_uis/selectors.kv')

class DateSelector(Popup):
    def __init__(self, current_day: datetime = None, return_date=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day = current_day or date.today()
        self.year: int = self.selected_day.year
        self.month: int = self.selected_day.month
        self.day: int = self.selected_day.day
        self.return_date = return_date

        self.bind(on_dismiss=self.close_popup)
        self.build()

    def build(self) -> None:
        self.ids.selector_calendar.clear_widgets()

        year: int = self.year
        month: int = self.month

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
                    btn = Button(
                        text=str(day.day)
                    )
                    btn.bind(on_release=self.on_day_selected)
                    self.ids.selector_calendar.add_widget(btn)
                else:
                    self.ids.selector_calendar.add_widget(Label(text=' '))

    def on_day_selected(self, instance) -> None:
        """ Highlight selected day, update self.selected day to this day """
        for child in self.ids.selector_calendar.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = [0.3, 0.6, 1, 1]  # highlight selected
        self.selected_day = date(
            year=self.year,
            month=self.month,
            day=int(instance.text)
        )

    def navigate_cal(self, direction: str) -> None:
        """ Logic to cycle through mini calendar """
        if direction == 'prev':
            if self.month == 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1
        elif direction == 'next':
            if self.month == 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1
        self.update_view(year=self.year, month=self.month)

    def update_view(self, year: int, month: int) -> None:
        self.build()

    def close_popup(self, instance) -> None:
        """ on_dismiss logic """
        self.return_day(self.selected_day)

    def return_day(self, selected_day) -> None:
        """ (Callback Function) Return selected day in 'datetime' to AddEventPopup """
        if self.return_date:
            self.return_date(selected_day)

class TimeSelector(Popup):
    def __init__(self, return_time=None, **kwargs):
        super().__init__(**kwargs)
        self.return_time = return_time
        self.meridiem_indicator: str = 'AM' # defaulted to 'AM'
        self.selected_hour: str = '12'
        self.selected_minute: str = '00'
        self.selected_time_string: str = f'{self.selected_hour}:{self.selected_minute} {self.meridiem_indicator}'
        self.selected_time = datetime.strptime(self.selected_time_string, '%I:%M %p')
        self.bind(on_dismiss=self.close_popup)
        self.build()

    def build(self) -> None:
        for hour in range(12):
            btn_hour = Button(
                text=f'{hour}',
                size_hint_y=None,
                height=dp(40)
            )
            btn_hour.bind(on_release=lambda instance, h=hour: self.select_hour(instance, h))
            self.ids.select_hour.add_widget(btn_hour)
        for minute in range(0, 60):
            btn_minute = Button(
                text=f'{minute:02}',
                size_hint_y=None,
                height=dp(40)
            )
            btn_minute.bind(on_release=lambda instance, m=minute: self.select_minute(instance, m))
            self.ids.select_minute.add_widget(btn_minute)

    def select_meridiem_indicator(self, instance, indicator: str) -> None:
        """ Highlight selected hour """
        for child in self.ids.select_meridiem.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = [0.3, 0.6, 1, 1]  # highlight selected
        self.meridiem_indicator = indicator

    def select_hour(self, instance, hour: int) -> None:
        """ Highlight selected hour """
        for child in self.ids.select_hour.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = [0.3, 0.6, 1, 1]  # highlight selected
        self.selected_hour = str(hour)

    def select_minute(self, instance, minute: int) -> None:
        """ Highlight selected minute """
        for child in self.ids.select_minute.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = [0.3, 0.6, 1, 1]  # highlight selected
        self.selected_minute = str(minute)

    def update_selected_time(self) -> None:
        """ Update the time string so that it's sendable - formatting it into 24-hr time """
        self.selected_time_string: str = f'{self.selected_hour}:{self.selected_minute} {self.meridiem_indicator}'
        self.selected_time = datetime.strptime(self.selected_time_string, '%I:%M %p').time()

    def close_popup(self, instance) -> None:
        """ on_dismiss logic """
        self.update_selected_time()
        self.return_selected_time(self.selected_time)

    def return_selected_time(self, selected_time: datetime) -> None:
        """ (Callback function) return selected time value to AddEventPopup """
        if self.return_time:
            self.return_time(selected_time)
