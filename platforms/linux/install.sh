#!/bin/bash

# AdorLipi IBus Installer (Monorepo)
# Run from project root: sudo bash platforms/linux/install.sh

echo "-----------------------------------"
echo "AdorLipi (আদরলিপি) IBus Installer"
echo "-----------------------------------"

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo bash platforms/linux/install.sh)"
  exit 1
fi

# Detect project root (two levels up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Project root: $PROJECT_ROOT"

# Check for Python 3 and install if missing
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing..."
    if [ -f /etc/debian_version ]; then
        apt update && apt install -y python3
    elif [ -f /etc/redhat-release ]; then
        dnf install -y python3
    else
        echo "Error: Please install Python 3 manually."
        exit 1
    fi
fi

DEST_DIR="/usr/share/adorlipi"
IBUS_COMPONENT_DIR="/usr/share/ibus/component"

echo "2. Installing System Dependencies..."
if [ -f /etc/debian_version ]; then
    apt update && apt install -y python3-gi gir1.2-ibus-1.0
elif [ -f /etc/redhat-release ]; then
    dnf install -y python3-gobject ibus-devel
else
    echo "Warning: Unknown distro. Please ensure python3-gi / python3-gobject is installed."
fi

echo "3. Copying files..."
mkdir -p $DEST_DIR

# Copy core engine
cp -r "$PROJECT_ROOT/core" "$DEST_DIR/"

# Copy shared data
cp -r "$PROJECT_ROOT/data" "$DEST_DIR/"

# Copy platform-specific files
cp "$SCRIPT_DIR/ibus_engine.py" "$DEST_DIR/"

# Copy assets
cp -r "$PROJECT_ROOT/assets" "$DEST_DIR/"

# Copy IBus component XML
cp "$SCRIPT_DIR/adorlipi-ibus.xml" "$IBUS_COMPONENT_DIR/"

echo "4. Setting permissions..."
chmod +x "$DEST_DIR/ibus_engine.py"

echo "5. Refreshing IBus..."
ibus restart || echo "Could not restart IBus automatically. Please restart it manually."

echo "-----------------------------------"
echo "Installation Complete!"
echo "Please restart IBus or Log out and Log back in."
echo "Then go to Settings -> Keyboard -> Input Sources -> Add -> Bangla -> AdorLipi (আদরলিপি)."
echo "-----------------------------------"
