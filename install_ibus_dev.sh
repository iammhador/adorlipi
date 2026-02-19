#!/bin/bash

# AdorLipi *Developer* IBus Installer
# Uses Symlinks so you can edit code and see changes (after ibus restart)

echo "-----------------------------------"
echo "AdorLipi DEV Installer (Symlinked)"
echo "-----------------------------------"

# Check for root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root (sudo ./install_ibus_dev.sh)"
  exit 1
fi

# Get absolute path of current directory
REPO_DIR=$(pwd)
DEST_DIR="/usr/share/adorlipi"
IBUS_COMPONENT_DIR="/usr/share/ibus/component"

echo "1. Installing Python dependencies in EDITABLE mode..."
# This allows python to import 'adorlipi' from the source directory directly
pip3 install -e .

echo "2. Installing System Dependencies..."
if [ -f /etc/debian_version ]; then
    apt update && apt install -y python3-gi gir1.2-ibus-1.0
elif [ -f /etc/redhat-release ]; then
    dnf install -y python3-gobject ibus-devel
fi

echo "3. creating Symlinks..."
# Remove existing directory/files if they exist
rm -rf $DEST_DIR
rm -f $IBUS_COMPONENT_DIR/adorlipi-ibus.xml

# Create the parent directory structure so we can link the repo inside it
# We want /usr/share/adorlipi to BE the repo dir, or contain it?
# The XML says exec: /usr/share/adorlipi/adorlipi/ibus_engine.py
# So if /usr/share/adorlipi -> REPO_DIR, then REPO_DIR/adorlipi/ibus_engine.py works.
ln -s "$REPO_DIR" "$DEST_DIR"

# Link XML
ln -s "$REPO_DIR/adorlipi-ibus.xml" "$IBUS_COMPONENT_DIR/adorlipi-ibus.xml"

echo "4. Setting permissions..."
chmod +x "$REPO_DIR/adorlipi/ibus_engine.py"

echo "5. Refreshing IBus..."
ibus restart || echo "Could not restart IBus automatically. Please restart it manually."

echo "-----------------------------------"
echo "DEV Installation Complete!"
echo "Your code at $REPO_DIR is now live."
echo "Edit files -> Run 'ibus restart' -> Test changes."
echo "-----------------------------------"
