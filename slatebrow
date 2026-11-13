#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$DIR"
export QTWEBENGINE_CHROMIUM_FLAGS="--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-features=VaapiVideoDecoder,VaapiVideoEncoder --autoplay-policy=no-user-gesture-required --no-sandbox"

if python3 -c "import PySide6.QtWebEngineWidgets" >/dev/null 2>&1; then
    exec python3 "$DIR/main.py" "$@"
elif [ -x "$DIR/.venv/bin/python" ]; then
    exec "$DIR/.venv/bin/python" "$DIR/main.py" "$@"
else
    echo "PySide6 не найден! Запустите ./install.sh или установите пакет:"
    echo "  Arch Linux:    sudo pacman -S python pyside6 qt6-webengine qt6-multimedia-ffmpeg"
    echo "  Ubuntu/Debian: sudo apt install python3-pyside6.qtwebenginewidgets python3-pyside6.qtwebenginecore"
    exit 1
fi
