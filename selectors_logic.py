"""
This file is used to create date/time selector UI in Kivy - only for MVP version
"""
from datetime import datetime, date

from kivy.lang import Builder
# from kivy.clock import Clock
# from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

from common_utils import LOCAL_CALENDAR, COLOUR_RGBA_SELECTED, get_month, format_month_kor
from palette import text_colour

Builder.load_file('kivy_uis/selectors.kv')

class DateSelector(Popup):
    def __init__(self, current_day: datetime = None, return_date=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.calendar = LOCAL_CALENDAR
        self.selected_day = current_day or date.today()
        self.year: int = self.selected_day.year
        self.month: int = self.selected_day.month
        self.day: int = self.selected_day.day
        self.return_date = return_date

        self.bind(on_dismiss=self.close_popup)
        self.build()

    def build(self) -> None:
        self.ids.selector_calendar_headers.clear_widgets()
        self.ids.selector_calendar.clear_widgets()

        year: int = self.year
        month: int = self.month

        self.ids.selector_month.text = format_month_kor(year, month)

        for weekday in range(7):
            self.ids.selector_calendar_headers.add_widget(Label(
                text=self.calendar.formatweekday(day=(weekday + 6) % 7, width=2),
                color=text_colour
            ))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(
                        text=str(day.day),
                        color=text_colour,
                        background_normal=''
                    )
                    btn.bind(on_release=self.on_day_selected)
                    self.ids.selector_calendar.add_widget(btn)
                else:
                    self.ids.selector_calendar.add_widget(Label(text=' '))

    def on_day_selected(self, instance) -> None:
        """
        Highlight selected day, update self.selected day to this day

        If the day was previously selected, close popup
        """
        if self.selected_day.day == int(instance.text):
            self.return_day(selected_day=self.selected_day)
            self.dismiss()

        for child in self.ids.selector_calendar.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = COLOUR_RGBA_SELECTED  # highlight selected
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
    """
    Time selector - divided into Meridiem Indicator(AM/PM), Hour and Minute

    'time' receives string value of 'HH:MM'

    Returns datetime value to parent class after closing
    """
    def __init__(self, return_time=None, time='', **kwargs):
        super().__init__(**kwargs)
        self.return_time = return_time

        if time:
            base = datetime.strptime(time, '%H:%M')
            hour = base.strftime('%I')
            minute = base.strftime('%M')
            mer = base.strftime('%p')
        else:
            now = datetime.now()
            hour = now.strftime('%I')
            minute = now.strftime('%M')
            mer = now.strftime('%p')

        self.selected_hour: str = hour
        self.selected_minute: str = minute
        self.meridiem_indicator: str = mer

        self.selected_time_string: str = f'{hour}:{minute} {mer}'
        self.selected_time = datetime.strptime(self.selected_time_string, '%I:%M %p')
        # self.scroll_timeout = None
        # self.snap_to_nearest = None

        self.build()
        self.highlight_selected()

    def build(self) -> None:
        """ Build hour & minute grids. Meridian indicators are included in KV file """
        for hour in range(1, 13):
            btn_hour = Button(
                text=f'{hour}',
                color=text_colour,
                background_normal='',
                size_hint_y=None,
                height=dp(40)
            )
            btn_hour.bind(on_release=lambda instance, h=hour: self.select_hour(instance, h))
            self.ids.select_hour.add_widget(btn_hour)
        for minute in range(0, 60):
            btn_minute = Button(
                text=f'{minute:02}',
                color=text_colour,
                background_normal='',
                size_hint_y=None,
                height=dp(40)
            )
            btn_minute.bind(on_release=lambda instance, m=minute: self.select_minute(instance, m))
            self.ids.select_minute.add_widget(btn_minute)

    def highlight_selected(self) -> None:
        """ and highlight initial values """
        if self.meridiem_indicator == 'AM':
            self.ids.am_indicator.background_color = COLOUR_RGBA_SELECTED
            self.ids.pm_indicator.background_color = [1, 1, 1, 1]
        else:
            self.ids.am_indicator.background_color = [1, 1, 1, 1]
            self.ids.pm_indicator.background_color = COLOUR_RGBA_SELECTED

        for child in self.ids.select_hour.children:
            child.background_color = (child.text == self.selected_hour) and COLOUR_RGBA_SELECTED or [1,1,1,1]

        for child in self.ids.select_minute.children:
            child.background_color = (child.text == self.selected_minute) and COLOUR_RGBA_SELECTED or [1,1,1,1]

    def select_meridiem_indicator(self, instance, indicator: str) -> None:
        """ Highlight selected hour """
        self.ids.am_indicator.background_color = [1,1,1,1]
        self.ids.pm_indicator.background_color = [1,1,1,1]
        instance.background_color = COLOUR_RGBA_SELECTED  # highlight selected
        self.meridiem_indicator = indicator

    def select_hour(self, instance, hour: int) -> None:
        """ Highlight selected hour """
        for child in self.ids.select_hour.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = COLOUR_RGBA_SELECTED  # highlight selected
        self.selected_hour = str(hour)

    def select_minute(self, instance, minute: int) -> None:
        """ Highlight selected minute """
        for child in self.ids.select_minute.children:
            if isinstance(child, Button):
                child.background_color = [1, 1, 1, 1]  # reset others
        instance.background_color = COLOUR_RGBA_SELECTED  # highlight selected
        self.selected_minute = str(minute)

    def update_selected_time(self) -> str:
        """ Update the time string so that it's sendable - formatting it into 24-hr time """
        dt = datetime.strptime(f'{self.selected_hour}:{self.selected_minute} {self.meridiem_indicator}', '%I:%M %p')
        self.selected_time_string = dt.strftime('%I:%M %p')
        self.selected_time = dt
        return dt

    def close_and_save(self, instance) -> None:
        """
        Called when OK button is pressed - stores selected time and closes popup

        Use .dismiss() to close without saving
        """
        dt: datetime = self.update_selected_time()
        if self.return_time:
            self.return_time(dt)
        self.dismiss()

class ColourPicker(Popup):
    """ Colour Picker Popup """
    selected_colour = [1, 1, 1, 1]  # defaulted to white
    def __init__(self, return_colour=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.return_colour = return_colour
        self.selected_colour = [1, 1, 1, 1]
        self.bind(on_dismiss=self._on_dismiss)

    def select_colour(self, instance) -> None:
        """ Logic to set selected colour """
        self.selected_colour = instance
        self.ids.colour_text.clear_widgets()
        self.ids.colour_text.text = 'Selected Colour'
        self.ids.colour_text.color = self.selected_colour

    def _on_dismiss(self, instance) -> None:
        """ on_dismiss logic """
        if self.return_colour:
            self.return_colour(self.selected_colour)
