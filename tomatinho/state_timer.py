"""Timer used to change the application state."""

from gi.repository import GLib


class StateTimer:
    """Timer used to change the application state."""

    def __init__(self):
        # Event Source ID representing GLib timeout timer.
        self._id = None

    def start(self, duration, callback) -> None:
        """Run the timer.

        Starting the timer again will cancel the previous timeout timer.

        :param duration: duration of the timer in milliseconds.
        :param callback: callback function to be executed on timeout.
        """

        def _callback():
            """Wrapper to make sure the callback is executed only once.

            `GLib.timeout_add` repeats the callback periodically until it's
            removed or it returns False, so we force that condition.
            """
            callback()
            return False

        if self._id is not None:
            GLib.source_remove(self._id)

        self._id = GLib.timeout_add(duration, _callback)

    def stop(self) -> None:
        """Stop the timer."""
        if self._id is not None:
            GLib.source_remove(self._id)
            self._id = None
