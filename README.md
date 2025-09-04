# Open-with-chooser

Универсальный селектор приложений для URL и файлов в Linux. Позволяет выбирать приложение для открытия файлов и ссылок с возможностью запоминания выбора для разных контекстов (IDE, файловый менеджер, терминал).

## ✨ Возможности

### Основные
- 🎯 **Интеллектуальный выбор**: Автоматическое определение подходящих приложений по MIME-типу
- 🧠 **Запоминание выбора**: Сохранение предпочтений для разных контекстов вызова
- 🔍 **Широкая поддержка**: Desktop файлы, Flatpak, Snap, портативные приложения
- 🖥️ **Удобный интерфейс**: GTK3 диалог с поиском и фильтрацией
- ⚙️ **Расширяемость**: Добавление пользовательских приложений
- 🌐 **Контекстная осведомлённость**: Разные приложения для разных программ-вызывателей

### 🆕 Enhanced возможности
- 🔄 **Отмена ассоциаций**: Полный контроль над запомненными выборами
- 🎯 **Умная сортировка**: Рекомендуемые → часто используемые → остальные
- 👁️ **Скрытие нерелевантных**: Чекбокс "показать все приложения"
- 🧠 **Умная фильтрация**: Исключение неподходящих приложений по типу
- 🔍 **Улучшенное обнаружение**: Специальный поиск Tor Browser и других
- 📊 **Настраиваемые колонки**: Изменяемая ширина, сортировка
- 💾 **Запоминание UI**: Размеры окна, колонок, настройки сохраняются

## 📦 Системные требования

- **ОС**: Linux (протестировано на Ubuntu 24.04, Linux Mint, Fedora, Arch)
- **Python**: 3.8+ (рекомендуется 3.11+)
- **GUI**: GTK3 с Python bindings

### Зависимости

```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-xdg wmctrl zenity

# Fedora/RHEL
sudo dnf install python3-gobject gtk3-devel python3-pyxdg wmctrl zenity

# Arch Linux
sudo pacman -S python-gobject gtk3 python-pyxdg wmctrl zenity

# openSUSE
sudo zypper install python3-gobject-Gdk typelib-1_0-Gtk-3_0 python3-pyxdg wmctrl zenity
```

## 🚀 Быстрая установка

### Автоматическая установка (рекомендуется)

```bash
# Клонирование или скачивание файлов
git clone <repository> && cd open-with-chooser

# Быстрая установка одной командой
chmod +x quick-install.sh && ./quick-install.sh
```

### Ручная установка

```bash
# 1. Установка зависимостей (см. выше)

# 2. Установка скрипта
chmod +x install.sh
./install.sh

# 3. Для системной установки (опционально)
sudo ./install.sh
```

### Установка пользователем (без sudo)

```bash
# Установка в ~/.local/bin (автоматически)
./install.sh

# Перезапустите терминал или выполните
source ~/.bashrc
```

## 📖 Использование

### Командная строка

```bash
# Открытие URL
open-with-chooser https://github.com

# Открытие файла
open-with-chooser /path/to/document.pdf

# Множественные файлы
open-with-chooser file1.txt file2.png file3.mp4
```

### Интеграция с системой

После установки приложение автоматически интегрируется:

- **Контекстное меню**: Правый клик → "Открыть с помощью" → "Open With Chooser"
- **Обработчик по умолчанию**: Опционально для HTTP/HTTPS ссылок
- **Desktop файл**: Появляется в меню приложений

### Интеграция с IDE

#### Cursor IDE
```
Settings → External Browser → /usr/local/bin/open-with-chooser
```

#### VS Code
```json
"workbench.externalBrowser": "open-with-chooser"
```

## 🎮 Функции интерфейса

### Главное окно

- **Список приложений**: Автоматически фильтруется по MIME-типу файла
- **Информация о контексте**: Показывает откуда вызвано приложение
- **Типы приложений**: Desktop, Flatpak, Snap, портативные, пользовательские

### Доступные действия

1. **Открыть** - Запустить выбранное приложение
2. **Запомнить выбор** - Сохранить для данного контекста и типа файла
3. **Добавить приложение** - Добавить пользовательское приложение
4. **Управление запомненными** - Просмотр и редактирование сохранённых правил

## ⚙️ Конфигурация

### Файлы конфигурации

```
~/.config/open-with-chooser/
├── config.json          # Основная конфигурация
├── chooser.log          # Лог файл
└── bin/                 # Пользовательские приложения (симлинки)
```

### Структура config.json

```json
{
  "context_choices": {
    "cursor:text/html": "Firefox",
    "file_manager:application/pdf": "Evince"
  },
  "custom_apps": [
    {
      "name": "My Editor",
      "exec_cmd": "/path/to/editor",
      "mime_types": ["text/plain"],
      "original_path": "/opt/myeditor/bin/editor"
    }
  ],
  "default_app": null
}
```

