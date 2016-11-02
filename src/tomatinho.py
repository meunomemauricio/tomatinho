#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import dbus
import gobject
import gtk
import os.path
import re
import sqlite3
import sys
import time

sqlite3.register_adapter(bool, int)
sqlite3.register_converter('BOOLEAN', lambda v: bool(int(v)))

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
HOME_DIR = os.path.expanduser('~')
TOMATINHO_DIR = os.path.join(HOME_DIR, '.tomatinho')


def start_database():
    if not os.path.exists(TOMATINHO_DIR):
        os.makedirs(TOMATINHO_DIR)

    conn = sqlite3.connect(os.path.join(TOMATINHO_DIR, 'tomatinho.db'))
    c = conn.cursor()

    # Create Statistics Table
    sql_cmd = ('CREATE TABLE statistics'
               '(oper TEXT, completed BOOLEAN, created TEXT)')
    try:
        c.execute(sql_cmd)
        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        # Table already Exists
        pass


class TomatinhoTimer(object):
    """Pomodoro Timer Application"""
    ICON_IDLE = os.path.join(CUR_DIR, 'icons/tomate-idle.png')
    ICON_POMO = os.path.join(CUR_DIR, 'icons/tomate-pomo.png')
    ICON_REST_S = os.path.join(CUR_DIR, 'icons/tomate-rest-s.png')
    ICON_REST_L = os.path.join(CUR_DIR, 'icons/tomate-rest-l.png')

    # States
    IDLE_STATE = 'Parado'
    POMO_STATE = 'Tomatando'
    REST_S_STATE = 'Pausa Curta'
    REST_L_STATE = 'Pausa Longa'

    # DBus for Desktop Notifications
    BUS_NAME = 'org.freedesktop.Notifications'
    OBJECT_PATH = '/org/freedesktop/Notifications'
    INTERFACE_NAME = 'org.freedesktop.Notifications'

    NOTIFICATION_TIME = 5000

    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file(self.ICON_IDLE)
        self.tray.set_tooltip('Status: Parado')

        self.state = self.IDLE_STATE

        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.connect('activate', self.on_left_click)

        self.timer_running = False
        self.time_left = 0

        self.statistics_db = sqlite3.connect(os.path.join(TOMATINHO_DIR, 'tomatinho.db'))

    def notify(self, summary):
        session_bus = dbus.SessionBus()
        obj = session_bus.get_object(self.BUS_NAME, self.OBJECT_PATH)

        interface = dbus.Interface(obj, self.INTERFACE_NAME)

        interface.Notify('', 0, '', summary, '', [], [], self.NOTIFICATION_TIME)

    def on_left_click(self, icon):
        self.tray.set_blinking(False)

    def on_right_click(self, icon, event_button, event_time):
        self.tray.set_blinking(False)

        menu = gtk.Menu()

        # Start Pomodoro
        menu_item = gtk.MenuItem('Tomatar')
        menu_item.show()
        menu.append(menu_item)
        menu_item.connect('activate', self.start_pomodoro)

        menu_item = gtk.MenuItem('Pausa Curta')
        menu_item.show()
        menu.append(menu_item)
        menu_item.connect('activate', self.start_short_rest)

        menu_item = gtk.MenuItem('Pausa Longa')
        menu_item.show()
        menu.append(menu_item)
        menu_item.connect('activate', self.start_long_rest)

        menu_item = gtk.MenuItem('Parar')
        menu_item.show()
        menu.append(menu_item)
        menu_item.connect('activate', self.stop_timer)

        # Separator
        separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.append(separator)

        # About dialog
        about = gtk.MenuItem('Sobre')
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

        separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.append(separator)

        # Add quit item
        quit = gtk.MenuItem('Sair')
        quit.show()
        menu.append(quit)
        quit.connect('activate', self.quit_application)

        menu.popup(None, None, gtk.status_icon_position_menu,
                   event_button, event_time, self.tray)

    def start_countdown_timer(self, start_time):
        if self.timer_running:
            gobject.source_remove(self.countdown_timer_id)

        # 1s Timer
        self.countdown_timer_id = gobject.timeout_add(1000, self.countdown)

        # Time left in seconds
        self.time_left = start_time
        self.update_tooltip()

        self.timer_running = True

    def stop_countdown_timer(self):
        if self.timer_running:
            gobject.source_remove(self.countdown_timer_id)
            self.timer_running = False

        self.update_tooltip()

    def countdown(self):
        self.time_left -= 1

        if self.time_left == 0:
            self.record_statistic(self.state, completed=True)
            self.tray.set_blinking(True)
            self.notify('Contador Parado.')
            self.tray.set_from_file(self.ICON_IDLE)
            self.state = self.IDLE_STATE
            self.stop_countdown_timer()
            return False

        self.update_tooltip()

        return True

    def update_tooltip(self):
        if self.state != self.IDLE_STATE:
            time_left = datetime.timedelta(seconds=self.time_left)
            tooltip = 'Status: {0} - Time Left: {1}'.format(self.state, time_left)
        else:
            tooltip = 'Status: {0}'.format(self.state)

        self.tray.set_tooltip(tooltip)

    def stop_timer(self, widge=None):
        self.notify('Contador Parado.')

        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.tray.set_from_file(self.ICON_IDLE)
        self.state = self.IDLE_STATE

        self.stop_countdown_timer()

    def start_pomodoro(self, widget=None):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.notify('Tomatando (25m)')

        self.tray.set_from_file(self.ICON_POMO)
        self.state = self.POMO_STATE
        self.start_countdown_timer(25 * 60)

    def start_short_rest(self, widget=None):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.notify('Pausa Curta (3m)')

        self.tray.set_from_file(self.ICON_REST_S)
        self.state = self.REST_S_STATE
        self.start_countdown_timer(3 * 60)

    def start_long_rest(self, widget=None):
        if self.state != self.IDLE_STATE:
            self.record_statistic(self.state, completed=False)

        self.notify('Pausa Longa (15m)')

        self.tray.set_from_file(self.ICON_REST_L)
        self.state = self.REST_L_STATE
        self.start_countdown_timer(15 * 60)

    def record_statistic(self, operation, completed):
        c = self.statistics_db.cursor()

        current_datetime = datetime.datetime.now()
        c.execute('INSERT INTO statistics VALUES (?, ?, ?)',
                  (operation, completed, current_datetime))

        self.statistics_db.commit()

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent (True)
        about_dialog.set_icon_name('Tomatinho Timer')
        about_dialog.set_name('Tomatinho Timer')
        about_dialog.set_version('0.1')
        about_dialog.set_copyright('(C) 2015 Mauricio Freitas')
        about_dialog.set_comments('Simples aplicativo temporizador para Técnica Pomodoro')
        about_dialog.set_authors(['Mauricio Freitas'])
        about_dialog.run()
        about_dialog.destroy()

    def quit_application(self, widget):
        self.stop_countdown_timer()
        gtk.main_quit()


if __name__ == '__main__':

    start_database()

    tomatinho = TomatinhoTimer()
    gtk.main()
