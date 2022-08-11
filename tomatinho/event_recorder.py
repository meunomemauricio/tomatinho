"""This module is responsible for storing event information on the DB."""

import datetime
import sqlite3

from tomatinho import appinfo


class EventRecorder:
    """Record events on the Database."""

    INSERT_QUERY = "INSERT INTO statistics VALUES (?, ?, ?)"
    CREATE_QUERY = (
        "CREATE TABLE IF NOT EXISTS statistics ("
        "operation INTEGER,"
        "completed BOOLEAN,"
        "datetime TIMESTAMP"
        ")"
    )

    def __init__(self):
        self.db = self._get_db_connection()

    def _get_db_connection(self) -> sqlite3.Connection:
        """Get a new DB connection.

        Creates the database file and table if it is not present already.
        """
        if not appinfo.USER_DIR.exists():
            appinfo.USER_DIR.makedir()

        conn = sqlite3.connect(appinfo.USER_DIR / "tomatinho.db")
        conn.cursor().execute(self.CREATE_QUERY)
        conn.commit()
        return conn

    def record(self, op, completed) -> None:
        """Record an event to the DB.

        :param op: A value from the States enum representing the state that has
        just finished.
        :param completed: True if the operation was completed or False if it
        was interrupted.
        """
        current_datetime = datetime.datetime.now()
        self.db.cursor().execute(
            self.INSERT_QUERY, (op, completed, current_datetime)
        )
        self.db.commit()
