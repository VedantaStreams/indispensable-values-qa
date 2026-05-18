"""
pages/10_Reflection_Journal.py — Personal reflection journal for seekers.
Entries are stored locally in data/journal_entries.json.
Each entry: { id, date, value_focus, prompt, reflection, created_at }
"""
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import sys
import json
import uuid
from pathlib import Path
from datetime import date, datetime

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
from src.page_header import render_om_symbol, render_page_quote

st.set_page_config(
    page_title="Reflection Journal | Indispensable Values",
    page_icon="📔",
    layout="wide",
)

# ── Storage ────────────────────────────────────────────────────────────────────
DATA_DIR = _ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
JOURNAL_FILE = DATA_DIR / "journal_entries.json"


def load_entries() -> list:
    if JOURNAL_FILE.exists():
        try:
            return json.loads(JOURNAL_FILE.read_text())
        except Exception:
            return []
    return []


def save_entries(entries: list) -> None:
    JOURNAL_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False))


# ── 20 Indispensable Values + Reflection Prompts ──────────────────────────────
VALUE_PROMPTS = [
    {
        "value": "amānitvam",
        "english": "Humility",
        "prompt": "When did I feel proud or seek recognition today? "
                  "Can I see this as an opportunity to practice humility?",
    },
    {
        "value": "adambhitvam",
        "english": "Absence of hypocrisy",
        "prompt": "Where in my life is my outer behaviour different from my "
                  "inner thoughts? How can I move toward inner-outer alignment?",
    },
    {
        "value": "ahiṃsā",
        "english": "Non-injury",
        "prompt": "Did I cause hurt today — by word, thought, or deed? "
                  "How can I practice gentleness with myself and others?",
    },
    {
        "value": "kṣāntiḥ",
        "english": "Forbearance",
        "prompt": "What tested my patience today? Did I forgive easily, "
                  "or did I hold on to the hurt?",
    },
    {
        "value": "ārjavam",
        "english": "Simplicity",
        "prompt": "Were my thoughts, words, and actions in alignment today? "
                  "Where did I complicate what could have been simple?",
    },
    {
        "value": "ācāryopāsanam",
        "english": "Devotion to teacher",
        "prompt": "How did I honour my teachers — past or present — today? "
                  "What teaching am I currently reflecting upon?",
    },
    {
        "value": "śaucam",
        "english": "Purity",
        "prompt": "How is the state of my mind today — clear or cluttered? "
                  "What can I let go of to invite more purity?",
    },
    {
        "value": "sthairyam",
        "english": "Steadfastness",
        "prompt": "Did I waver in my sādhana today? What kept me going, "
                  "or what made me give up?",
    },
    {
        "value": "ātmavinigrahaḥ",
        "english": "Self-control",
        "prompt": "Where did my senses pull me today? How did I respond — "
                  "with awareness or reactively?",
    },
    {
        "value": "vairāgyam",
        "english": "Dispassion",
        "prompt": "What did I cling to today — possessions, opinions, outcomes? "
                  "Can I sit with the freedom of holding things lightly?",
    },
    {
        "value": "anahaṅkāra",
        "english": "Absence of ego",
        "prompt": "Where did my sense of 'I' assert itself today? "
                  "Can I see the Self that observes the ego?",
    },
    {
        "value": "asaktiḥ",
        "english": "Non-attachment",
        "prompt": "What am I attached to that brings me anxiety? "
                  "Can I love without clinging today?",
    },
    {
        "value": "samacittatvam",
        "english": "Equanimity",
        "prompt": "Was I equally accepting of pleasant and unpleasant events today? "
                  "Where did I lose my balance?",
    },
    {
        "value": "bhakti avyabhicāriṇī",
        "english": "Unswerving devotion",
        "prompt": "How did I remember the Divine today? "
                  "What deepens my devotion?",
    },
    {
        "value": "viveka",
        "english": "Discrimination",
        "prompt": "Where did I confuse the real with the unreal today? "
                  "What is permanent, what is fleeting?",
    },
    {
        "value": "abhayaṁ",
        "english": "Fearlessness (BG 16.1)",
        "prompt": "What fear is holding me back today? "
                  "What would I do if I were not afraid?",
    },
    {
        "value": "sattva-saṁśuddhiḥ",
        "english": "Purity of mind (BG 16.1)",
        "prompt": "What thoughts dominated my mind today — sattvic, rajasic, "
                  "or tamasic? How can I cultivate more sattva?",
    },
    {
        "value": "satyam",
        "english": "Truthfulness (BG 16.2)",
        "prompt": "Was I truthful today — to myself and others? "
                  "Where did I stretch or hide the truth?",
    },
    {
        "value": "dānam",
        "english": "Charity (BG 16.1)",
        "prompt": "How did I give today — of my time, attention, resources? "
                  "What is the spirit behind my giving?",
    },
    {
        "value": "tapas",
        "english": "Austerity (BG 16.1)",
        "prompt": "What sādhana did I undertake today? "
                  "Where did I choose discipline over comfort?",
    },
]


