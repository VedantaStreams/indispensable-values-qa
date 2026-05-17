"""
page_header.py — Shared Om symbol and rotating Swamiji quote for every page.

Call render_header() at the top of each Streamlit page.
"""

from __future__ import annotations

import random

import streamlit as st

# Rotating quotes drawn from the spirit of Swamiji's teachings
_SWAMIJI_QUOTES = [
    (
        "Humility is not weakness — it is the supreme strength of one who knows the Self.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "Amānitvam: the absence of the demand for honour. "
        "Demand nothing; give everything.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "Non-violence begins in thought. "
        "Every violent word is a wound inflicted on the Self.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "Kṣāntiḥ — forbearance — is the fire that burns the fuel of others' provocations "
        "without letting smoke cloud your peace.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "Purity of body, mind, and heart is the altar on which knowledge dawns.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "The teacher's grace is the boat; your sādhana is the oar. "
        "Without both, the crossing is impossible.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "Steadfastness (sthairyam) means the mind does not oscillate "
        "between the pleasant and the good.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
    (
        "Dispassion (vairāgyam) is not indifference — it is the mature recognition "
        "of what is eternally worthwhile.",
        "Pūjya Swāmī Aparājitānandajī",
    ),
]

_GOOGLE_FONTS_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
"""

_GLOBAL_CSS = """
<style>
  /* Apply custom fonts */
  h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #4A7C59; }
  body, p, div, span, li { font-family: 'Lato', sans-serif !important; }
  .sanskrit, blockquote { font-family: 'Cormorant Garamond', serif !important; }

  /* Photo / image border */
  .photo-border {
    border: 4px solid transparent;
    border-radius: 12px;
    background:
      linear-gradient(white, white) padding-box,
      linear-gradient(135deg, #FFB6C1, #D4A017) border-box;
  }

  /* Quote card */
  .quote-card {
    background: #EDF3EC;
    border-left: 4px solid #4A7C59;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0 1.5rem 0;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: #3A3A3A;
  }
  .quote-attribution {
    font-size: 0.85rem;
    color: #8B6914;
    font-family: 'Lato', sans-serif;
    margin-top: 0.4rem;
  }

  /* Om symbol */
  .om-symbol {
    font-size: 2.2rem;
    color: #8B6914;
    font-family: 'Cormorant Garamond', serif;
  }

  /* Divider */
  .sage-divider {
    border: none;
    border-top: 2px solid #4A7C59;
    opacity: 0.3;
    margin: 1rem 0;
  }
</style>
"""


def inject_fonts_and_css() -> None:
    """Inject Google Fonts and global CSS (call once per page)."""
    st.markdown(_GOOGLE_FONTS_CSS + _GLOBAL_CSS, unsafe_allow_html=True)


def render_header(page_title: str = "") -> None:
    """Render the Om symbol, optional page title, and a rotating Swamiji quote."""
    inject_fonts_and_css()

    quote_text, attribution = random.choice(_SWAMIJI_QUOTES)

    title_html = f"<h2 style='margin:0;'>{page_title}</h2>" if page_title else ""

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <span class="om-symbol">ॐ</span>
            {title_html}
        </div>
        <hr class="sage-divider">
        <div class="quote-card">
            <span class="sanskrit">"{quote_text}"</span>
            <div class="quote-attribution">— {attribution}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
