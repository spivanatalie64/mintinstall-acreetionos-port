#!/usr/bin/python3
# ACREETIONOS-ARCH: pacman / libalpm backend shim for mintinstall-acreetionos-port
# This module provides a minimal pacman equivalent of mintcommon.installer._apt
# so the Arch port can run without python-apt/aptkit. Flatpak is handled by
# mintcommon.installer._flatpak unchanged.
#
# Cherry-pick policy: keep this file isolated; upstream linuxmint/mintinstall
# does not have it — do not send it upstream. When cherry-picking upstream,
# this file should remain as-is.

import subprocess
import os
import re
import json

# Prefix used for pacman package hashes — mirrors _apt.add_prefix ("apt:")
# The cache expects "apt:" historically; on Arch we use "pacman:" and the
# installer/cache layer translates. For backward-compat with existing caches
# we accept both.
PACMAN_PREFIX = "pacman:"
APT_PREFIX_ALIAS = "apt:"

def add_prefix(name: str) -> str:
    return f"{PACMAN_PREFIX}{name}"

def make_pkg_hash(pkg_name_or_obj) -> str:
    # Accept string name or an alpm/pacman pkg object with .name
    name = getattr(pkg_name_or_obj, "name", pkg_name_or_obj)
    if isinstance(name, bytes):
        name = name.decode()
    return add_prefix(str(name))

def get_pacman_db_path() -> str:
    # ACREETIONOS-ARCH: pacman sync db location (vs /var/lib/apt/lists)
    return "/var/lib/pacman/sync"

def is_pacman_available() -> bool:
    return os.path.exists("/usr/bin/pacman") or os.path.exists("/bin/pacman")

def list_installed_pacman_names():
    """Return set of installed pacman package names via `pacman -Qq`."""
    try:
        out = subprocess.check_output(["pacman", "-Qq"], text=True, stderr=subprocess.DEVNULL)
        return set(line.strip() for line in out.splitlines() if line.strip())
    except Exception:
        return set()

def pacman_search_names(query: str):
    """Search pacman sync dbs for names matching query (best-effort)."""
    try:
        out = subprocess.check_output(["pacman", "-Ss", query], text=True, stderr=subprocess.DEVNULL)
        names = set()
        for line in out.splitlines():
            # pacman -Ss lines: "repo/name version [installed]"
            if "/" in line and " " in line:
                repo_name = line.split()[0]
                if "/" in repo_name:
                    names.add(repo_name.split("/", 1)[1])
        return names
    except Exception:
        return set()

# Placeholder that mimics _apt.process_full_apt_cache signature
# Real implementation lives in mintcommon-acreetionos-port; this is a
# lightweight fallback so mintinstall can at least start on Arch without
# that package.
def process_full_pacman_cache(cache: dict):
    """Fallback pacman cache population (very small) — real cache is built by mintcommon."""
    # If mintcommon with pacman_backend is available, delegate
    try:
        from mintcommon.installer import pacman_backend as _real
        return _real.process_full_pacman_cache(cache)
    except Exception:
        pass

    # Minimal fallback: populate cache with installed packages only
    sections = {}
    try:
        installed = list_installed_pacman_names()
        # Lazy import to avoid circular deps
        from mintcommon.installer.pkgInfo import AptPkgInfo  # reuse AptPkgInfo shape for now
        for name in installed:
            pkg_hash = add_prefix(name)
            # We don't have version/summary here; create a stub that the UI can display
            # The cache layer will fill more via AppStream if available
            try:
                info = AptPkgInfo(name, pkg_hash)  # may vary by mintcommon version
                cache[pkg_hash] = info
            except Exception:
                continue
    except Exception:
        pass
    return cache, sections
