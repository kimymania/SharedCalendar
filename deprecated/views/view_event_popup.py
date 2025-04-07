from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.metrics import dp
from models import EventContainer
from datetime import datetime

KV = '''
<ViewEventPopup>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        Label:
            id: title_label
            text: 'Title'
                
        GridLayout:
            cols: 2
            size_hint_y: None
            Label:
                id: start_time_label
                text: 'Start Time'
            Label:
                id: end_time_label
                text: 'End Time'

        Label:
            id: location_label
            text: 'Location'
    
        Label:
            id: type_label
            text: 'Type'

        Button:
            text: 'Edit Event'
'''

Builder.load_string(KV)

class ViewEventPopup(Popup):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
    
    def build(self, event_id: int) -> None:
        event = self.controller.get_event_by_id(event_id)  # Add a method in EventController if needed
        if event:
            self.ids.title_label.text = event.title
            self.ids.start_time_label.text = event.time_start.strftime('%H:%M')
            self.ids.end_time_label.text = event.time_end.strftime('%H:%M') if event.time_end else 'N/A'
            self.ids.location_label.text = event.location
            self.ids.type_label.text = event.type