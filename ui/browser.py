from pathlib import Path
from typing import List
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.browser_logic import (
    SlateWebPage,
    configure_web_view_settings,
    create_browser_profile,
    generate_dashboard_html,
    resolve_user_input,
)
from core.config import config
from ui.shortcuts import setup_shortcuts
from ui.toolbar import Toolbar


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cinema_mode = False
        self.closed_tabs_stack: List[str] = []
        self.profile = create_browser_profile(self)

        self.setup_window()
        self.load_stylesheet()
        self.setup_ui()
        self.connect_signals()
        setup_shortcuts(self)

    def setup_window(self):
        self.setWindowTitle("SlateBrow")
        self.resize(1280, 820)

    def load_stylesheet(self):
        qss_path = Path(__file__).resolve().parent.parent / "assets" / "style.qss"
        if qss_path.exists():
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = Toolbar()
        self.toolbar.update_bookmarks(config.bookmarks)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.tabs, 1)
        self.setCentralWidget(central_widget)

        # Открываем первую стартовую вкладку
        self.add_new_tab(config.get("homepage", "slate://home"))

    def connect_signals(self):
        self.toolbar.url_bar.returnPressed.connect(self.load_url_from_bar)
        self.toolbar.back_button.clicked.connect(self.go_back)
        self.toolbar.forward_button.clicked.connect(self.go_forward)
        self.toolbar.reload_button.clicked.connect(self.reload_page)
        self.toolbar.home_button.clicked.connect(self.go_home)
        self.toolbar.new_tab_button.clicked.connect(lambda: self.add_new_tab())
        self.toolbar.bookmark_button.clicked.connect(self.toggle_current_bookmark)
        self.toolbar.fullscreen_button.clicked.connect(self.toggle_fullscreen_mode)
        self.toolbar.bookmarkClicked.connect(self.navigate_current_tab)

        self.tabs.currentChanged.connect(self.update_current_tab)
        self.tabs.tabCloseRequested.connect(self.close_tab)

    def add_new_tab(self, url: str | None = "slate://home", switch_to: bool = True) -> QWebEngineView:
        web_view = QWebEngineView()
        page = SlateWebPage(self.profile, self, web_view)
        web_view.setPage(page)
        configure_web_view_settings(web_view.settings())

        # Сигналы только для активной вкладки (исправляет рассинхрон URL-бара)
        web_view.urlChanged.connect(
            lambda qurl, browser=web_view: self.on_view_url_changed(browser, qurl)
        )
        web_view.titleChanged.connect(
            lambda title, browser=web_view: self.update_tab_title(browser, title)
        )
        web_view.titleChanged.connect(
            lambda title, browser=web_view: self.update_window_title(browser, title)
        )
        web_view.loadProgress.connect(
            lambda progress, browser=web_view: self.on_load_progress(browser, progress)
        )
        web_view.loadFinished.connect(
            lambda ok, browser=web_view: self.on_load_finished(browser, ok)
        )
        page.fullScreenRequested.connect(self.handle_fullscreen_request)

        index = self.tabs.addTab(web_view, "Новая вкладка")
        if switch_to:
            self.tabs.setCurrentIndex(index)

        if url is not None:
            self.navigate_view(web_view, url)

        return web_view

    def navigate_view(self, web_view: QWebEngineView, target: str):
        resolved = resolve_user_input(target)
        if resolved == "slate://home":
            web_view.setHtml(generate_dashboard_html(), QUrl("slate://home"))
            if web_view == self.current_web_view():
                self.toolbar.url_bar.clear()
                self.toolbar.set_bookmarked_state(False)
        else:
            web_view.setUrl(QUrl(resolved))

    def navigate_current_tab(self, target: str):
        view = self.current_web_view()
        if view:
            self.navigate_view(view, target)

    def load_url_from_bar(self):
        raw_text = self.toolbar.url_bar.text().strip()
        if not raw_text:
            return
        self.navigate_current_tab(raw_text)

    def go_home(self):
        self.navigate_current_tab("slate://home")

    def on_view_url_changed(self, browser: QWebEngineView, qurl: QUrl):
        if browser != self.current_web_view():
            return
        url_str = qurl.toString()
        if url_str in ("slate://home", "about:blank") or url_str.startswith("data:"):
            self.toolbar.url_bar.clear()
            self.toolbar.set_bookmarked_state(False)
        else:
            self.toolbar.url_bar.setText(url_str)
            self.toolbar.url_bar.setCursorPosition(0)
            self.toolbar.set_bookmarked_state(config.is_bookmarked(url_str))

    def on_load_progress(self, browser: QWebEngineView, progress: int):
        if browser != self.current_web_view():
            return
        if 0 < progress < 100:
            self.toolbar.progress_bar.show()
            self.toolbar.progress_bar.setValue(progress)
        else:
            self.toolbar.progress_bar.hide()

    def on_load_finished(self, browser: QWebEngineView, _ok: bool):
        if browser == self.current_web_view():
            self.toolbar.progress_bar.hide()

    def current_web_view(self) -> QWebEngineView | None:
        return self.tabs.currentWidget()

    def go_back(self):
        view = self.current_web_view()
        if view:
            view.back()

    def go_forward(self):
        view = self.current_web_view()
        if view:
            view.forward()

    def reload_page(self):
        view = self.current_web_view()
        if view:
            if view.url().toString() == "slate://home":
                self.navigate_view(view, "slate://home")
            else:
                view.reload()

    def hard_reload_page(self):
        view = self.current_web_view()
        if view:
            view.page().triggerAction(QWebEnginePage.WebAction.ReloadAndBypassCache)

    def update_current_tab(self):
        web_view = self.current_web_view()
        if web_view:
            self.on_view_url_changed(web_view, web_view.url())
            self.update_window_title(web_view, web_view.title())

    def update_tab_title(self, browser: QWebEngineView, title: str):
        index = self.tabs.indexOf(browser)
        if index != -1:
            clean = (title or "Новая вкладка").strip()
            short_title = (clean[:24] + "…") if len(clean) > 25 else clean
            self.tabs.setTabText(index, short_title)
            self.tabs.setTabToolTip(index, clean)

    def update_window_title(self, browser: QWebEngineView, title: str):
        if browser == self.current_web_view():
            if title:
                self.setWindowTitle(f"{title} — SlateBrow")
            else:
                self.setWindowTitle("SlateBrow")

    def close_tab(self, index: int):
        widget: QWebEngineView = self.tabs.widget(index)
        if widget:
            url_str = widget.url().toString()
            if url_str and url_str not in ("slate://home", "about:blank"):
                self.closed_tabs_stack.append(url_str)

        if self.tabs.count() == 1:
            self.navigate_view(widget, "slate://home")
            return

        self.tabs.removeTab(index)
        if widget:
            widget.deleteLater()

    def close_current_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def reopen_closed_tab(self):
        if self.closed_tabs_stack:
            last_url = self.closed_tabs_stack.pop()
            self.add_new_tab(last_url, switch_to=True)

    def switch_relative_tab(self, delta: int):
        count = self.tabs.count()
        if count > 1:
            next_idx = (self.tabs.currentIndex() + delta) % count
            self.tabs.setCurrentIndex(next_idx)

    def switch_to_tab_index(self, idx: int):
        if 0 <= idx < self.tabs.count():
            self.tabs.setCurrentIndex(idx)

    def switch_to_last_tab(self):
        if self.tabs.count() > 0:
            self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def focus_url_bar(self):
        if self.cinema_mode:
            self.exit_cinema_mode()
        self.toolbar.url_bar.setFocus()
        self.toolbar.url_bar.selectAll()

    def toggle_current_bookmark(self):
        view = self.current_web_view()
        if not view:
            return
        url_str = view.url().toString()
        if not url_str or url_str in ("slate://home", "about:blank"):
            return
        added = config.toggle_bookmark(view.title() or url_str, url_str)
        self.toolbar.set_bookmarked_state(added)
        self.toolbar.update_bookmarks(config.bookmarks)

    def toggle_bookmarks_bar(self):
        visible = not self.toolbar.bookmarks_bar.isVisible()
        self.toolbar.bookmarks_bar.setVisible(visible)

    def adjust_zoom(self, delta: float):
        view = self.current_web_view()
        if view:
            new_zoom = max(0.25, min(5.0, round(view.zoomFactor() + delta, 2)))
            view.setZoomFactor(new_zoom)

    def reset_zoom(self):
        view = self.current_web_view()
        if view:
            view.setZoomFactor(1.0)

    def handle_fullscreen_request(self, request):
        request.accept()
        if request.toggleOn():
            self.enter_cinema_mode()
        else:
            self.exit_cinema_mode()

    def toggle_fullscreen_mode(self):
        if self.cinema_mode or self.isFullScreen():
            self.exit_cinema_mode()
        else:
            self.enter_cinema_mode()

    def enter_cinema_mode(self):
        self.cinema_mode = True
        self.toolbar.hide()
        self.tabs.tabBar().hide()
        self.showFullScreen()

    def exit_cinema_mode(self):
        if not self.cinema_mode and not self.isFullScreen():
            return
        self.cinema_mode = False
        self.toolbar.show()
        self.tabs.tabBar().show()
        self.showNormal()

    def handle_escape(self):
        if self.cinema_mode or self.isFullScreen():
            view = self.current_web_view()
            if view:
                view.page().runJavaScript("if (document.fullscreenElement) document.exitFullscreen();")
            self.exit_cinema_mode()
        else:
            view = self.current_web_view()
            if view:
                view.setFocus()

    def closeEvent(self, event):
        while self.tabs.count() > 0:
            widget = self.tabs.widget(0)
            self.tabs.removeTab(0)
            if widget:
                widget.setPage(None)
                widget.deleteLater()
        super().closeEvent(event)
