"""
Handles database operations for MVP version
"""

import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.json')

class Database:
    def __init__(self) -> None:
        self.db_path = DB_PATH

    def add_event(
            self, title: str, start_date: str, end_date: str,
            start_time: str, end_time: str, location: str
        ) -> None:
        new_event = {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location
        }

        # get file and store data in local 'events' list
        if os.path.isfile(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                try:
                    events = json.load(f)
                except json.JSONDecodeError:
                    events = []
        else:
            events = []

        # add new data to this list
        events.append(new_event)

        # rewrite all data to .json file
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db_path, f, ensure_ascii=False, indent=4)

    def load_event(self):
        pass