### Контексты вызова

Приложение определяет контекст по дереву процессов:

- `cursor` - Cursor IDE
- `file_manager` - Nautilus, Dolphin, Thunar, PCManFM
- `terminal` - Gnome Terminal, Konsole, XTerm, Alacritty  
- `desktop` - Прямой вызов из рабочего стола
- `unknown` - Неопределённый контекст

## 🔧 Продвинутое использование

### Добавление пользовательских приложений

1. Через интерфейс: "Добавить приложение" → выбрать исполняемый файл
2. Вручную в конфигурации:

```bash
# Создание симлинка
ln -s /opt/myapp/bin/myapp ~/.local/share/open-with-chooser/bin/

# Добавление в config.json (автоматически при первом использовании)
```

### Управление MIME обработчиками

```bash
# Установка как обработчик по умолчанию
xdg-mime default open-with-chooser.desktop x-scheme-handler/http
xdg-mime default open-with-chooser.desktop x-scheme-handler/https

# Проверка текущего обработчика
xdg-mime query default x-scheme-handler/http

# Сброс к системному обработчику
xdg-mime default firefox.desktop x-scheme-handler/http
```

### Очистка конфигурации

```bash
# Удаление всех настроек
rm -rf ~/.config/open-with-chooser/

# Удаление только запомненных выборов
rm ~/.config/open-with-chooser/config.json
```

## 🐛 Устранение неполадок

### Общие проблемы

**Проблема**: Приложение не запускается
```bash
# Проверка зависимостей
python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk; print('OK')"

# Проверка установки
which open-with-chooser
```

**Проблема**: Не видны приложения Flatpak/Snap
```bash
# Проверка установки Flatpak
flatpak list --app

# Проверка установки Snap
snap list
```

**Проблема**: Ошибки в логах
```bash
# Просмотр логов
tail -f ~/.config/open-with-chooser/chooser.log

# Проверка уровня логирования
export PYTHONPATH=/usr/local/bin:$PYTHONPATH
```

### Отладка

Включение подробного логирования:

```bash
# Запуск с отладкой
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import sys
sys.path.insert(0, '/usr/local/bin')
from open_with_chooser import main
main()
" https://example.com
```

### Переустановка

```bash
# Полная очистка
sudo rm -f /usr/local/bin/open-with-chooser
sudo rm -f /usr/local/share/applications/open-with-chooser.desktop
rm -f ~/.local/bin/open-with-chooser
rm -f ~/.local/share/applications/open-with-chooser.desktop
rm -rf ~/.config/open-with-chooser/

# Повторная установка
./install.sh
```

## 🔒 Безопасность

- ✅ Проверка исполняемых файлов перед добавлением
- ✅ Вычисление SHA256 хэшей пользовательских приложений
- ✅ Атомарное сохранение конфигурации
- ✅ Изоляция пользовательских приложений в ~/.local/
- ✅ Проверка прав доступа к файлам

## 📋 Примеры использования

### Разработчику

```bash
# Открытие GitHub репозитория в разных браузерах из разных IDE
# Cursor → Firefox Developer Edition
# VS Code → Chrome
# Терминал → Lynx (текстовый браузер)
```

### Дизайнеру

```bash
# Открытие изображений в разных программах
open-with-chooser design.svg   # → Inkscape из файлового менеджера
open-with-chooser design.svg   # → GIMP из терминала (запомненный выбор)
```

### Обычному пользователю

```bash
# Выбор видеоплеера по ситуации
open-with-chooser movie.mp4    # → VLC для фильмов
open-with-chooser lecture.mp4  # → SMPlayer для лекций
```

## 🤝 Разработка

### Структура проекта

```
open-with-chooser/
├── open-with-chooser.py     # Основной скрипт
├── install.sh               # Установочный скрипт
├── quick-install.sh         # Быстрая установка
├── README.md               # Документация
└── examples/               # Примеры конфигураций
```

### Архитектура

- `AppDiscovery` - Обнаружение приложений
- `ContextDetector` - Определение контекста вызова
- `ConfigManager` - Управление конфигурацией
- `AppChooserDialog` - GTK интерфейс
- `OpenWithChooser` - Главный класс приложения

### Расширение функциональности

Приложение спроектировано модульно для лёгкого расширения:

1. **Новые источники приложений**: Добавить методы в `AppDiscovery`
2. **Новые контексты**: Расширить `ContextDetector`
3. **Дополнительные форматы**: Обновить MIME mapping
4. **Улучшенный UI**: Модифицировать `AppChooserDialog`

## 📄 Лицензия

MIT License - свободное использование и модификация.

## 🙏 Благодарности

- Проект основан на спецификациях XDG Desktop Entry
- Использует PyXDG для парсинга desktop файлов
- GTK3 для графического интерфейса
- Вдохновлён классическими утилитами вроде xdg-open

---

**Создано для улучшения пользовательского опыта в Linux** 🐧
