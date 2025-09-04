#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open-with-chooser Enhanced - Улучшенный селектор приложений
Новые возможности:
- Отмена ассоциаций
- Умная сортировка (рекомендуемые → часто используемые → остальные)
- Скрытие/показ дополнительных приложений
- Умная фильтрация по типу
- Улучшенное обнаружение (включая Tor Browser)
- Настраиваемые колонки
- Запоминание настроек UI
"""

import os
import sys
import json
import logging
import subprocess
import shlex
import tempfile
import stat
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk

try:
    from xdg.DesktopEntry import DesktopEntry
    from xdg.BaseDirectory import xdg_data_dirs, xdg_config_home
    from xdg import Mime
    HAS_XDG = True
except ImportError:
    HAS_XDG = False

# Конфигурация
CONFIG_DIR = Path.home() / '.config' / 'open-with-chooser'
BIN_DIR = Path.home() / '.local' / 'share' / 'open-with-chooser' / 'bin'
CONFIG_FILE = CONFIG_DIR / 'chooser.json'
LOG_FILE = CONFIG_DIR / 'chooser.log'

# Создание директорий
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
BIN_DIR.mkdir(parents=True, exist_ok=True)

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DesktopApp:
    def __init__(self, name: str, exec_cmd: str, icon: str = '', mime_types: List[str] = None, 
                 app_type: str = 'desktop', desktop_file: str = '', app_id: str = '', 
                 priority: int = 0, usage_count: int = 0):
        self.name = name
        self.exec_cmd = exec_cmd
        self.icon = icon
        self.mime_types = mime_types or []
        self.app_type = app_type  # desktop, flatpak, snap, binary
        self.desktop_file = desktop_file
        self.app_id = app_id
        self.priority = priority  # 0=обычное, 1=рекомендуемое, 2=часто используемое
        self.usage_count = usage_count
        self.last_used = 0
        self.is_available = None  # None=не проверено, True=доступно, False=требует установки
        self.install_command = None  # Команда для установки

    def can_open(self, mime_type: str) -> bool:
        if not self.mime_types:
            return True
        # Приводим mime_type к строке на случай, если это объект MIMEtype
        mime_str = str(mime_type)
        return any(mt in mime_str or mime_str in mt for mt in self.mime_types)

    def is_relevant_for_target(self, target: str, mime_type: str) -> bool:
        """Проверка релевантности приложения для конкретной цели"""
        target_lower = target.lower()
        mime_str = str(mime_type).lower()
        
        # URL специфичные фильтры
        if target.startswith(('http://', 'https://')):
            # Исключаем явно неподходящие для веб
            if any(x in self.name.lower() for x in [
                'gimp', 'inkscape', 'blender', 'audacity', 
                'libreoffice calc', 'libreoffice impress'
            ]):
                return False
            # Приоритет для браузеров
            if any(x in self.name.lower() for x in [
                'firefox', 'chrome', 'chromium', 'browser', 'tor'
            ]):
                self.priority = max(self.priority, 1)
        
        # Файлы изображений
        elif mime_str.startswith('image/'):
            if any(x in self.name.lower() for x in [
                'gimp', 'image', 'photo', 'viewer', 'paint'
            ]):
                self.priority = max(self.priority, 1)
            # Исключаем текстовые редакторы для изображений
            if any(x in self.name.lower() for x in [
                'writer', 'calc', 'impress', 'text editor'
            ]):
                return False
        
        # Видео файлы
        elif mime_str.startswith('video/'):
            if any(x in self.name.lower() for x in [
                'vlc', 'player', 'video', 'mpv', 'totem'
            ]):
                self.priority = max(self.priority, 1)
            # Исключаем редакторы изображений для видео
            if any(x in self.name.lower() for x in [
                'gimp', 'inkscape', 'image viewer'
            ]):
                return False
        
        # Аудио файлы
        elif mime_str.startswith('audio/'):
            if any(x in self.name.lower() for x in [
                'rhythmbox', 'vlc', 'player', 'audio', 'music'
            ]):
                self.priority = max(self.priority, 1)
        
        # PDF документы
        elif 'pdf' in mime_str:
            if any(x in self.name.lower() for x in [
                'evince', 'okular', 'reader', 'pdf', 'document viewer'
            ]):
                self.priority = max(self.priority, 1)
        
        return True

    def check_availability(self) -> bool:
        """Проверка доступности приложения в системе"""
        if self.is_available is not None:
            return self.is_available
        
        # Получаем основную команду (первое слово)
        try:
            main_cmd = shlex.split(self.exec_cmd)[0]
        except (ValueError, IndexError):
            self.is_available = False
            return False
        
        # Проверяем различные типы приложений
        if self.app_type == 'flatpak':
            # Для Flatpak проверяем через flatpak list
            try:
                result = subprocess.run(['flatpak', 'info', self.app_id], 
                                      capture_output=True, timeout=3)
                self.is_available = result.returncode == 0
            except Exception:
                self.is_available = False
        elif self.app_type == 'snap':
            # Для Snap проверяем через snap list
            try:
                result = subprocess.run(['snap', 'info', self.app_id], 
                                      capture_output=True, timeout=3)
                self.is_available = result.returncode == 0
            except Exception:
                self.is_available = False
        else:
            # Для обычных приложений проверяем наличие в PATH или абсолютный путь
            if os.path.isabs(main_cmd):
                self.is_available = os.path.isfile(main_cmd) and os.access(main_cmd, os.X_OK)
            else:
                try:
                    result = subprocess.run(['which', main_cmd], 
                                          capture_output=True, timeout=2)
                    self.is_available = result.returncode == 0
                except Exception:
                    self.is_available = False
        
        # Определяем команду установки если приложение недоступно
        if not self.is_available:
            self.install_command = self._get_install_command()
        
        return self.is_available
    
    def _get_install_command(self) -> Optional[str]:
        """Определение команды установки для недоступного приложения"""
        install_commands = {
            # Браузеры
            'firefox': 'sudo apt install firefox',
            'google-chrome': 'wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && sudo apt install google-chrome-stable',
            'chromium': 'sudo apt install chromium-browser',
            'brave-browser': 'sudo apt install brave-browser',
            'opera': 'sudo snap install opera',
            
            # Медиа
            'vlc': 'sudo apt install vlc',
            'mpv': 'sudo apt install mpv',
            'rhythmbox': 'sudo apt install rhythmbox',
            'totem': 'sudo apt install totem',
            
            # Графика
            'gimp': 'sudo apt install gimp',
            'inkscape': 'sudo apt install inkscape',
            'blender': 'sudo snap install blender --classic',
            
            # Офис
            'libreoffice': 'sudo apt install libreoffice',
            'code': 'sudo snap install code --classic',
            'atom': 'sudo snap install atom --classic',
            
            # Просмотрщики
            'evince': 'sudo apt install evince',
            'okular': 'sudo apt install okular',
            'eog': 'sudo apt install eog',
            
            # Архиваторы
            'file-roller': 'sudo apt install file-roller',
            'ark': 'sudo apt install ark',
            
            # Текстовые редакторы
            'gedit': 'sudo apt install gedit',
            'kate': 'sudo apt install kate',
            'vim': 'sudo apt install vim',
            'nano': 'sudo apt install nano'
        }
        
        # Получаем основную команду
        try:
            main_cmd = shlex.split(self.exec_cmd)[0]
            return install_commands.get(main_cmd)
        except (ValueError, IndexError):
            return None
    
    def format_exec(self, targets: List[str]) -> List[str]:
        """Форматирование exec команды с правильной заменой плейсхолдеров"""
        cmd = self.exec_cmd
        
        # Удаляем стандартные плейсхолдеры
        cmd = cmd.replace('%U', '').replace('%F', '').replace('%u', '').replace('%f', '')
        cmd = cmd.replace('%i', '').replace('%c', '').replace('%k', '')
        
        # Разбиваем команду и добавляем цели
        parts = shlex.split(cmd)
        return parts + targets

class AppDiscovery:
    def __init__(self):
        self.apps = {}
        
    def discover_all(self) -> Dict[str, DesktopApp]:
        """Полное обнаружение всех приложений"""
        self.apps = {}
        
        # Основные методы обнаружения
        self._discover_desktop_files()
        self._discover_flatpak_apps()
        self._discover_snap_apps()
        self._discover_common_browsers()
        self._discover_tor_browser()  # Специальное обнаружение Tor
        
        # Проверяем доступность всех найденных приложений
        self._check_apps_availability()
        
        logger.info(f"Обнаружено {len(self.apps)} приложений")
        return self.apps
    
    def _check_apps_availability(self):
        """Проверка доступности всех приложений"""
        available_count = 0
        unavailable_count = 0
        
        for app in self.apps.values():
            if app.check_availability():
                available_count += 1
            else:
                unavailable_count += 1
        
        logger.info(f"Доступно: {available_count}, Требует установки: {unavailable_count}")
    
    def _discover_desktop_files(self):
        """Обнаружение через .desktop файлы"""
        desktop_dirs = []
        
        if HAS_XDG:
            desktop_dirs.extend([Path(d) / 'applications' for d in xdg_data_dirs])
        
        # Стандартные директории
        desktop_dirs.extend([
            Path('/usr/share/applications'),
            Path('/usr/local/share/applications'),
            Path.home() / '.local/share/applications',
            Path('/var/lib/flatpak/exports/share/applications'),
            Path.home() / '.local/share/flatpak/exports/share/applications'
        ])
        
        for desktop_dir in desktop_dirs:
            if not desktop_dir.exists():
                continue
                
            for desktop_file in desktop_dir.glob('*.desktop'):
                try:
                    self._parse_desktop_file(desktop_file)
                except Exception as e:
                    logger.debug(f"Ошибка парсинга {desktop_file}: {e}")
    
    def _parse_desktop_file(self, desktop_file: Path):
        """Парсинг .desktop файла"""
        if HAS_XDG:
            try:
                entry = DesktopEntry(str(desktop_file))
                name = entry.getName()
                exec_cmd = entry.getExec()
                icon = entry.getIcon()
                mime_types = entry.getMimeTypes()
                
                if exec_cmd and name and not entry.getHidden():
                    app_type = 'flatpak' if 'flatpak' in str(desktop_file) else 'desktop'
                    self.apps[name] = DesktopApp(
                        name=name,
                        exec_cmd=exec_cmd,
                        icon=icon,
                        mime_types=mime_types,
                        app_type=app_type,
                        desktop_file=str(desktop_file)
                    )
            except Exception:
                # Fallback парсинг
                self._parse_desktop_file_manual(desktop_file)
        else:
            self._parse_desktop_file_manual(desktop_file)
    
    def _parse_desktop_file_manual(self, desktop_file: Path):
        """Ручной парсинг .desktop файла"""
        try:
            with open(desktop_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entry_data = {}
            for line in content.split('\n'):
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    entry_data[key.strip()] = value.strip()
            
            name = entry_data.get('Name', '')
            exec_cmd = entry_data.get('Exec', '')
            icon = entry_data.get('Icon', '')
            mime_types = entry_data.get('MimeType', '').split(';')
            mime_types = [mt.strip() for mt in mime_types if mt.strip()]
            
            if exec_cmd and name and entry_data.get('Hidden', '').lower() != 'true':
                app_type = 'flatpak' if 'flatpak' in str(desktop_file) else 'desktop'
                self.apps[name] = DesktopApp(
                    name=name,
                    exec_cmd=exec_cmd,
                    icon=icon,
                    mime_types=mime_types,
                    app_type=app_type,
                    desktop_file=str(desktop_file)
                )
        except Exception as e:
            logger.debug(f"Ошибка ручного парсинга {desktop_file}: {e}")
    
    def _discover_flatpak_apps(self):
        """Обнаружение Flatpak приложений"""
        try:
            result = subprocess.run(['flatpak', 'list', '--app'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            name = parts[0]
                            app_id = parts[1]
                            exec_cmd = f"flatpak run {app_id}"
                            
                            if name not in self.apps:
                                self.apps[name] = DesktopApp(
                                    name=name,
                                    exec_cmd=exec_cmd,
                                    app_type='flatpak',
                                    app_id=app_id
                                )
        except Exception as e:
            logger.debug(f"Ошибка обнаружения Flatpak: {e}")
    
    def _discover_snap_apps(self):
        """Обнаружение Snap приложений"""
        try:
            result = subprocess.run(['snap', 'list'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Пропускаем заголовок
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 1:
                            name = parts[0]
                            exec_cmd = f"snap run {name}"
                            
                            if name not in self.apps:
                                self.apps[name] = DesktopApp(
                                    name=name.title(),
                                    exec_cmd=exec_cmd,
                                    app_type='snap',
                                    app_id=name
                                )
        except Exception as e:
            logger.debug(f"Ошибка обнаружения Snap: {e}")
    
    def _discover_common_browsers(self):
        """Обнаружение популярных браузеров"""
        common_browsers = [
            ('Firefox', 'firefox'),
            ('Google Chrome', 'google-chrome'),
            ('Chromium', 'chromium-browser'),
            ('Chromium', 'chromium'),
            ('Opera', 'opera'),
            ('Brave', 'brave-browser'),
            ('Microsoft Edge', 'microsoft-edge'),
            ('Vivaldi', 'vivaldi')
        ]
        
        for name, cmd in common_browsers:
            if self._command_exists(cmd) and name not in self.apps:
                self.apps[name] = DesktopApp(
                    name=name,
                    exec_cmd=cmd,
                    mime_types=['text/html', 'application/xhtml+xml'],
                    app_type='browser',
                    priority=1  # Браузеры получают высокий приоритет для URL
                )
    
    def _discover_tor_browser(self):
        """Специальное обнаружение Tor Browser"""
        # Стандартные пути установки Tor Browser
        tor_paths = [
            Path.home() / 'tor-browser_en-US' / 'Browser' / 'start-tor-browser',
            Path.home() / 'tor-browser' / 'Browser' / 'start-tor-browser',
            Path('/opt/tor-browser/Browser/start-tor-browser'),
            Path('/usr/local/bin/tor-browser'),
            Path('/usr/bin/tor-browser')
        ]
        
        # Поиск исполняемых файлов Tor
        tor_executables = []
        for tor_path in tor_paths:
            if tor_path.exists() and tor_path.is_file():
                tor_executables.append(tor_path)
        
        # Поиск в PATH
        if self._command_exists('tor-browser'):
            tor_executables.append('tor-browser')
        
        # Поиск через find (если есть права)
        try:
            result = subprocess.run([
                'find', str(Path.home()), '-name', 'start-tor-browser', 
                '-type', 'f', '-executable'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                for path in result.stdout.strip().split('\n'):
                    if path.strip():
                        tor_executables.append(Path(path.strip()))
        except Exception:
            pass
        
        # Добавляем найденные экземпляры Tor Browser
        for i, tor_exec in enumerate(tor_executables):
            name = 'Tor Browser' if i == 0 else f'Tor Browser ({i+1})'
            if name not in self.apps:
                self.apps[name] = DesktopApp(
                    name=name,
                    exec_cmd=str(tor_exec),
                    mime_types=['text/html', 'application/xhtml+xml'],
                    app_type='browser',
                    priority=1  # Высокий приоритет для приватности
                )
    
    def _command_exists(self, command: str) -> bool:
        """Проверка существования команды в PATH"""
        try:
            subprocess.run(['which', command], 
                         capture_output=True, timeout=2)
            return True
        except Exception:
            return False

class ConfigManager:
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        default_config = {
            'context_choices': {},
            'custom_apps': [],
            'default_app': None,
            'usage_stats': {},  # Статистика использования
            'ui_preferences': {  # Настройки UI
                'window_width': 800,
                'window_height': 600,
                'column_widths': {
                    'name': 200,
                    'type': 100,
                    'priority': 80
                },
                'sort_column': 'priority',
                'sort_order': 'desc',
                'show_all_apps': True,
                'last_geometry': None
            }
        }
        
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    loaded_config = json.load(f)
                    # Объединяем с дефолтными настройками
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in loaded_config[key]:
                                    loaded_config[key][subkey] = subvalue
                    return loaded_config
            except Exception as e:
                logger.error(f"Ошибка загрузки конфигурации: {e}")
        
        return default_config
    
    def save_config(self):
        """Сохранение конфигурации в файл"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения конфигурации: {e}")

    def get_context_choice(self, context: str, mime_type: str) -> Optional[str]:
        """Получение запомненного выбора для контекста и MIME типа"""
        return self.config['context_choices'].get(f"{context}:{mime_type}")

    def set_context_choice(self, context: str, mime_type: str, app_name: str):
        """Запоминание выбора для контекста и MIME типа"""
        self.config['context_choices'][f"{context}:{mime_type}"] = app_name

    def clear_context_choice(self, context: str, mime_type: str):
        """Очистка запомненного выбора для контекста и MIME типа"""
        choice_key = f"{context}:{mime_type}"
        if choice_key in self.config['context_choices']:
            del self.config['context_choices'][choice_key]

    def clear_all_associations(self):
        """Очистка всех ассоциаций"""
        self.config['context_choices'] = {}

    def increment_usage(self, app_name: str):
        """Увеличение счетчика использования приложения"""
        if 'usage_stats' not in self.config:
            self.config['usage_stats'] = {}
        
        if app_name not in self.config['usage_stats']:
            self.config['usage_stats'][app_name] = {
                'count': 0,
                'last_used': 0
            }
        
        self.config['usage_stats'][app_name]['count'] += 1
        self.config['usage_stats'][app_name]['last_used'] = int(time.time())

    def get_usage_stats(self, app_name: str) -> Tuple[int, int]:
        """Получение статистики использования приложения"""
        stats = self.config.get('usage_stats', {}).get(app_name, {})
        return stats.get('count', 0), stats.get('last_used', 0)

    def save_ui_preferences(self, prefs: Dict[str, Any]):
        """Сохранение настроек UI"""
        self.config['ui_preferences'].update(prefs)

    def get_ui_preferences(self) -> Dict[str, Any]:
        """Получение настроек UI"""
        return self.config.get('ui_preferences', {})

