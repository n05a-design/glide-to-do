# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 17: version checks between the shell and the packages or hosts built on it (Shell 0.7.0).

Tk-free. A consumer (Glide Bento, a host application) declares the lowest
shell version it was built and tested against and calls `require_shell` at
import time. Two values of the shell decide:

- `SHELL_VERSION`: the installed version; it must be at least the consumer's
  minimum.
- `SHELL_COMPAT_SINCE`: the oldest version whose public interface is still
  unchanged. A breaking change raises it to the new version, so every consumer
  that was built against an older shell is rejected with `ShellVersionError`
  instead of failing later with a missing attribute or a changed signature.

Compatible additions raise `SHELL_VERSION` only; `SHELL_COMPAT_SINCE` stays.
"""
from __future__ import annotations

import re

_VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


class ShellVersionError(ImportError):
    """The installed shell does not satisfy a consumer's version requirement."""


def parse_version(text):
    """`"0.7.0"` -> `(0, 7, 0)`; anything else raises `ValueError`."""
    treffer = _VERSION.match(str(text).strip())
    if not treffer:
        raise ValueError(f"not a MAJOR.MINOR.PATCH version: {text!r}")
    return tuple(int(teil) for teil in treffer.groups())


def compatible(installed, minimum, compat_since):
    """True when a consumer built against `minimum` may use the `installed` shell."""
    ist, soll, seit = parse_version(installed), parse_version(minimum), parse_version(compat_since)
    return ist >= soll and soll >= seit


def require_shell(minimum, consumer, installed=None, compat_since=None):
    """Raise `ShellVersionError` unless the shell satisfies `minimum` for `consumer`."""
    if installed is None or compat_since is None:
        from glide_shell import SHELL_COMPAT_SINCE, SHELL_VERSION
        installed = SHELL_VERSION if installed is None else installed
        compat_since = SHELL_COMPAT_SINCE if compat_since is None else compat_since
    if parse_version(installed) < parse_version(minimum):
        raise ShellVersionError(f"{consumer} requires glide_shell >= {minimum}, installed is {installed}")
    if parse_version(minimum) < parse_version(compat_since):
        raise ShellVersionError(
            f"{consumer} was built for glide_shell {minimum}; the interface changed in {compat_since} "
            f"(installed {installed}) – update {consumer} first")
    return installed
