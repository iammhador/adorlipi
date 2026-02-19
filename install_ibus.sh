#!/bin/bash

# AdorLipi IBus Installer

echo "-----------------------------------"
echo "AdorLipi IBus Installer"
echo "-----------------------------------"

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install_ibus.sh)"
  exit 1
fi

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

# echo "1. Installing Python dependencies..."
# pip3 install . (Skipped for lightweight install)

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
cp -r adorlipi $DEST_DIR/
cp setup.py $DEST_DIR/
# Copy icon if we had one, creating a dummy one or skipping for now.
cp adorlipi/assets/logo.svg $DEST_DIR/

cp adorlipi-ibus.xml $IBUS_COMPONENT_DIR/

echo "4. Setting permissions..."
chmod +x $DEST_DIR/adorlipi/ibus_engine.py

echo "5. Refreshing IBus..."
# Restart ibus-daemon or just exit, user usually needs to logout/login or restart ibus
ibus restart || echo "Could not restart IBus automatically. Please restart it manually."

echo "-----------------------------------"
echo "Installation Complete!"
echo "Please restart IBus or Log out and Log back in."
echo "Then go to Settings -> Keyboard -> Input Sources -> Add -> Bangla -> AdorLipi."
echo "-----------------------------------"
