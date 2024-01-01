#!/usr/bin/env bash
ENTRY_PATH=$PWD"/src/main.py"
ICON_PATH=$PWD"/res/palette.png"

echo "[Desktop Entry]"
echo "Name=Pywal Theme Switcher Widget"
echo "Comment=Theme switcher using pywal"
echo "Exec=$ENTRY_PATH"
echo "Icon=$ICON_PATH"
echo "Terminal=false"
echo "Type=Application"
echo "Categories=Widget;"
