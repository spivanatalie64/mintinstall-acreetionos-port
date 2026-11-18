# mintinstall-acreetionos-port

Software Manager for AcreetionOS — **Arch Linux port** of [linuxmint/mintinstall](https://github.com/linuxmint/mintinstall).

![image](https://user-images.githubusercontent.com/19881231/122644976-86767180-d120-11eb-9cf4-eed2813f749b.png)

> **Upstream cherry-pick policy (please read):**
> This repository is a downstream Arch port. **We cherry-pick from upstream only** — we do not diverge with independent feature forks.
> Future contributors: keep `master` rebaseable onto `linuxmint/mintinstall` `master`; put all Arch-specific differences behind small, clearly-marked patches (search `ACREETIONOS-ARCH` in the tree) so they can be reapplied after a cherry-pick. Bug fixes and features that belong upstream should be sent to https://github.com/linuxmint/mintinstall first and then cherry-picked here. Do not merge unrelated upstream history wholesale — use `git cherry-pick -x` and reference the upstream commit in the commit message.

Original description: *Software Manager for Linux Mint.*

## What this port changes

- **Backend:** `apt`/`aptkit`/`packagekit-apt` → **pacman / libalpm + Flatpak**. Native packages are queried/installed via `pacman` (through `mintcommon-acreetionos-port` → `pacman_backend`, falling back to `PackageKit` with the `alpm` backend or direct `pacman`/`pamac` subprocess when `python-apt` is absent). Flatpak support is unchanged.
- **Packaging:** `debian/` retained for reference; Arch packaging is via `PKGBUILD` (`makepkg -si`). No `dpkg-buildpackage`.
- **Paths:** APT cache paths (`/var/lib/apt/lists`) are replaced with pacman db checks (`/var/lib/pacman/sync`). Translation-file handling is adapted for `pacman`/`alpm`.
- **Dependencies:** `python-apt`, `aptkit`, `app-install-data`, `mint-common (deb)` → `python-gobject`, `python-setproctitle`, `xapp`, `libalpm`/`pacman`, `flatpak` (opt), `appstream` (opt), `mintcommon-acreetionos-port`. See `PKGBUILD` for the authoritative list.

Flatpak, reviews, screenshots, categories, and featured apps behave as upstream.

## Build — Arch Linux (AcreetionOS)

Get source:

```
git clone https://github.com/spivanatalie64/mintinstall-acreetionos-port
# mirror: https://github.com/AcreetionOS-Linux/mintinstall-acreetionos-port
cd mintinstall-acreetionos-port
```

Build and install with makepkg:

```
makepkg -si
```

Or install directly after building:

```
makepkg --noextract
sudo pacman -U mintinstall-acreetionos-port-*.pkg.tar.zst
```

Run:

```
mintinstall
```

### Dependencies (Arch)

- `python` `python-gobject` `python-cairo` `python-setproctitle` `xapp` `gtk3` `glib2` `cinnamon-translations` or `mint-common-acreetionos` (provides `mintcommon.installer`)
- `pacman` `pacman-contrib` `libalpm` (via `pacman`)
- Optional: `flatpak` `gir1.2-flatpak-1.0` / `libflatpak` + `xdg-desktop-portal-gtk` for Flatpak support
- `appstream` for AppStream metadata (replaces `app-install-data` on Arch)

> On AcreetionOS the `mintcommon-acreetionos-port` package provides `mintcommon.installer.pacman_backend`. If it is not yet installed, `mintinstall` will fall back to `PackageKit (alpm)` and then to direct `pacman` subprocess calls.

## Build — Debian/Ubuntu (upstream reference)

Upstream builds with `dpkg-buildpackage`. This is documented for cherry-pick verification only:

```
git clone https://github.com/linuxmint/mintinstall
cd mintinstall
dpkg-buildpackage --no-sign
cd ..
sudo dpkg -i mintinstall*.deb
```

## Contributing — how to cherry-pick upstream

1. Add upstream if needed: `git remote add upstream https://github.com/linuxmint/mintinstall.git`
2. Fetch: `git fetch upstream`
3. Cherry-pick the commit(s): `git cherry-pick -x <upstream-sha>` (keep `-x` so the upstream commit is recorded)
4. If conflicts touch Arch-specific hunks (`ACREETIONOS-ARCH`), resolve by keeping the Arch adaptation and adding a comment referencing the upstream commit
5. Rebuild on Arch: `makepkg -g` if `PKGBUILD` checksums need updating, then `makepkg -si` and smoke-test `mintinstall`

Please do not send Arch-only changes upstream, and do not send Mint-only changes here without an upstream PR. This keeps the port trivially rebaseable.

## Translations

Please use Launchpad to translate Mintinstall: https://translations.launchpad.net/linuxmint/latest/.

The PO files in this project are imported from there.

## Upstream

- Upstream repo: https://github.com/linuxmint/mintinstall
- Upstream license: GPL-3.0 (see `COPYING`/`LICENSE` if present; otherwise same as upstream)

## Mirrors

- Primary fork: https://github.com/spivanatalie64/mintinstall-acreetionos-port
- Organization mirror: https://github.com/AcreetionOS-Linux/mintinstall-acreetionos-port

> **Note on the former typo name:** `mintinstall-acreetinos-port` (missing `o`) was an initial typo and now redirects/deprecated. Please use `mintinstall-acreetionos-port`.
