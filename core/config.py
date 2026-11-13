import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_CONFIG: Dict[str, Any] = {
    "homepage": "slate://home",
    "search_engine": "https://duckduckgo.com/?q={query}",
    "user_agent": "",
    "shortcuts": [
        {"name": "YouTube", "url": "https://www.youtube.com", "icon": "▶"},
        {"name": "Twitch Live", "url": "https://www.twitch.tv", "icon": "📡"},
        {"name": "GitHub", "url": "https://github.com", "icon": "🐙"},
        {"name": "ChatGPT", "url": "https://chatgpt.com", "icon": "✦"},
        {"name": "DuckDuckGo", "url": "https://duckduckgo.com", "icon": "🔍"},
        {"name": "Reddit", "url": "https://www.reddit.com", "icon": "💬"},
    ],
    "bookmarks": [
        {"name": "YouTube Live", "url": "https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig"},
        {"name": "GitHub", "url": "https://github.com"},
        {"name": "Lofi Radio", "url": "https://www.youtube.com/results?search_query=lofi+hip+hop+radio+live"},
    ],
    "last_session_tabs": ["slate://home"],
    "restore_session": True,
}


class ConfigManager:
    def __init__(self, config_path: str | Path | None = None):
        if config_path is None:
            self.path = Path(__file__).resolve().parent.parent / "config.json"
        else:
            self.path = Path(config_path)
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        merged = json.loads(json.dumps(DEFAULT_CONFIG))
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    merged.update(loaded)
            except Exception as e:
                print(f"[SlateBrow] Config load warning: {e}")
        self.data = merged
        self.save()
        return self.data

    def save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[SlateBrow] Config save warning: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    @property
    def shortcuts(self) -> List[Dict[str, str]]:
        return self.data.get("shortcuts", DEFAULT_CONFIG["shortcuts"])

    @property
    def bookmarks(self) -> List[Dict[str, str]]:
        return self.data.get("bookmarks", DEFAULT_CONFIG["bookmarks"])

    def toggle_bookmark(self, title: str, url: str) -> bool:
        """Добавляет или удаляет закладку. Возвращает True, если добавлена."""
        bms = list(self.bookmarks)
        for i, bm in enumerate(bms):
            if bm.get("url") == url:
                bms.pop(i)
                self.set("bookmarks", bms)
                return False
        clean_title = (title or url).replace(" — SlateBrow", "").strip()[:28]
        bms.append({"name": clean_title, "url": url})
        self.set("bookmarks", bms)
        return True

    def is_bookmarked(self, url: str) -> bool:
        return any(bm.get("url") == url for bm in self.bookmarks)


config = ConfigManager()
