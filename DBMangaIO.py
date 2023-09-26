from DBIO import DBIO


class DBMangaIO(DBIO):
    def __init__(self):
        super().__init__()
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS manga(
                           id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                           title TEXT NOT NULL,
                           href TEXT UNIQUE ON CONFLICT IGNORE NOT NULL
                           )''')

    def add_to_table(self, title: str, href: str):
        self._cursor.execute('INSERT INTO manga(title, href) VALUES(?,?)', (title, href))
        self._conn.commit()
