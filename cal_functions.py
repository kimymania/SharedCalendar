"""
Core functions - calendar logic goes through here
Orientation isn't implemented yet
"""
from datetime import datetime, timedelta

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from common_utils import LOCAL_CALENDAR
from cal_views import MonthView, YearView, WeekView

def get_displayed_date(date_string: str) -> datetime:
    """ Universal date controller """
    current_day: datetime = None
    return current_day.strptime(date_string, '%Y%m%d')

class CoreFunctions(BoxLayout):
    def __init__(self, locale: str, **kwargs):
        super().__init__(**kwargs)
        LOCAL_CALENDAR.locale = locale
        today = datetime.today()
        self.current_date = today

        self.orientation = 'vertical'
        Window.size = (414, 896) # iPhone 13 resolution scaled down to half
        Window.bind(
            on_key_down=self.on_key_down,
            on_resize=self.on_window_resize
        )
        self._touch_start_x = 0
        self._touch_start_y = 0

        self.views = [
            YearView(year=self.current_date.year),
            MonthView(year=self.current_date.year, month=self.current_date.month),
            WeekView(current_day=self.current_date)
        ]
        self.view_index = 1 # initialize to MonthView
        self.add_widget(self.views[self.view_index])

    def on_window_resize(self, instance, width, height) -> None:
        """ Adjust layout depending on orientation """
        orientation = self.check_orientation()
        self.adjust_layout(orientation)

    def check_orientation(self) -> str:
        """ Get screen orientation and return result """
        if Window.width > Window.height:
            return 'landscape'
        else:
            return 'portrait'

    def adjust_layout(self, orientation) -> None:
        """ Actual changes applied """
        if orientation == 'landscape':
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'

    def on_key_down(self, window, key, scancode, codepoint, modifier) -> None:
        """
        Keyboard key press -
        left/right is inverted as the argument swipe_right was
        based on swiping movement when it was first made
        """
        if key == 273:  # Arrow Up
            return self.switch_view(go_down=True, view_number=self.view_index)
        elif key == 274:  # Arrow Down
            return self.switch_view(go_down=False, view_number=self.view_index)
        elif key == 276:  # Left arrow
            return self.navigate(swipe_right=True)
        elif key == 275:  # Right arrows
            return self.navigate(swipe_right=False)

    def on_touch_down(self, touch) -> bool | None:
        self._touch_start_y = touch.y
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch) -> bool | None:
        """
        Touch release - actions run here

        Swipe directions inverted to simulate natural swipe movement
        """
        dy = touch.y - self._touch_start_y
        dx = touch.x - self._touch_start_x
        if abs(dy) > 50:  # minimum swipe distance
            if dy < 0:
                self.switch_view(go_down=True, view_number=self.view_index)
            else:
                self.switch_view(go_down=False, view_number=self.view_index)
        if abs(dx) > 50:
            if dx > 0:
                self.navigate(swipe_right=True)
            else:
                self.navigate(swipe_right=False)
        return super().on_touch_up(touch)

    def navigate(self, swipe_right: bool) -> None:
        """
        Screen navigation

        Check view index -> Change current year/date/week accordingly
        """
        # Initialization, just in case
        year: int = self.current_date.year
        month: int = self.current_date.month

        if self.view_index == 0:
            if swipe_right is True:
                year = self.current_date.year - 1
            elif swipe_right is False:
                year = self.current_date.year + 1
            self.current_date = self.current_date.replace(year=year)

        elif self.view_index == 1:
            if swipe_right is True:
                if self.current_date.month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
            elif swipe_right is False:
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
            self.current_date = self.current_date.replace(year=year, month=month)

        elif self.view_index == 2:
            if swipe_right is True:
                self.current_date += timedelta(days=-7)
            elif swipe_right is False:
                self.current_date += timedelta(days=+7)
        self.update_calendar_gui()

    def update_calendar_gui(self, *args) -> None:
        """
        Update year/month/week display based on user input (left/right swipe or keyboard button press)

        Currently clears the entire widget and loads a new one

        You can give year & month arguments, though they default to self.current_date
        """
        year = args[0] if len(args) > 0 else self.current_date.year
        month = args[1] if len(args) > 1 else self.current_date.month

        self.clear_widgets()
        if self.view_index == 0:
            self.add_widget(YearView(year=year))
        elif self.view_index == 1:
            self.add_widget(MonthView(year=year, month=month))
        elif self.view_index == 2:
            self.add_widget(WeekView(current_day=self.current_date))

    def switch_view(self, go_down: bool, view_number: int) -> None:
        """
        Clear current view, load new view.

        if True -> go up / if False -> go down

        Booleans just feel much faster
        """
        index = view_number
        if go_down is True:
            if index == 0:
                index = 2
            else:
                index -= 1
        elif go_down is False:
            if index == 2:
                index = 0
            else:
                index += 1
        self.view_index = index
        self.update_calendar_gui()

    def switch_view_to_selected(self, *args) -> None:
        """
        Switch views on clicking an interactive ui element, e.g. clicking on a month in the YearView

        Can take 2 arguments (year) and (month) -
        which are defaulted to self.current_date if not explicitly given
        """
        year = args[0] if len(args) > 0 else self.current_date.year
        month = args[1] if len(args) > 1 else self.current_date.month
        self.current_date = self.current_date.replace(year=year, month=month)

        self.view_index = 1
        self.clear_widgets()
        self.add_widget(MonthView(year=year, month=self.current_date.month))
