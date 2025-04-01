from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from utils.localizations import MONTHS_OF_YEAR, _

KV = '''
<YearView>:
    orientation: 'vertical'

    Label:
        id: label_year
        font_size: 24
        size_hint_y: 0.1
        text: ''  # filled in build_view()

    GridLayout:
        id: calendar_grid
        cols: 3
        rows: 4
        spacing: 5
        padding: 10
'''

Builder.load_string(KV)

class YearView(BoxLayout):
    def __init__(self, get_current_date, controller, on_month_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.get_current_date = get_current_date
        self.controller = controller
        self.on_month_selected = on_month_selected
        self.build_view()

    def build_view(self):
        self.ids.calendar_grid.clear_widgets()

        year, _, _ = self.get_current_date()
        self.ids.label_year.text = str(year)

        for index, month_name in enumerate(MONTHS_OF_YEAR, start=1):
            btn = Button(text=month_name)
            btn.bind(on_release=lambda instance, m=index: self.on_month_selected(m))
            self.ids.calendar_grid.add_widget(btn)

    def update_year(self, year):
        self.build_view()