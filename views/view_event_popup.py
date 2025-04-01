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
            text: 'Title'
                
        GridLayout:
            cols: 2
            size_hint_y: None
            Label:
                text: 'Start Time'
            Label:
                text: 'End Time'

        Label:
            text: 'Location'
    
        Label:
            text: 'Type'

        Button:
            text: 'Edit Event'
'''

Builder.load_string(KV)

class ViewEventPopup(Popup):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build()
    
    def build(self) -> None:
        pass