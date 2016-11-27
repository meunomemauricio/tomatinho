"""About Dialog definition."""

from gi.repository import Gtk
from gi.repository import GdkPixbuf

from . import resources
from . import appinfo


def about_dialog(source):
    about_dialog = Gtk.AboutDialog(parent=Gtk.Window())
    about_dialog.set_destroy_with_parent(True)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(resources.ICON_POMO)
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
