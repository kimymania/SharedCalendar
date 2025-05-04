"""
Calendar UI using Kivy
"""
from datetime import datetime

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.factory import Factory

from selectors_logic import DateSelector, TimeSelector, ColourPicker

from database import Database
from common_utils import (
    LOCAL_CALENDAR, get_month, get_week_number, get_week_days,
    find_ancestor, format_month_kor
)
from palette import RED, background_colour, text_colour, selected_colour


WINDOW_WIDTH, WINDOW_HEIGHT = Window.size

class AddEventPopup(Popup):
    date_start = StringProperty('')
    date_end = StringProperty('')
    time_start = StringProperty('')
    time_end = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        selected_date: datetime = datetime.today()
        this_time = selected_date.time()
        selected_date.combine(date=selected_day, time=this_time)
        self.selected_date = selected_day
        self.date_start = selected_day.strftime('%y/%m/%d')
        self.date_end = selected_day.strftime('%y/%m/%d')
        self.time_start: str = f'{selected_date.hour:02}:00'
        if selected_date.hour < 23:
            end_hour = selected_date.hour + 1
        else:
            end_hour = 0
        self.time_end: str = f'{end_hour:02}:00'
        self.group_tag_name: str = 'None'
        self.group_tag_colour: list = [0, 0, 0, 1]  # black by default
        self.repeat: bool = False
        self.notification: bool = False
        self.important: bool = False

    def toggle_date_selector(self, instance, target: str) -> None:
        if target == 'start':
            date_selector = DateSelector(
                current_day=self.selected_date,
                return_date=self.receive_date_start
            )
            date_selector.open()
        elif target == 'end':
            date_selector = DateSelector(
                current_day=self.selected_date,
                return_date=self.receive_date_end
            )
            date_selector.open()
        else:
            return

    def receive_date_start(self, date: datetime):
        """ Store start date """
        self.date_start = date.strftime('%y/%m/%d')

    def receive_date_end(self, date: datetime):
        """ Store end date """
        self.date_end = date.strftime('%y/%m/%d')

    def toggle_time_selector(self, instance, target: str) -> None:
        """ Open time selector for start/end time """
        if target == 'start':
            time_selector = TimeSelector(
                return_time=self.receive_time_start,
                time=self.time_start
            )
            time_selector.open()
        elif target == 'end':
            time_selector = TimeSelector(
                return_time=self.receive_time_end,
                time=self.time_end
            )
            time_selector.open()
        else:
            return

    def receive_time_start(self, time: datetime) -> None:
        """ Store start time """
        self.time_start = time.strftime('%H:%M')

    def receive_time_end(self, time: datetime) -> None:
        """ Store end time """
        self.time_end = time.strftime('%H:%M')

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
            start_date=self.date_start,
            end_date=self.date_end,
            start_time=self.time_start,
            end_time=self.time_end,
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
    def __init__(self, event_key: int, event_date: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.event_date = event_date
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
        ... # Change to editing screen
        self.dismiss()

class DayView(BoxLayout):
    selected_day_text = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day: datetime = selected_day
        self.selected_day_text: str = f'{selected_day.strftime('%Y년 %m월 %d일 %A')}'
        self.build()

    def build(self) -> None:
        self.ids.day_events_list.clear_widgets()

        current_day: str = self.selected_day.strftime('%y/%m/%d')
        db = Database()
        events = db.load_event()
        no_events = True
        for event in events:
            if current_day == event['start_date'] or current_day == event['end_date']:
                # Create event UI boxes
                self.ids.day_events_list.add_widget(DayViewEvent(
                    event_data=event,
                    event_date=self.selected_day
                ))
                no_events = False
            else:
                continue
        if no_events:
            no_label = Label(
                text='일정 없음',
                color=text_colour,
                size_hint_y=None,
                height=dp(20)
            )
            self.ids.day_events_list.add_widget(no_label)

    def add_event(self, instance) -> None:
        add_event = AddEventPopup(selected_day=self.selected_day)
        add_event.open()
        add_event.bind(on_dismiss=self.refresh_view)

    def refresh_view(self, instance) -> None:
        self.build()

    def close_view(self, instance) -> None:
        self.parent.close_dayview(self)

class DayViewEvent(ButtonBehavior, BoxLayout):
    def __init__(self, event_data, event_date: datetime, **kwargs):
        super().__init__(**kwargs)
        self.event_data = event_data
        self.event_date = event_date
        self.ids.event_name.text = self.event_data['title']
        self.ids.start_time.text = self.event_data['start_time']
        self.ids.end_time.text = self.event_data['end_time']
        self.bind(on_release=self._on_release)

    def _on_release(self, instance) -> None:
        """ Open ViewEvent Popup """
        popup = ViewEventPopup(
            event_key=self.event_data['key'],
            event_date=self.event_date
        )
        popup.open()

class MonthView(FloatLayout):
    def __init__(self, year: int, month: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_year = year
        self.current_month = month
        self.selected_box = None
        self.build()

    def build(self) -> None:
        self.ids.month_grid.clear_widgets()

        year = self.current_year
        month = self.current_month

        self.ids.month_label.text = format_month_kor(year, month)

        for day in range(7):
            label = Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                size_hint_y=0.2
            )
            if day == 0:
                label.color = RED
            else:
                label.color = text_colour
            self.ids.month_grid_days.add_widget(label)

        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = MonthGridBox(day=day)
                    self.ids.month_grid.add_widget(btn)
                else:
                    btn = MonthGridBox()
                    self.ids.month_grid.add_widget(btn)

    def track_selection(self, instance, day: datetime) -> None:
        """ Change colour of grid boxes """
        if not self.selected_box:
            self.selected_box = instance
            self.selected_box.bg_colour = selected_colour
        elif self.selected_box != instance:
            self.selected_box.bg_colour = background_colour
            self.selected_box = instance
            self.selected_box.bg_colour = selected_colour
        elif self.selected_box == instance:
            day_view = DayView(selected_day=day)
            self.add_widget(day_view)

    def close_dayview(self, widget):
        widgets: list = []
        widgets.append(widget)
        self.clear_widgets(children=widgets)

class MonthGridBox(ButtonBehavior, BoxLayout):
    bg_colour = ListProperty(background_colour)
    def __init__(self, day: datetime = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.date: datetime = day

        with self.canvas.before:
            self._colour = Color(rgba=self.bg_colour)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=self.update_graphics,
            size=self.update_graphics,
            bg_colour=self.update_colour
        )

        if day:
            self.ids.date_label.text = str(self.date.day)
            self.bind(on_release=lambda instance, d=day: self.on_day_selected(instance, d))

    def update_graphics(self, *args) -> None:
        self._rect.pos = self.pos
        self._rect.size = self.size

    def update_colour(self, instance, new_rgba) -> None:
        self._colour.rgba = new_rgba

    def on_day_selected(self, instance, day: datetime) -> None:
        # MonthGridBox > GridLayout > BoxLayout > MonthView(FloatLayout)
        self.parent.parent.parent.track_selection(instance, day)

class YearView(BoxLayout):
    def __init__(self, year: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.year = year
        self.year_label = f'{self.year}년'
        self.build()

    def build(self) -> None:
        self.ids.year_label.text = self.year_label
        self.ids.year_grid.clear_widgets()

        for month in range(1, 13):
            box = YearGridBox(self.year, month)
            self.ids.year_grid.add_widget(box)

class YearGridBox(ButtonBehavior, BoxLayout):
    """ Loads month cal as a grid box - but it's slow atm """
    def __init__(self, year: int, month: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.year: int = year
        self.month: int = month

        self.ids.month_box_label.text = LOCAL_CALENDAR.formatmonthname(
            theyear=self.year,
            themonth=self.month,
            width=3,
            withyear=False
        )

        # week_headers = LOCAL_CALENDAR.formatweekheader(width=2).split(' ')
        # not suitable for localization but less processing = better performance i think
        week_headers: list = ['일', '월', '화', '수', '목', '금', '토']
        for i in range(7):
            header_label = Label(
                text = week_headers[i],
                font_size = dp(10),
                color = text_colour
            )
            self.ids.month_box_grid.add_widget(header_label)

        for week in LOCAL_CALENDAR.monthdays2calendar(year=self.year, month=self.month):
            for day, index in enumerate(week):
                day_label = Label(
                    text = str(index[0]),
                    font_size = dp(10),
                    color = text_colour
                )
                if index[0] == 0:
                    day_label.text = ''
                self.ids.month_box_grid.add_widget(day_label)

        self.bind(
            on_release=lambda instance, m=self.month: self.on_month_selected(m)
        )

    def on_month_selected(self, month: int) -> None:
        core = find_ancestor(widget=self, class_name=Factory.CoreFunctions)
        if core:
            core.switch_view_to_selected(self.year, month)
        else:
            print("Can't find CoreFunctions")

class WeekView(BoxLayout):
    def __init__(self, current_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_day: datetime = current_day
        self.year_month_label: str = format_month_kor(self.current_day.year, self.current_day.month)
        self.week_label: str = get_week_number(current_day=self.current_day)
        self.week: list = get_week_days(self.current_day)
        self.build()

        db = Database()
        events = db.load_event()
        self.build_events(events)

    def build(self) -> None:
        self.ids.week_label.text = f'{self.year_month_label}\n{self.week_label}주차'
        self.ids.week_label.color = text_colour

        for day in range(7):
            weekday_label = Label(
                text=LOCAL_CALENDAR.formatweekday(day=(day + 6) % 7, width=3),
                color = text_colour
            )
            self.ids.week_days.add_widget(weekday_label)
        for date in self.week:
            self.ids.week_days.add_widget(
                Label(
                    text=f'{date}', font_size=dp(13),
                    color = text_colour
                ))

    def build_events(self, events) -> None:
        week: list = self.week
        for event in events:
            for day in week:
                formatted_day = f'{self.current_day.strftime('%y')}/{day}'
                if formatted_day == event['start_date'] or formatted_day == event['end_date']:
                    event_title_label = Label(
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

Builder.load_file('kivy_uis/main_views.kv')
