"""
src/page_header.py — Om symbol + page quote utilities.
render_om_symbol() : small centered Om image
render_page_quote() : centered italic quoted text below a heading
"""
import streamlit as st

_OM_SRC = "data:image/jpeg;base64,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"

_OM_CSS = """
<style>
.om-symbol-center {
    text-align:center; margin:0 auto 1rem;
}
.om-symbol-center img {
    width:60px; height:60px; border-radius:12px;
    object-fit:contain;
    border:2px solid #B8D4BC;
    box-shadow:0 2px 10px rgba(74,124,89,.10);
}
.page-quote-block {
    text-align:center;
    max-width:780px;
    margin:.5rem auto 1.8rem;
    font-family:'Cormorant Garamond', serif;
    font-style:italic;
    font-size:1.45rem;
    font-weight:700;
    color:#2A4A38;
    line-height:1.75;
    padding:0 1.5rem;
}
.page-quote-attr {
    display:block;
    font-family:'Playfair Display', serif;
    font-style:normal;
    font-size:1.05rem;
    font-weight:700;
    color:#4A7C59;
    letter-spacing:.3px;
    margin-top:.7rem;
}
</style>
"""

def render_om_symbol() -> None:
    """Render a small centered Om symbol. Call near top of page content."""
    st.markdown(
        _OM_CSS + f'''<div class="om-symbol-center">
        <img src="{_OM_SRC}" alt="Om"/>
    </div>''',
        unsafe_allow_html=True,
    )


def render_page_quote(quote_html: str) -> None:
    """
    Render a centered, italic, double-quoted Swamiji quote.
    quote_html may contain <strong> tags for selective bold.
    Call this AFTER the page heading.
    """
    st.markdown(
        _OM_CSS + f'''<div class="page-quote-block">
        &ldquo;{quote_html}&rdquo;
        <span class="page-quote-attr">— Swāmī Aparājitānandajī</span>
    </div>''',
        unsafe_allow_html=True,
    )
