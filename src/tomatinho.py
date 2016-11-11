#! /usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import os.path
import signal
import sqlite3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk  # noqa: E402
from gi.repository import AppIndicator3  # noqa: E402
from gi.repository import Notify  # noqa: E402
from gi.repository import GObject  # noqa: E402

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
HOME_DIR = os.path.expanduser('~')
TOMATINHO_DIR = os.path.join(HOME_DIR, '.tomatinho')


def start_database():
    if not os.path.exists(TOMATINHO_DIR):
        os.makedirs(TOMATINHO_DIR)

    conn = sqlite3.connect(os.path.join(TOMATINHO_DIR, 'tomatinho.db'))
    cursor = conn.cursor()

    # Create Statistics Table
    sql_cmd = ('CREATE TABLE statistics'
               '(oper TEXT, completed BOOLEAN, datetime TEXT)')
    try:
        cursor.execute(sql_cmd)
        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        # Table already Exists
        pass


class Tomatinho(object):
    """Pomodoro Timer Application"""

    # GTK Variables
    APPINDICATOR_ID = "tomatinho"

    # Icons
    ICON_IDLE = os.path.join(CUR_DIR, 'icons/tomate-idle.png')
    ICON_POMO = os.path.join(CUR_DIR, 'icons/tomate-pomo.png')
    ICON_REST_S = os.path.join(CUR_DIR, 'icons/tomate-rest-s.png')
    ICON_REST_L = os.path.join(CUR_DIR, 'icons/tomate-rest-l.png')

    # States
    IDLE_STATE = 'Parado'
    POMO_STATE = 'Tomatando'
    REST_S_STATE = 'Pausa Curta'
    REST_L_STATE = 'Pausa Longa'

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            self.APPINDICATOR_ID,
            self.ICON_IDLE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.menu = None
        self.build_menu()

        self.state = self.IDLE_STATE
        self.timer_running = False
        self.time_left = 0

        self.countdown_timer_id = None

        self.statistics_db = sqlite3.connect(
            os.path.join(TOMATINHO_DIR, 'tomatinho.db'))

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
        Notify.init(self.APPINDICATOR_ID)

    def add_new_menu_item(self, text, action):
        menu_item = Gtk.MenuItem(text)
        menu_item.connect('activate', action)
        self.menu.append(menu_item)

    def start_countdown_timer(self, start_time):
        if self.timer_running:
            GObject.source_remove(self.countdown_timer_id)

        # 1s Timer
        self.countdown_timer_id = GObject.timeout_add(1000, self.countdown)

        # Time left in seconds
        self.time_left = start_time
        self.timer_running = True

    def stop_countdown_timer(self):
        if self.timer_running:
            GObject.source_remove(self.countdown_timer_id)
            self.timer_running = False

    def countdown(self):
        self.time_left -= 1

        if self.time_left == 0:
            self.record_statistic(self.state, completed=True)
            self.state = self.IDLE_STATE
            self.stop_countdown_timer()
            self.indicator.set_icon(self.ICON_IDLE)
            self.notify('Contador Parado', self.ICON_IDLE)
            return False

        return True

    def start_pomodoro(self, source):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.state = self.POMO_STATE
        self.start_countdown_timer(25 * 60)
        self.indicator.set_icon(self.ICON_POMO)
        self.notify('Tomatando (25m)', self.ICON_POMO)

    def start_short_rest(self, source):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.state = self.REST_S_STATE
        self.start_countdown_timer(3 * 60)
        self.indicator.set_icon(self.ICON_REST_S)
        self.notify('Pausa Curta (3m)', self.ICON_REST_S)

    def start_long_rest(self, source):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.state = self.REST_S_STATE
        self.start_countdown_timer(3 * 60)
        self.indicator.set_icon(self.ICON_REST_L)
        self.notify('Pausa Longa (15m)', self.ICON_REST_L)

    def stop_timer(self, source):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.state = self.IDLE_STATE
        self.stop_countdown_timer()
        self.indicator.set_icon(self.ICON_IDLE)
        self.notify('Contador Parado', self.ICON_IDLE)

    def notify(self, message, icon):
        Notify.Notification.new('Tomatinho', message, icon).show()

    def record_statistic(self, operation, completed):
        current_datetime = datetime.datetime.now()
        self.statistics_db.cursor().execute(
            'INSERT INTO statistics VALUES (?, ?, ?)',
            (operation, completed, current_datetime)
        )
        self.statistics_db.commit()

    def about_dialog(self, source):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name('Tomatinho Timer')
        about_dialog.set_name('Tomatinho Timer')
        about_dialog.set_version('0.1')
        about_dialog.set_copyright('(C) 2016 Mauricio Freitas')
        about_dialog.set_comments('Simples aplicativo temporizador para '
                                  'Técnica Pomodoro')
        about_dialog.set_authors(['Mauricio Freitas'])
        about_dialog.run()
        about_dialog.destroy()

    def quit(self, source):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        Gtk.main_quit()


def main():
    # Enable quiting the app with ^C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    start_database()
    Tomatinho()
    Gtk.main()


if __name__ == "__main__":
    main()
