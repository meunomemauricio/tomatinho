# -*- coding: utf-8 -*-
"""Timer used to change the application state."""

from gi.repository import GLib


class StateTimer:
    """Timer used to change the application state."""

    def __init__(self):
        self._is_running = False
        self._id = None

    def start(self, duration, callback):
        """Run the timer.

        :param duration: duration of the timer in milliseconds.
        :param callback: callback function to be executed on timeout.
        """

        def _callback():
            """Wrapper to make sure False is returned to GLib function"""
            callback()
            return False

        if self._is_running:
            GLib.source_remove(self._id)

        self._is_running = True
        self._id = GLib.timeout_add(duration, _callback)

    def stop(self):
        """Stop the timer."""
        if self._is_running:
            GLib.source_remove(self._id)
            self._is_running = False
