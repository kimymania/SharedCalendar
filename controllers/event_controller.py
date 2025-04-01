import json
from datetime import date, time
from os.path import exists
from models.events import EventContainer

class EventController:
    def __init__(self):
        self.events = []

    def add_event(self, event: EventContainer):
        self.events.append(event)

    def get_events_on(self, target_date: date):
        return [e for e in self.events if e.date == target_date]

    def search_by_type_or_title(self, keyword: str):
        keyword = keyword.lower()
        return [
            e for e in self.events
            if keyword in e.title.lower() or keyword in e.type.lower()
        ]

    def save_to_file(self, filename="temp/events_temp.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([
                {
                    "title": e.title,
                    "date": e.date.isoformat(),
                    "time": e.time.strftime("%H:%M"),
                    "type": e.type,
                    "location": e.location
                } for e in self.events
            ], f, indent=2)

    def load_from_file(self, filename="temp/events_temp.json"):
        if not exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.events = [
                EventContainer(
                    title=d["title"],
                    date=date.fromisoformat(d["date"]),
                    time=time.fromisoformat(d["time"]),
                    type=d["type"],
                    location=d["location"]
                ) for d in data
            ]