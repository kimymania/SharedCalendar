import calendar
from calendar import monthrange
from datetime import date, timedelta
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from views.year_view import YearView
from views.month_view import MonthView
from views.week_view import WeekView
from views.day_view import DayView

calendar.setfirstweekday(calendar.SUNDAY)

class CalendarUI(BoxLayout):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.event_controller = controller

        today = date.today() # used to return to today's date
        current_day = today # initialize to Today's date first - update through navigation

        self.today_year = today.year
        self.today_month = today.month
        self.today_day = today.day

        self.current_year = current_day.year
        self.current_month = current_day.month
        self.current_day = current_day.day

        self.current_week = date(self.current_year, self.current_month, self.current_day).isocalendar().week

        # view list (currently 3)
        self.views = [
            YearView(
                get_current_date=self.get_current_date,
                controller=self.event_controller,
                on_month_selected=self.handle_month_selected
                ),
            MonthView(
                get_current_date=self.get_current_date,
                controller=self.event_controller,
                on_day_selected=self.handle_day_selected
                ),
            WeekView(
                get_current_date=self.get_current_date,
                get_current_week=self.get_current_week,
                controller=self.event_controller,
                on_day_selected=self.handle_day_selected
                )
            ]
        self.current_view_index = 1 # initial page = MonthView
        self.add_widget(self.views[self.current_view_index])

        # key/touch bind
        Window.bind(on_key_down=self.on_key_down)
        self.touch_start_y = 0

        # orientation bind
        Window.bind(on_resize=self.on_window_resize)
    
    # screen orientation check
    def check_orientation(self) -> str:
        if Window.width > Window.height:
            return 'landscape'
        else:
            return 'portrait'

    def on_window_resize(self, instance, width, height) -> None:
        orientation = self.check_orientation()
        # print(f'[DEBUG] Orientation changed: {orientation}')
        self.adjust_layout(orientation)
    
    def adjust_layout(self, orientation) -> None:
        if orientation == 'landscape':
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'
    # orientation check ends here

    # update current year & month
    def get_current_date(self) -> {int, int, int}:
        return self.current_year, self.current_month, self.current_day
    
    # update current week
    def get_current_week(self) -> int:
        return self.current_week

    # key binds
    def on_key_down(self, window, key, scancode, codepoint, modifier) -> None:
        if key == 273:  # Arrow Up
            self.switch_view('up')
        elif key == 274:  # Arrow Down
            self.switch_view('down')
        elif key == 276:  # Left arrow
            self.navigate('prev')
        elif key == 275:  # Right arrow
            self.navigate('next')

    # touch binds: touch down -> touch up (release)
    def on_touch_down(self, touch):
        self._touch_start_y = touch.y
        self._touch_start_x = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dy = touch.y - self._touch_start_y
        dx = touch.x - self._touch_start_x
        if abs(dy) > 50:  # minimum swipe distance
            if dy > 0:
                self.switch_view('down') # swapped down and up to imitate realistic swipe movement
            else:
                self.switch_view('up')
        if abs(dx) > 50:
            if dx > 0:
                self.navigate('prev')
            else:
                self.navigate('next')
        return super().on_touch_up(touch)

    # vertical swipe: YearView <-> MonthView <-> WeekView <-> YearView ...
    def switch_view(self, direction) -> None:
        self.remove_widget(self.views[self.current_view_index])
        if direction == 'up':
            self.current_view_index = (self.current_view_index - 1) % len(self.views)
        elif direction == 'down':
            self.current_view_index = (self.current_view_index + 1) % len(self.views)
        
        # update views to current date
        new_view = self.views[self.current_view_index]
        if isinstance(new_view, YearView):
            new_view.update_year(self.current_year)
        elif isinstance(new_view, MonthView):
            new_view.update_month(self.current_year, self.current_month)
        # Update WeekView to any week in month (depending on current day)
        elif isinstance(new_view, WeekView):
            try:
                safe_day = min(self.current_day, monthrange(self.current_year, self.current_month)[1])
                current_date = date(self.current_year, self.current_month, safe_day)
            except ValueError:
                current_date = date.today()  # fallback just in case

            self.current_week = current_date.isocalendar().week
            self.current_day = current_date.day  # sync in case it was clamped

            new_view.update_week(self.current_year, self.current_month)

        # Update WeekView to first week of current month, anchored to first day of month
        # elif isinstance(new_view, WeekView):
        #     first_day = date(self.current_year, self.current_month, 1)
        #     self.current_day = 1  # Sync day
        #     self.current_week = first_day.isocalendar().week
        #     new_view.update_week(self.current_year, self.current_month)

        self.add_widget(self.views[self.current_view_index])

    # horizontal swipe: YearView
    def change_year(self, direction) -> None:
        if direction == 'next':
            self.current_year += 1
        elif direction == 'prev':
            self.current_year -= 1
        current_view = self.views[self.current_view_index]
        if isinstance(current_view, YearView):
            current_view.update_year(self.current_year)

    # horizontal swipe: MonthView
    def change_month(self, direction) -> None:
        if direction == 'next':
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
        elif direction == 'prev':
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else:
                self.current_month -= 1
        current_view = self.views[self.current_view_index]
        if isinstance(current_view, MonthView):
            current_view.update_month(self.current_year, self.current_month)
    
    # horizontal swipe: WeekView
    def change_week(self, direction) -> None:
        max_day = monthrange(self.current_year, self.current_month)[1]
        safe_day = min(self.current_day, max_day)

        current_date = date(self.current_year, self.current_month, safe_day)
        if direction == 'next':
            new_date = current_date + timedelta(days=7)
        elif direction == 'prev':
            new_date = current_date - timedelta(days=7)
        
        self.current_year = new_date.year
        self.current_month = new_date.month
        self.current_day = new_date.day
        self.current_week = new_date.isocalendar().week

        current_view = self.views[self.current_view_index]
        if isinstance(current_view, WeekView):
            current_view.update_week(self.current_year, self.current_month)

    # combined navigator function
    def navigate(self, direction) -> None:
        current_view = self.views[self.current_view_index]
        if isinstance(current_view, YearView):
            self.change_year(direction)
        elif isinstance(current_view, MonthView):
            self.change_month(direction)
        elif isinstance(current_view, WeekView):
            self.change_week(direction)

    # open MonthView window from YearView
    def handle_month_selected(self, month) -> None:
        self.remove_widget(self.views[self.current_view_index])
        self.current_month = month # update month value to value returned from button click
        new_month_view = MonthView(
            get_current_date=self.get_current_date,
            controller=self.event_controller,
            on_day_selected=self.handle_day_selected
            )
        self.views[1] = new_month_view
        self.current_view_index = 1
        self.add_widget(new_month_view)

    # open DayView popup from MonthView
    def handle_day_selected(self, day) -> None:
        selected_date = date(self.current_year, self.current_month, day)
        popup = DayView(
            selected_date,
            controller=self.event_controller
            )
        popup.open()