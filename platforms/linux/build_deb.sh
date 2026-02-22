#!/bin/bash
set -e

VERSION="1.0.0"
ARCH="all"
PKG_NAME="adorlipi"
DEB_DIR="${PKG_NAME}_${VERSION}_${ARCH}"

echo "Building Debian package for AdorLipi v$VERSION..."

# Create directory structure
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/share/ibus/component"
mkdir -p "$DEB_DIR/usr/libexec"
mkdir -p "$DEB_DIR/usr/share/adorlipi"

# Create control file
cat <<EOT > "$DEB_DIR/DEBIAN/control"
Package: adorlipi
Version: $VERSION
Architecture: $ARCH
Maintainer: Your Name <your.email@example.com>
Depends: ibus, gir1.2-ibus-1.0, python3, python3-gi
Description: AdorLipi Phonetic Banglish Keyboard
 A smart phonetic keyboard for typing Bengali via IBus.
 Features a 10,000+ word dictionary with slang support.
EOT

# Copy files
cp -r ../../core "$DEB_DIR/usr/share/adorlipi/"
cp -r ../../data "$DEB_DIR/usr/share/adorlipi/"
cp ibus_engine.py "$DEB_DIR/usr/libexec/ibus-engine-adorlipi"
chmod +x "$DEB_DIR/usr/libexec/ibus-engine-adorlipi"

# Adapt adorlipi.xml paths for the package
cat adorlipi.xml | sed 's|/usr/libexec/ibus-engine-adorlipi|/usr/libexec/ibus-engine-adorlipi|g' > "$DEB_DIR/usr/share/ibus/component/adorlipi.xml"


# Build the package
dpkg-deb --build "$DEB_DIR"

echo "Package built: ${DEB_DIR}.deb"
# Cleanup
rm -r "$DEB_DIR"
