"""ImageMagick IM6/IM7 argv resolution."""
from __future__ import annotations

from omr_leadsheet.utils.imagemagick import has_imagemagick, magick_argv


def test_has_imagemagick():
    assert has_imagemagick() is True


def test_magick_argv_crop_uses_available_frontend(monkeypatch):
    # Simulate IM6-only: no magick, convert present.
    def fake_which(name: str):
        return "/usr/bin/convert" if name == "convert" else None

    monkeypatch.setattr("omr_leadsheet.utils.imagemagick.shutil.which", fake_which)
    assert magick_argv("in.png", "-crop", "10x10+0+0", "out.png") == [
        "convert", "in.png", "-crop", "10x10+0+0", "out.png",
    ]


def test_magick_argv_identify_im6(monkeypatch):
    def fake_which(name: str):
        return f"/usr/bin/{name}" if name in {"identify", "convert"} else None

    monkeypatch.setattr("omr_leadsheet.utils.imagemagick.shutil.which", fake_which)
    assert magick_argv("identify", "-format", "%w", "x.png") == [
        "identify", "-format", "%w", "x.png",
    ]


def test_magick_argv_prefers_im7(monkeypatch):
    def fake_which(name: str):
        return f"/usr/bin/{name}" if name in {"magick", "convert", "identify"} else None

    monkeypatch.setattr("omr_leadsheet.utils.imagemagick.shutil.which", fake_which)
    assert magick_argv("identify", "-format", "%w", "x.png") == [
        "magick", "identify", "-format", "%w", "x.png",
    ]
