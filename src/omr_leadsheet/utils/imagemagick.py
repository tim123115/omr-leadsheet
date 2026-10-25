"""Resolve ImageMagick CLI across IM7 (`magick`) and IM6 (`convert`/`identify`).

Debian/Ubuntu ship ImageMagick 6, which has no `magick` frontend. Call sites
should build argv via :func:`magick_argv` so the pipeline works on both.
"""
from __future__ import annotations

import shutil

__all__ = ["magick_argv", "has_imagemagick"]

_IM6_FRONTENDS = frozenset({
    "identify", "convert", "mogrify", "composite", "montage",
    "compare", "stream", "display", "import", "conjure",
})


def has_imagemagick() -> bool:
    """True if either the IM7 ``magick`` or IM6 ``convert`` binary is on PATH."""
    return shutil.which("magick") is not None or shutil.which("convert") is not None


def magick_argv(*args: str) -> list[str]:
    """Build an argv list for an ImageMagick operation.

    Prefer the IM7 ``magick`` frontend. On IM6-only systems, rewrite
    ``magick identify ...`` → ``identify ...`` and bare ops → ``convert ...``.
    """
    if shutil.which("magick") is not None:
        return ["magick", *args]
    if not args:
        raise FileNotFoundError(_missing_msg())
    if args[0] in _IM6_FRONTENDS:
        if shutil.which(args[0]) is None:
            raise FileNotFoundError(_missing_msg())
        return list(args)
    if shutil.which("convert") is None:
        raise FileNotFoundError(_missing_msg())
    return ["convert", *args]


def _missing_msg() -> str:
    return (
        "ImageMagick not found (need `magick` from IM7 or `convert`/`identify` "
        "from IM6). On Debian/Ubuntu: sudo apt install imagemagick. "
        "On macOS: brew install imagemagick."
    )
