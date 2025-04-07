"""
Calendar UI using Kivy
"""
import calendar
from datetime import datetime

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file('kivy_uis/views.kv')
Window.size = (360, 780)

class DayView(Popup):
    """
    Selected day view popup
    """
    selected_day = StringProperty('')
    def __init__(self, selected_date: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day = f'{selected_date.strftime('%Y / %m / %d %A')}'
        self.build_view()

    def build_view(self) -> None:
        ...

    def close_popup(self, instance) -> None:
        self.dismiss()

class CalendarUI(BoxLayout):
    """
    Main Calendar UI
    """
    def __init__(self, locale: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.calendar = calendar.LocaleTextCalendar(firstweekday=6, locale=locale)
        today = datetime.today()
        self.current_year: int = today.year
        self.current_month: int = today.month
        self.current_day: int = today.day
        self.current_date: tuple[int, int, int] = (self.current_year, self.current_month, self.current_day)
        self._touch_start_x: int = 0
        self._touch_start_y: int = 0
        self.build_view()

        Window.bind(
            on_key_down=self.on_key_down,
            on_resize=self.on_window_resize
        )
        self.touch_start_y = 0

    def build_view(self) -> None:
        self.ids.calendar_grid.clear_widgets()

        year = self.current_year
        month = self.current_month

        self.ids.month_label.text = f"{self.calendar.formatmonthname(
            theyear=year,
            themonth=month,
            width=0,
            withyear=True
            )}"

        for day in range(7):
            self.ids.calendar_grid.add_widget(Label(text=self.calendar.formatweekday(day, 3)))
        for week in self.get_month(year, month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.calendar_grid.add_widget(btn)
                else:
                    self.ids.calendar_grid.add_widget(Label(text=' '))

    def update_view(self, year: int, month: int) -> None:
        self.build_view()

    def on_day_selected(self, day: str) -> None:
        day_view = DayView(selected_date=day)
        day_view.open()

    # Touch/keyboard input handling
    def on_key_down(self, window, key, scancode, codepoint, modifier) -> None:
        if key == 273:  # Arrow Up
            ...
        elif key == 274:  # Arrow Down
            ...
        elif key == 276:  # Left arrow
            return self.navigate(direction='prev')
        elif key == 275:  # Right arrows
            return self.navigate(direction='next')

    def on_touch_down(self, touch) -> bool | None:
        self._touch_start_y = touch.y
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch) -> bool | None:
        dy = touch.y - self._touch_start_y
        dx = touch.x - self._touch_start_x
        if abs(dy) > 50:  # minimum swipe distance
            if dy > 0:
                ...
            else:
                ...
        if abs(dx) > 50:
            if dx > 0:
                self.navigate('prev')
            else:
                self.navigate('next')
        return super().on_touch_up(touch)

    def navigate(self, direction: str) -> None:
        """
        Screen navigation
        """
        if direction == 'prev':
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else:
                self.current_month -= 1
        elif direction == 'next':
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
        self.update_view(self.current_year, self.current_month)

    # screen orientation, window size check
    def check_orientation(self) -> str:
        if Window.width > Window.height:
            return 'landscape'
        else:
            return 'portrait'

    def on_window_resize(self, instance, width, height) -> None:
        orientation = self.check_orientation()
        self.adjust_layout(orientation)

    def adjust_layout(self, orientation) -> None:
        if orientation == 'landscape':
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'

    # ...datescalendar returns MonthList[WeekList[datetime.date]]
    def get_year(self, year: int) -> str:
        year_keys = self.calendar.yeardatescalendar(year)
        return year_keys

    def get_month(self, year: int, month: int) -> str:
        month_keys = self.calendar.monthdatescalendar(year, month)
        return month_keys

    def get_week(self, year: int, month: int, day: int) -> str:
        month_calendar = self.get_month(year, month)

        # Find the week containing the specified day
        for week in month_calendar:
            if day in week:
                return ' '.join(str(d) if d != 0 else ' ' for d in week)

        # Day not found in the month
        return "Invalid date"