class ContextDetector:
    @staticmethod
    def get_invoker_context() -> str:
        """Определение контекста вызова приложения"""
        # Проверяем переменные окружения
        if os.environ.get('CURSOR_SESSION'):
            return 'cursor'
        if os.environ.get('VSCODE_PID'):
            return 'vscode'
        if os.environ.get('TERMINAL'):
            return 'terminal'
        
        # Проверяем родительские процессы
        try:
            import psutil
            current = psutil.Process()
            for parent in current.parents():
                parent_name = parent.name().lower()
                if 'cursor' in parent_name:
                    return 'cursor'
                elif 'code' in parent_name:
                    return 'vscode'
                elif any(term in parent_name for term in ['terminal', 'konsole', 'gnome-terminal']):
                    return 'terminal'
                elif any(fm in parent_name for fm in ['nautilus', 'dolphin', 'thunar', 'nemo']):
                    return 'filemanager'
        except ImportError:
            pass
        
        # Fallback определение через PPID
        try:
            result = subprocess.run(['ps', '-p', str(os.getppid()), '-o', 'comm='], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                parent_name = result.stdout.strip().lower()
                if 'cursor' in parent_name:
                    return 'cursor'
                elif any(term in parent_name for term in ['terminal', 'bash', 'zsh']):
                    return 'terminal'
        except Exception:
            pass
        
        return 'unknown'

class AppChooserDialog:
    def __init__(self, apps: Dict[str, DesktopApp], targets: List[str], 
                 context: str, mime_type: str, config_manager: ConfigManager):
        self.apps = apps
        self.targets = targets
        self.context = context
        self.mime_type = mime_type
        self.config_manager = config_manager
        self.selected_app = None
        self.remember_choice = False
        self.show_all_apps = True
        
        # Загружаем настройки UI
        self.ui_prefs = config_manager.get_ui_preferences()
        
        # Применяем статистику использования к приложениям
        self._apply_usage_stats()
        
        # Фильтруем и сортируем приложения
        self.filtered_apps = self._filter_and_sort_apps()
        
    def _apply_usage_stats(self):
        """Применение статистики использования к приложениям"""
        for app in self.apps.values():
            usage_count, last_used = self.config_manager.get_usage_stats(app.name)
            app.usage_count = usage_count
            app.last_used = last_used
            
            # Определяем приоритет на основе использования
            if usage_count >= 10:  # Часто используемое
                app.priority = max(app.priority, 2)
            elif usage_count >= 3:  # Умеренно используемое
                app.priority = max(app.priority, 1)
    
    def _filter_and_sort_apps(self) -> Dict[str, DesktopApp]:
        """Фильтрация и сортировка приложений"""
        # Фильтруем по совместимости и релевантности
        compatible_apps = {}
        for name, app in self.apps.items():
            if app.can_open(self.mime_type) and app.is_relevant_for_target(self.targets[0], self.mime_type):
                compatible_apps[name] = app
        
        # Сортируем по приоритету, затем по использованию, затем по имени
        sorted_apps = dict(sorted(
            compatible_apps.items(),
            key=lambda x: (-x[1].priority, -x[1].usage_count, x[1].name.lower())
        ))
        
        return sorted_apps
    
    def show(self) -> Tuple[Optional[DesktopApp], bool]:
        """Показ диалога выбора приложения"""
        dialog = Gtk.Dialog(
            title="Выберите приложение",
            modal=True,
            destroy_with_parent=True
        )
        
        # Устанавливаем размер из настроек
        dialog.set_default_size(
            self.ui_prefs.get('window_width', 800),
            self.ui_prefs.get('window_height', 600)
        )
        
        # Основные кнопки
        dialog.add_button("Отмена", Gtk.ResponseType.CANCEL)
        dialog.add_button("Открыть", Gtk.ResponseType.OK)
        
        # Дополнительные кнопки
        reset_button = dialog.add_button("Сбросить ассоциации", Gtk.ResponseType.HELP)
        reset_button.connect("clicked", self._on_reset_associations)
        
        content_area = dialog.get_content_area()
        content_area.set_spacing(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        
        # Информация о контексте
        context_label = Gtk.Label()
        context_label.set_text(f"Контекст: {self.context} | MIME: {self.mime_type}")
        context_label.set_margin_bottom(10)
        content_area.pack_start(context_label, False, False, 0)
        
        # Чекбокс показать все приложения
        self.show_all_checkbox = Gtk.CheckButton(label="Показать все приложения")
        self.show_all_checkbox.set_active(self.ui_prefs.get('show_all_apps', True))
        self.show_all_checkbox.connect("toggled", self._on_show_all_toggled)
        content_area.pack_start(self.show_all_checkbox, False, False, 0)
        
        # Поиск
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        search_label = Gtk.Label(label="Поиск:")
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Введите название приложения...")
        self.search_entry.connect("changed", self._on_search_changed)
        search_box.pack_start(search_label, False, False, 0)
        search_box.pack_start(self.search_entry, True, True, 0)
        content_area.pack_start(search_box, False, False, 0)
        
        # Создаем TreeView с настраиваемыми колонками
        self._create_tree_view()
        
        # ScrolledWindow для списка
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.tree_view)
        scrolled.set_size_request(-1, 350)
        content_area.pack_start(scrolled, True, True, 0)
        
        # Чекбокс запоминания
        self.remember_checkbox = Gtk.CheckButton(label="Запомнить выбор для этого типа файлов")
        content_area.pack_start(self.remember_checkbox, False, False, 0)
        
        # Кнопка добавления приложения
        add_button = Gtk.Button(label="Добавить приложение...")
        add_button.connect("clicked", self._on_add_custom_app)
        content_area.pack_start(add_button, False, False, 0)
        
        dialog.show_all()
        
        # Обновляем список приложений
        self._update_app_list()
        
        # Показываем диалог
        response = dialog.run()
        
        # Сохраняем настройки UI перед закрытием
        self._save_ui_state(dialog)
        
        if response == Gtk.ResponseType.OK:
            selection = self.tree_view.get_selection()
            model, treeiter = selection.get_selected()
            if treeiter:
                app_name = model[treeiter][0]
                selected_app = self.filtered_apps.get(app_name)
                
                # Проверяем доступность приложения
                if selected_app and not selected_app.is_available:
                    # Показываем диалог подтверждения для недоступного приложения
                    if self._confirm_install_app(selected_app, dialog):
                        self.selected_app = selected_app
                        self.remember_choice = self.remember_checkbox.get_active()
                    else:
                        # Пользователь отменил, не закрываем диалог
                        dialog.destroy()
                        return self.show()  # Показываем диалог заново
                else:
                    self.selected_app = selected_app
                    self.remember_choice = self.remember_checkbox.get_active()
        
        dialog.destroy()
        return self.selected_app, self.remember_choice
    
    def _create_tree_view(self):
        """Создание TreeView с настраиваемыми колонками"""
        # Модель данных: название, тип, приоритет, использование
        self.list_store = Gtk.ListStore(str, str, str, str)
        
        self.tree_view = Gtk.TreeView(model=self.list_store)
        self.tree_view.set_headers_visible(True)
        self.tree_view.set_reorderable(False)
        self.tree_view.set_search_column(0)
        
        # Колонка названия
        name_column = Gtk.TreeViewColumn("Приложение")
        name_renderer = Gtk.CellRendererText()
        name_column.pack_start(name_renderer, True)
        name_column.add_attribute(name_renderer, "text", 0)
        name_column.set_resizable(True)
        name_column.set_sort_column_id(0)
        name_column.set_fixed_width(self.ui_prefs.get('column_widths', {}).get('name', 200))
        self.tree_view.append_column(name_column)
        
        # Колонка типа
        type_column = Gtk.TreeViewColumn("Тип")
        type_renderer = Gtk.CellRendererText()
        type_column.pack_start(type_renderer, True)
        type_column.add_attribute(type_renderer, "text", 1)
        type_column.set_resizable(True)
        type_column.set_sort_column_id(1)
        type_column.set_fixed_width(self.ui_prefs.get('column_widths', {}).get('type', 100))
        self.tree_view.append_column(type_column)
        
        # Колонка приоритета
        priority_column = Gtk.TreeViewColumn("Статус")
        priority_renderer = Gtk.CellRendererText()
        priority_column.pack_start(priority_renderer, True)
        priority_column.add_attribute(priority_renderer, "text", 2)
        priority_column.set_resizable(True)
        priority_column.set_sort_column_id(2)
        priority_column.set_fixed_width(self.ui_prefs.get('column_widths', {}).get('priority', 80))
        self.tree_view.append_column(priority_column)
        
        # Колонка использования
        usage_column = Gtk.TreeViewColumn("Использований")
        usage_renderer = Gtk.CellRendererText()
        usage_column.pack_start(usage_renderer, True)
        usage_column.add_attribute(usage_renderer, "text", 3)
        usage_column.set_resizable(True)
        usage_column.set_sort_column_id(3)
        usage_column.set_fixed_width(self.ui_prefs.get('column_widths', {}).get('usage', 100))
        self.tree_view.append_column(usage_column)
        
        # Применяем сохраненную сортировку
        sort_column = self.ui_prefs.get('sort_column', 'priority')
        sort_order = self.ui_prefs.get('sort_order', 'desc')
        
        column_map = {'name': 0, 'type': 1, 'priority': 2, 'usage': 3}
        if sort_column in column_map:
            sort_type = Gtk.SortType.DESCENDING if sort_order == 'desc' else Gtk.SortType.ASCENDING
            self.list_store.set_sort_column_id(column_map[sort_column], sort_type)
    
    def _update_app_list(self):
        """Обновление списка приложений"""
        self.list_store.clear()
        
        search_text = self.search_entry.get_text().lower() if hasattr(self, 'search_entry') else ""
        show_all = self.show_all_checkbox.get_active() if hasattr(self, 'show_all_checkbox') else True
        
        for name, app in self.filtered_apps.items():
            # Фильтр поиска
            if search_text and search_text not in name.lower():
                continue
            
            # Фильтр показа всех приложений
            if not show_all and app.priority == 0 and app.usage_count == 0:
                continue
            
            # Определяем статус приложения
            if not app.is_available:
                status = "❌ Установить"
            elif app.priority == 2:
                status = "★★ Часто используемое"
            elif app.priority == 1:
                status = "★ Рекомендуемое"
            elif app.usage_count > 0:
                status = f"Использовано {app.usage_count}x"
            else:
                status = "✅ Доступно"
            
            # Тип приложения
            type_map = {
                'desktop': 'Системное',
                'flatpak': 'Flatpak',
                'snap': 'Snap',
                'browser': 'Браузер',
                'custom': 'Пользовательское'
            }
            app_type = type_map.get(app.app_type, app.app_type.title())
            
            self.list_store.append([name, app_type, status, str(app.usage_count)])
    
    def _on_show_all_toggled(self, checkbox):
        """Обработчик переключения показа всех приложений"""
        self._update_app_list()
    
    def _on_search_changed(self, entry):
        """Обработчик изменения поискового запроса"""
        self._update_app_list()
    
    def _on_reset_associations(self, button):
        """Обработчик сброса ассоциаций"""
        dialog = Gtk.MessageDialog(
            transient_for=button.get_toplevel(),
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Сбросить ассоциации?"
        )
        dialog.format_secondary_text(
            "Это удалит все запомненные выборы приложений для всех типов файлов. "
            "Вы уверены?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.YES:
            self.config_manager.clear_all_associations()
            self.config_manager.save_config()
            
            # Показываем уведомление
            info_dialog = Gtk.MessageDialog(
                transient_for=button.get_toplevel(),
                flags=Gtk.DialogFlags.MODAL,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Ассоциации сброшены"
            )
            info_dialog.format_secondary_text("Все запомненные выборы приложений удалены.")
            info_dialog.run()
            info_dialog.destroy()
    
    def _on_add_custom_app(self, button):
        """Обработчик добавления пользовательского приложения"""
        dialog = Gtk.FileChooserDialog(
            title="Выберите исполняемый файл",
            parent=button.get_toplevel(),
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_button("Отмена", Gtk.ResponseType.CANCEL)
        dialog.add_button("Выбрать", Gtk.ResponseType.OK)
        
        # Фильтр для исполняемых файлов
        filter_exec = Gtk.FileFilter()
        filter_exec.set_name("Исполняемые файлы")
        filter_exec.add_mime_type("application/x-executable")
        filter_exec.add_pattern("*.AppImage")
        dialog.add_filter(filter_exec)
        
        filter_all = Gtk.FileFilter()
        filter_all.set_name("Все файлы")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            if file_path:
                # Создаем пользовательское приложение
                app_name = Path(file_path).stem.title()
                custom_app = DesktopApp(
                    name=app_name,
                    exec_cmd=file_path,
                    app_type='custom'
                )
                
                # Добавляем в список
                self.apps[app_name] = custom_app
                self.filtered_apps[app_name] = custom_app
                
                # Сохраняем в конфигурацию
                self.config_manager.config['custom_apps'].append({
                    'name': app_name,
                    'exec_cmd': file_path,
                    'mime_types': [],
                    'original_path': file_path
                })
                self.config_manager.save_config()
                
                # Обновляем список
                self._update_app_list()
        
        dialog.destroy()
    
    def _save_ui_state(self, dialog):
        """Сохранение состояния UI"""
        # Размер окна
        width, height = dialog.get_size()
        
        # Ширина колонок
        columns = self.tree_view.get_columns()
        column_widths = {
            'name': columns[0].get_width(),
            'type': columns[1].get_width(),
            'priority': columns[2].get_width(),
            'usage': columns[3].get_width()
        }
        
        # Сортировка
        sort_column_id, sort_order = self.list_store.get_sort_column_id()
        sort_column_map = {0: 'name', 1: 'type', 2: 'priority', 3: 'usage'}
        sort_column = sort_column_map.get(sort_column_id, 'priority')
        sort_order_str = 'desc' if sort_order == Gtk.SortType.DESCENDING else 'asc'
        
        # Сохраняем настройки
        ui_prefs = {
            'window_width': width,
            'window_height': height,
            'column_widths': column_widths,
            'sort_column': sort_column,
            'sort_order': sort_order_str,
            'show_all_apps': self.show_all_checkbox.get_active()
        }
        
        self.config_manager.save_ui_preferences(ui_prefs)
    
    def _confirm_install_app(self, app: DesktopApp, parent_dialog) -> bool:
        """Диалог подтверждения для установки недоступного приложения"""
        confirm_dialog = Gtk.MessageDialog(
            transient_for=parent_dialog,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Приложение '{app.name}' не установлено"
        )
        
        # Формируем детальное сообщение
        secondary_text = f"Выбранное приложение '{app.name}' отсутствует в системе.\n\n"
        
        if app.install_command:
            secondary_text += f"Команда для установки:\n{app.install_command}\n\n"
            secondary_text += "Хотите продолжить? Приложение не будет запущено, но выбор будет сохранён."
        else:
            secondary_text += "Команда установки неизвестна.\n\n"
            secondary_text += "Установите приложение вручную или выберите другое.\n"
            secondary_text += "Продолжить с недоступным приложением?"
        
        confirm_dialog.format_secondary_text(secondary_text)
        
        # Добавляем кнопку "Установить" если есть команда установки
        if app.install_command:
            install_button = confirm_dialog.add_button("Установить сейчас", Gtk.ResponseType.APPLY)
            install_button.get_style_context().add_class("suggested-action")
        
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        
        if response == Gtk.ResponseType.APPLY and app.install_command:
            # Показываем диалог установки
            self._show_install_dialog(app, parent_dialog)
            return False  # Не продолжаем с выбором
        elif response == Gtk.ResponseType.YES:
            return True  # Продолжаем с недоступным приложением
        else:
            return False  # Отменяем выбор
    
    def _show_install_dialog(self, app: DesktopApp, parent_dialog):
        """Показ диалога установки приложения"""
        install_dialog = Gtk.MessageDialog(
            transient_for=parent_dialog,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=f"Установка {app.name}"
        )
        
        secondary_text = f"Скопируйте и выполните команду в терминале:\n\n{app.install_command}\n\n"
        secondary_text += "После установки приложение станет доступным для выбора."
        
        install_dialog.format_secondary_text(secondary_text)
        
        # Добавляем кнопку копирования в буфер обмена
        copy_button = install_dialog.add_button("Скопировать команду", Gtk.ResponseType.HELP)
        copy_button.connect("clicked", lambda btn: self._copy_to_clipboard(app.install_command))
        
        install_dialog.run()
        install_dialog.destroy()
    
    def _copy_to_clipboard(self, text: str):
        """Копирование текста в буфер обмена"""
        try:
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(text, -1)
            clipboard.store()
        except Exception as e:
            logger.debug(f"Ошибка копирования в буфер: {e}")

class OpenWithChooser:
    def __init__(self):
        self.discovery = AppDiscovery()
        self.config_manager = ConfigManager()
        
    def get_mime_type(self, target: str) -> str:
        """Получение MIME типа для цели"""
        if target.startswith(('http://', 'https://')):
            return 'text/html'
        elif target.startswith('file://'):
            target = target[7:]  # Удаляем префикс file://
        
        # Пытаемся получить MIME тип
        if HAS_XDG:
            try:
                mime_obj = Mime.get_type(target)
                return str(mime_obj) if mime_obj else 'application/octet-stream'
            except:
                pass
        
        # Fallback на основе расширения
        ext = Path(target).suffix.lower()
        mime_map = {
            '.txt': 'text/plain',
            '.html': 'text/html', '.htm': 'text/html',
            '.pdf': 'application/pdf',
            '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.gif': 'image/gif', '.bmp': 'image/bmp',
            '.mp4': 'video/mp4', '.avi': 'video/x-msvideo',
            '.mp3': 'audio/mpeg', '.wav': 'audio/wav',
            '.zip': 'application/zip', '.tar': 'application/x-tar',
            '.gz': 'application/gzip',
            '.deb': 'application/vnd.debian.binary-package',
            '.AppImage': 'application/x-executable'
        }
        
        return mime_map.get(ext, 'application/octet-stream')
    
    def run_app(self, app: DesktopApp, targets: List[str]) -> bool:
        """Запуск приложения с целями"""
        # Проверяем доступность приложения
        if not app.is_available:
            logger.warning(f"Приложение {app.name} недоступно, запуск пропущен")
            return False
            
        try:
            cmd = app.format_exec(targets)
            logger.info(f"Запуск: {' '.join(cmd)}")
            
            # Увеличиваем счетчик использования
            self.config_manager.increment_usage(app.name)
            self.config_manager.save_config()
            
            subprocess.Popen(cmd, start_new_session=True)
            return True
        except Exception as e:
            logger.error(f"Ошибка запуска {app.name}: {e}")
            return False
    
    def choose_and_run(self, targets: List[str]):
        """Основной метод: выбор и запуск приложения"""
        if not targets:
            return
        
        # Определяем контекст и MIME тип
        context = ContextDetector.get_invoker_context()
        mime_type = self.get_mime_type(targets[0])
        
        logger.info(f"Контекст: {context}, MIME: {mime_type}, Цели: {targets}")
        
        # Проверяем запомненный выбор
        remembered_app = self.config_manager.get_context_choice(context, mime_type)
        apps = self.discovery.discover_all()
        
        if remembered_app and remembered_app in apps:
            if self.run_app(apps[remembered_app], targets):
                return
            else:
                # Удаляем плохой запомненный выбор
                self.config_manager.clear_context_choice(context, mime_type)
                self.config_manager.save_config()
        
        # Показываем диалог выбора
        try:
            dialog = AppChooserDialog(apps, targets, context, mime_type, self.config_manager)
            selected_app, remember = dialog.show()
            
            if selected_app:
                if remember:
                    self.config_manager.set_context_choice(context, mime_type, selected_app.name)
                    self.config_manager.save_config()

                self.run_app(selected_app, targets)
        except Exception as e:
            logger.error(f"Ошибка диалога: {e}")

def main():
    if len(sys.argv) < 2:
        print("Использование: open-with-chooser <url|файл> [файл2] ...")
        sys.exit(1)
    
    targets = sys.argv[1:]
    
    try:
        chooser = OpenWithChooser()
        chooser.choose_and_run(targets)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
