"""Timer used to change the application state."""
from datetime import datetime, timedelta
from typing import Callable, Optional

from gi.repository import GLib

#: Label refresh period in seconds
REFRESH_PERIOD = 1


class StateTimer:
    """Timer used to change the application state.

    :callable label_cb: Callback function to call to update the App label.
    """

    def __init__(self, label_cb: Callable[[str], None]):
        self._label_cb = label_cb

        #: Event Source ID representing GLib timeout timer.
        self._id: Optional[int] = None
        #: Event Source ID representing the label updater timer
        self._label_id: Optional[int] = None
        #: Date time estimating when the time is going to stop. Only meaningful
        # when `self._id` is not None.
        self._end_dt: datetime = datetime.now()

    @property
    def time_left(self) -> str:
        """Time left on the timer (approximate).

        Return only minutes and seconds in format "MM:SS".
        """
        if self._id is None:
            return ""

        td = self._end_dt - datetime.now()
        return str(td).split(":", maxsplit=1)[1].split(".", maxsplit=1)[0]

    def _update_label(self) -> bool:
        """Call the Callback to update the App label with the time left."""
        self._label_cb(self.time_left)
        return True  # Repeat

    def start(self, duration: int, callback: Callable[..., None]) -> None:
        """Run the timer.

        Starting the timer again will cancel the previous timeout timer.

        :int duration: duration of the timer in seconds.
        :callable callback: callback function to be executed on timeout. The
            callback function needs to return None, otherwise it will be
            repeated continuously.
        """
        if self._id is not None:
            GLib.source_remove(self._id)

        self._id = GLib.timeout_add_seconds(
            interval=duration, function=callback
        )

        self._end_dt = datetime.now() + timedelta(seconds=duration)
        if self._label_id is None:
            self._label_id = GLib.timeout_add_seconds(
                interval=REFRESH_PERIOD, function=self._update_label
            )

        self._update_label()

    def stop(self) -> None:
        """Stop the timer."""
        if self._id is not None:
            GLib.source_remove(self._id)
            self._id = None
            self._end_dt = None

        if self._label_id is not None:
            GLib.source_remove(self._label_id)
            self._label_id = None

        self._update_label()
