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
        "prompts": [
            "When did I feel proud or seek recognition today? Can I see this as an opportunity to practice humility?",
            "Whose contribution did I overlook today? How can I appreciate them more?",
            "If no one was watching, would my actions today have been the same?",
            "What does my reaction to being ignored or criticized reveal about my ego?",
        ],
        "prompt":   'When did I feel proud or seek recognition today? Can I see this as an opportunity to practice humility?',
    },
    {
        "value": "adambhitvam",
        "english": "Absence of hypocrisy",
        "prompts": [
            "Where in my life is my outer behaviour different from my inner thoughts? How can I move toward inner-outer alignment?",
            "Did I exaggerate or embellish anything today to impress someone?",
            "In which area of my life am I wearing a mask? What would happen if I removed it?",
            "Where do I display my achievements rather than simply being content with them?",
        ],
        "prompt":   'Where in my life is my outer behaviour different from my inner thoughts? How can I move toward inner-outer alignment?',
    },
    {
        "value": "ahiṃsā",
        "english": "Non-injury",
        "prompts": [
            "Did I cause hurt today — by word, thought, or deed? How can I practice gentleness with myself and others?",
            "Whose pain did I notice today? How did I respond?",
            "Am I being harsh with myself in any way today?",
            "When did I speak unkindly today? What was beneath that unkindness?",
        ],
        "prompt":   'Did I cause hurt today — by word, thought, or deed? How can I practice gentleness with myself and others?',
    },
    {
        "value": "kṣāntiḥ",
        "english": "Forbearance",
        "prompts": [
            "What tested my patience today? Did I forgive easily, or did I hold on to the hurt?",
            "Whom have I not yet fully forgiven? What is the cost of holding that resentment?",
            "When was I provoked today? Did I pause before reacting?",
            "What old hurt am I still carrying? Can I release a small piece of it today?",
        ],
        "prompt":   'What tested my patience today? Did I forgive easily, or did I hold on to the hurt?',
    },
    {
        "value": "ārjavam",
        "english": "Simplicity",
        "prompts": [
            "Were my thoughts, words, and actions in alignment today? Where did I complicate what could have been simple?",
            "Where did I say one thing but mean another?",
            "What truth, spoken simply and kindly, would lighten my heart?",
            "Where am I taking a crooked path when a straight one is available?",
        ],
        "prompt":   'Were my thoughts, words, and actions in alignment today? Where did I complicate what could have been simple?',
    },
    {
        "value": "ācāryopāsanam",
        "english": "Devotion to teacher",
        "prompts": [
            "How did I honour my teachers — past or present — today? What teaching am I currently reflecting upon?",
            "Which of Swamiji's teachings touched me most deeply this week? How am I living it?",
            "If I had ten minutes with my Guru today, what would I most want to ask?",
            "Who in my life teaches me through their being, not just their words?",
        ],
        "prompt":   'How did I honour my teachers — past or present — today? What teaching am I currently reflecting upon?',
    },
    {
        "value": "śaucam",
        "english": "Purity",
        "prompts": [
            "How is the state of my mind today — clear or cluttered? What can I let go of to invite more purity?",
            "What media, conversations, or environments influenced my inner state today?",
            "Is there an area of my home, life, or mind that needs cleansing? Where shall I begin?",
            "What thought-pattern is muddying my mind that I can release?",
        ],
        "prompt":   'How is the state of my mind today — clear or cluttered? What can I let go of to invite more purity?',
    },
    {
        "value": "sthairyam",
        "english": "Steadfastness",
        "prompts": [
            "Did I waver in my sādhana today? What kept me going, or what made me give up?",
            "What spiritual practice have I been inconsistent with? What's the smallest step to resume?",
            "When did I feel like giving up today? What gave me strength to continue?",
            "Where am I demanding quick results when steady effort is what's needed?",
        ],
        "prompt":   'Did I waver in my sādhana today? What kept me going, or what made me give up?',
    },
    {
        "value": "ātmavinigrahaḥ",
        "english": "Self-control",
        "prompts": [
            "Where did my senses pull me today? How did I respond — with awareness or reactively?",
            "Which sense-craving keeps returning despite knowing it doesn't satisfy?",
            "When did I act mindfully today versus on autopilot?",
            "What one sense-pleasure can I gently moderate this week?",
        ],
        "prompt":   'Where did my senses pull me today? How did I respond — with awareness or reactively?',
    },
    {
        "value": "vairāgyam",
        "english": "Dispassion",
        "prompts": [
            "What did I cling to today — possessions, opinions, outcomes? Can I sit with the freedom of holding things lightly?",
            "Where am I overestimating a sense-pleasure? What does my experience really show?",
            "If I lost what I'm most attached to, who would I still be?",
            "What is my mind chasing today that it cannot find there?",
        ],
        "prompt":   'What did I cling to today — possessions, opinions, outcomes? Can I sit with the freedom of holding things lightly?',
    },
    {
        "value": "anahaṅkāra",
        "english": "Absence of ego",
        "prompts": [
            "Where did my sense of 'I' assert itself today? Can I see the Self that observes the ego?",
            "Where did I claim credit that was really collective effort or Īśvara's grace?",
            "What criticism stung me today? What does that reveal about my self-image?",
            "Can I do a small kind act today without anyone knowing?",
        ],
        "prompt":   "Where did my sense of 'I' assert itself today? Can I see the Self that observes the ego?",
    },
    {
        "value": "asaktiḥ",
        "english": "Non-attachment",
        "prompts": [
            "What am I attached to that brings me anxiety? Can I love without clinging today?",
            "Where is my happiness conditional on someone behaving a certain way?",
            "What role or identity am I clinging to as 'me'?",
            "Can I love someone today without expecting anything in return?",
        ],
        "prompt":   'What am I attached to that brings me anxiety? Can I love without clinging today?',
    },
    {
        "value": "samacittatvam",
        "english": "Equanimity",
        "prompts": [
            "Was I equally accepting of pleasant and unpleasant events today? Where did I lose my balance?",
            "What disturbed me most today? Where did the disturbance actually arise — outside or within?",
            "What moment of elation and what moment of low did I have today? What lay beneath both?",
            "What if I greeted every event today as a teacher?",
        ],
        "prompt":   'Was I equally accepting of pleasant and unpleasant events today? Where did I lose my balance?',
    },
    {
        "value": "bhakti avyabhicāriṇī",
        "english": "Unswerving devotion",
        "prompts": [
            "How did I remember the Divine today? What deepens my devotion?",
            "When was I most aware of the Lord's presence today? When did I forget?",
            "What single act today can I offer up as worship?",
            "If God walked into my room right now, what would I want to feel or say?",
        ],
        "prompt":   'How did I remember the Divine today? What deepens my devotion?',
    },
    {
        "value": "viveka",
        "english": "Discrimination",
        "prompts": [
            "Where did I confuse the real with the unreal today? What is permanent, what is fleeting?",
            "What am I treating as a problem when it's just the nature of the world?",
            "What within me is the unchanging witness amid all change?",
            "What did I assume was real today that, on reflection, was just thought?",
        ],
        "prompt":   'Where did I confuse the real with the unreal today? What is permanent, what is fleeting?',
    },
    {
        "value": "abhayaṁ",
        "english": "Fearlessness (BG 16.1)",
        "prompts": [
            "What fear is holding me back today? What would I do if I were not afraid?",
            "What is my worst-case scenario? Even then, would my essential Self be untouched?",
            "Where is fear masquerading as wisdom or caution?",
            "What truth do I know but am afraid to act upon?",
        ],
        "prompt":   'What fear is holding me back today? What would I do if I were not afraid?',
    },
    {
        "value": "sattva-saṁśuddhiḥ",
        "english": "Purity of mind (BG 16.1)",
        "prompts": [
            "What thoughts dominated my mind today — sattvic, rajasic, or tamasic? How can I cultivate more sattva?",
            "What did I consume today — food, media, conversations — and what mental state did it produce?",
            "Which habits foster clarity in me, and which dull or agitate me?",
            "What sattvic practice can I add tomorrow — silence, study, prayer, sattvic food, time in nature?",
        ],
        "prompt":   'What thoughts dominated my mind today — sattvic, rajasic, or tamasic? How can I cultivate more sattva?',
    },
    {
        "value": "satyam",
        "english": "Truthfulness (BG 16.2)",
        "prompts": [
            "Was I truthful today — to myself and others? Where did I stretch or hide the truth?",
            "What truth am I avoiding because it's uncomfortable to face?",
            "When did a small white lie feel easier today? What was I protecting?",
            "How can I speak truth that is also kind and necessary?",
        ],
        "prompt":   'Was I truthful today — to myself and others? Where did I stretch or hide the truth?',
    },
    {
        "value": "dānam",
        "english": "Charity (BG 16.1)",
        "prompts": [
            "How did I give today — of my time, attention, resources? What is the spirit behind my giving?",
            "Did I give expecting something in return today — recognition, gratitude, reciprocity?",
            "Whom near me needs my time more than my money?",
            "What can I give silently today, without telling anyone?",
        ],
        "prompt":   'How did I give today — of my time, attention, resources? What is the spirit behind my giving?',
    },
    {
        "value": "tapas",
        "english": "Austerity (BG 16.1)",
        "prompts": [
            "What sādhana did I undertake today? Where did I choose discipline over comfort?",
            "What small daily discipline can I commit to this week?",
            "Where am I being indulgent in a way that weakens me?",
            "What discomfort can I welcome today as a teacher?",
        ],
        "prompt":   'What sādhana did I undertake today? Where did I choose discipline over comfort?',
    },
]


