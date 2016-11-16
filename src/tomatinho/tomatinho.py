# -*- coding: utf-8 -*-
"""Main Application module."""

import gi
import signal

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk  # noqa: E402
from gi.repository import GdkPixbuf  # noqa: E402
from gi.repository import AppIndicator3  # noqa: E402
from gi.repository import Notify  # noqa: E402

from pkg_resources import resource_filename  # noqa: E402

from . import appinfo  # noqa: E402
from . event_recorder import EventRecorder  # noqa: E402
from . state_timer import StateTimer  # noqa: E402


class States:
    """Enum representing the Application states."""
    IDLE = 1
    POMODORO = 2
    SHORT_REST = 3
    LONG_REST = 4


class Tomatinho:
    """Pomodoro Timer Application"""

    ICON_IDLE = resource_filename(__name__, 'icons/tomate-idle.png')
    ICON_POMO = resource_filename(__name__, 'icons/tomate-pomo.png')
    ICON_REST_S = resource_filename(__name__, 'icons/tomate-rest-s.png')
    ICON_REST_L = resource_filename(__name__, 'icons/tomate-rest-l.png')

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            appinfo.ID,
            self.ICON_IDLE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.menu = None
        self.build_menu()

        self.state = States.IDLE

        self.recorder = EventRecorder()
        self.timer = StateTimer()

    def build_menu(self):
        self.menu = Gtk.Menu()
        self.add_new_menu_item('Tomatar', self.start_pomodoro)
        self.add_new_menu_item('Pausa Curta', self.start_short_rest)
        self.add_new_menu_item('Pausa Longa', self.start_long_rest)
        self.add_new_menu_item('Parar', self.stop_timer)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.add_new_menu_item('Sobre', self.about_dialog)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.add_new_menu_item('Sair', self.quit)
        self.menu.show_all()

        self.indicator.set_menu(self.menu)
        Notify.init(appinfo.ID)

    def add_new_menu_item(self, text, action):
        menu_item = Gtk.MenuItem(text)
        menu_item.connect('activate', action)
        self.menu.append(menu_item)

    def start_pomodoro(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.POMODORO
        self.timer.start(25 * 60 * 1000, self.stop_timer)
        self.indicator.set_icon(self.ICON_POMO)
        self.notify('Tomatando (25m)', self.ICON_POMO)

    def start_short_rest(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.SHORT_REST
        self.timer.start(5 * 60 * 1000, self.stop_timer)
        self.indicator.set_icon(self.ICON_REST_S)
        self.notify('Pausa Curta (3m)', self.ICON_REST_S)

    def start_long_rest(self, source):
        if self.state != States.IDLE:
            self.recorder.record(self.state, False)

        self.state = States.LONG_REST
        self.timer.start(15 * 60 * 1000, self.stop_timer)
        self.indicator.set_icon(self.ICON_REST_L)
        self.notify('Pausa Longa (15m)', self.ICON_REST_L)

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
        self.indicator.set_icon(self.ICON_IDLE)
        self.notify('Contador Parado', self.ICON_IDLE)

    def notify(self, message, icon):
        Notify.Notification.new(appinfo.NAME, message, icon).show()

    def about_dialog(self, source):
        about_dialog = Gtk.AboutDialog(parent=Gtk.Window())
        about_dialog.set_destroy_with_parent(True)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.ICON_POMO)
        about_dialog.set_logo(pixbuf)
        about_dialog.set_program_name(appinfo.NAME)
        about_dialog.set_version(appinfo.VERSION)
        about_dialog.set_copyright(appinfo.COPYRIGHT)
        about_dialog.set_comments(appinfo.DESCRIPTION)
        about_dialog.set_authors([appinfo.AUTHOR])
        about_dialog.set_license_type(Gtk.License.MIT_X11)
        about_dialog.set_website(appinfo.SITE)
        about_dialog.run()
        about_dialog.destroy()

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
