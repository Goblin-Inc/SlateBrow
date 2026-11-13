#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

echo "=== Установка зависимостей SlateBrow ==="
if command -v pacman >/dev/null 2>&1; then
    echo "-> Обнаружен Arch Linux (pacman)"
    sudo pacman -S --needed python pyside6 qt6-webengine qt6-multimedia-ffmpeg
elif command -v apt >/dev/null 2>&1; then
    echo "-> Обнаружен Debian/Ubuntu (apt)"
    sudo apt update
    sudo apt install -y python3 python3-pyside6.qtwebenginewidgets python3-pyside6.qtwebenginecore
elif command -v dnf >/dev/null 2>&1; then
    echo "-> Обнаружен Fedora (dnf)"
    sudo dnf install -y python3 python3-pyside6
fi

mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications" "$HOME/.local/share/icons/hicolor/scalable/apps"
ln -sf "$DIR/run.sh" "$HOME/.local/bin/slatebrow"
if [ -f "$DIR/assets/icon.svg" ]; then
    cp -f "$DIR/assets/icon.svg" "$HOME/.local/share/icons/hicolor/scalable/apps/slatebrow.svg"
fi

cat << DESKTOP > "$HOME/.local/share/applications/slatebrow.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=SlateBrow
GenericName=Web Browser
Comment=Minimalist Dark Slate Web Browser with H.264/AAC Live Stream Support
Exec=$DIR/run.sh %U
Icon=slatebrow
Terminal=false
Categories=Network;WebBrowser;
DESKTOP
chmod +x "$HOME/.local/share/applications/slatebrow.desktop"

echo "=== Готово! Запускайте через ./run.sh, команду 'slatebrow' или ярлык в меню приложений ==="
