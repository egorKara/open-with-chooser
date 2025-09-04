# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-04 - Enhanced Release

### Added
- ✨ Application availability checking system
- ✨ Installation dialog for unavailable applications
- ✨ Installation commands database (25+ popular apps)
- ✨ Smart sorting: recommended → frequently used → others
- ✨ Configurable columns with width memory
- ✨ Show/hide irrelevant apps checkbox
- ✨ Reset associations button
- ✨ Copy installation commands to clipboard
- ✨ Enhanced Tor Browser detection
- ✨ Smart filtering by file type

### Changed
- 🔧 Improved GTK3 compatibility (fixed deprecation warnings)
- 🔧 Enhanced UI responsiveness and performance
- 🔧 Better MIME type detection and handling
- 🔧 Improved error handling and logging

### Fixed
- 🐛 Fixed application command validation
- 🐛 Fixed crash when selecting unavailable apps
- 🐛 Fixed column resizing issues
- 🐛 Fixed context detection accuracy

## [1.0.0] - 2025-09-03 - Initial Release

### Added
- 🎉 Initial release of Open With Chooser
- ✨ Basic application selection functionality
- ✨ Context-aware choice memory
- ✨ Desktop files, Flatpak, and Snap support
- ✨ GTK3 interface with search functionality
- ✨ MIME type detection
- ✨ Usage statistics tracking
- ✨ Custom application support

### Features
- Application discovery from multiple sources
- Context detection (IDE, terminal, file manager)
- Persistent configuration
- Cross-platform Linux support
- Extensible architecture