def get_today_value():
    """Pick today's value based on day of year (rotates daily)."""
    idx = date.today().toordinal() % len(VALUE_PROMPTS)
    return VALUE_PROMPTS[idx]


# ── Page CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#4A7C59,#6A9E78);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#2A5C3A,#4A7C59);transform:translateY(-2px);}

.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;
    box-shadow:0 4px 20px rgba(74,124,89,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.1rem;color:#4A7C59;}

.value-card{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);
    border:2px solid #B8D4BC;border-left:5px solid #4A7C59;
    border-radius:14px;padding:1.8rem 2rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(74,124,89,.07);}
.value-sanskrit{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.8rem;font-weight:700;color:#2A5C3A;margin-bottom:.2rem;}
.value-english{font-family:'Lato',sans-serif;font-size:.95rem;color:#4A7C59;
    font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:1rem;}
.value-prompt{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.15rem;color:#1A3A28;line-height:1.7;
    padding:1rem 1.2rem;background:white;border-radius:10px;
    border-left:3px solid #8B6914;}

.entry-card{background:white;border:1.5px solid #B8D4BC;border-radius:12px;
    padding:1.2rem 1.5rem;margin-bottom:1rem;
    box-shadow:0 2px 8px rgba(74,124,89,.05);}
.entry-date{font-family:'Playfair Display',serif;font-weight:700;color:#2A5C3A;
    font-size:.95rem;margin-bottom:.3rem;}
.entry-value{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#4A7C59;font-size:.9rem;margin-bottom:.5rem;}
.entry-text{color:#1A3A28;font-size:.92rem;line-height:1.7;white-space:pre-wrap;}

.section-title{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;
    color:#2A5C3A;margin:1.5rem 0 1rem;padding-bottom:.4rem;
    border-bottom:2px solid #B8D4BC;}

.stTextArea textarea{border:1.5px solid #B8D4BC!important;border-radius:10px!important;
    font-family:'Cormorant Garamond',serif!important;font-size:1.05rem!important;
    color:#1A3A28!important;background:#F8F9F5!important;}
.stTextArea textarea:focus{border-color:#4A7C59!important;}
</style>
""", unsafe_allow_html=True)

render_om_symbol()

st.markdown("""
<div class="page-header">
    <div style="font-size:2rem;margin-bottom:.3rem;">📔</div>
    <div class="page-header-title">Reflection Journal</div>
    <div class="page-header-sub">A private space to contemplate Swamiji's teachings</div>
</div>
""", unsafe_allow_html=True)

render_page_quote(
    "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!"
)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_write, tab_history, tab_browse = st.tabs([
    "✍️ Write Today's Reflection",
    "📚 My Journal History",
    "🪷 Browse by Value"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — WRITE TODAY'S REFLECTION
# ══════════════════════════════════════════════════════════════════════════════
with tab_write:
    today_value = get_today_value()

    st.markdown(f"""
    <div class="value-card">
        <div class="value-sanskrit">{today_value['value']}</div>
        <div class="value-english">{today_value['english']} · Today's Focus</div>
        <div class="value-prompt">"{today_value['prompt']}"</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Allow user to pick a different value if they want
    with st.expander("🪷 Choose a different value to reflect on today"):
        other_value_options = [
            f"{v['value']} — {v['english']}" for v in VALUE_PROMPTS
        ]
        selected = st.selectbox(
            "Select value:", other_value_options,
            index=VALUE_PROMPTS.index(today_value),
            key="value_picker"
        )
        chosen_idx = other_value_options.index(selected)
        if chosen_idx != VALUE_PROMPTS.index(today_value):
            today_value = VALUE_PROMPTS[chosen_idx]
            st.markdown(f"""
            <div class="value-card">
                <div class="value-sanskrit">{today_value['value']}</div>
                <div class="value-english">{today_value['english']}</div>
                <div class="value-prompt">"{today_value['prompt']}"</div>
            </div>
            """, unsafe_allow_html=True)

    # Reflection text area
    reflection_text = st.text_area(
        "Your reflection:",
        height=220,
        placeholder=("Write your thoughts, observations, and reflections here. "
                     "This is a private space for your inner inquiry."),
        key="reflection_input",
    )

    col_save, col_clear = st.columns([3, 1])
    with col_save:
        if st.button("💾 Save Reflection", use_container_width=True):
            if not reflection_text.strip():
                st.warning("⚠️ Please write your reflection before saving.")
            else:
                entries = load_entries()
                new_entry = {
                    "id":           str(uuid.uuid4()),
                    "date":         str(date.today()),
                    "value":        today_value["value"],
                    "english":      today_value["english"],
                    "prompt":       today_value["prompt"],
                    "reflection":   reflection_text.strip(),
                    "created_at":   datetime.now().isoformat(timespec="seconds"),
                }
                entries.append(new_entry)
                save_entries(entries)
                st.success("✅ Reflection saved. May this inquiry deepen your sādhana 🪷")
                st.balloons()

    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MY JOURNAL HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    entries = load_entries()

    if not entries:
        st.info("📔 Your journal is empty. Write your first reflection in the "
                "**Write Today's Reflection** tab above.")
    else:
        st.markdown(f"**📚 {len(entries)} reflection(s) saved**")
        st.markdown("<br>", unsafe_allow_html=True)

        # Sort newest first
        sorted_entries = sorted(
            entries, key=lambda e: e.get("created_at", ""), reverse=True
        )

        # Export options
        col_x1, col_x2, col_x3 = st.columns(3)
        with col_x1:
            export_txt = "\n\n" + ("─" * 60 + "\n").join([
                f"Date: {e['date']}\n"
                f"Value: {e['value']} ({e['english']})\n"
                f"Prompt: {e['prompt']}\n\n"
                f"Reflection:\n{e['reflection']}"
                for e in sorted_entries
            ])
            st.download_button(
                "⬇️ Download as TXT",
                data=export_txt,
                file_name=f"reflection_journal_{date.today()}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_x2:
            export_json = json.dumps(sorted_entries, indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ Download as JSON",
                data=export_json,
                file_name=f"reflection_journal_{date.today()}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_x3:
            if st.button("🗑️ Delete All", use_container_width=True):
                st.session_state["confirm_delete_all_journal"] = True

        if st.session_state.get("confirm_delete_all_journal"):
            st.warning("⚠️ Delete ALL journal entries? This cannot be undone.")
            cy, cn = st.columns(2)
            with cy:
                if st.button("✅ Yes, delete all", key="del_yes"):
                    save_entries([])
                    st.session_state["confirm_delete_all_journal"] = False
                    st.success("All entries deleted.")
                    st.rerun()
            with cn:
                if st.button("❌ Cancel", key="del_no"):
                    st.session_state["confirm_delete_all_journal"] = False
                    st.rerun()

        st.divider()

        # Display entries
        for entry in sorted_entries:
            st.markdown(f"""
            <div class="entry-card">
                <div class="entry-date">📅 {entry['date']}</div>
                <div class="entry-value">🪷 {entry['value']} — {entry.get('english','')}</div>
                <div class="entry-text">{entry['reflection']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Delete this entry", key=f"del_{entry['id']}"):
                entries = [e for e in entries if e["id"] != entry["id"]]
                save_entries(entries)
                st.success("Entry deleted.")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BROWSE BY VALUE
# ══════════════════════════════════════════════════════════════════════════════
with tab_browse:
    st.markdown('<div class="section-title">🪷 Explore All 20 Values</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#EDF3EC;border-left:4px solid #4A7C59;border-radius:10px;
        padding:1rem 1.4rem;margin-bottom:1.2rem;font-size:.9rem;color:#3A5040;">
        Each value has a reflection prompt to guide your inner inquiry.
        Click any value below to write a reflection on it.
    </div>
    """, unsafe_allow_html=True)

    for i, v in enumerate(VALUE_PROMPTS):
        st.markdown(f"""
        <div class="entry-card">
            <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
                font-size:1.3rem;font-weight:700;color:#2A5C3A;">
                {v['value']}
            </div>
            <div style="font-family:'Lato',sans-serif;font-size:.85rem;color:#4A7C59;
                font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:.5rem;">
                {v['english']}
            </div>
            <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
                color:#1A3A28;font-size:1rem;line-height:1.7;">
                "{v['prompt']}"
            </div>
        </div>
        """, unsafe_allow_html=True)
