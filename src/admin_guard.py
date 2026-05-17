"""
src/admin_guard.py — Password protection for admin-only pages.
Call require_admin() at the top of any page to restrict access.
"""

import streamlit as st


LOTUS_CSS = """
<style>
.admin-gate {
    max-width: 420px;
    margin: 4rem auto;
    background: white;
    border: 2px solid #B8D4BC;
    border-radius: 18px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 8px 30px rgba(74,124,89,.10);
}
.admin-gate-icon { font-size: 3rem; margin-bottom: .8rem; }
.admin-gate-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem; font-weight: 700;
    color: #2A5C3A; margin-bottom: .4rem;
}
.admin-gate-sub {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic; color: #4A7C59;
    font-size: 1rem; margin-bottom: 1.5rem;
}
</style>
"""


def require_admin() -> bool:
    """
    Show a password gate. Returns True if authenticated, False otherwise.
    Call at the very top of any admin page — use st.stop() if False.

    Usage:
        if not require_admin():
            st.stop()
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Cormorant+Garamond:ital@1&display=swap');
    html,body,[class*="css"]{background-color:#F8F9F5!important;}
    div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
    div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}
    .stButton>button{background:linear-gradient(135deg,#4A7C59,#6A9E78);color:white!important;border:none;border-radius:8px;font-weight:700;padding:.5rem 1.2rem;}
    </style>
    """ + LOTUS_CSS, unsafe_allow_html=True)

    # Already authenticated this session
    if st.session_state.get("admin_authenticated"):
        return True

    # Show gate
    st.markdown("""
    <div class="admin-gate">
        <div class="admin-gate-icon">🔐</div>
        <div class="admin-gate-title">Admin Access Only</div>
        <div class="admin-gate-sub">
            This page is restricted to authorised administrators.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input(
            "Enter admin password",
            type="password",
            key="admin_pwd_input",
            placeholder="Password",
        )
        if st.button("🪷 Enter", use_container_width=True):
            correct = st.secrets.get("ADMIN_PASSWORD", "vedanta2025")
            if pwd == correct:
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

    return False
