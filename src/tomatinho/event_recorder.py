import datetime
import sqlite3
import os.path

from . import appinfo


class EventRecorder(object):
    """Record events on the Database."""

    INSERT_QUERY = 'INSERT INTO statistics VALUES (?, ?, ?)'
    CREATE_QUERY = ('CREATE TABLE statistics ('
                    'operation INTEGER,'
                    'completed BOOLEAN,'
                    'datetime TIMESTAMP'
                    ')')

    def __init__(self):
        self.statistics_db = self.get_db_connection()

    def get_db_connection(self):
        """Get a new DB connection.

        Creates the table if it is not present already.

        :return: New connection to the DB
        """
        if not os.path.exists(appinfo.APP_DIR):
            os.makedirs(appinfo.APP_DIR)
        conn = sqlite3.connect(os.path.join(appinfo.APP_DIR, 'tomatinho.db'))
        cursor = conn.cursor()

        try:
            cursor.execute(self.CREATE_QUERY)
            conn.commit()
        except sqlite3.OperationalError:
            # Table already exists
            pass

        return conn

    def record(self, operation, completed):
        current_datetime = datetime.datetime.now()
        self.statistics_db.cursor().execute(
            self.INSERT_QUERY,
            (operation, completed, current_datetime)
        )
        self.statistics_db.commit()

    def close(self):
        self.statistics_db.close()