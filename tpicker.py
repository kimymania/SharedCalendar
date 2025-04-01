from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup  # Import Popup
from kivy.properties import StringProperty

class TimePicker(BoxLayout):
    selected_time = StringProperty("12:00 AM")

    def __init__(self, on_time_selected=None, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.hour = 12
        self.minute = 0
        self.period = "AM"
        self.on_time_selected = on_time_selected  # Callback for when time is selected

        self.display = Label(
            text=self.selected_time, font_size=32, size_hint=(1, 0.2)
        )
        self.add_widget(self.display)

        picker_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.8))
        self.add_widget(picker_layout)

        # Hour Picker
        self.hour_picker = self.create_picker(range(1, 13), self.set_hour)
        picker_layout.add_widget(self.hour_picker)

        # Minute Picker
        self.minute_picker = self.create_picker(range(0, 60), self.set_minute, step=5)
        picker_layout.add_widget(self.minute_picker)

        # Period Picker
        self.period_picker = self.create_picker(["AM", "PM"], self.set_period)
        picker_layout.add_widget(self.period_picker)

        # Confirm Button
        confirm_button = Button(
            text="Confirm", size_hint=(1, 0.2), on_release=self.confirm_time
        )
        self.add_widget(confirm_button)

    def create_picker(self, values, callback, step=1):
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter("height"))

        for value in values:
            btn = Button(
                text=str(value),
                size_hint_y=None,
                height=50,
                on_release=lambda btn: callback(btn.text),
            )
            grid.add_widget(btn)

        scroll.add_widget(grid)
        return scroll

    def set_hour(self, hour):
        self.hour = int(hour)
        self.update_time()

    def set_minute(self, minute):
        self.minute = int(minute)
        self.update_time()

    def set_period(self, period):
        self.period = period
        self.update_time()

    def update_time(self):
        self.selected_time = f"{self.hour:02}:{self.minute:02} {self.period}"
        self.display.text = self.selected_time

    def confirm_time(self, instance):
        if self.on_time_selected:
            self.on_time_selected(self.selected_time)