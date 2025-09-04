#!/bin/bash
# Универсальный установщик Open-with-chooser для Linux

# ОБРАБОТКА АРГУМЕНТОВ В САМОМ НАЧАЛЕ
AUTO_YES=false
for arg in "$@"; do
    case $arg in
        --yes|-y)
            AUTO_YES=true
            ;;
        --help|-h)
            echo "Open-with-chooser Installer v2.0.1"
            echo "Использование: $0 [--yes|-y] [--help|-h]"
            echo ""
            echo "Опции:"
            echo "  --yes, -y    Неинтерактивная установка (автоматически 'да' на все вопросы)"
            echo "  --help, -h   Показать эту справку"
            echo ""
            echo "Описание:"
            echo "  Устанавливает Open-with-chooser - универсальный селектор приложений"
            echo "  для открытия файлов и URL в Linux."
            exit 0
            ;;
    esac
done

# Теперь включаем строгий режим
set -e

echo "=== Установщик Open-with-chooser ==="
echo "Универсальный селектор приложений для URL и файлов"
if [ "$AUTO_YES" = true ]; then
    echo "🚀 Режим: автоматическая установка (--yes)"
fi
echo

# Проверка прав
if [ "$EUID" -eq 0 ]; then
    INSTALL_TYPE="system"
    INSTALL_DIR="/usr/local/bin"
    DESKTOP_DIR="/usr/local/share/applications"
    echo "🔒 Установка в системные директории"
else
    INSTALL_TYPE="user"
    INSTALL_DIR="$HOME/.local/bin"
    DESKTOP_DIR="$HOME/.local/share/applications"
    echo "👤 Установка в пользовательские директории"
fi

# Создание директорий
echo "📁 Создание директорий..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$HOME/.config/open-with-chooser"

# Упрощенная установка зависимостей
echo "📦 Проверка зависимостей..."
if [ "$AUTO_YES" = true ]; then
    echo "🚀 Автоматический режим: пропускаем интерактивную установку зависимостей"
else
    echo "⚠️  Убедитесь что установлены: python3-gi python3-gi-cairo gir1.2-gtk-3.0 wmctrl zenity python3-xdg"
    echo "Продолжить установку? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Установка прервана"
        exit 1
    fi
fi

# УМНЫЙ ПОИСК ФАЙЛА
echo "📋 Поиск основного скрипта..."
SCRIPT_FILE=""

# Ищем в разных местах
for path in \
    "open-with-chooser.py" \
    "../src/open-with-chooser.py" \
    "src/open-with-chooser.py" \
    "./src/open-with-chooser.py" \
    "../open-with-chooser.py" \
    "*/open-with-chooser.py"; do
    
    if [ -f "$path" ]; then
        SCRIPT_FILE="$path"
        echo "✅ Найден: $path"
        break
    fi
done

if [ -z "$SCRIPT_FILE" ]; then
    echo "❌ Файл open-with-chooser.py не найден!"
    echo "📂 Ищем в текущей директории:"
    find . -name "*.py" -type f 2>/dev/null | head -5 || echo "Python файлы не найдены"
    echo ""
    echo "💡 Запустите установщик из корня проекта или убедитесь что файл существует"
    exit 1
fi

# Установка скрипта
echo "📋 Установка скрипта..."
cp "$SCRIPT_FILE" "$INSTALL_DIR/open-with-chooser"
chmod +x "$INSTALL_DIR/open-with-chooser"
echo "✅ Установлен: $INSTALL_DIR/open-with-chooser"

# Desktop файл
echo "🖥️ Создание .desktop файла..."
cat > "$DESKTOP_DIR/open-with-chooser.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Open With Chooser
Name[ru]=Выбор приложения
Comment=Universal application chooser for URLs and files
Comment[ru]=Универсальный селектор приложений для URL и файлов
Exec=open-with-chooser %U
Icon=applications-other
Terminal=false
MimeType=text/html;text/plain;application/pdf;image/png;image/jpeg;image/gif;video/mp4;audio/mpeg;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;
Categories=Utility;System;
NoDisplay=false
StartupNotify=true
EOF

echo "✅ Desktop файл: $DESKTOP_DIR/open-with-chooser.desktop"

# Обновление базы
if command -v update-desktop-database >/dev/null 2>&1; then
    echo "🔄 Обновление базы приложений..."
    if [ "$INSTALL_TYPE" = "system" ]; then
        update-desktop-database /usr/local/share/applications/ 2>/dev/null || true
    else
        update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
    fi
    echo "✅ База обновлена"
fi

# PATH
if [ "$INSTALL_TYPE" = "user" ]; then
    echo "🔧 Проверка PATH..."
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        echo "✅ ~/.local/bin уже в PATH"
    else
        echo "⚠️  Добавляем ~/.local/bin в PATH"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo "✅ Добавлено в ~/.bashrc"
    fi
fi

# Обработчики
echo ""
echo "🌐 Настройка обработчиков..."
if [ "$AUTO_YES" = true ]; then
    echo "🚀 Автоматический режим: настраиваем веб-обработчики"
    if command -v xdg-mime >/dev/null 2>&1; then
        xdg-mime default open-with-chooser.desktop x-scheme-handler/http 2>/dev/null || true
        xdg-mime default open-with-chooser.desktop x-scheme-handler/https 2>/dev/null || true
        echo "✅ Веб-обработчики настроены"
    fi
else
    echo "Настроить как обработчик веб-ссылок? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        if command -v xdg-mime >/dev/null 2>&1; then
            xdg-mime default open-with-chooser.desktop x-scheme-handler/http
            xdg-mime default open-with-chooser.desktop x-scheme-handler/https
            echo "✅ Веб-обработчики настроены"
        fi
    fi
fi

echo ""
echo "🎉 УСТАНОВКА ЗАВЕРШЕНА!"
echo ""
echo "📋 Использование:"
echo "   open-with-chooser <файл_или_URL>"
echo "   open-with-chooser https://github.com"
echo "   open-with-chooser /path/to/file.txt"
echo ""
echo "🖥️  Также доступно через контекстное меню файлов"

if [ "$INSTALL_TYPE" = "user" ] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  ВАЖНО: Перезапустите терминал или выполните:"
    echo "   source ~/.bashrc"
fi

echo ""
echo "✨ Open-with-chooser v2.0.1 готов к использованию!"
