"""
Calendar UI using Kivy
"""
from datetime import datetime

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.lang import Builder

from database import Database
from cal_selectors import DateSelector, TimeSelector
from common_utils import LOCAL_CALENDAR, get_month

Builder.load_file('kivy_uis/views.kv')
Window.size = (360, 780)

class AddEventPopup(Popup):
    """ Popup for adding events """
    selected_date_start = StringProperty('')
    selected_date_end = StringProperty('')
    selected_time = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_date: datetime = selected_day
        self.selected_date_start = str(selected_day)
        self.selected_date_end = str(selected_day)
        hour: str = '12'
        minute: str = '00'
        self.selected_time: str = f'{hour}:{minute}'
        self.build_view()

    def build_view(self) -> None:
        pass

    def toggle_date_selector(self, instance, target: str) -> None:
        """ Toggle date selector for start/end date """
        #
        # TRIED AND FAILED TO MAKE DROPDOWN STYLE CALENDAR
        #
        # widget = self.ids.date_selector
        # if widget.disabled:
        #     widget.size = 350, 600
        #     widget.opacity = 1
        #     widget.disabled = False
        # else:
        #     widget.size = 0, 0
        #     widget.opacity = 0
        #     widget.disabled = True

        if target == 'start':
            date_selector = DateSelector(current_day=self.selected_date)
            date_selector.open()
        elif target == 'end':
            date_selector = DateSelector(current_day=self.selected_date)
            date_selector.open()
        else:
            return

    def toggle_time_selector(self, instance, target: str) -> None:
        """ Open time selector for start/end time """
        if target == 'start':
            time_selector = TimeSelector()
            time_selector.open()
        elif target == 'end':
            time_selector = TimeSelector()
            time_selector.open()
        else:
            return

    def save_event(self, instance) -> None:
        """ Save to JSON DB """
        Database().add_event(

        )

class DayView(Popup):
    """ Selected day view popup """
    selected_day_text = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day: datetime = selected_day
        self.selected_day_text: str = f'{selected_day.strftime('%Y / %m / %d %A')}'
        self.build_view()

    def build_view(self) -> None:
        pass

    def add_event(self, instance) -> None:
        """ Load AddEvent popup """
        add_event = AddEventPopup(selected_day=self.selected_day)
        add_event.open()

    def close_popup(self, instance) -> None:
        """ Close DayView """
        self.dismiss()

class CalendarUI(BoxLayout):
    """ Main Calendar UI """
    def __init__(self, locale: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        LOCAL_CALENDAR.locale = locale
        today = datetime.today()
        self.current_year: int = today.year
        self.current_month: int = today.month
        self.current_day: int = today.day
        self.current_date: tuple[int, int, int] = (
            self.current_year,
            self.current_month,
            self.current_day
        )
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

        self.ids.month_label.text = f"{LOCAL_CALENDAR.formatmonthname(
            theyear=year,
            themonth=month,
            width=0,
            withyear=True
        )}"

        for day in range(7):
            self.ids.calendar_grid.add_widget(Label(text=LOCAL_CALENDAR.formatweekday(day=day, width=3)))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.calendar_grid.add_widget(btn)
                else:
                    self.ids.calendar_grid.add_widget(Label(text=' '))

    def update_view(self, year: int, month: int) -> None:
        """ Refresh screen """
        self.build_view()

    def on_day_selected(self, day: str) -> None:
        """ Load DayView popup """
        day_view = DayView(selected_day=day)
        day_view.open()

    def on_key_down(self, window, key, scancode, codepoint, modifier) -> None:
        """ Keyboard key press """
        if key == 273:  # Arrow Up
            ...
        elif key == 274:  # Arrow Down
            ...
        elif key == 276:  # Left arrow
            return self.navigate(direction='prev')
        elif key == 275:  # Right arrows
            return self.navigate(direction='next')

    def on_touch_down(self, touch) -> bool | None:
        """ Touch down """
        self._touch_start_y = touch.y
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch) -> bool | None:
        """ Touch release - actions run here """
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
        """ Screen navigation """
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
        """ Get screen orientation """
        if Window.width > Window.height:
            return 'landscape'
        else:
            return 'portrait'

    def on_window_resize(self, instance, width, height) -> None:
        """ Adjust layout depending on orientation """
        orientation = self.check_orientation()
        self.adjust_layout(orientation)

    def adjust_layout(self, orientation) -> None:
        if orientation == 'landscape':
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'