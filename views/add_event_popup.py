from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.uix.pickers import MDTimePickerDialVertical
from kivy.metrics import dp
from models import EventContainer
from datetime import datetime

KV = '''
<AddEventPopup>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        GridLayout:
            cols: 2
            rows: 4
            Label:
                text: 'Title'
            TextInput:
                id: title_input

            Button:
                text: 'Start Time'
                id: time_start_input
                on_release: root.show_time_picker
            Button:
                text: 'End Time'
                id: time_end_input
                on_release: root.show_time_picker

            Label:
                text: 'Location'
            TextInput:
                id: location_input
        
            Label:
                text: 'Type'
            TextInput:
                id: type_input

        Button:
            text: 'Add Event'
            on_release: root.add_event()
'''

Builder.load_string(KV)

class AddEventPopup(Popup):
    def __init__(self, selected_date, controller, on_event_added=None, **kwargs):
        super().__init__(**kwargs)
        self.selected_date = selected_date
        self.controller = controller
        self.on_event_added = on_event_added
        self.title = f'Add Event on {selected_date}'
        self.size_hint = (0.8, 0.6)

        self.selected_hour_start = '11'
        self.selected_minute_start = '00'
        self.selected_hour_end = '12'
        self.selected_minute_end = '00'
        self.selected_am_pm = 'am'

    def add_event(self) -> None:
        hour = int(self.selected_hour)
        if self.selected_am_pm == 'pm' and hour < 12:
            hour += 12
        elif self.selected_am_pm == 'am' and hour == 12:
            hour = 0
        self.selected_hour_start = str(hour)
        self.selected_hour_end = str(hour)
        selected_time_start = f'{self.selected_hour_start}:{self.selected_minute_start}'
        selected_time_end = f'{self.selected_hour_end}:{self.selected_minute_end}'

        event = EventContainer(
            title=self.ids.title_input.text.strip(),
            date=self.selected_date,
            time_start=datetime.strptime(selected_time_start, '%H:%M').time(),
            time_end=datetime.strptime(selected_time_end, '%H:%M').time(),
            type=self.ids.type_input.text.strip(),
            location=self.ids.location_input.text.strip()
        )

        self.controller.add_event(event)
        self.controller.save_to_file()

        if self.on_event_added:
            self.on_event_added(event)

        self.dismiss()

    # Time picker needs construction
    def show_time_picker(self, *args) -> None:
        pass