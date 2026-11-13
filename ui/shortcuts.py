from PySide6.QtGui import QKeySequence, QShortcut


def setup_shortcuts(window) -> None:
    """Регистрирует все горячие клавиши для быстрой работы в SlateBrow."""
    bindings = [
        # Вкладки
        ("Ctrl+T", lambda: window.add_new_tab()),
        ("Ctrl+W", lambda: window.close_current_tab()),
        ("Ctrl+F4", lambda: window.close_current_tab()),
        ("Ctrl+Shift+T", lambda: window.reopen_closed_tab()),
        ("Ctrl+Tab", lambda: window.switch_relative_tab(1)),
        ("Ctrl+Shift+Tab", lambda: window.switch_relative_tab(-1)),
        ("Ctrl+PageDown", lambda: window.switch_relative_tab(1)),
        ("Ctrl+PageUp", lambda: window.switch_relative_tab(-1)),
        # Навигация и обновление
        ("Ctrl+R", lambda: window.reload_page()),
        ("F5", lambda: window.reload_page()),
        ("Ctrl+Shift+R", lambda: window.hard_reload_page()),
        ("Alt+Left", lambda: window.go_back()),
        ("Alt+Right", lambda: window.go_forward()),
        ("Alt+Home", lambda: window.go_home()),
        # Адресная строка и закладки
        ("Ctrl+L", lambda: window.focus_url_bar()),
        ("Alt+D", lambda: window.focus_url_bar()),
        ("Ctrl+D", lambda: window.toggle_current_bookmark()),
        ("Ctrl+B", lambda: window.toggle_bookmarks_bar()),
        # Масштаб
        ("Ctrl+=", lambda: window.adjust_zoom(0.1)),
        ("Ctrl++", lambda: window.adjust_zoom(0.1)),
        ("Ctrl+-", lambda: window.adjust_zoom(-0.1)),
        ("Ctrl+0", lambda: window.reset_zoom()),
        # Полноэкранный режим и выход из него
        ("F11", lambda: window.toggle_fullscreen_mode()),
        ("Escape", lambda: window.handle_escape()),
    ]

    # Переключение вкладок Ctrl+1 .. Ctrl+9
    for i in range(1, 9):
        bindings.append((f"Ctrl+{i}", lambda idx=i - 1: window.switch_to_tab_index(idx)))
    bindings.append(("Ctrl+9", lambda: window.switch_to_last_tab()))

    window._registered_shortcuts = []
    for key_seq, callback in bindings:
        sc = QShortcut(QKeySequence(key_seq), window)
        sc.activated.connect(callback)
        window._registered_shortcuts.append(sc)
