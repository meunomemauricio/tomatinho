"""File to store App Information

Used to generate About page and package information.
"""

from pathlib import Path

# General information
# TODO: Load from project config
ID = "tomatinho"
NAME = "Tomatinho"
COPYRIGHT = "(C) 2016 Mauricio Freitas"
VERSION = "0.2"
DESCRIPTION = "GTK Pomodoro Timer application"
LICENSE = "MIT"
AUTHOR = "Mauricio Freitas"
SITE = "https://github.com/meunomemauricio/tomatinho"

# Application Directories
HOME_DIR = Path.home()
USER_DIR = HOME_DIR / ".tomatinho"
BASE_DIR = Path(__file__).parent  # TODO: Will it change with setuptools?
RESOURCES_DIR = BASE_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
# TODO: Fix locale directory
LOCALE_DIR = "/usr/share/locale/"

# Icons location
# NOTE: Converted to str, since GTK can't take Path directly
ICON_IDLE = str(ICONS_DIR / "tomate-idle.png")
ICON_POMO = str(ICONS_DIR / "tomate-pomo.png")
ICON_REST_S = str(ICONS_DIR / "tomate-rest-s.png")
ICON_REST_L = str(ICONS_DIR / "tomate-rest-l.png")
