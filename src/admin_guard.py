"""
admin_guard.py — Password-protected admin page guard.

Usage at the top of any admin page:

    from src.admin_guard import require_admin
    require_admin()

If the user has not authenticated, a password form is shown and execution stops.
"""

from __future__ import annotations

import streamlit as st


def require_admin() -> None:
    """Block page rendering until the correct admin password is entered.

    The password is read from st.secrets["ADMIN_PASSWORD"].
    Once authenticated, the status is stored in st.session_state for the session.
    """
    if st.session_state.get("admin_authenticated"):
        return  # Already authenticated in this session

    st.markdown(
        """
        <div style="text-align:center; margin-top:2rem;">
            <span style="font-size:2.5rem;">🔐</span>
            <h3 style="color:#4A7C59;">Admin Access Required</h3>
            <p style="color:#555;">This page is restricted to administrators.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("admin_login"):
        password = st.text_input("Admin password", type="password", label_visibility="collapsed")
        submitted = st.form_submit_button("Unlock", use_container_width=True)

    if submitted:
        expected = st.secrets.get("ADMIN_PASSWORD", "")
        if password == expected and expected:
            st.session_state["admin_authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")

    st.stop()
