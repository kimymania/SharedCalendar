from dataclasses import dataclass
from datetime import date, time

@dataclass
class EventContainer:
    index: None
    title: str
    date: date
    time_start: time
    time_end: time
    type: str
    location: str

@dataclass
class MonthEventContainer:
    title: str
    date: date
    type: str