# -*- coding: utf-8 -*-
"""Main Application module."""

import signal

from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify

from . import appinfo
from . about_dialog import about_dialog
from . event_recorder import EventRecorder
from . locale import _
from . state_timer import StateTimer
from . states import States
from . settings import Settings, SettingsDialog


class Tomatinho:
    """Pomodoro Timer Application"""

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            appinfo.ID,
            appinfo.ICON_IDLE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.settings = Settings()

        self.menu = None
        self.build_menu()

        self.state = States.IDLE

        self.recorder = EventRecorder()
        self.timer = StateTimer()

        Notify.init(appinfo.ID)

    def build_menu(self):
        self.menu = Gtk.Menu()
        self.add_new_menu_item(_('Pomodoro'), self.start_pomodoro)
        self.add_new_menu_item(_('Short Pause'), self.start_short_rest)
        self.add_new_menu_item(_('Long Break'), self.start_long_rest)
        self.add_new_menu_item(_('Stop'), self.stop_timer)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.add_new_menu_item(_('Settings'), SettingsDialog.display)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.add_new_menu_item(_('About'), about_dialog)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.add_new_menu_item(_('Quit'), self.quit)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def add_new_menu_item(self, text, action):
        menu_item = Gtk.MenuItem(text)
        menu_item.connect('activate', action)
        self.menu.append(menu_item)

    def start_pomodoro(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.POMODORO
        time_ms = self.settings.pomo_intvl * 60 * 1000
        self.timer.start(time_ms, self.stop_timer)
        self.indicator.set_icon(appinfo.ICON_POMO)
        msg = _('Pomodoro') + ' ({0}m)'.format(self.settings.pomo_intvl)
        self.notify(msg, appinfo.ICON_POMO)

    def start_short_rest(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.SHORT_REST
        time_ms = self.settings.s_rest_intvl * 60 * 1000
        self.timer.start(time_ms, self.stop_timer)
        self.indicator.set_icon(appinfo.ICON_REST_S)
        msg = _('Short Pause') + ' ({0}m)'.format(self.settings.s_rest_intvl)
        self.notify(msg, appinfo.ICON_REST_S)

    def start_long_rest(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.LONG_REST
        time_ms = self.settings.l_rest_intvl * 60 * 1000
        self.timer.start(time_ms, self.stop_timer)
        self.indicator.set_icon(appinfo.ICON_REST_L)
        msg = _('Long Break') + ' ({0}m)'.format(self.settings.l_rest_intvl)
        self.notify(msg, appinfo.ICON_REST_L)

    def stop_timer(self, source=None):
        """Stop timer and go back to the idle state.

        If no ``source`` is specified, this method records that the last
        operation was finished successfully, considering that it was probably
        called directly and not from the menu button. If it's specified, the
        method was called from the app menu and it records the last operation
        as interrupted.
        """
        if source is None:
            self.recorder.record(self.state, True)
        elif self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.IDLE
        self.timer.stop()
        self.indicator.set_icon(appinfo.ICON_IDLE)
        self.notify(_('Stopped'), appinfo.ICON_IDLE)

    def notify(self, message, icon):
        Notify.Notification.new(appinfo.NAME, message, icon).show()

    def quit(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)
        Gtk.main_quit()


def main():
    # Enable quiting the app with ^C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Tomatinho()
    Gtk.main()


if __name__ == "__main__":
    main()
