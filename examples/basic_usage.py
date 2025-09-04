#!/usr/bin/env python3
"""
Пример базового использования Open With Chooser
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from open_with_chooser import OpenWithChooser

def example_basic_usage():
    """Базовый пример выбора приложения"""
    chooser = OpenWithChooser()
    
    # Выбор приложения для URL
    print("Выбор приложения для https://github.com")
    chooser.choose_and_run(['https://github.com'])

def example_file_handling():
    """Пример работы с файлами"""
    chooser = OpenWithChooser()
    
    # Создаем тестовый файл
    test_file = '/tmp/test_document.pdf'
    with open(test_file, 'w') as f:
        f.write('%PDF-1.4\n%Test PDF file')
    
    print(f"Выбор приложения для {test_file}")
    chooser.choose_and_run([test_file])
    
    # Очистка
    os.remove(test_file)

if __name__ == "__main__":
    print("🎯 Open With Chooser - Примеры использования")
    print("=" * 50)
    
    try:
        example_basic_usage()
        example_file_handling()
    except KeyboardInterrupt:
        print("\n👋 Работа прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
