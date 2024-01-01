# pywal-theme-switcher-widget

Switches the terminal theme using `pywal`

## Install

```bash
git clone https://github.com/Infinnitor/pywal-theme-switcher-widget
cd pywal-theme-switcher-widget
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
python3 src/main.py
```

## Configuration

By default the program loads wallpaper images from `~/Pictures/wallpapers`. Simply place, jpg/jpeg or png images in there and they will be availible to select from the menu.

You can configure the paths it loads from by editing `~/.config/pywal-theme-switcher-widget/config.txt`

Each path should be on a seperate line, and should point to a folder where images will be contained.


## Create .desktop file for the current user
```bash
./create_desktop_file.sh > ~/.local/share/applications/pywal-theme-switcher-widget.desktop
```

## Create an autostart .desktop file for the current user
```bash
./create_desktop_file.sh > ~/.config/autostat/pywal-theme-switcher-widget.desktop
```
