# Maintainer: AcreetionOS Team <acreetionos@acreetionos.org>
# Upstream: Linux Mint <root@linuxmint.com>
# ACREETIONOS-ARCH: Arch port of mintinstall — pacman/libalpm + Flatpak

pkgname=mintinstall-acreetionos-port
pkgver=8.4.2
pkgrel=1
pkgdesc="Software Manager for AcreetionOS (Arch Linux port of Linux Mint mintinstall) — pacman + Flatpak"
arch=('any')
url="https://github.com/spivanatalie64/mintinstall-acreetionos-port"
license=('GPL3')
depends=(
  'python'
  'python-gobject'
  'python-cairo'
  'python-setproctitle'
  'xapp'
  'gtk3'
  'glib2'
  'gdk-pixbuf2'
  'cairo'
  'pacman'
  'polkit'
  # mintcommon Arch port provides mintcommon.installer.pacman_backend; fallback to PackageKit alpm
  # 'mintcommon-acreetionos-port'
)
makedepends=('python' 'glib2')
optdepends=(
  'flatpak: Flatpak support'
  'xdg-desktop-portal-gtk: Flatpak portal'
  'appstream: AppStream metadata (replaces app-install-data)'
  'packagekit: PackageKit alpm backend (fallback installer)'
  'pamac-aur: alternative AUR/pacman helper'
)
provides=('mintinstall')
conflicts=('mintinstall')
source=()
sha256sums=()

# ACREETIONOS-ARCH: we build from the checked-out tree; no tarball fetch.
# makepkg expects source files in $srcdir — we copy from $startdir.

pkgver() {
  # Prefer debian/changelog version
  if [[ -f "$startdir/debian/changelog" ]]; then
    dpkg-parsechangelog -l "$startdir/debian/changelog" 2>/dev/null | awk '/^Version:/{print $2; exit}'
  else
    echo "8.4.2"
  fi
}

prepare() {
  # nothing to patch at prepare time; ACREETIONOS-ARCH hunks are already in-tree
  true
}

build() {
  # Compile GResources if present
  if [[ -f "$startdir/resources/mintinstall.gresource.xml" ]]; then
    mkdir -p "$srcdir/build"
    glib-compile-resources \
      --target="$srcdir/build/mintinstall.gresource" \
      "$startdir/resources/mintinstall.gresource.xml" \
      --sourcedir="$startdir/resources" 2>/dev/null || true
  fi
}

package() {
  cd "$startdir"

  # Install Python libs
  install -dm755 "$pkgdir/usr/lib/linuxmint/mintinstall"
  if [[ -d usr/lib/linuxmint/mintinstall ]]; then
    cp -a usr/lib/linuxmint/mintinstall/* "$pkgdir/usr/lib/linuxmint/mintinstall/"
  fi

  # ACREETIONOS-ARCH: ship pacman_backend shim if present
  if [[ -f usr/lib/linuxmint/mintinstall/pacman_backend.py ]]; then
    install -Dm644 usr/lib/linuxmint/mintinstall/pacman_backend.py "$pkgdir/usr/lib/linuxmint/mintinstall/pacman_backend.py"
  fi

  # Bin wrappers
  install -dm755 "$pkgdir/usr/bin"
  if [[ -d usr/bin ]]; then
    for f in usr/bin/*; do
      install -Dm755 "$f" "$pkgdir/usr/bin/$(basename "$f")"
    done
  fi

  # Data / categories / featured / icons / desktop / schemas
  if [[ -d usr/share ]]; then
    cp -a usr/share "$pkgdir/usr/"
  fi

  # Compiled gresource (Arch path mirrors Debian post-install location)
  if [[ -f "$srcdir/build/mintinstall.gresource" ]]; then
    install -Dm644 "$srcdir/build/mintinstall.gresource" "$pkgdir/usr/share/linuxmint/mintinstall/mintinstall.gresource"
  fi

  # Locale is provided by build artifacts if any; mintinstall.pot is source-only

  # GSchema — compile at install time via hook, just install it
  if [[ -f usr/share/glib-2.0/schemas/com.linuxmint.install.gschema.xml ]]; then
    install -Dm644 usr/share/glib-2.0/schemas/com.linuxmint.install.gschema.xml \
      "$pkgdir/usr/share/glib-2.0/schemas/com.linuxmint.install.gschema.xml"
  fi

  # License
  if [[ -f LICENSE ]]; then
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  elif [[ -f COPYING ]]; then
    install -Dm644 COPYING "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  fi
}
