#!/bin/bash
# Универсальный установщик Open-with-chooser для Linux
set -e

echo "=== Установщик Open-with-chooser ==="
echo "Универсальный селектор приложений для URL и файлов"
echo

# Проверка прав администратора для системной установки
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

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$HOME/.config/open-with-chooser"

# Определение пакетного менеджера и установка зависимостей
echo "📦 Установка зависимостей..."

install_dependencies() {
    local deps="python3-gi python3-gi-cairo gir1.2-gtk-3.0 wmctrl zenity python3-xdg"
    
    if command -v apt-get >/dev/null 2>&1; then
        echo "🔄 Используется APT (Debian/Ubuntu)"
        if [ "$INSTALL_TYPE" = "system" ]; then
            apt-get update
            apt-get install -y $deps
        else
            echo "⚠️  Для установки зависимостей требуются права администратора:"
            echo "sudo apt-get update && sudo apt-get install -y $deps"
            echo "Продолжить без установки зависимостей? (y/N)"
            read -r response
            if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
                exit 1
            fi
        fi
    elif command -v dnf >/dev/null 2>&1; then
        echo "🔄 Используется DNF (Fedora/RHEL)"
        local fedora_deps="python3-gobject gtk3-devel wmctrl zenity python3-pyxdg"
        if [ "$INSTALL_TYPE" = "system" ]; then
            dnf install -y $fedora_deps
        else
            echo "⚠️  Для установки зависимостей требуются права администратора:"
            echo "sudo dnf install -y $fedora_deps"
        fi
    elif command -v pacman >/dev/null 2>&1; then
        echo "🔄 Используется Pacman (Arch Linux)"
        local arch_deps="python-gobject gtk3 wmctrl zenity python-pyxdg"
        if [ "$INSTALL_TYPE" = "system" ]; then
            pacman -S --noconfirm $arch_deps
        else
            echo "⚠️  Для установки зависимостей требуются права администратора:"
            echo "sudo pacman -S --noconfirm $arch_deps"
        fi
    elif command -v zypper >/dev/null 2>&1; then
        echo "🔄 Используется Zypper (openSUSE)"
        local suse_deps="python3-gobject-Gdk typelib-1_0-Gtk-3_0 wmctrl zenity python3-pyxdg"
        if [ "$INSTALL_TYPE" = "system" ]; then
            zypper install -y $suse_deps
        else
            echo "⚠️  Для установки зависимостей требуются права администратора:"
            echo "sudo zypper install -y $suse_deps"
        fi
    else
        echo "❌ Неизвестный пакетный менеджер. Установите зависимости вручную:"
        echo "   python3-gi, gir1.2-gtk-3.0, python3-xdg, wmctrl, zenity"
    fi
}

# Установка зависимостей
install_dependencies

# Копирование основного скрипта
echo "📋 Установка основного скрипта..."
if [ -f "open-with-chooser.py" ]; then
    cp "open-with-chooser.py" "$INSTALL_DIR/open-with-chooser"
    chmod +x "$INSTALL_DIR/open-with-chooser"
    echo "✅ Скрипт установлен в $INSTALL_DIR/open-with-chooser"
else
    echo "❌ Файл open-with-chooser.py не найден в текущей директории"
    exit 1
fi

# Создание .desktop файла
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

echo "✅ Desktop файл создан: $DESKTOP_DIR/open-with-chooser.desktop"

# Обновление базы данных desktop файлов
echo "🔄 Обновление базы данных приложений..."
if command -v update-desktop-database >/dev/null 2>&1; then
    if [ "$INSTALL_TYPE" = "system" ]; then
        update-desktop-database /usr/local/share/applications/ 2>/dev/null || true
        update-desktop-database /usr/share/applications/ 2>/dev/null || true
    else
        update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
    fi
    echo "✅ База данных приложений обновлена"
else
    echo "⚠️  update-desktop-database не найдена, пропускается"
fi

# Настройка PATH для пользовательской установки
if [ "$INSTALL_TYPE" = "user" ]; then
    echo "🔧 Настройка PATH..."
    
    # Проверяем, есть ли уже ~/.local/bin в PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        # Добавляем в .bashrc
        if [ -f "$HOME/.bashrc" ]; then
            echo "" >> "$HOME/.bashrc"
            echo "# Добавлено установщиком open-with-chooser" >> "$HOME/.bashrc"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            echo "✅ PATH добавлен в ~/.bashrc"
        fi
        
        # Добавляем в .profile для совместимости
        if [ -f "$HOME/.profile" ]; then
            echo "" >> "$HOME/.profile"
            echo "# Добавлено установщиком open-with-chooser" >> "$HOME/.profile"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
            echo "✅ PATH добавлен в ~/.profile"
        fi
        
        echo "ℹ️  Перезапустите терминал или выполните: source ~/.bashrc"
    else
        echo "✅ ~/.local/bin уже в PATH"
    fi
fi

# Опциональная настройка как обработчика по умолчанию
echo
echo "🌐 Настройка обработчиков по умолчанию..."
echo "Установить open-with-chooser как обработчик по умолчанию для веб-ссылок? (y/N)"
read -r response

if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    if command -v xdg-mime >/dev/null 2>&1; then
        xdg-mime default open-with-chooser.desktop x-scheme-handler/http 2>/dev/null || true
        xdg-mime default open-with-chooser.desktop x-scheme-handler/https 2>/dev/null || true
        xdg-mime default open-with-chooser.desktop text/html 2>/dev/null || true
        echo "✅ Установлен как обработчик по умолчанию для HTTP/HTTPS"
    else
        echo "⚠️  xdg-mime не найдена, настройка пропущена"
    fi
else
    echo "ℹ️  Обработчики по умолчанию не настроены"
fi

# Проверка установки
echo
echo "🧪 Проверка установки..."

if [ -x "$INSTALL_DIR/open-with-chooser" ]; then
    echo "✅ Исполняемый файл установлен и доступен"
else
    echo "❌ Ошибка: исполняемый файл недоступен"
    exit 1
fi

if [ -f "$DESKTOP_DIR/open-with-chooser.desktop" ]; then
    echo "✅ Desktop файл установлен"
else
    echo "❌ Ошибка: desktop файл не найден"
    exit 1
fi

# Проверка зависимостей Python
echo "🐍 Проверка зависимостей Python..."
python3 -c "
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    print('✅ GTK3 bindings доступны')
except ImportError as e:
    print(f'❌ Ошибка импорта GTK: {e}')
    exit(1)

try:
    from xdg.DesktopEntry import DesktopEntry
    print('✅ PyXDG доступен')
except ImportError:
    print('⚠️  PyXDG недоступен (опциональная зависимость)')
" 2>/dev/null || echo "⚠️  Некоторые зависимости Python могут отсутствовать"

echo
echo "🎉 Установка завершена успешно!"
echo
echo "📖 Использование:"
echo "  • Командная строка: open-with-chooser <url|file>"
echo "  • Правый клик на файле: 'Открыть с помощью' -> 'Open With Chooser'"
echo "  • Автоматически для веб-ссылок (если настроено)"
echo
echo "📂 Конфигурация сохраняется в: ~/.config/open-with-chooser/"
echo "📝 Логи: ~/.config/open-with-chooser/chooser.log"
echo

if [ "$INSTALL_TYPE" = "user" ] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "⚠️  ВАЖНО: Перезапустите терминал для применения изменений PATH"
fi

echo "✨ Готово к использованию!"
