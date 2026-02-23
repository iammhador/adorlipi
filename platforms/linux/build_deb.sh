#!/bin/bash
set -e

VERSION="1.0.0"
ARCH="all"
PKG_NAME="adorlipi"
DEB_DIR="${PKG_NAME}_${VERSION}_${ARCH}"

# Resolve project root (two levels up from this script: platforms/linux/ -> root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Building Debian package for AdorLipi v$VERSION..."
echo "Project root: $PROJECT_ROOT"

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
Maintainer: AdorLipi Team <adorlipi@example.com>
Depends: ibus, gir1.2-ibus-1.0, python3, python3-gi
Description: AdorLipi (আদরলিপি) - Modern Banglish Keyboard
 The first modern and easy-to-use Banglish keyboard for Linux users.
 Type exactly how you speak on social media. Features a 10,000+ word conversational dictionary.
EOT

# Copy files
cp -r "$PROJECT_ROOT/core" "$DEB_DIR/usr/share/adorlipi/"
cp -r "$PROJECT_ROOT/data" "$DEB_DIR/usr/share/adorlipi/"
cp -r "$PROJECT_ROOT/assets" "$DEB_DIR/usr/share/adorlipi/"
cp "$SCRIPT_DIR/ibus_engine.py" "$DEB_DIR/usr/libexec/ibus-engine-adorlipi"
chmod +x "$DEB_DIR/usr/libexec/ibus-engine-adorlipi"
cp "$SCRIPT_DIR/adorlipi-ibus.xml" "$DEB_DIR/usr/share/ibus/component/adorlipi.xml"

# Add a post-install script to restart IBus
mkdir -p "$DEB_DIR/DEBIAN"
cat <<'POSTINST' > "$DEB_DIR/DEBIAN/postinst"
#!/bin/bash
ibus restart 2>/dev/null || true
echo "AdorLipi installed! Restart IBus and add AdorLipi in Settings -> Keyboard."
POSTINST
chmod +x "$DEB_DIR/DEBIAN/postinst"

# Build the package
dpkg-deb --build "$DEB_DIR"

echo "Package built: ${DEB_DIR}.deb"
# Cleanup
rm -r "$DEB_DIR"

