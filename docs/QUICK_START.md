# 🚀 Open-with-chooser для Linux Mint 22.1

Универсальный селектор приложений адаптированный для вашей системы.

## ⚡ Быстрая установка (рекомендуется)

```bash
# Оптимизированный установщик для Linux Mint 22.1
./install-for-mint.sh
```

**Все зависимости уже установлены в вашей системе!** ✅

## 📦 Альтернативные способы

### 1. Самораспаковывающийся архив
```bash
./open-with-chooser-installer.sh
```

### 2. Исходники
```bash
cd src/shared/open_with_chooser/
./quick-install.sh
```

## 🧪 Тестирование

```bash
# После установки
./test-open-with-chooser.sh
```

## 📖 Использование

### Командная строка
```bash
open-with-chooser https://github.com
open-with-chooser document.pdf
```

### Интеграция с Cursor IDE
```
Settings → External Browser → open-with-chooser
```

### Системная интеграция
- Контекстное меню: Правый клик → "Открыть с помощью"
- Меню приложений: "Open With Chooser"

## ✨ Возможности

- 🎯 **Контекстно-зависимый выбор**: Разные приложения для Cursor, терминала, файлового менеджера
- 🧠 **Запоминание выбора**: Автоматическое применение предпочтений
- 🔍 **Поддержка всех типов**: Desktop, Flatpak, Snap, портативные приложения
- 🖥️ **Удобный интерфейс**: GTK3 диалог с фильтрацией по MIME-типам

## 📂 Расположение файлов

После установки:
```
~/.local/bin/open-with-chooser              # Исполняемый файл
~/.local/share/applications/...desktop      # Desktop файл
~/.config/open-with-chooser/                # Конфигурация и логи
```

## 🔧 Устранение проблем

### PATH не обновился
```bash
# Перезапустите терминал или выполните:
source ~/.bashrc
```

### Команда не найдена
```bash
# Проверьте установку:
ls -la ~/.local/bin/open-with-chooser

# Запустите напрямую:
~/.local/bin/open-with-chooser https://example.com
```

### Отладка
```bash
# Просмотр логов:
tail -f ~/.config/open-with-chooser/chooser.log

# Запуск с отладкой:
python3 ~/.local/bin/open-with-chooser --debug
```

## 🆘 Поддержка

- 📖 Полная документация: `~/.config/open-with-chooser/README.md`
- 📝 Логи: `~/.config/open-with-chooser/chooser.log`
- 🧪 Тестирование: `./test-open-with-chooser.sh`

---

**Оптимизировано для Linux Mint 22.1 • Python 3.12.3** 🐧
