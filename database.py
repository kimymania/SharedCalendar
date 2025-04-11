"""
Handles database operations for MVP version
"""

import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.json')

class Database:
    def __init__(self) -> None:
        self.db_path = DB_PATH

    def add_event(
            self, title: str, start_date: str, end_date: str,
            start_time: str, end_time: str, location: str
        ) -> None:
        """ Add Event to db.json file """
        new_event: dict = {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location
        }

        if os.path.isfile(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                try:
                    events = json.load(f)
                except json.JSONDecodeError:
                    events = []
        else:
            events = []

        events.append(dict(new_event))
        events.sort(key=lambda x: (datetime.strptime(x['start_date'], '%y/%m/%d'), datetime.strptime(x['start_time'], '%H:%M')))
        print(events)

        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=4)

    def load_event(self) -> list | None:
        """ Get data from db.json -> return list to caller """
        events = []
        if os.path.isfile(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                try:
                    events: list = json.load(f)
                    events.sort(key=lambda x: (datetime.strptime(x['start_date'], '%y/%m/%d'), datetime.strptime(x['start_time'], '%H:%M')))
                    return events
                except json.JSONDecodeError:
                    return None
        else:
            return
