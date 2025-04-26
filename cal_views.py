"""
Calendar UI using Kivy
"""
from datetime import datetime

from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.graphics import Line, Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp

from selectors_logic import DateSelector, TimeSelector, ColourPicker

from database import Database
from common_utils import (
    LOCAL_CALENDAR, get_month, get_month_name, get_week_number, get_week_days
)
import palette

class AddEventPopup(Popup):
    selected_date_start = StringProperty('')
    selected_date_end = StringProperty('')
    selected_time_start = StringProperty('')
    selected_time_end = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_date: datetime = selected_day
        self.selected_date_start = selected_day.strftime('%y/%m/%d')
        self.selected_date_end = selected_day.strftime('%y/%m/%d')
        hour: str = '12'
        minute: str = '00'
        self.selected_time_start: str = f'{hour}:{minute}'
        self.selected_time_end: str = f'{hour}:{minute}'
        self.group_tag_name: str = 'None'
        self.group_tag_colour: list = [1, 1, 1, 1]  # white by default
        self.repeat: bool = False
        self.notification: bool = False
        self.important: bool = False

    def toggle_date_selector(self, instance, target: str) -> None:
        """ Toggle date selector for start/end date """
        if target == 'start':
            date_selector = DateSelector(
                current_day=self.selected_date,
                return_date=self.receive_selected_date_start
            )
            date_selector.open()
        elif target == 'end':
            date_selector = DateSelector(
                current_day=self.selected_date,
                return_date=self.receive_selected_date_end
            )
            date_selector.open()
        else:
            return

    def receive_selected_date_start(self, date: datetime):
        """ Store start date """
        self.selected_date_start = date.strftime('%y/%m/%d')

    def receive_selected_date_end(self, date: datetime):
        """ Store end date """
        self.selected_date_end = date.strftime('%y/%m/%d')

    def toggle_time_selector(self, instance, target: str) -> None:
        """ Open time selector for start/end time """
        if target == 'start':
            time_selector = TimeSelector(
                return_time=self.receive_selected_time_start,
                time=self.selected_time_start
            )
            time_selector.open()
        elif target == 'end':
            time_selector = TimeSelector(
                return_time=self.receive_selected_time_end,
                time=self.selected_time_end
            )
            time_selector.open()
        else:
            return

    def receive_selected_time_start(self, time: datetime) -> None:
        """ Store start time """
        self.selected_time_start = time.strftime('%H:%M')

    def receive_selected_time_end(self, time: datetime) -> None:
        """ Store end time """
        self.selected_time_end = time.strftime('%H:%M')

    def open_colour_picker(self, instance) -> None:
        """ Open colour picker """
        picker = ColourPicker(return_colour=self.update_group_tag_colour)
        picker.open()

    def update_group_tag_colour(self, instance) -> None:
        """ Update group tag colour """
        if self.group_tag_colour:
            self.group_tag_colour = instance

    def toggle_repeat(self, instance) -> None:
        """ Toggle repeat checkbox """
        if not self.ids.event_repeat_checkbox.active:
            self.repeat = False
        elif self.ids.event_repeat_checkbox.active:
            self.repeat = True

    def toggle_notification(self, instance) -> None:
        """ Toggle notification checkbox """
        if not self.ids.event_notification_checkbox.active:
            self.notification = False
        elif self.ids.event_notification_checkbox.active:
            self.notification = True

    def toggle_important(self, instance) -> None:
        """ Toggle important checkbox """
        if not self.ids.event_important_checkbox.active:
            self.important = False
        elif self.ids.event_important_checkbox.active:
            self.important = True

    def save_event(self, instance) -> None:
        """ Save to db.json and close popup """
        Database().add_event(
            key=None,
            title=self.ids.event_name.text,
            start_date=self.selected_date_start,
            end_date=self.selected_date_end,
            start_time=self.selected_time_start,
            end_time=self.selected_time_end,
            group_tag={'name': self.ids.event_group_tag_name.text, 'colour': self.group_tag_colour},
            location=self.ids.event_location.text,
            repeat=self.repeat,
            repeat_details={},
            notification=self.notification,
            notification_details={},
            important=self.important
        )
        self.dismiss()

class ViewEventPopup(Popup):
    def __init__(self, event_key: int, **kwargs) -> None:
        super().__init__(**kwargs)
        db = Database()
        events = db.load_event()
        for event in events:
            if events and event['key'] == event_key:
                self.ids.event_name.text = event['title']
                self.ids.date_start.text = event['start_date']
                self.ids.date_end.text = event['end_date']
                self.ids.time_start.text = event['start_time']
                self.ids.time_end.text = event['end_time']
                self.ids.group_tag.text = event['group_tag']['name']
                self.ids.group_tag.color = event['group_tag']['colour']
                self.ids.event_location.text = event['location']
                if event['repeat']:
                    self.ids.repeat.text = 'Yes'
                elif not event['repeat']:
                    self.ids.repeat.text = 'No'
                if event['notification']:
                    self.ids.notification.text = 'Yes'
                elif not event['notification']:
                    self.ids.notification.text = 'No'

    def open_edit_event(self, instance):
        """ 'Edit Event' function """
        pass

