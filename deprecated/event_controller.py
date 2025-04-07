import sqlite3
from datetime import datetime, date
from models import EventContainer
from database import get_connection, create_table

class EventController:
    def __init__(self):
        create_table()

    def add_event(self, event: EventContainer) -> None:
        """
        Insert a new event into the database.
        For new events, you might set event.index to None.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (title, date, time_start, time_end, type, location)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                event.title,
                event.date.isoformat(),
                event.time_start.strftime('%H:%M'),
                event.time_end.strftime('%H:%M') if event.time_end else None,
                event.type,
                event.location
            ))
            conn.commit()

    def get_events_by_date(self, event_date: date) -> list:
        """
        Retrieve all events for a specific date.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, date, time_start, time_end, type, location
                FROM events
                WHERE date = ?
            ''', (event_date.isoformat(),))
            rows = cursor.fetchall()

        events = []
        for row in rows:
            try:
                event = EventContainer(
                    index=row[0],
                    title=row[1],
                    date=date.fromisoformat(row[2]),
                    time_start=datetime.strptime(row[3], '%H:%M').time(),
                    time_end=datetime.strptime(row[4], '%H:%M').time() if row[4] else None,
                    type=row[5],
                    location=row[6]
                )
                events.append(event)
            except Exception as e:
                print("Error processing event row:", row, e)
        return events

    def get_event_by_id(self, event_id: int) -> EventContainer:
        """
        Retrieve a single event by its ID.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, date, time_start, time_end, type, location
                FROM events
                WHERE id = ?
            ''', (event_id,))
            row = cursor.fetchone()

        if row:
            return EventContainer(
                index=row[0],
                title=row[1],
                date=date.fromisoformat(row[2]),
                time_start=datetime.strptime(row[3], '%H:%M').time(),
                time_end=datetime.strptime(row[4], '%H:%M').time() if row[4] else None,
                type=row[5],
                location=row[6]
            )
        return None
    
    def search_by_type_or_title(self, keyword: str):
        keyword = keyword.lower()
        return [
            e for e in self.events
            if keyword in e.title.lower() or keyword in e.type.lower()
        ]