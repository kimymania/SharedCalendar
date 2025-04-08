"""
Handles database operations for MVP version
"""

import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.json')

class Database:
    def __init__(self) -> None:
        self.db_path = DB_PATH
        self.data = {}

    def add_event(self) -> None:
        pass