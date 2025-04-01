from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.pickers import MDDockedDatePicker, MDTimePickerDialVertical
from kivy.metrics import dp
from models.events import EventContainer
from datetime import datetime

KV = '''
<AddEventPopup>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        MDTextField:
            id: title_input
            mode: 'outlined'
            MDTextFieldHintText:
                text: 'Title'

        MDButton:
            id: time_input
            style: 'outlined'
            on_release: root.show_time_picker()
            MDButtonText:
                text: 'Select time'

        MDTextField:
            id: location_input
            mode: 'outlined'
            MDTextFieldHintText:
                text: 'Location'

        MDTextField:
            id: type_input
            mode: 'outlined'
            MDTextFieldHintText:
                text: 'Type'

        MDButton:
            style: 'outlined'
            on_release: root.add_event()
            MDButtonText:
                text: 'Add Event'
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

        self.selected_hour = '12'
        self.selected_minute = '00'
        self.selected_am_pm = 'am'

    def add_event(self):
        hour = int(self.selected_hour)
        if self.selected_am_pm == 'pm' and hour < 12:
            hour += 12
        elif self.selected_am_pm == 'am' and hour == 12:
            hour = 0
        self.selected_hour = str(hour)
        selected_time = f'{self.selected_hour}:{self.selected_minute}'

        event = EventContainer(
            title=self.ids.title_input.text.strip(),
            date=self.selected_date, # considering implementing date picker
            time=datetime.strptime(selected_time, '%H:%M').time(),
            type=self.ids.type_input.text.strip(),
            location=self.ids.location_input.text.strip()
        )

        self.controller.add_event(event)
        self.controller.save_to_file()

        if self.on_event_added:
            self.on_event_added(event)

        self.dismiss()

    # DatePicker - not implemented yet
    # def show_date_picker(self, focus):
    #     if not focus:
    #         return
        
    #     date_dialog = MDDockedDatePicker()
    #     date_dialog.pos = [
    #         self.root.ids.field.center_x - date_dialog.width / 2,
    #         self.root.ids.field.y - (date_dialog.height + dp(32)),
    #     ]
    #     date_dialog.open()

    def show_time_picker(self, *args):
        time_picker = MDTimePickerDialVertical(hour=self.selected_hour, minute=self.selected_minute)
        time_picker.bind(on_cancel=self.time_picker_cancel)
        time_picker.bind(on_ok=self.time_picker_ok)
        time_picker.bind(on_am_pm=self.time_picker_am_pm)
        time_picker.open()

    def time_picker_cancel(self, time_picker):
        time_picker.dismiss()
    
    def time_picker_ok(self, time_picker):
        self.selected_hour = time_picker.hour
        self.selected_minute = time_picker.minute
        time_picker.dismiss()
    
    def time_picker_am_pm(self, time_picker, am_pm_value):
        self.selected_am_pm = am_pm_value