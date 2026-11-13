import os
import sys

# Подключаем флаги аппаратного декодирования и мультимедиа до инициализации QtWebEngine
os.environ.setdefault(
    "QTWEBENGINE_CHROMIUM_FLAGS",
    "--autoplay-policy=no-user-gesture-required "
    "--enable-features=PlatformHEVCDecoderSupport,VaapiVideoDecodeLinuxGL "
    "--ignore-gpu-blocklist "
    "--enable-gpu-rasterization "
    "--enable-smooth-scrolling",
)

from PySide6.QtWidgets import QApplication
from ui.browser import BrowserWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SlateBrow")

    window = BrowserWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
