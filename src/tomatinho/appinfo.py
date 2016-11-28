"""File to store App Information

Used to generate About page and package information.
"""

import os.path

# General information
ID = 'com.github.meunomemauricio.tomatinho'
NAME = 'Tomatinho'
COPYRIGHT = '(C) 2016 Mauricio Freitas'
VERSION = '0.1'
DESCRIPTION = 'GTK Pomodoro Timer application'
LICENSE = 'MIT'
AUTHOR = 'Mauricio Freitas'
SITE = 'https://github.com/meunomemauricio/tomatinho'

# Application Directories
HOME_DIR = os.path.expanduser('~')
USER_DIR = os.path.join(HOME_DIR, '.tomatinho')
APP_DIR = '/usr/share/tomatinho'
ICONS_DIR = os.path.join(APP_DIR, 'icons')

# Locale Info
LOCALE_DIR = '/usr/share/locale/'
GETTEXT_ID = 'tomatinho'

# Icons location
ICON_IDLE = os.path.join(ICONS_DIR, 'tomate-idle.png')
ICON_POMO = os.path.join(ICONS_DIR, 'tomate-pomo.png')
ICON_REST_S = os.path.join(ICONS_DIR, 'tomate-rest-s.png')
ICON_REST_L = os.path.join(ICONS_DIR, 'tomate-rest-l.png')
