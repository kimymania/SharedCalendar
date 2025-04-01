from dataclasses import dataclass
from datetime import date, time

@dataclass
class EventContainer:
    title: str
    date: date
    time: time
    type: str
    location: str

@dataclass
class MonthEventContainer:
    title: str
    date: date
    type: str