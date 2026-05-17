"""
visitor_counter.py — Session-based persistent visitor tracking.

Visitor count is stored in data/visitors.json.
Each unique Streamlit session ID is counted once.
"""

from __future__ import annotations

import json
import os

import streamlit as st

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "visitors.json")


def _load() -> dict:
    try:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"count": 0, "sessions": []}


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(_DATA_PATH), exist_ok=True)
    with open(_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_visit() -> int:
    """Record the current session as a visitor (once per session).

    Returns the updated total visitor count.
    """
    session_id = st.session_state.get("_visitor_session_id")
    if session_id is None:
        import uuid
        session_id = str(uuid.uuid4())
        st.session_state["_visitor_session_id"] = session_id

    data = _load()
    sessions: list = data.get("sessions", [])

    if session_id not in sessions:
        sessions.append(session_id)
        # Keep only the last 10 000 session IDs to bound file size
        data["sessions"] = sessions[-10_000:]
        data["count"] = data.get("count", 0) + 1
        _save(data)

    return data.get("count", 0)


def get_count() -> int:
    """Return the current visitor count without recording a new visit."""
    return _load().get("count", 0)
