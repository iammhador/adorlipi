#!/bin/bash
set -e

VERSION="1.0.0"
PKG_NAME="adorlipi"
BUILD_DIR="${PKG_NAME}-${VERSION}-rpm"

echo "Building RPM package for AdorLipi v$VERSION (Fedora/RHEL)..."

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
tar --exclude="$BUILD_DIR" --exclude=".git" -czf "$BUILD_DIR/SOURCES/$SOURCE_TAR" -C ../../ .

# Write the SPEC file
cat <<EOT > "$BUILD_DIR/SPECS/adorlipi.spec"
Name:           adorlipi
Version:        $VERSION
Release:        1%{?dist}
Summary:        AdorLipi Phonetic Banglish Keyboard for IBus

License:        MIT
URL:            https://github.com/iammhador/adorlipi
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       ibus, python3, python3-gobject

%description
A smart phonetic keyboard for typing Bengali via IBus.
Features a large 6,400+ word dictionary with slang support.

%prep
%setup -q -c

%install
rm -rf \$RPM_BUILD_ROOT
mkdir -p \$RPM_BUILD_ROOT/usr/share/adorlipi
mkdir -p \$RPM_BUILD_ROOT/usr/share/ibus/component
mkdir -p \$RPM_BUILD_ROOT/usr/libexec

# Copy files
cp -r core \$RPM_BUILD_ROOT/usr/share/adorlipi/
cp -r data \$RPM_BUILD_ROOT/usr/share/adorlipi/
cp platforms/linux/ibus_engine.py \$RPM_BUILD_ROOT/usr/libexec/ibus-engine-adorlipi
chmod +x \$RPM_BUILD_ROOT/usr/libexec/ibus-engine-adorlipi

# Handle IBus XML
cat platforms/linux/adorlipi.xml | sed 's|/usr/libexec/ibus-engine-adorlipi|/usr/libexec/ibus-engine-adorlipi|g' > \$RPM_BUILD_ROOT/usr/share/ibus/component/adorlipi.xml

%clean
rm -rf \$RPM_BUILD_ROOT

%files
/usr/share/adorlipi
/usr/share/ibus/component/adorlipi.xml
%attr(755, root, root) /usr/libexec/ibus-engine-adorlipi

%changelog
* Sun Feb 22 2026 Your Name <your.email@example.com> - 1.0.0-1
- Initial RPM package
EOT

# Build it
echo "Running rpmbuild..."
rpmbuild --define "_topdir $(pwd)/$BUILD_DIR" -bb "$BUILD_DIR/SPECS/adorlipi.spec"

# Move the generated RPM to the root and clean up
find "$BUILD_DIR/RPMS" -name "*.rpm" -exec cp {} . \;
rm -rf "$BUILD_DIR"

echo "RPM Package successfully built! You can install it via: sudo dnf install ./adorlipi-$VERSION-1.*.rpm"
