import sqlite3


class DBIO:
    def __init__(self):
        self._conn = sqlite3.connect('manga_reader.db')
        self._cursor = self._conn.cursor()
