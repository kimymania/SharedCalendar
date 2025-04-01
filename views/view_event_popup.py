from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivy.metrics import dp
from models.events import EventContainer
from datetime import datetime

KV = '''
<ViewEventPopup>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10
'''

Builder.load_string(KV)

class EventView(Popup):
    def __init__(self, selected_date, controller, **kwargs):
        super().__init__(**kwargs)
        self.selected_date = selected_date
        self.controller = controller
        self.build()
    
    def build(self):
        pass