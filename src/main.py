#!/usr/bin/env python3
import os
from pathlib import Path
import signal
import json

from entries import ImageEntry, find_all_entries, availible_backends

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = "gtk-theme-switcher-widget"
current_theme = None
setup_lock = True


def main():
	icon_rel_path = Path("res/palette.png")
	icon_path = Path(__file__).parent.parent.joinpath(icon_rel_path).absolute()

	indicator = appindicator.Indicator.new(
		APPINDICATOR_ID,
		str(icon_path),
		appindicator.IndicatorCategory.SYSTEM_SERVICES
	)
	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	indicator.set_menu(build_menu(indicator))
	# notify.init(APPINDICATOR_ID)
	gtk.main()


def build_pywal_backend_select(menu):
	def act_factory(backend: str):
		def inner(_):
			ImageEntry.PYWAL_OPTIONS = ["--backend", backend]
			if current_theme is not None:
				current_theme.pywal_switch()
		return inner

	group = []
	for backend, availible in [("wal", True)] + list(availible_backends().items()):
		item = gtk.RadioMenuItem.new_with_label(group, backend)
		group = item.get_group()
		item.set_sensitive(availible)

		item.connect("activate", act_factory(backend))
		menu.append(item)


def build_menu(indicator):
	global setup_lock
	setup_lock = True

	entries = find_all_entries()
	menu = gtk.Menu()

	def append_sep(menu: gtk.Menu):
		sep = gtk.SeparatorMenuItem()
		menu.append(sep)

	def act_factory(entry: ImageEntry):
		def inner(_):
			if setup_lock: return
			entry.pywal_switch()
			global current_theme
			current_theme = entry
		return inner

	group = []
	image_entry_menu_items = []
	for entry in entries:
		item = gtk.RadioMenuItem.new_with_label(group, entry.label)
		group = item.get_group()
		item.connect("activate", act_factory(entry))
		menu.append(item)
		image_entry_menu_items.append((entry, item))

	try:
		with open(os.path.expanduser("~/.cache/wal/colors.json")) as file:
			data = json.load(file)
			current_wallpaper_path = data["wallpaper"]

			global current_theme
			for entry, radio in image_entry_menu_items:
				if str(entry.path) == current_wallpaper_path:
					current_theme = entry
					radio.set_active(True)
					break

	except OSError as e:
		pass

	append_sep(menu)
	build_pywal_backend_select(menu)
	append_sep(menu)

	def refresh(_):
		new_menu = build_menu(indicator)
		indicator.set_menu(new_menu)

	item_refresh = gtk.MenuItem(label="Refresh")
	item_refresh.connect("activate", refresh)
	menu.append(item_refresh)

	item_quit = gtk.MenuItem(label="Quit")
	item_quit.connect("activate", exit_application)
	menu.append(item_quit)

	menu.show_all()

	setup_lock = False
	return menu


def exit_application(_):
	# notify.uninit()
	gtk.main_quit()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()
