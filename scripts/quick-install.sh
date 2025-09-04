#!/bin/bash
# Быстрая установка Open-with-chooser одной командой
set -e

echo "🚀 Быстрая установка Open-with-chooser"
echo "======================================"

# Проверка наличия основных файлов
if [ ! -f "open-with-chooser.py" ] || [ ! -f "install.sh" ]; then
    echo "❌ Файлы установки не найдены в текущей директории"
    echo "Убедитесь, что вы находитесь в директории с файлами:"
    echo "  • open-with-chooser.py"
    echo "  • install.sh"
    exit 1
fi

# Делаем установочный скрипт исполняемым
chmod +x install.sh

# Запускаем установку
echo "▶️  Запуск установки..."
./install.sh

echo
echo "🎯 Быстрая проверка работоспособности..."

# Тестирование с простым URL
if command -v open-with-chooser >/dev/null 2>&1; then
    echo "✅ Команда open-with-chooser доступна"
    echo "💡 Тест: open-with-chooser --help"
else
    echo "⚠️  Команда open-with-chooser недоступна"
    echo "   Возможно, требуется перезапуск терминала"
fi

echo
echo "🏁 Быстрая установка завершена!"
echo "📚 Для тестирования попробуйте:"
echo "   open-with-chooser https://example.com"
