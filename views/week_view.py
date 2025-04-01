from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
import calendar
from utils.localizations import DAYS_OF_WEEK, _

KV = """
<WeekView>:
    orientation: "vertical"

    Label:
        id: label_month_year
        font_size: 24
        size_hint_y: 0.1
        text: ""

    Label:
        id: label_week
        font_size: 18
        size_hint_y: None
        height: 30
        text: ""

    GridLayout:
        id: calendar_grid
        cols: 8
        rows: 25
        spacing: 2
        size_hint_y: 1
"""

Builder.load_string(KV)

class WeekView(BoxLayout):
    def __init__(self, get_current_date, get_current_week, controller, on_day_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.get_current_date = get_current_date
        self.get_current_week = get_current_week
        self.controller = controller
        self.on_day_selected = on_day_selected
        self.build_view()

    def build_view(self):
        self.ids.calendar_grid.clear_widgets()

        this_week = self.get_current_week()
        year, month = self.get_current_date()
        self.ids.label_month_year.text = f"{calendar.month_name[month]} {year}"

        self.ids.calendar_grid.add_widget(Label(text=f"Week {this_week}"))
        # Add weekday labels
        for day in DAYS_OF_WEEK:
            self.ids.calendar_grid.add_widget(Label(text=day, bold=True))

        # Add time grid
        for hour in range(24):
            time_label = f"{hour:02}:00"
            self.ids.calendar_grid.add_widget(Label(text=time_label, size_hint_x=None, width=60))
            for _ in range(7):
                self.ids.calendar_grid.add_widget(Label(text=""))

    def update_week(self, year, month):
        self.build_view()