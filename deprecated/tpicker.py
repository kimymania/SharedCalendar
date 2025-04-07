from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup  # Import Popup
from kivy.properties import StringProperty
from kivy.lang import Builder

KV = '''
<TimePicker>:
    
'''

Builder.load_string('''
<TimePicker>:
    orientation: "vertical"
    Label:
        id: display
        text: root.selected_time
        font_size: 32
        size_hint: (1, 0.2)
    BoxLayout:
        orientation: "horizontal"
        size_hint: (1, 0.8)
        ScrollView:
            id: hour_picker
        ScrollView:
            id: minute_picker
        ScrollView:
            id: period_picker
    Button:
        text: "Confirm"
        size_hint: (1, 0.2)
        on_release: root.confirm_time()
''')

class TimePicker(BoxLayout):
    selected_time = StringProperty("12:00 AM")

    def __init__(self, on_time_selected=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.hour = 12
        self.minute = 0
        self.period = "AM"
        self.on_time_selected = on_time_selected  # Callback for when time is selected

        # Populate pickers with 2-digit formatting and enable endless rotation
        self.populate_picker(self.ids.hour_picker, [f"{i:02}" for i in range(1, 13)], self.set_hour)
        self.populate_picker(self.ids.minute_picker, [f"{i:02}" for i in range(0, 60)], self.set_minute)

        # Enable endless rotation for hour_picker
        self.ids.hour_picker.scroll_type = ['content']
        self.ids.hour_picker.effect_cls = 'ScrollEffect'

        # Enable endless rotation for minute_picker
        self.ids.minute_picker.scroll_type = ['content']
        self.ids.minute_picker.effect_cls = 'ScrollEffect'

        # Populate period_picker as usual
        self.populate_picker(self.ids.period_picker, ["AM", "PM"], self.set_period)

    def populate_picker(self, scroll_view, values, callback, step=1):
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

        scroll_view.add_widget(grid)

    def set_hour(self, hour) -> None:
        self.hour = int(hour)
        self.update_time()

    def set_minute(self, minute) -> None:
        self.minute = int(minute)
        self.update_time()

    def set_period(self, period) -> None:
        self.period = period
        self.update_time()

    def update_time(self) -> None:
        self.selected_time = f"{self.hour:02}:{self.minute:02} {self.period}"
        self.ids.display.text = self.selected_time

    def confirm_time(self) -> None:
        if self.on_time_selected:
            self.on_time_selected(self.selected_time)