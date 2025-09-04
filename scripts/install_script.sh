#!/bin/bash
set -e

echo "=== Open-with-chooser Installation ==="

# Create directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.config/open-with-chooser

# Install dependencies
echo "Installing dependencies..."
if command -v apt-get >/dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 wmctrl zenity python3-xdg
elif command -v dnf >/dev/null; then
    sudo dnf install -y python3-gobject gtk3-devel wmctrl zenity python3-pyxdg
elif command -v pacman >/dev/null; then
    sudo pacman -S --noconfirm python-gobject gtk3 wmctrl zenity python-pyxdg
elif command -v zypper >/dev/null; then
    sudo zypper install -y python3-gobject-Gdk typelib-1_0-Gtk-3_0 wmctrl zenity python3-pyxdg
else
    echo "Warning: Unknown package manager. Please install python3-gi, wmctrl, zenity manually"
fi

# Copy main script
cp open-with-chooser.py ~/.local/bin/
chmod +x ~/.local/bin/open-with-chooser.py

# Create symlink without .py extension
ln -sf ~/.local/bin/open-with-chooser.py ~/.local/bin/open-with-chooser

# Create desktop file
cat > ~/.local/share/applications/open-with-chooser.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Open With Chooser
Comment=Universal application chooser for URLs and files
Exec=open-with-chooser %U
Icon=applications-other
Terminal=false
MimeType=text/html;text/plain;application/pdf;image/png;image/jpeg;video/mp4;audio/mpeg;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;
Categories=Utility;
NoDisplay=false
EOF

# Update desktop database
if command -v update-desktop-database >/dev/null; then
    update-desktop-database ~/.local/share/applications/
fi

# Set as default for web schemes (optional)
echo "Setting as default handler for web URLs..."
xdg-mime default open-with-chooser.desktop x-scheme-handler/http
xdg-mime default open-with-chooser.desktop x-scheme-handler/https

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "Added ~/.local/bin to PATH in ~/.bashrc"
fi

echo ""
echo "=== Installation Complete ==="
echo "open-with-chooser is now installed and registered as default web handler"
echo "You can:"
echo "  - Run 'open-with-chooser <url>' from terminal"
echo "  - Right-click files and choose 'Open With -> Open With Chooser'"
echo "  - It will automatically handle web links"
echo ""
echo "Log file: ~/.config/open-with-chooser/chooser.log"
echo "Config: ~/.config/open-with-chooser/config.json"