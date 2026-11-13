from typing import List, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Toolbar(QWidget):
    bookmarkClicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("topContainer")
        self.setup_ui()

    def setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Основная панель навигации
        nav_frame = QFrame()
        nav_frame.setObjectName("navBar")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(10, 6, 10, 6)
        nav_layout.setSpacing(6)

        self.back_button = QPushButton("←")
        self.back_button.setObjectName("navBtn")
        self.back_button.setToolTip("Назад (Alt+←)")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.forward_button = QPushButton("→")
        self.forward_button.setObjectName("navBtn")
        self.forward_button.setToolTip("Вперёд (Alt+→)")
        self.forward_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.reload_button = QPushButton("⟳")
        self.reload_button.setObjectName("navBtn")
        self.reload_button.setToolTip("Перезагрузить (Ctrl+R / F5)")
        self.reload_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.home_button = QPushButton("⌂")
        self.home_button.setObjectName("navBtn")
        self.home_button.setToolTip("Домашний дашборд (Alt+Home)")
        self.home_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Адресная строка (Omnibox)
        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setPlaceholderText("Введите адрес сайта или поисковый запрос...")

        self.bookmark_button = QPushButton("☆")
        self.bookmark_button.setObjectName("navBtn")
        self.bookmark_button.setToolTip("Добавить/удалить закладку (Ctrl+D)")
        self.bookmark_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setObjectName("newTabBtn")
        self.new_tab_button.setToolTip("Новая вкладка (Ctrl+T)")
        self.new_tab_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.fullscreen_button = QPushButton("⛶")
        self.fullscreen_button.setObjectName("navBtn")
        self.fullscreen_button.setToolTip("Полный экран / Cinema Mode (F11)")
        self.fullscreen_button.setCursor(Qt.CursorShape.PointingHandCursor)

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar, 1)
        nav_layout.addWidget(self.bookmark_button)
        nav_layout.addWidget(self.new_tab_button)
        nav_layout.addWidget(self.fullscreen_button)

        root_layout.addWidget(nav_frame)

        # Панель быстрых закладок
        self.bookmarks_bar = QFrame()
        self.bookmarks_bar.setObjectName("bookmarksBar")
        self.bookmarks_layout = QHBoxLayout(self.bookmarks_bar)
        self.bookmarks_layout.setContentsMargins(12, 2, 12, 4)
        self.bookmarks_layout.setSpacing(6)
        self.bookmarks_layout.addStretch()
        root_layout.addWidget(self.bookmarks_bar)

        # Тонкий прогресс-бар загрузки страницы
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("loadProgress")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(2)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        root_layout.addWidget(self.progress_bar)

    def update_bookmarks(self, bookmarks: List[Dict[str, str]]):
        while self.bookmarks_layout.count():
            item = self.bookmarks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for bm in bookmarks:
            name = bm.get("name", "Bookmark")
            url = bm.get("url", "")
            btn = QPushButton(name)
            btn.setObjectName("bookmarkItem")
            btn.setToolTip(url)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _=False, u=url: self.bookmarkClicked.emit(u))
            self.bookmarks_layout.addWidget(btn)

        self.bookmarks_layout.addStretch()
        self.bookmarks_bar.setVisible(len(bookmarks) > 0)

    def set_bookmarked_state(self, is_bookmarked: bool):
        self.bookmark_button.setText("★" if is_bookmarked else "☆")
        self.bookmark_button.setProperty("bookmarked", is_bookmarked)
        self.bookmark_button.style().unpolish(self.bookmark_button)
        self.bookmark_button.style().polish(self.bookmark_button)
