"""Main Application module."""

import signal
from typing import Callable

from gi.repository import AppIndicator3, Gtk, Notify

from tomatinho import appinfo
from tomatinho.about_dialog import about_dialog
from tomatinho.event_recorder import EventRecorder
from tomatinho.locale import _
from tomatinho.state_timer import StateTimer
from tomatinho.states import States

MenuCallable = Callable[[Gtk.MenuItem], None]

POMODORO = 25  # Minutes
SHORT_REST = 5
LONG_REST = 15


class Tomatinho:
    """Pomodoro Timer Application"""

    def __init__(self):
        self._state = States.IDLE
        self._recorder = EventRecorder()

        self._indicator = AppIndicator3.Indicator.new(
            appinfo.ID,
            appinfo.ICON_IDLE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self._indicator.set_menu(self._build_menu())

        self._timer = StateTimer(label_cb=self.update_label)

        Notify.init(appinfo.ID)

    @staticmethod
    def _notify(msg: str, icon: str) -> None:
        """Send a System Notification"""
        Notify.Notification.new(appinfo.NAME, msg, icon).show()

    @staticmethod
    def _add_menu_item(
        menu: Gtk.Menu, text: str, action: MenuCallable
    ) -> None:
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

    def update_label(self, label: str) -> None:
        """Update app's label with the time left on the Timer."""
        self._indicator.set_label(label, "")

    def start_pomodoro(self, source: Gtk.MenuItem) -> None:
        """Start the Pomodoro timer."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.POMODORO
        self._timer.start(POMODORO * 60, self.stop_timer)
        self._indicator.set_icon(appinfo.ICON_POMO)
        msg = _("Pomodoro") + f" ({POMODORO}m)"
        self._notify(msg=msg, icon=appinfo.ICON_POMO)

    def start_short_rest(self, source: Gtk.MenuItem) -> None:
        """Start a Short Pause."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.SHORT_REST
        self._timer.start(SHORT_REST, self.stop_timer)
        self._indicator.set_icon(appinfo.ICON_REST_S)
        msg = _("Short Pause") + f" ({SHORT_REST}m)"
        self._notify(msg=msg, icon=appinfo.ICON_REST_S)

    def start_long_rest(self, source: Gtk.MenuItem) -> None:
        """Start a Long Rest."""
        if self._state != States.IDLE:
            self._recorder.record(op=self._state, completed=False)

        self._state = States.LONG_REST
        self._timer.start(LONG_REST * 60, self.stop_timer)
        self._indicator.set_icon(appinfo.ICON_REST_L)
        msg = _("Long Break") + f" ({LONG_REST}m)"
        self._notify(msg=msg, icon=appinfo.ICON_REST_L)

    def stop_timer(self, source: Gtk.MenuItem = None) -> None:
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
        self._notify(msg=_("Stopped"), icon=appinfo.ICON_IDLE)

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
