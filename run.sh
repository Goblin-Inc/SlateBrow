#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$DIR"
export QTWEBENGINE_CHROMIUM_FLAGS="--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-features=VaapiVideoDecoder,VaapiVideoEncoder --autoplay-policy=no-user-gesture-required --no-sandbox"

# 1. Проверяем системный /usr/bin/python3 первым (чтобы mise / pyenv / conda в $PATH не перехватывали вызов)
for PY in /usr/bin/python3 "$DIR/.venv/bin/python" python3; do
    if command -v "$PY" >/dev/null 2>&1 && "$PY" -c "import PySide6.QtWebEngineWidgets" >/dev/null 2>&1; then
        exec "$PY" "$DIR/main.py" "$@"
    fi
done

echo "PySide6 не найден ни в /usr/bin/python3, ни в окружении! Запустите ./install.sh или установите:"
echo "  Arch Linux:    sudo pacman -S python pyside6 qt6-webengine qt6-multimedia-ffmpeg"
echo "  Ubuntu/Debian: sudo apt install python3-pyside6.qtwebenginewidgets python3-pyside6.qtwebenginecore"
exit 1
