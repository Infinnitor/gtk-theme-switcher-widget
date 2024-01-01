from dataclasses import dataclass
import os
import subprocess
from pathlib import Path
from typing import Union, List, Dict
import itertools
import shutil


@dataclass(slots=True, frozen=True)
class ImageEntry:
	label: str
	path: Path

	ACCEPTED_SUFFIXES = [".jpg", ".jpeg", ".png"]
	PYWAL_OPTIONS = []

	@classmethod
	def from_path(cls, given_path: Union[str, Path]):
		path = Path(given_path)
		if not path.is_file():
			raise ValueError("Path must point to a file")
		if path.suffix not in ImageEntry.ACCEPTED_SUFFIXES:
			raise ValueError("Image must be a JPG or a PNG")

		return cls(label=path.name, path=path)

	def pywal_switch(self):
		wal_command = [
			# "wal",
			WAL_PATH,
			"-i",
			str(self.path),
			*ImageEntry.PYWAL_OPTIONS
		]

		background_change_command = [
			"gsettings",
			"set",
			"org.gnome.desktop.background",
			"picture-uri-dark",
			f"\"file://{self.path.absolute()}\""
		]

		subprocess.run(background_change_command, capture_output=True)
		subprocess.run(wal_command, capture_output=True)


def find_all_entries() -> List[ImageEntry]:
	DEFAUlt_PATH_STR = "~/Pictures/wallpapers/"
	paths = [Path(DEFAUlt_PATH_STR).expanduser()]

	CONFIG_PATH = Path("~/.config/pywal-theme-switcher-widget/config.txt").expanduser()

	if not CONFIG_PATH.exists():
		if not CONFIG_PATH.parent.exists():
			CONFIG_PATH.parent.mkdir()
		try:
			with CONFIG_PATH.open("w+") as file:
				file.write(DEFAUlt_PATH_STR + "\n")
		except OsError as e:
			pass

	else:
		paths = []
		try:
			with CONFIG_PATH.open("r") as file:
				paths.extend(map(Path, (line.rstrip() for line in file.readlines())))
		except OsError as e:
			pass

	entries = []
	for path in (p.expanduser() for p in paths):
		for pattern in ImageEntry.ACCEPTED_SUFFIXES:
			for entry_path in path.glob("*" + pattern):
				entries.append(ImageEntry.from_path(Path(entry_path)))

	return sorted(entries, key=lambda p: p.label)


def availible_backends() -> Dict[str, bool]:
	BACKENDS = ("colorthief", "colorz")
	# lol havent got this shit working yet
	# return { k: v is not None for k, v in zip(BACKENDS, map(shutil.which, BACKENDS)) }
	return { k: True for k in BACKENDS }


def get_wal_path() -> Path:
	base = Path(os.path.abspath(__file__)).parent
	wal_path = base.parent.joinpath("venv/bin/wal")
	if not (wal_path.exists() and wal_path.is_file()):
		sys_wal = shutil.which("wal")
		if sys_wal is not None:
			return sys_wal
		print("E: Could not find wal in venv or in path. Did you run 'pip -r requirements.txt' in the venv?")
	return wal_path


WAL_PATH = str(get_wal_path())


if __name__ == "__main__":
	print(find_all_entries())
