"""I18N utilities."""

import gettext

from tomatinho import appinfo

gettext.bindtextdomain(appinfo.ID, appinfo.LOCALE_DIR)
gettext.textdomain(appinfo.ID)
_ = gettext.gettext
