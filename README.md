# SlateBrow

**SlateBrow** is a lightweight, fast, and minimalist desktop web browser built with **Python** and **PySide6 (QtWebEngine)**. It features a custom **Slate Obsidian & Emerald** dark theme, a built-in Speed Dial dashboard, full keyboard navigation, and hardware-accelerated support for live streams (`H.264` / `AAC` / `VP9` / `AV1`) and Cinema / Fullscreen video playback.

---

## ✨ Key Features

- **Live Stream & Fullscreen Ready:** Full support for YouTube Live, Twitch, and HTML5 Fullscreen / Cinema Mode (`F11` or player fullscreen button), hiding all browser chrome for distraction-free viewing.
- **Smart Omnibox:** Automatically distinguishes between direct URLs, domains, `localhost`, and DuckDuckGo search queries.
- **Built-in Speed Dial Dashboard (`slate://home`):** Instant access to favorite services and search on every new tab.
- **Bookmarks Bar:** One-click bookmarking (`Ctrl+D`) and persistent JSON configuration (`config.json`).
- **Tab Management & Session Recovery:** Multi-tab browsing with tab reordering, background tab URL isolation, and `Ctrl+Shift+T` to restore recently closed tabs.
- ** Slate Obsidian UI:** Custom dark stylesheet (`assets/style.qss`) with slim loading progress indicator and clean controls.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+T` | Open a new tab |
| `Ctrl+W` / `Ctrl+F4` | Close current tab |
| `Ctrl+Shift+T` | Reopen last closed tab |
| `Ctrl+Tab` / `Ctrl+Shift+Tab` | Cycle through tabs |
| `Ctrl+1` … `Ctrl+9` | Jump to specific tab |
| `Ctrl+R` / `F5` | Reload current page |
| `Ctrl+Shift+R` | Hard reload (bypass cache) |
| `Ctrl+L` / `Alt+D` | Focus address bar (Omnibox) |
| `Alt+Left` / `Alt+Right` | Navigate Back / Forward |
| `Alt+Home` | Open SlateBrow Home Dashboard |
| `Ctrl+D` | Bookmark current page |
| `Ctrl+B` | Toggle Bookmarks Bar |
| `Ctrl++` / `Ctrl+-` / `Ctrl+0` | Zoom In / Out / Reset |
| `F11` / `Esc` | Toggle Fullscreen / Cinema Mode |

---

## 🚀 Getting Started

```bash
./.venv/bin/python main.py
```
