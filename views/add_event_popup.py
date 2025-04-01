from kivy.uix.popup import Popup
from kivy.lang import Builder
from models import EventContainer
from datetime import datetime
from tpicker import TimePicker

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
                on_release: root.toggle_time_picker('start')
            Button:
                text: 'End Time'
                id: time_end_input
                on_release: root.toggle_time_picker('end')

            Label:
                text: 'Location'
            TextInput:
                id: location_input
        
            Label:
                text: 'Type'
            TextInput:
                id: type_input

        BoxLayout:
            id: time_picker_container
            size_hint_y: None
            height: 0  # Initially hidden

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

        self.time_picker = None  # Keep track of the active TimePicker
        self.active_time_type = None  # Track whether it's 'start' or 'end'

    def toggle_time_picker(self, time_type):
        """
        Toggle the TimePicker UI below the button.
        :param time_type: 'start' or 'end' to indicate which time to update.
        """
        container = self.ids.time_picker_container

        # If the TimePicker is already active, remove it
        if self.time_picker:
            container.clear_widgets()
            container.height = 0
            self.time_picker = None
            self.active_time_type = None
            return

        # Create a new TimePicker
        def on_time_selected(selected_time):
            # Update the button text and store the selected time
            if time_type == 'start':
                self.ids.time_start_input.text = selected_time
            elif time_type == 'end':
                self.ids.time_end_input.text = selected_time

            # Remove the TimePicker after selection
            container.clear_widgets()
            container.height = 0
            self.time_picker = None
            self.active_time_type = None

        self.time_picker = TimePicker(on_time_selected=on_time_selected)
        container.add_widget(self.time_picker)
        container.height = 300  # Adjust height to fit the TimePicker
        self.active_time_type = time_type

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

        self.controller.add_event(event)  # Save directly to SQLite

        if self.on_event_added:
            self.on_event_added(event)

        self.dismiss()