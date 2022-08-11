"""Main Application module."""

import signal

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
gi.require_version("Notify", "0.7")

from gi.repository import AppIndicator3, Gtk, Notify

from tomatinho import appinfo
from tomatinho.about_dialog import about_dialog
from tomatinho.event_recorder import EventRecorder
from tomatinho.locale import _
from tomatinho.state_timer import StateTimer
from tomatinho.states import States

POMODORO = 25  # Minutes
SHORT_REST = 5
LONG_REST = 15


class Tomatinho:
    """Pomodoro Timer Application"""

    def __init__(self):
        self._state = States.IDLE
        self._recorder = EventRecorder()
        self._timer = StateTimer()

        self._indicator = AppIndicator3.Indicator.new(
            appinfo.ID,
            appinfo.ICON_IDLE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self._indicator.set_menu(self._build_menu())

        Notify.init(appinfo.ID)

    @staticmethod
    def _notify(message, icon):
        """Send a System Notification"""
        Notify.Notification.new(appinfo.NAME, message, icon).show()

    @staticmethod
    def _add_menu_item(menu, text, action):
        """Add a new Item to the menu."""
        menu_item = Gtk.MenuItem(text)
        menu_item.connect("activate", action)
        menu.append(menu_item)

    def _build_menu(self) -> Gtk.Menu:
        """Build the Application Menu."""
        menu = Gtk.Menu()
        self._add_menu_item(menu, _("Pomodoro"), self.start_pomodoro)
        self._add_menu_item(menu, _("Short Pause"), self.start_short_rest)
        self._add_menu_item(menu, _("Long Break"), self.start_long_rest)
        self._add_menu_item(menu, _("Stop"), self.stop_timer)
        menu.append(Gtk.SeparatorMenuItem())
        self._add_menu_item(menu, _("About"), about_dialog)
        menu.append(Gtk.SeparatorMenuItem())
        self._add_menu_item(menu, _("Quit"), self.quit)
        menu.show_all()

        return menu

    def start_pomodoro(self, source) -> None:
        """Start the Pomodoro timer."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.POMODORO
        self._timer.start(POMODORO * 60, self.stop_timer)
        self._indicator.set_icon(appinfo.ICON_POMO)
        self._indicator.set_label("PO", "")
        msg = _("Pomodoro") + f" ({POMODORO}m)"
        self._notify(msg, appinfo.ICON_POMO)

    def start_short_rest(self, source) -> None:
        """Start a Short Pause."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.SHORT_REST
        self._timer.start(SHORT_REST * 60, self.stop_timer)
        self._indicator.set_icon(appinfo.ICON_REST_S)
        self._indicator.set_label("SR", "")
        msg = _("Short Pause") + f" ({SHORT_REST}m)"
        self._notify(msg, appinfo.ICON_REST_S)

    def start_long_rest(self, source) -> None:
        """Start a Long Rest."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.LONG_REST
        self._timer.start(LONG_REST * 60, self.stop_timer)
        self._indicator.set_icon(appinfo.ICON_REST_L)
        self._indicator.set_label("LR", "")
        msg = _("Long Break") + f" ({LONG_REST}m)"
        self._notify(msg, appinfo.ICON_REST_L)

    def stop_timer(self, source=None) -> None:
        """Stop timer and go back to the idle state.

        If no ``source`` is specified, this method records that the last
        operation was finished successfully, considering that it was probably
        called directly and not from the menu button. If it's specified, the
        method was called from the app menu and it records the last operation
        as interrupted.
        """
        if source is None:
            self._recorder.record(op=self._state, completed=True)
        elif self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.IDLE
        self._timer.stop()
        self._indicator.set_icon(appinfo.ICON_IDLE)
        self._indicator.set_label("", "")
        self._notify(_("Stopped"), appinfo.ICON_IDLE)

    def quit(self, source) -> None:
        """Quit the Application."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        Gtk.main_quit()


def main():
    # Enable quiting the app with ^C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Tomatinho()
    Gtk.main()


if __name__ == "__main__":
    main()
