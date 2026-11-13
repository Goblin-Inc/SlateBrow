<div align="center">

# 🌐 SlateBrow

**Минималистичный десктопный веб-браузер в эстетике Dark Slate с аппаратным декодированием прямых трансляций (`H.264/AAC`), Cinema Mode и персистентными сессиями**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![QtWebEngine](https://img.shields.io/badge/Engine-QtWebEngine_6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qt-6/qtwebengine-index.html)
[![Platform](https://img.shields.io/badge/Platform-Linux_x86__64-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#)
[![Release](https://img.shields.io/github/v/release/Goblin-Inc/SlateBrow?style=for-the-badge&color=38bdf8)](https://github.com/Goblin-Inc/SlateBrow/releases)

<br/>

![SlateBrow Browser Preview](assets/screenshots/slatebrow_preview.png)

</div>

---

## 📖 О проекте

**SlateBrow** — быстрый, не перегруженный лишними панелями и телеметрией веб-браузер на базе **PySide6 / QtWebEngine (Chromium)**, спроектированный для комфортного просмотра видео, стримов и повседневного веб-сёрфинга в тёмном окружении Linux.

В отличие от стандартных сборок PySide6 из PyPI (где проприетарные медиа-кодеки отключены), **SlateBrow** напрямую задействует системный движок `QtWebEngineCore` с поддержкой аппаратного декодирования **H.264 / AAC / MSE / WebRTC**, благодаря чему **YouTube Live, Twitch и VK Play Live** работают плавно и без ошибок воспроизведения.

### ✨ Ключевые возможности
- **Полная поддержка Live-стримов и видео (`H.264 / AAC / Widevine`)**:
  - Активированы флаги Chromium `ignore-gpu-blocklist`, `enable-gpu-rasterization`, `enable-zero-copy` и ` autoplay-policy=no-user-gesture-required`.
  - Плавное воспроизведение 1080p60/4K60 роликов и прямых трансляций YouTube / Twitch.
- **Персистентный профиль и авто-восстановление вкладок**:
  - Принудительное хранение куки (`ForcePersistentCookies`), `LocalStorage` и кэша в `~/.local/share/SlateBrow/`.
  - Авторизация в аккаунтах Google, YouTube, GitHub, Twitch сохраняется после закрытия браузера.
  - Все открытые вкладки автоматически сохраняются в `session.json` и восстанавливаются при следующем запуске.
- **Настоящий Fullscreen и Cinema Mode (`F11`)**:
  - Поддержка HTML5 Fullscreen API (`FullScreenSupportEnabled`) — при нажатии кнопки «Во весь экран» в плеере YouTube/Twitch панели вкладок и адресная строка автоматически скрываются, а по `Esc` или `F11` возвращаются обратно.
- **Менеджер загрузок и масштабирование страниц**:
  - Встроенная панель прогресса скачивания файлов (`~/Downloads`) и плавный зум (`Ctrl +` / `Ctrl -` / `Ctrl 0`).

---

## ⌨️ Горячие клавиши

| Сочетание клавиш | Действие |
|---|---|
| `Ctrl + T` | Открыть новую вкладку |
| `Ctrl + W` | Закрыть текущую вкладку |
| `Ctrl + R` / `F5` | Обновить страницу |
| `Ctrl + L` | Выделить адресную строку (ввод URL или поискового запроса Google) |
| `F11` | Переключить полноэкранный режим (Cinema Mode с авто-скрытием тулбара и вкладок) |
| `Esc` | Выйти из полноэкранного режима видео или окна |
| `Alt + ←` / `Alt + →` | Назад / Вперёд по истории вкладки |
| `Ctrl + +` / `Ctrl + -` / `Ctrl + 0` | Увеличить / Уменьшить / Сбросить масштаб страницы (`100%`) |

---

## 🏗️ Архитектура проекта

```
SlateBrow/
├── main.py          # Точка входа, настройка флагов Chromium/GPU и инициализация профиля
├── browser.py       # Ядро браузера: управление вкладками, сессией, куки, Fullscreen API и загрузками
├── styles.py        # Фирменная тёмная тема Slate Dark (#0d0f12 / #161920)
├── run.sh           # Скрипт запуска с системным QtWebEngine (поддержка H.264/AAC кодеков)
└── requirements.txt # Зависимости окружения
```

---

## 📦 Установка и запуск

### Вариант 1: Установка из `.deb` пакета (Рекомендуется)
Перейдите в [**Releases**](https://github.com/Goblin-Inc/SlateBrow/releases), скачайте `slatebrow_1.0.0_amd64.deb` и выполните:

```bash
sudo dpkg -i slatebrow_1.0.0_amd64.deb
sudo apt-get install -f
```
После этого **SlateBrow** появится в списке веб-браузеров вашей системы и будет запускаться командой `slatebrow`.

### Вариант 2: Arch Linux (`pacman`) / Универсальная установка из репозитория
```bash
git clone https://github.com/Goblin-Inc/SlateBrow.git
cd SlateBrow

# Автоматическая установка (сам определит Arch Linux pacman или Ubuntu/Debian apt):
./install.sh

# Либо вручную на Arch Linux:
sudo pacman -S python pyside6 qt6-webengine qt6-multimedia-ffmpeg
./run.sh

# Либо вручную на Ubuntu / Debian:
sudo apt install python3-pyside6.qtwebenginewidgets python3-pyside6.qtwebenginecore
./run.sh
```

---

## 📋 Changelog

### `v1.0.0` — Релиз SlateBrow с поддержкой Live-трансляций и Cinema Mode *(Текущая версия)*
- **Добавлено**: Аппаратное ускорение видео и поддержка кодеков `H.264/AAC` для прямых трансляций YouTube Live и Twitch.
- **Добавлено**: Персистентное хранилище `ForcePersistentCookies` и авто-сохранение открытых вкладок в `~/.local/share/SlateBrow/session.json`.
- **Добавлено**: Полноценный HTML5 Fullscreen API + режим `F11` со скрытием интерфейса.
- **Добавлено**: Инсталлятор `.deb` и portable-сборка в GitHub Releases.

---

<div align="center">
Разработано <a href="https://github.com/Goblin-Inc">@Goblin-Inc</a>
</div>
