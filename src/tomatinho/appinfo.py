"""File to store App Information

Used to generate About page and package information.
"""

import os.path

# General information
ID = 'tomatinho'
NAME = 'Tomatinho'
COPYRIGHT = '(C) 2016 Mauricio Freitas'
VERSION = '0.1'
DESCRIPTION = 'GTK Pomodoro Timer application'
LICENSE = 'MIT'
AUTHOR = 'Mauricio Freitas'
SITE = 'https://github.com/meunomemauricio/tomatinho'

# Application Directories
HOME_DIR = os.path.expanduser('~')
APP_DIR = os.path.join(HOME_DIR, '.tomatinho')
