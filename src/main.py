#!/usr/bin/env python3
import os
import signal

from entries import ImageEntry, find_all_entries, availible_backends

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = "gnome-pywal-switcher"

current_theme = None


def main():
	indicator = appindicator.Indicator.new(
		APPINDICATOR_ID,
		# os.path.abspath("/home/.local/share/icons/hicolor/256x256/apps/palette.png"),
		os.path.abspath("res/palette.png"),
		appindicator.IndicatorCategory.SYSTEM_SERVICES
	)
	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	indicator.set_menu(build_menu(indicator))
	gtk.main()


def build_pywal_backend_select(menu):
	def act_factory(backend: str):
		def inner(_):
			ImageEntry.PYWAL_OPTIONS = ["--backend", backend]
			if current_theme is not None:
				current_theme.pywal_switch()
		return inner

	group = []

	av_backends = [("wal", True)] + list(availible_backends().items())

	for backend, availible in av_backends:
		item = gtk.RadioMenuItem.new_with_label(group, backend)
		group = item.get_group()
		item.set_sensitive(availible)

		item.connect("activate", act_factory(backend))
		menu.append(item)


def build_menu(indicator):
	entries = find_all_entries()
	menu = gtk.Menu()

	def append_sep(menu: gtk.Menu):
		sep = gtk.SeparatorMenuItem()
		menu.append(sep)

	def act_factory(entry: ImageEntry):
		def inner(_):
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
		image_entry_menu_items.append(item)

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
	item_quit.connect("activate", gtk.main_quit)
	menu.append(item_quit)

	menu.show_all()
	return menu


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()
