"""
src/image_utils.py — Image loading with absolute path resolution.
Uses __file__ to find assets regardless of working directory.
"""
import base64
from pathlib import Path

# Resolve assets directory relative to THIS file's location
_SRC_DIR    = Path(__file__).parent
_PROJECT    = _SRC_DIR.parent
_ASSETS_DIR = _PROJECT / "assets" / "images"


def load_image_b64(filename: str) -> tuple[str, str]:
    """
    Load image from assets/images/ as base64 data URI.
    Returns (data_uri, mime_type) or ("", "") if not found.
    """
    path = _ASSETS_DIR / filename
    if not path.exists():
        return "", ""
    ext  = path.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else "png" if ext == "png" else ext
    b64  = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/{mime};base64,{b64}", mime


def photo_html(filename: str, css_class: str = "guru-photo",
               alt: str = "", fallback: str = "🪷") -> str:
    """Return <img> tag or emoji fallback."""
    src, _ = load_image_b64(filename)
    if src:
        return f'<img class="{css_class}" src="{src}" alt="{alt}"/>'
    return f'<div class="{css_class}-placeholder">{fallback}</div>'
