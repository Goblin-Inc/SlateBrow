import re
from pathlib import Path
from urllib.parse import quote_plus
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings

from .config import config


DOMAIN_RE = re.compile(
    r"^(localhost(:\d+)?|(\d{1,3}\.){3}\d{1,3}(:\d+)?|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})(?:[/?#].*)?$"
)


def resolve_user_input(raw_input: str) -> str:
    """Превращает ввод пользователя в валидный URL или поисковый запрос."""
    text = raw_input.strip()
    if not text:
        return config.get("homepage", "slate://home")

    if text in ("slate://home", "about:home", "about:blank"):
        return "slate://home"

    if text.startswith(("http://", "https://", "file://", "data:")):
        return text

    if " " not in text and DOMAIN_RE.match(text):
        scheme = "http://" if text.startswith(("localhost", "127.0.0.1")) else "https://"
        return scheme + text

    search_tpl = config.get("search_engine", "https://duckduckgo.com/?q={query}")
    return search_tpl.format(query=quote_plus(text))


def create_browser_profile(parent=None) -> QWebEngineProfile:
    """Создаёт общий профиль браузера с поддержкой стримов, кодеков и полноэкранного видео."""
    storage_dir = Path.home() / ".local" / "share" / "SlateBrow"
    cache_dir = Path.home() / ".cache" / "SlateBrow"
    storage_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    profile = QWebEngineProfile("SlateBrowProfile", parent)
    profile.setPersistentStoragePath(str(storage_dir))
    profile.setCachePath(str(cache_dir))
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
    )
    custom_ua = config.get("user_agent", "").strip()
    if custom_ua:
        profile.setHttpUserAgent(custom_ua)

    settings = profile.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)

    return profile


def configure_web_view_settings(settings: QWebEngineSettings) -> None:
    """Включает необходимые атрибуты для конкретной вкладки."""
    settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)


class SlateWebPage(QWebEnginePage):
    """Кастомная страница с поддержкой target='_blank' и разрешений медиа/fullscreen."""

    def __init__(self, profile: QWebEngineProfile, browser_window, parent=None):
        super().__init__(profile, parent)
        self.browser_window = browser_window
        self.featurePermissionRequested.connect(self._on_feature_permission)

    def _on_feature_permission(self, security_origin: QUrl, feature: QWebEnginePage.Feature):
        # Разрешаем аудио/видео/захват экрана при запросе со страницы
        self.setFeaturePermission(
            security_origin,
            feature,
            QWebEnginePage.PermissionPolicy.PermissionGrantedByUser,
        )

    def createWindow(self, _type: QWebEnginePage.WebWindowType) -> QWebEnginePage:
        new_view = self.browser_window.add_new_tab(url=None, switch_to=True)
        return new_view.page()


def generate_dashboard_html() -> str:
    """Генерирует стильную стартовую страницу SlateBrow (Speed Dial + Поиск)."""
    cards_html = ""
    for item in config.shortcuts:
        name = item.get("name", "Site")
        url = item.get("url", "https://duckduckgo.com")
        icon = item.get("icon", "🌐")
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        cards_html += f"""
        <a class="card" href="{url}">
            <div class="card-icon">{icon}</div>
            <div class="card-info">
                <div class="card-title">{name}</div>
                <div class="card-domain">{domain}</div>
            </div>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Новая вкладка — SlateBrow</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        min-height: 100vh;
        background: radial-gradient(circle at 20% 20%, #162238 0%, #0b0f17 55%, #070a10 100%);
        color: #e2e8f0;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 24px;
        user-select: none;
    }}
    .brand {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }}
    .brand-badge {{
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: linear-gradient(135deg, #10b981, #0ea5e9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 22px;
        color: #061018;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.32);
    }}
    h1 {{
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -0.8px;
        background: linear-gradient(90deg, #f8fafc, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
        color: #64748b;
        font-size: 14px;
        margin-bottom: 34px;
    }}
    .search-box {{
        width: 100%;
        max-width: 640px;
        position: relative;
        margin-bottom: 42px;
    }}
    .search-box input {{
        width: 100%;
        padding: 16px 22px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.22);
        background: rgba(15, 23, 42, 0.78);
        color: #f8fafc;
        font-size: 16px;
        outline: none;
        transition: all 0.2s ease;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
    }}
    .search-box input:focus {{
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2), 0 12px 32px rgba(0, 0, 0, 0.45);
    }}
    .grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(190px, 210px));
        gap: 16px;
        max-width: 680px;
        width: 100%;
    }}
    .card {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 16px 18px;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.14);
        text-decoration: none;
        color: #f1f5f9;
        transition: all 0.18s ease;
    }}
    .card:hover {{
        transform: translateY(-3px);
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(16, 185, 129, 0.55);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
    }}
    .card-icon {{
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }}
    .card-title {{
        font-size: 14px;
        font-weight: 600;
        color: #f8fafc;
    }}
    .card-domain {{
        font-size: 12px;
        color: #64748b;
        margin-top: 2px;
    }}
    .hotkeys {{
        margin-top: 44px;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
        color: #64748b;
        font-size: 12px;
    }}
    .hk {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.12);
        padding: 6px 12px;
        border-radius: 10px;
    }}
    .hk b {{ color: #94a3b8; }}
</style>
</head>
<body>
    <div class="brand">
        <div class="brand-badge">S</div>
        <h1>SlateBrow</h1>
    </div>
    <div class="subtitle">Быстрый, минималистичный браузер с поддержкой Live-стримов и Cinema Mode</div>

    <form class="search-box" onsubmit="event.preventDefault(); const q=this.q.value.trim(); if(q) window.location.href='https://duckduckgo.com/?q='+encodeURIComponent(q);">
        <input type="text" name="q" placeholder="Поиск в DuckDuckGo или введите адрес в строку сверху..." autofocus>
    </form>

    <div class="grid">
        {cards_html}
    </div>

    <div class="hotkeys">
        <span class="hk"><b>Ctrl+T</b> Новая вкладка</span>
        <span class="hk"><b>Ctrl+W</b> Закрыть вкладку</span>
        <span class="hk"><b>Ctrl+Shift+T</b> Вернуть вкладку</span>
        <span class="hk"><b>Ctrl+R / F5</b> Обновить</span>
        <span class="hk"><b>Ctrl+L</b> Адресная строка</span>
        <span class="hk"><b>F11</b> Полный экран</span>
    </div>
</body>
</html>"""
