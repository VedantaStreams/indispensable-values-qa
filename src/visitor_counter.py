"""
src/visitor_counter.py
Simple persistent visitor counter stored in data/visitors.json.
Uses session_state to count each browser session only once.
"""
import json
import streamlit as st
from pathlib import Path
from datetime import date

_DATA_DIR = Path(__file__).parent.parent / "data"
_COUNTER_FILE = _DATA_DIR / "visitors.json"


def _load() -> dict:
    if _COUNTER_FILE.exists():
        try:
            return json.loads(_COUNTER_FILE.read_text())
        except Exception:
            pass
    return {"total": 0, "daily": {}, "first_visit": str(date.today())}


def _save(data: dict) -> None:
    _DATA_DIR.mkdir(exist_ok=True)
    _COUNTER_FILE.write_text(json.dumps(data, indent=2))


def record_visit() -> dict:
    """
    Record a visit if this is a new session.
    Returns dict with total, today, and all-time counts.
    """
    if not st.session_state.get("_visit_recorded"):
        data = _load()
        today = str(date.today())
        data["total"] = data.get("total", 0) + 1
        data["daily"][today] = data["daily"].get(today, 0) + 1
        _save(data)
        st.session_state["_visit_recorded"] = True
        st.session_state["_visitor_data"] = data

    data = st.session_state.get("_visitor_data", _load())
    today = str(date.today())
    return {
        "total":   data.get("total", 0),
        "today":   data.get("daily", {}).get(today, 0),
        "since":   data.get("first_visit", str(date.today())),
    }


def get_counts() -> dict:
    """Get current counts without recording a new visit."""
    data = _load()
    today = str(date.today())
    return {
        "total":   data.get("total", 0),
        "today":   data.get("daily", {}).get(today, 0),
        "since":   data.get("first_visit", str(date.today())),
    }
