from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
import calendar
from utils.localizations import DAYS_OF_WEEK, _
from datetime import datetime, timedelta

KV = '''
<WeekView>:
    orientation: 'vertical'

    Label:
        id: label_month_year
        font_size: 24
        size_hint_y: 0.1
        text: ''

    Label:
        id: label_week
        font_size: 18
        size_hint_y: None
        height: 30
        text: ''

    FloatLayout:
        id: main_container

        GridLayout:
            id: calendar_grid
            cols: 8
            rows: 25
            spacing: 1
            size_hint: (1, 1)
            pos_hint: {'x': 0, 'y': 0}

        FloatLayout:
            id: event_overlay
            size_hint: (1, 1)
            pos_hint: {'x': 0, 'y': 0}
'''

Builder.load_string(KV)

class WeekView(BoxLayout):
    def __init__(self, get_current_date, get_current_week, controller, on_day_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.get_current_date = get_current_date
        self.get_current_week = get_current_week
        self.controller = controller
        self.on_day_selected = on_day_selected
        self.current_date = get_current_date()
        self.build_view()

    def build_view(self) -> None:
        self.ids.calendar_grid.clear_widgets()
        self.ids.event_overlay.clear_widgets()

        this_week = self.get_current_week()
        year, month, _ = self.get_current_date()
        today = datetime(*self.current_date)
        start_on_sunday = (today.weekday() + 1 ) % 7 # shift start of week Monday -> Sunday
        start_of_week = today - timedelta(days=start_on_sunday)

        # Display current year & headers
        self.ids.label_month_year.text = f'{calendar.month_name[month]} {year}'
        self.ids.calendar_grid.add_widget(Label(text=f'Week {this_week}'))
        for day in DAYS_OF_WEEK:
            self.ids.calendar_grid.add_widget(Label(text=day, bold=True))

        # Build empty 24-hour x 7-day grid
        for hour in range(24):
            self.ids.calendar_grid.add_widget(Label(text=f'{hour:02}:00'))
            for _ in range(7):
                self.ids.calendar_grid.add_widget(Label())  # background cells

        # Populate event blocks per day
        for i in range(7):
            current_day = (start_of_week + timedelta(days=i)).date()
            events = self.controller.get_events_by_date(current_day)  # Updated method
            for event in events:
                self.add_event_block(event)
        
    def add_event_block(self, event) -> None:
        dt = datetime.strptime(f'{event.date} {event.time}', '%Y-%m-%d %H:%M:%S')
        weekday_index = (dt.weekday() + 1) % 7
        hour = dt.hour
        minute = dt.minute

        # Assuming grid is full width/height, calculate positions
        grid_width = self.ids.calendar_grid.width
        grid_height = self.ids.calendar_grid.height

        col_width = grid_width / 8  # 1 for hour labels + 7 days
        row_height = grid_height / 25  # 1 row for weekday labels + 24 hours

        x = col_width * (weekday_index + 1)
        y = row_height * (24 - hour - (minute / 60))

        event_label = Label(
            text=event.title,
            size_hint=(None, None),
            size=(col_width, row_height),
            pos=(x, y),
            color=(1, 1, 1, 1)
        )
        self.ids.event_overlay.add_widget(event_label)

    def update_week(self, year, month) -> None:
        self.build_view()