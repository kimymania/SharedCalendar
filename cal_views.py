"""
Calendar UI using Kivy
"""
from datetime import datetime

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.metrics import dp

from selectors_logic import DateSelector, TimeSelector

from database import Database
from common_utils import (
    LOCAL_CALENDAR, get_month, get_month_name, get_week_number, get_week_days
)

Builder.load_file('kivy_uis/views.kv')

class AddEventPopup(Popup):
    """ Popup for adding events """
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
        self.build_view()

    def build_view(self) -> None:
        pass

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
            time_selector = TimeSelector(return_time=self.receive_selected_time_start)
            time_selector.open()
        elif target == 'end':
            time_selector = TimeSelector(return_time=self.receive_selected_time_end)
            time_selector.open()
        else:
            return

    def receive_selected_time_start(self, time: datetime):
        """ Store start time """
        self.selected_time_start = time.strftime('%H:%M')

    def receive_selected_time_end(self, time: datetime):
        """ Store end time """
        self.selected_time_end = time.strftime('%H:%M')

    def save_event(self, instance) -> None:
        """ Save to db.json and close popup """
        Database().add_event(
            title=self.ids.event_name.text,
            start_date=self.selected_date_start,
            end_date=self.selected_date_end,
            start_time=self.selected_time_start,
            end_time=self.selected_time_end,
            location=self.ids.event_location.text
        )
        self.dismiss()

class DayView(Popup):
    """ Selected day view popup """
    selected_day_text = StringProperty('')
    def __init__(self, selected_day: datetime, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_day: datetime = selected_day
        self.selected_day_text: str = f'{selected_day.strftime('%Y / %m / %d %A')}'
        self.build_view()

    def build_view(self) -> None:
        """ Load events from database """
        current_day: str = self.selected_day.strftime('%y/%m/%d')
        db = Database()
        events = db.load_event()
        no_events = True
        for event in events:
            if current_day == event['start_date'] or current_day == event['end_date']:
                # Create event UI boxes
                event_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(40),
                    spacing=dp(10),
                    padding=[dp(10), dp(5)]
                )
                event_time_box = BoxLayout(
                    orientation='vertical',
                    size_hint_x=0.35
                )

                event_title_label = Label(
                    text=event['title'],
                    halign='left',
                    valign='middle'
                )
                event_title_label.bind(size=event_title_label.setter('text_size'))

                event_start_time_label = Label(
                    text=event['start_time'],
                    halign='left',
                    font_size=dp(15)
                )

                event_end_time_label = Label(
                    text=event['end_time'],
                    halign='left',
                    font_size=dp(15)
                )

                event_location_label = Label(
                    text=event['location'],
                    halign='left'
                )
                event_location_label.bind(size=event_location_label.setter('text_size'))

                event_time_box.add_widget(event_start_time_label)
                event_time_box.add_widget(event_end_time_label)
                event_box.add_widget(event_time_box)
                event_box.add_widget(event_title_label)
                event_box.add_widget(event_location_label)
                self.ids.events_list.add_widget(event_box)
                no_events = False
            else:
                continue
        if no_events:
            no_label = Label(text='No Events')
            self.ids.events_list.add_widget(no_label)

    def add_event(self, instance) -> None:
        """ Load AddEvent popup """
        add_event = AddEventPopup(selected_day=self.selected_day)
        add_event.open()

    def close_popup(self, instance) -> None:
        """ Close DayView """
        self.dismiss()

class MonthView(BoxLayout):
    """ Main Calendar UI - MonthView """
    def __init__(self, year: int, month: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_year = year
        self.current_month = month
        self.build_view()

    def build_view(self) -> None:
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
            self.ids.month_grid.add_widget(Label(
                text=LOCAL_CALENDAR.formatweekday(day=day, width=3),
                size_hint_y=0.15
            ))
        for week in get_month(year=year, month=month):
            for day in week:
                if day.month == month:
                    btn = Button(text=str(day.day))
                    btn.bind(on_release=lambda instance, d=day: self.on_day_selected(d))
                    self.ids.month_grid.add_widget(btn)
                else:
                    self.ids.month_grid.add_widget(Label(text=' '))

    def on_day_selected(self, day: str) -> None:
        """ Load DayView popup """
        day_view = DayView(selected_day=day)
        day_view.open()

class YearView(BoxLayout):
    """ Year View - show months & buttons for each month """
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
            btn = Button(text=month_name)
            btn.bind(on_release=lambda instance, m=month: self.on_month_selected(m))
            self.ids.year_grid.add_widget(btn)

    def on_month_selected(self, month: str) -> None:
        """ Callback to CoreFunctions to load MonthView """
        selected_month = month
        if self.callback:
            callback = self.callback(self.year, selected_month)
        # MonthView(year=self.year, month=selected_month)

class WeekView(BoxLayout):
    """ Week View - shows days of week, display week number """
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
        self.week: list = get_week_days(current_day=current_day)
        self.build()

        db = Database()
        events = db.load_event()
        # wip = trying to match event['start_date'], which is in YYYY/MM/DD format to
        # self.week which currently returns MM/DD
        # date_condition = f'{self.current_day.year}'
        # for event in events:
        #     if event['start_date'] == self.current_day
        self.build_events(events)

    def build(self) -> None:
        """
        Top: Month, Year & Week Number

        Add empty grid at first column
        """
        self.ids.week_label.text = f'{self.year_month_label}\nWeek {self.week_label}'

        for day in range(7):
            self.ids.week_days.add_widget(Label(text=LOCAL_CALENDAR.formatweekday(day=day, width=3)))
        for date in self.week:
            self.ids.week_days.add_widget(Label(text=f'{date}', font_size=dp(13)))

        # Draw colored rectangles to show hour grid
        for d in range(7):
            for h in range(24):
                widget = WeekGrid()
                time_label: str = f'{h:02}:00'
                self.ids.week_grid.add_widget(widget)
                # if d == 0:
                #     self.ids.week_grid.add_widget(Label(
                #         text=time_label,
                #         halign='left',
                #         valign='top',
                #         text_size=self.size
                #     ))

    def build_events(self, events) -> None:
        for event in events:
            # if current_day == event['start_date'] or current_day == event['end_date']:
            #     # Create event UI boxes
            #     pass
            # else:
            #     continue
            pass

class WeekGrid(Widget):
    """ Used to create empty grid in weekview"""
    def __init__(self, **kwargs) -> None:
        super().__init__(*kwargs)
        self.build()

    def build(self) -> None:
        pass

class WeekEvent(Widget):
    """ Used to draw event widgets on grid """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.build()

    def build(self) -> None:
        pass
