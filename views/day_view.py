from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from views.add_event_popup import AddEventPopup
from views.view_event_popup import ViewEventPopup

KV = '''
<DayView>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        BoxLayout:
            id: event_list
            orientation: 'vertical'
            size_hint_y: 1

        Button:
            text: 'Add Event'
            size_hint_y: None
            height: dp(40)
            on_release: root.open_add_event_popup(self)

        Button:
            text: 'X'
            size_hint_y: None
            height: dp(40)
            on_release: root.close_popup(self)
'''

Builder.load_string(KV)

class DayView(Popup):
    def __init__(self, selected_date, controller, **kwargs):
        super().__init__(**kwargs)
        self.title = selected_date.strftime('%Y-%m-%d')
        self.size_hint = (0.9, 0.9)
        self.selected_date = selected_date
        self.controller = controller
        self.build_view()

    def build_view(self):
        self.ids.event_list.clear_widgets()

        events = self.controller.get_events_by_date(self.selected_date)  # Updated method
        if events:
            for event in events:
                self.ids.event_list.add_widget(
                    Button(
                        text=f'{event.time_start.strftime("%H:%M")} - {event.title}'  # Fixed formatting
                    )
                )
        else:
            self.ids.event_list.add_widget(Label(text='No events'))

    def open_add_event_popup(self, _):
        popup = AddEventPopup(
            selected_date=self.selected_date,
            controller=self.controller,
            on_event_added=self.refresh
        )
        popup.open()

    def open_view_event_popup(self, _):
        popup = ViewEventPopup(
            controller=self.controller
        )
        popup.open()

    def refresh(self, _) -> None:
        self.build_view()

    def close_popup(self, _) -> None:
        self.dismiss()