#!/bin/bash
set -e

VERSION="1.0.0"
PKG_NAME="adorlipi"
BUILD_DIR="${PKG_NAME}-${VERSION}-rpm"

# Resolve project root (two levels up: platforms/linux/ -> root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Building RPM package for AdorLipi v$VERSION (Fedora/RHEL)..."
echo "Project root: $PROJECT_ROOT"

# Ensure rpm-build is installed
if ! command -v rpmbuild &> /dev/null; then
    echo "rpmbuild not found. Installing rpm-build..."
    sudo dnf install -y rpm-build
fi

# Setup RPM build environment
mkdir -p "$BUILD_DIR/RPMS" "$BUILD_DIR/SOURCES" "$BUILD_DIR/SPECS" "$BUILD_DIR/BUILD" "$BUILD_DIR/SRPMS"

# Create the tarball of the current source for rpmbuild
SOURCE_TAR="${PKG_NAME}-${VERSION}.tar.gz"
echo "Creating source tarball..."
tar --exclude="$BUILD_DIR" --exclude=".git" -czf "$BUILD_DIR/SOURCES/$SOURCE_TAR" -C "$PROJECT_ROOT" .

# Write the SPEC file
cat <<EOT > "$BUILD_DIR/SPECS/adorlipi.spec"
Name:           adorlipi
Version:        $VERSION
Release:        1%{?dist}
Summary:        AdorLipi (আদরলিপি) - Modern Banglish Keyboard for IBus

License:        MIT
URL:            https://github.com/iammhador/adorlipi
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       ibus, python3, python3-gobject

%description
The first modern and easy-to-use Banglish keyboard for Linux users.
Type exactly how you speak on social media. Features a 10,000+ word conversational dictionary.

%prep
%setup -q -c

%install
rm -rf \$RPM_BUILD_ROOT
mkdir -p \$RPM_BUILD_ROOT/usr/share/adorlipi
mkdir -p \$RPM_BUILD_ROOT/usr/share/ibus/component
mkdir -p \$RPM_BUILD_ROOT/usr/libexec

cp -r core \$RPM_BUILD_ROOT/usr/share/adorlipi/
cp -r data \$RPM_BUILD_ROOT/usr/share/adorlipi/
cp -r assets \$RPM_BUILD_ROOT/usr/share/adorlipi/
cp platforms/linux/ibus_engine.py \$RPM_BUILD_ROOT/usr/libexec/ibus-engine-adorlipi
chmod +x \$RPM_BUILD_ROOT/usr/libexec/ibus-engine-adorlipi
cp platforms/linux/adorlipi-ibus.xml \$RPM_BUILD_ROOT/usr/share/ibus/component/adorlipi.xml

%post
ibus restart 2>/dev/null || true

%clean
rm -rf \$RPM_BUILD_ROOT

%files
/usr/share/adorlipi
/usr/share/ibus/component/adorlipi.xml
%attr(755, root, root) /usr/libexec/ibus-engine-adorlipi

%changelog
* Sat Feb 22 2026 AdorLipi Team <adorlipi@example.com> - 1.0.0-1
- Initial release with 10,000+ word dictionary
EOT

echo "Running rpmbuild..."
rpmbuild --define "_topdir $(pwd)/$BUILD_DIR" -bb "$BUILD_DIR/SPECS/adorlipi.spec"

find "$BUILD_DIR/RPMS" -name "*.rpm" -exec cp {} . \;
rm -rf "$BUILD_DIR"

echo "RPM built! Install via: sudo dnf install ./adorlipi-$VERSION-1.*.rpm"
