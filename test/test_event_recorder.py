import datetime
import os
import sqlite3
import sys

from freezegun import freeze_time

sys.path.append("src")
from tomatinho import event_recorder
from tomatinho.tomatinho import States


class TestEventRecorder:
    def test_app_dir_creation(self, monkeypatch, tmpdir):
        """Should create Application directory if it does not exist."""
        dir = os.path.join(str(tmpdir.realpath()), "tomatinho")
        monkeypatch.setattr(event_recorder.appinfo, "USER_DIR", dir)

        event_recorder.EventRecorder()

        assert tmpdir.ensure_dir("tomatinho")

    def test_db_file_creation(self, monkeypatch, tmpdir):
        """Should create a new DB file."""
        dir = str(tmpdir.realpath())
        monkeypatch.setattr(event_recorder.appinfo, "USER_DIR", dir)

        event_recorder.EventRecorder()

        assert tmpdir.ensure("tomatinho.db")

    def test_table_creation(self, monkeypatch, tmpdir):
        """Check if the statistics table is being created."""
        dir = str(tmpdir.realpath())
        monkeypatch.setattr(event_recorder.appinfo, "USER_DIR", dir)

        recorder = event_recorder.EventRecorder()

        assert table_exists("statistics", recorder.statistics_db.cursor())

    def test_table_already_exists(self, monkeypatch, tmpdir):
        """Test what happens when the statistics table already exists."""
        dir = str(tmpdir.realpath())
        monkeypatch.setattr(event_recorder.appinfo, "USER_DIR", dir)
        create_db_table(dir)

        assert event_recorder.EventRecorder()

    @freeze_time("2016-11-14 01:23:45")
    def test_completed_record(self, monkeypatch, tmpdir):
        """Create a new record on the DB."""
        dir = str(tmpdir.realpath())
        monkeypatch.setattr(event_recorder.appinfo, "USER_DIR", dir)
        recorder = event_recorder.EventRecorder()

        recorder.record(States.POMODORO, True)

        results = query_db_table(dir)
        assert len(results) == 1
        assert results[0][0] == States.POMODORO
        assert results[0][1] == 1  # True
        assert results[0][2] == datetime.datetime(2016, 11, 14, 1, 23, 45)


def table_exists(table_name, cursor):
    query = (
        "SELECT name " "FROM sqlite_master " 'WHERE type="table" AND name=?'
    )
    result = cursor.execute(query, (table_name,)).fetchone()
    return table_name in result


def create_db_table(dir):
    conn = sqlite3.connect(os.path.join(dir, "tomatinho.db"))
    create_query = (
        "CREATE TABLE statistics ("
        "operation INTEGER,"
        "completed BOOLEAN,"
        "datetime TIMESTAMP"
        ")"
    )
    conn.cursor().execute(create_query)
    conn.commit()
    conn.close()


def query_db_table(dir):
    conn = sqlite3.connect(
        os.path.join(dir, "tomatinho.db"),
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    )
    create_query = "SELECT * FROM statistics"
    result = conn.cursor().execute(create_query).fetchall()
    conn.close()

    return result