class DayView(Popup):
    selected_day_text = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day: datetime = selected_day
        self.selected_day_text: str = f'{selected_day.strftime('%Y / %m / %d %A')}'
        self.build()

    def build(self) -> None:
        self.ids.events_list.clear_widgets()

        current_day: str = self.selected_day.strftime('%y/%m/%d')
        db = Database()
        events = db.load_event()
        no_events = True
        for event in events:
            if current_day == event['start_date'] or current_day == event['end_date']:
                # Create event UI boxes
                self.ids.events_list.add_widget(DayViewEvent(event))
                no_events = False
            else:
                continue
        if no_events:
            no_label = Label(text='No Events')
            self.ids.events_list.add_widget(no_label)

    def add_event(self, instance) -> None:
        add_event = AddEventPopup(selected_day=self.selected_day)
        add_event.open()
        add_event.bind(on_dismiss=self.refresh_view)

    def refresh_view(self, instance) -> None:
        self.build()

    def close_popup(self, instance) -> None:
        self.dismiss()

class DayViewEvent(ButtonBehavior, BoxLayout):
    """ Reusable Event block viewed in DayView """
    def __init__(self, event_data, **kwargs):
        super().__init__(**kwargs)
        self.event_data = event_data
        self.ids.event_name.text = self.event_data['title']
        self.ids.start_time.text = self.event_data['start_time']
        self.ids.end_time.text = self.event_data['end_time']
        self.bind(on_release=self._on_release)

    def _on_release(self, instance) -> None:
        """ Open ViewEvent Popup """
        popup = ViewEventPopup(self.event_data['key'])
        popup.open()

class MonthView(BoxLayout):
    def __init__(self, year: int, month: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_year = year
        self.current_month = month
        self.build()

    def build(self) -> None:
        self.ids.month_grid.clear_widgets()

        year = self.current_year
        month = self.current_month

        self.ids.month_label.text = f"{LOCAL_CALENDAR.formatmonthname(
            theyear=year,
            themonth=month,
            width=0,
            withyear=True
        )}"

        for day in range(7):
            label = Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                size_hint_y=0.2,
                color=palette.LIGHT_TEXT
                )
            with label.canvas:
                Color(palette.LIGHT_BACKGROUND)
                label.border = Line(rectangle=(label.x, label.y, label.width, label.height), width=3)
            label.bind(pos=self.update_label_border, size=self.update_label_border)
            self.ids.month_grid.add_widget(label)
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = MonthGridBox(day=day)
                    self.ids.month_grid.add_widget(btn)
                else:
                    btn = MonthGridBox()
                    self.ids.month_grid.add_widget(btn)

    def update_label_border(self, instance, *args):
        instance.border.rectangle = (instance.x, instance.y, instance.width, instance.height)

class MonthGridBox(ButtonBehavior, BoxLayout):
    def __init__(self, day: datetime = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.date: datetime = day

        if day:
            self.ids.date_label.text = str(self.date.day)
            self.bind(
                on_release=lambda instance, d=day: self.on_day_selected(d)
            )

    def on_day_selected(self, day: str) -> None:
        day_view = DayView(selected_day=day)
        day_view.open()

class YearView(BoxLayout):
    def __init__(self, year: int, callback=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.year = year
        self.year_label = str(self.year)
        self.callback = callback
        self.build()

    def build(self) -> None:
        self.ids.year_label.text = self.year_label
        self.ids.year_grid.clear_widgets()

        for month in range(1, 13):
            month_name = get_month_name(month)
            btn = Button(
                    text=month_name,
                    background_color=palette.LIGHT_BACKGROUND,
                    color=palette.LIGHT_TEXT
                )
            btn.bind(on_release=lambda instance, m=month: self.on_month_selected(m))
            self.ids.year_grid.add_widget(btn)

    def on_month_selected(self, month: str) -> None:
        """ Callback to CoreFunctions to load MonthView """
        selected_month = month
        if self.callback:
            callback = self.callback(self.year, selected_month)
        MonthView(year=self.year, month=selected_month)

class WeekView(BoxLayout):
    def __init__(self, current_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_day: datetime = current_day
        self.year_month_label: str = LOCAL_CALENDAR.formatmonthname(
            theyear=self.current_day.year,
            themonth=self.current_day.month,
            width=0,
            withyear=True
        )
        self.week_label: str = get_week_number(current_day=current_day)
        self.week: list = get_week_days(current_day)
        self.build()

        db = Database()
        events = db.load_event()
        self.build_events(events)

    def build(self) -> None:
        self.ids.week_label.text = f'{self.year_month_label}\nWeek {self.week_label}'
        self.ids.week_label.color = palette.LIGHT_TEXT

        for day in range(7):
            self.ids.week_days.add_widget(
                Label(
                    text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                    color = palette.LIGHT_TEXT
                ))
        for date in self.week:
            self.ids.week_days.add_widget(
                Label(
                    text=f'{date}', font_size=dp(13),
                    color = palette.LIGHT_TEXT
                ))

    def build_events(self, events) -> None:
        week: list = self.week
        for event in events:
            for day in week:
                formatted_day = f'{self.current_day.strftime('%y')}/{day}'
                if formatted_day == event['start_date'] or formatted_day == event['end_date']:
                    event_title_label = \
                        Label(
                            text=event['title'],
                            halign='left',
                            valign='middle',
                            size_hint_y=None,
                            height=dp(40)
                        )
                    event_title_label.bind(size=event_title_label.setter('text_size'))

                    self.ids.week_grid.add_widget(event_title_label)
                else:
                    self.ids.week_grid.add_widget(Label(text=''))

Builder.load_file('kivy_uis/views.kv')
