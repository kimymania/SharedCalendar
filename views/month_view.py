from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import calendar
from kivy.uix.button import Button
from kivy.uix.label import Label
from utils.localizations import DAYS_OF_WEEK, _

KV = '''
<MonthView>:
    orientation: 'vertical'
    
    Label:
        id: label_month_year
        font_size: 24
        size_hint_y: 0.1
        text: ''  # dynamically filled from Python

    GridLayout:
        id: calendar_grid
        cols: 7
'''

Builder.load_string(KV)

class MonthView(BoxLayout):
    def __init__(self, get_current_date, controller, on_day_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.get_current_date = get_current_date
        self.controller = controller
        self.on_day_selected = on_day_selected
        self.build_view()

    def build_view(self) -> None:
        self.ids.calendar_grid.clear_widgets()

        year, month, _ = self.get_current_date()

        self.ids.label_month_year.text = f'{calendar.month_name[month]} {year}'

        # Add weekday labels
        for day in DAYS_OF_WEEK:
            self.ids.calendar_grid.add_widget(Label(text=day))

        # Add day buttons
        month_days = calendar.monthcalendar(year, month)
        for week in month_days:
            for day in week:
                if day == 0:
                    self.ids.calendar_grid.add_widget(Label(text=''))
                else:
                    day_btn = Button(text=str(day))
                    day_btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.calendar_grid.add_widget(day_btn)

    def load_events_for_date(self, selected_date):
        """
        Example method to load events for a specific date and update the UI.
        """
        events = self.event_controller.get_events_by_date(selected_date)
        # Now update your UI with the retrieved events
        print("Loaded events:", events)

    def update_month(self, year, month) -> None:
        self.build_view()