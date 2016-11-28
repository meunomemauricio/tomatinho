"""I18N utilities."""

import gettext

from . import appinfo

gettext.bindtextdomain(appinfo.GETTEXT_ID, appinfo.LOCALE_DIR)
gettext.textdomain(appinfo.GETTEXT_ID)
_ = gettext.gettext
