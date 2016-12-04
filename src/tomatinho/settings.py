"""For settings access and displaying the Settings Dialog.

Settings are stored using GSettings.
"""

from gi.repository import Gio
from gi.repository import Gtk

from . import appinfo
from . locale import _


class Settings(Gio.Settings):
    """Makes the GSettings available as properties."""

    def __init__(self):
        super(Settings, self).__init__(appinfo.ID)
        self.delay()

    def bind(self, set, widget, pty, flags=Gio.SettingsBindFlags.DEFAULT):
        """Makes the flags argument optional."""
        super(Settings, self).bind(set, widget, pty, flags)

    @property
    def pomo_intvl(self):
        return self.get_int('pomo-intvl')

    @property
    def s_rest_intvl(self):
        return self.get_int('s-rest-intvl')

    @property
    def l_rest_intvl(self):
        return self.get_int('l-rest-intvl')


class SettingsDialog(Gtk.Dialog):

    def __init__(self):
        super(SettingsDialog, self).__init__(_('Settings'), Gtk.Window())
        self.add_button(_('Cancel'), Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.settings = Settings()
        self._build_content()

    def _build_content(self):
        nb = Gtk.Notebook()
        nb.append_page(self._timers_grid, Gtk.Label(_('Timers')))

        box = self.get_content_area()
        box.add(nb)
        box.show_all()

    @property
    def _timers_grid(self):
        self._create_timers_spin_buttons()
        self._create_timers_labels()

        timers_grid = Gtk.Grid()
        timers_grid.attach(self.pomo_label, 0, 0, 1, 1)
        timers_grid.attach(self.pomo_entry, 1, 0, 1, 1)
        timers_grid.attach(self.s_rest_label, 0, 1, 1, 1)
        timers_grid.attach(self.s_rest_entry, 1, 1, 1, 1)
        timers_grid.attach(self.l_rest_label, 0, 2, 1, 1)
        timers_grid.attach(self.l_rest_entry, 1, 2, 1, 1)

        timers_grid.set_column_spacing(50)
        timers_grid.set_row_spacing(5)
        timers_grid.set_margin_top(20)
        timers_grid.set_margin_bottom(20)
        timers_grid.set_margin_left(10)
        timers_grid.set_margin_right(10)

        return timers_grid

    def _create_timers_labels(self):
        self.pomo_label = Gtk.Label(_('Pomodoro') + ':')
        self.s_rest_label = Gtk.Label(_('Short Pause') + ':')
        self.l_rest_label = Gtk.Label(_('Long Break') + ':')

        # Align labels to the left instead of center
        self.pomo_label.set_halign(Gtk.Align.START)
        self.s_rest_label.set_halign(Gtk.Align.START)
        self.l_rest_label.set_halign(Gtk.Align.START)

    def _create_timers_spin_buttons(self):
        self.pomo_entry = Gtk.SpinButton()
        self.pomo_entry.set_range(1, 120)
        self.pomo_entry.set_increments(1, 5)

        self.s_rest_entry = Gtk.SpinButton()
        self.s_rest_entry.set_range(1, 15)
        self.s_rest_entry.set_increments(1, 5)

        self.l_rest_entry = Gtk.SpinButton()
        self.l_rest_entry.set_range(1, 30)
        self.l_rest_entry.set_increments(1, 5)

        self.settings.bind('pomo-intvl', self.pomo_entry, 'value')
        self.settings.bind('s-rest-intvl', self.s_rest_entry, 'value')
        self.settings.bind('l-rest-intvl', self.l_rest_entry, 'value')

    @classmethod
    def display(cls, source):
        """Display the dialog and apply config changes on OK."""
        dialog = cls()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.settings.apply()
        else:
            dialog.settings.revert()
        dialog.destroy()
