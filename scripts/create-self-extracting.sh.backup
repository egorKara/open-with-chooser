#!/bin/bash
# Создание самораспаковывающегося архива open-with-chooser
set -e

echo "🔨 Создание самораспаковывающегося архива..."

# Проверка наличия файлов
required_files=(
    "open-with-chooser.py"
    "install.sh"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Ошибка: файл $file не найден"
        exit 1
    fi
done

# Создание временной директории для архива
tmp_dir=$(mktemp -d)
archive_dir="$tmp_dir/open-with-chooser"
mkdir -p "$archive_dir"

# Копирование файлов
echo "📋 Копирование файлов..."
cp open-with-chooser.py "$archive_dir/"
cp install.sh "$archive_dir/"
cp README.md "$archive_dir/"

# Создание архива
echo "📦 Создание tar.gz архива..."
cd "$tmp_dir"
tar -czf open-with-chooser.tar.gz open-with-chooser/

# Кодирование в base64
echo "🔤 Кодирование в base64..."
base64_data=$(base64 -w 0 open-with-chooser.tar.gz)

# Создание самораспаковывающегося скрипта
echo "🚀 Создание самораспаковывающегося установщика..."
cat > "open-with-chooser-installer.sh" << 'EOF'
#!/bin/bash
# Самораспаковывающийся установщик open-with-chooser
set -e

echo "=== Open-with-chooser Автоматический установщик ==="
echo "Универсальный селектор приложений для Linux"
echo

# Создание временной директории
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

echo "📦 Распаковка файлов..."

# Извлечение встроенных данных (base64 encoded tar.gz)
sed -n '/^__DATA__$/,$p' "$0" | tail -n +2 | base64 -d | tar -xzf -

# Переход в директорию с файлами
cd open-with-chooser

echo "🚀 Запуск установки..."

# Запуск установки
chmod +x install.sh
./install.sh

# Очистка
cd /
rm -rf "$TMPDIR"

echo
echo "🎉 Установка завершена успешно!"
echo "📚 Для получения справки: open-with-chooser --help"
echo "📖 Документация: ~/.config/open-with-chooser/README.md"

exit 0

__DATA__
EOF

# Добавление base64 данных
echo "$base64_data" >> "open-with-chooser-installer.sh"

# Перемещение в исходную директорию
mv "open-with-chooser-installer.sh" "$OLDPWD/"

# Очистка
cd "$OLDPWD"
rm -rf "$tmp_dir"

# Делаем исполняемым
chmod +x "open-with-chooser-installer.sh"

echo "✅ Самораспаковывающийся архив создан: open-with-chooser-installer.sh"
echo "📏 Размер: $(du -h open-with-chooser-installer.sh | cut -f1)"
echo
echo "🚀 Использование:"
echo "   ./open-with-chooser-installer.sh"
echo "   # или:"
echo "   bash open-with-chooser-installer.sh"
echo
echo "📤 Файл готов к распространению!"
