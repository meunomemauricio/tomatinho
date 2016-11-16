# -*- coding: utf-8 -*-
"""This module is responsible for storing event information on the DB."""

import datetime
import sqlite3
import os.path

from . import appinfo


class EventRecorder:
    """Record events on the Database."""

    INSERT_QUERY = 'INSERT INTO statistics VALUES (?, ?, ?)'
    CREATE_QUERY = ('CREATE TABLE IF NOT EXISTS statistics ('
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
        conn.cursor().execute(self.CREATE_QUERY)
        conn.commit()
        return conn

    def record(self, operation, completed):
        """Record an event to the DB.

        :param operation: A value from the States enum representing the state
        that has just finished.
        :param completed: True if the operation was completed or False if it
        was interrupted.
        """
        current_datetime = datetime.datetime.now()
        self.statistics_db.cursor().execute(
            self.INSERT_QUERY,
            (operation, completed, current_datetime)
        )
        self.statistics_db.commit()