def get_today_value():
    """Pick today's value AND rotate through prompts daily."""
    today_ordinal = date.today().toordinal()
    idx = today_ordinal % len(VALUE_PROMPTS)
    # Each value gets 4 day-cycles, then moves to next prompt
    cycle = (today_ordinal // len(VALUE_PROMPTS)) % 4
    value_copy = dict(VALUE_PROMPTS[idx])
    # If multi-prompts exist, rotate; else use single
    prompts = value_copy.get("prompts")
    if prompts:
        value_copy["prompt"] = prompts[cycle % len(prompts)]
    return value_copy


# ── Page CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#1A3A45;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#0A4A58!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #88C5D0;}
div[data-testid="stSidebar"] *{color:#1A3A45!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#1A7A8C,#2C95A8);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#0A4A58,#1A7A8C);transform:translateY(-2px);}

.page-header{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);border:2px solid #88C5D0;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;
    box-shadow:0 4px 20px rgba(0,0,0,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:800;color:#0A4A58;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.1rem;color:#1A7A8C;}

.value-card{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);
    border:2px solid #88C5D0;border-left:5px solid #1A7A8C;
    border-radius:14px;padding:1.8rem 2rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(0,0,0,.07);}
.value-sanskrit{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.8rem;font-weight:700;color:#0A4A58;margin-bottom:.2rem;}
.value-english{font-family:'Lato',sans-serif;font-size:.95rem;color:#1A7A8C;
    font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:1rem;}
.value-prompt{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.15rem;color:#1A3A45;line-height:1.7;
    padding:1rem 1.2rem;background:#FFFFFF;border-radius:10px;
    border-left:3px solid #0A4A58;}

.entry-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
    padding:1.2rem 1.5rem;margin-bottom:1rem;
    box-shadow:0 2px 8px rgba(0,0,0,.05);}
.entry-date{font-family:'Playfair Display',serif;font-weight:700;color:#0A4A58;
    font-size:.95rem;margin-bottom:.3rem;}
.entry-value{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#1A7A8C;font-size:.9rem;margin-bottom:.5rem;}
.entry-text{color:#1A3A45;font-size:.92rem;line-height:1.7;white-space:pre-wrap;}

.section-title{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;
    color:#0A4A58;margin:1.5rem 0 1rem;padding-bottom:.4rem;
    border-bottom:2px solid #88C5D0;}

.stTextArea textarea{border:1.5px solid #88C5D0!important;border-radius:10px!important;
    font-family:'Cormorant Garamond',serif!important;font-size:1.05rem!important;
    color:#1A3A45!important;background:#E8F4F6!important;}
.stTextArea textarea:focus{border-color:#1A7A8C!important;}
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
        today_idx = date.today().toordinal() % len(VALUE_PROMPTS)
        selected = st.selectbox(
            "Select value:", other_value_options,
            index=today_idx,
            key="value_picker"
        )
        chosen_idx = other_value_options.index(selected)
        if chosen_idx != today_idx:
            today_value = dict(VALUE_PROMPTS[chosen_idx])
            # Apply rotating prompt
            prompts = today_value.get("prompts", [])
            if prompts:
                cycle = (date.today().toordinal() // len(VALUE_PROMPTS)) % 4
                today_value["prompt"] = prompts[cycle % len(prompts)]
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
    <div style="background:#FFFFFF;border-left:4px solid #1A7A8C;border-radius:10px;
        padding:1rem 1.4rem;margin-bottom:1.2rem;font-size:.9rem;color:#3A5C68;">
        Each value has a reflection prompt to guide your inner inquiry.
        Click any value below to write a reflection on it.
    </div>
    """, unsafe_allow_html=True)

    for i, v in enumerate(VALUE_PROMPTS):
        st.markdown(f"""
        <div class="entry-card">
            <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
                font-size:1.3rem;font-weight:700;color:#0A4A58;">
                {v['value']}
            </div>
            <div style="font-family:'Lato',sans-serif;font-size:.85rem;color:#1A7A8C;
                font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:.5rem;">
                {v['english']}
            </div>
            <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
                color:#1A3A45;font-size:1rem;line-height:1.7;">
                "{v['prompt']}"
            </div>
        </div>
        """, unsafe_allow_html=True)
