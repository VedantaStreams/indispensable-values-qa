"""
pages/11_Value_of_the_Day.py — Daily contemplation page.
Auto-rotates through 20 values from Bhagavad Gītā Chapters 13 & 16.
Shows: Sanskrit value, English meaning, verse reference, reflection prompt,
       and a related Swamiji quote.
"""
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import sys
from pathlib import Path
from datetime import date

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
from src.page_header import render_om_symbol

st.set_page_config(
    page_title="Value of the Day | Indispensable Values",
    page_icon="🪷",
    layout="wide",
)

# ── 20 Values with full daily contemplation content ──────────────────────────
DAILY_VALUES = [
    {
        "value":    "amānitvam",
        "english":  "Humility",
        "devanagari": "अमानित्वम्",
        "verse":    "BG 13.7",
        "definition": "Absence of self-glorification, of the desire for recognition, "
                      "or seeking honor and respect from others.",
        "teaching": "Humility is not low self-esteem. It is the natural state of one who "
                    "has seen the infinite Self and recognizes the same Self in all beings. "
                    "True humility arises from the understanding that whatever talents or "
                    "accomplishments we possess have been given by Īśvara.",
        "prompt":   "Reflect: Where did I seek recognition or praise today? "
                    "Can I dedicate my actions and accomplishments to the Lord?",
        "quote":    "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!",
    },
    {
        "value":    "adambhitvam",
        "english":  "Absence of Pretense",
        "devanagari": "अदम्भित्वम्",
        "verse":    "BG 13.7",
        "definition": "The quality of not displaying or showing off one's qualifications, "
                      "wealth, status, or spiritual practices.",
        "teaching": "Where there is dambha (hypocrisy/show), there is a gap between what we "
                    "are inside and what we project outside. The seeker walks a path of "
                    "inner-outer alignment — being the same in private as in public.",
        "prompt":   "Reflect: Where am I projecting an image rather than being authentic? "
                    "How can I bring my outer behavior in alignment with my inner truth?",
        "quote":    "<strong>True happiness</strong> shouldn't be because of! "
                    "<strong>True happiness</strong> should be in spite of!",
    },
    {
        "value":    "ahiṃsā",
        "english":  "Non-Injury",
        "devanagari": "अहिंसा",
        "verse":    "BG 13.7",
        "definition": "Not causing pain to any living being — by thought, word, or deed.",
        "teaching": "Ahiṃsā is not merely avoiding physical violence. It includes harsh words, "
                    "cutting remarks, hateful thoughts, and indifference to others' suffering. "
                    "It is positive love and compassion, not just the absence of cruelty.",
        "prompt":   "Reflect: Did I cause hurt today — by word, action, or thought? "
                    "How can I practice greater tenderness in all my relationships?",
        "quote":    "A heart filled with <strong>noble emotions</strong> like kindness, "
                    "compassion, mercy, truthfulness, honesty — such a heart is called a "
                    "<strong>pure heart</strong>.",
    },
    {
        "value":    "kṣāntiḥ",
        "english":  "Forbearance",
        "devanagari": "क्षान्तिः",
        "verse":    "BG 13.7",
        "definition": "Patience, forgiveness, and forbearance in the face of provocation or injury.",
        "teaching": "Kṣānti is not weakness or suppression. It is the strength to remain "
                    "unaffected when wronged, knowing that anger only burns the one who holds it. "
                    "The mighty one is not who can strike back, but who can forgive.",
        "prompt":   "Reflect: What tested my patience today? Did I respond with peace "
                    "or with reactivity? What can I forgive today?",
        "quote":    "Rate your <strong>spiritual progress</strong> with the "
                    "<strong>intensity of Peace</strong> which you experience.",
    },
    {
        "value":    "ārjavam",
        "english":  "Simplicity / Straightforwardness",
        "devanagari": "आर्जवम्",
        "verse":    "BG 13.7",
        "definition": "Alignment of thought, word, and action — the absence of crookedness.",
        "teaching": "Ārjavam is the simplicity of one whose inner and outer lives are unified. "
                    "What is thought is spoken; what is spoken is acted upon. There is no "
                    "duplicity, no hidden agenda, no double-dealing.",
        "prompt":   "Reflect: Were my thoughts, words, and deeds aligned today? "
                    "Where did I take the easy crooked path instead of the simple straight one?",
        "quote":    "God resides in the hearts of all. But only those <strong>blessed ones</strong> "
                    "who have kept their <strong>heart pure</strong> can experience it.",
    },
    {
        "value":    "ācāryopāsanam",
        "english":  "Service to the Teacher",
        "devanagari": "आचार्योपासनम्",
        "verse":    "BG 13.7",
        "definition": "Devoted service and reverence to one's spiritual teacher (Guru).",
        "teaching": "The Guru is the channel through which the eternal teaching flows. "
                    "Upāsana means 'sitting near' — not just physically, but with surrender, "
                    "attentiveness, and a heart ready to receive. Without a Guru, the scriptures "
                    "remain mere words.",
        "prompt":   "Reflect: How am I honoring my teachers — past and present? "
                    "What teaching am I currently studying and applying?",
        "quote":    "Remember, in life, the <strong>only permanent relationship</strong> "
                    "is our relationship with <strong>God</strong>.",
    },
    {
        "value":    "śaucam",
        "english":  "Purity",
        "devanagari": "शौचम्",
        "verse":    "BG 13.7",
        "definition": "Cleanliness — both external (body, surroundings) and internal (mind, thoughts).",
        "teaching": "External cleanliness reflects inner cleanliness. The mind cleansed of "
                    "raga (attachment), dveṣa (aversion), and ahaṅkāra (ego) becomes a fit "
                    "vessel for higher knowledge. As Swamiji teaches — God resides in a pure heart.",
        "prompt":   "Reflect: What is the state of my mind today — clear or cluttered? "
                    "What thoughts can I release to invite more purity?",
        "quote":    "God is not someone who can be seen through the naked eyes. "
                    "He is someone who can be experienced in a <strong>pure heart</strong>.",
    },
    {
        "value":    "sthairyam",
        "english":  "Steadfastness",
        "devanagari": "स्थैर्यम्",
        "verse":    "BG 13.7",
        "definition": "Steadiness and perseverance in spiritual practice, especially in difficulties.",
        "teaching": "The path is long and the obstacles many. Sthairyam is the inner resolve "
                    "that says — 'I will continue, whatever may come.' It is not enthusiasm "
                    "of a moment but the quiet determination of a lifetime.",
        "prompt":   "Reflect: Did I waver in my practice today? What strengthens my resolve? "
                    "What weakens it, and how can I guard against that?",
        "quote":    "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!",
    },
    {
        "value":    "ātmavinigrahaḥ",
        "english":  "Self-Control",
        "devanagari": "आत्मविनिग्रहः",
        "verse":    "BG 13.7",
        "definition": "Control of the senses and mind — not allowing them to run unchecked.",
        "teaching": "The senses by nature run outward, seeking objects of pleasure. "
                    "Ātma-vinigraha is the conscious choice to direct them inward, "
                    "toward the Self. Not by suppression, but by wisdom — knowing that "
                    "lasting joy is within, not in fleeting objects.",
        "prompt":   "Reflect: Where did my senses pull me today? Did I respond with "
                    "awareness or impulsively? What am I learning about my impulses?",
        "quote":    "Rate your <strong>spiritual progress</strong> with the "
                    "<strong>intensity of Peace</strong> which you experience.",
    },
    {
        "value":    "vairāgyam",
        "english":  "Dispassion",
        "devanagari": "वैराग्यम्",
        "verse":    "BG 13.8",
        "definition": "Dispassion toward sense objects — not attachment to pleasures of body or world.",
        "teaching": "Vairāgya is not hatred of the world or escapism. It is the wisdom to "
                    "engage fully with life without being enslaved by its objects. "
                    "Like a lotus untouched by water — present yet free.",
        "prompt":   "Reflect: What do I cling to that brings me anxiety? "
                    "Can I love fully without grasping?",
        "quote":    "<strong>True happiness</strong> shouldn't be because of! "
                    "<strong>True happiness</strong> should be in spite of!",
    },
    {
        "value":    "anahaṅkāra",
        "english":  "Absence of Ego",
        "devanagari": "अनहङ्कारः",
        "verse":    "BG 13.8",
        "definition": "Freedom from the false sense of 'I' identifying with body, mind, and ego.",
        "teaching": "The 'I' that takes credit, fears criticism, and seeks to be special — "
                    "that is ahaṅkāra. The Self (Ātman) needs no recognition because it is "
                    "already complete. Anahaṅkāra is the natural ease of one who knows this.",
        "prompt":   "Reflect: Where did my ego assert itself today? "
                    "Can I see the witness Self behind the ego's movements?",
        "quote":    "God resides in the hearts of all. But only those <strong>blessed ones</strong> "
                    "who have kept their <strong>heart pure</strong> can experience it.",
    },
    {
        "value":    "asaktiḥ",
        "english":  "Non-Attachment",
        "devanagari": "असक्तिः",
        "verse":    "BG 13.9",
        "definition": "Freedom from clinging — to people, possessions, situations, outcomes.",
        "teaching": "Asakti does not mean cold detachment. It means the freedom that allows "
                    "us to love deeply without dependence. We hold our relationships and "
                    "responsibilities with open hands, not clenched fists.",
        "prompt":   "Reflect: What attachment is causing me suffering? "
                    "Can I hold this lightly while still loving completely?",
        "quote":    "Remember, in life, the <strong>only permanent relationship</strong> "
                    "is our relationship with <strong>God</strong>.",
    },
    {
        "value":    "samacittatvam",
        "english":  "Equanimity",
        "devanagari": "समचित्तत्वम्",
        "verse":    "BG 13.9",
        "definition": "Evenness of mind in pleasant and unpleasant events, success and failure.",
        "teaching": "Sama-citta is not indifference. It is the inner stability of one who "
                    "knows that situations come and go, but the Self remains. Both praise "
                    "and criticism are received with the same calm presence.",
        "prompt":   "Reflect: Was I equally accepting of pleasant and unpleasant events today? "
                    "Where did I lose my inner balance, and what helped restore it?",
        "quote":    "Rate your <strong>spiritual progress</strong> with the "
                    "<strong>intensity of Peace</strong> which you experience.",
    },
    {
        "value":    "bhakti avyabhicāriṇī",
        "english":  "Unswerving Devotion",
        "devanagari": "भक्तिरव्यभिचारिणी",
        "verse":    "BG 13.10",
        "definition": "Single-pointed, unwavering devotion to the Lord, without distraction.",
        "teaching": "Bhakti is not emotional excitement. It is the steady flow of love and "
                    "remembrance of God in all moments — in joy and sorrow, success and failure. "
                    "Like oil poured continuously, unbroken, unswerving.",
        "prompt":   "Reflect: How did I remember the Divine today? "
                    "What practices help me stay connected throughout the day?",
        "quote":    "Whatever you may offer — it doesn't matter. What Bhagavān sees is "
                    "the <strong>devotion</strong> with which you offer.",
    },
    {
        "value":    "viveka",
        "english":  "Discrimination",
        "devanagari": "विवेक",
        "verse":    "BG 13.11",
        "definition": "Discrimination between the real (eternal) and the unreal (transient).",
        "teaching": "Viveka is the prime faculty of the seeker. Everything in this world is "
                    "transient — relationships, success, body itself. Only the Self is eternal. "
                    "The wise person constantly turns the mind toward the imperishable.",
        "prompt":   "Reflect: Where did I confuse the temporary with the permanent today? "
                    "What is unchanging in my experience right now?",
        "quote":    "That which is <strong>infinite, all-pervading</strong> cannot have a form. "
                    "But for the sake of the devotee, Bhagawān <strong>takes up a form</strong>.",
    },
    {
        "value":    "abhayaṁ",
        "english":  "Fearlessness",
        "devanagari": "अभयम्",
        "verse":    "BG 16.1",
        "definition": "Freedom from fear — the first of the daivī sampat (divine qualities).",
        "teaching": "Fear arises from a sense of separation — from God, from the Self, from "
                    "the wholeness of existence. The realized one is fearless because they "
                    "know nothing can be lost — the Self is forever full and eternal.",
        "prompt":   "Reflect: What fear is holding me back today? "
                    "What would I do if I knew I was truly safe and supported?",
        "quote":    "Remember, in life, the <strong>only permanent relationship</strong> "
                    "is our relationship with <strong>God</strong>.",
    },
    {
        "value":    "sattva-saṁśuddhiḥ",
        "english":  "Purity of Mind",
        "devanagari": "सत्त्वसंशुद्धिः",
        "verse":    "BG 16.1",
        "definition": "Purity of inner antaḥkaraṇa (mind, intellect, ego) — established in sattva.",
        "teaching": "When the mind is pure, it reflects the Self clearly — like a polished mirror "
                    "reflecting the sun. Sattvic qualities — clarity, peace, contentment — emerge "
                    "naturally. The grossness of rajas and tamas falls away.",
        "prompt":   "Reflect: What thoughts dominated my mind today — peaceful, restless, or dull? "
                    "What can I do to cultivate more sattva tomorrow?",
        "quote":    "God is not someone who can be seen through the naked eyes. "
                    "He is someone who can be experienced in a <strong>pure heart</strong>.",
    },
    {
        "value":    "satyam",
        "english":  "Truthfulness",
        "devanagari": "सत्यम्",
        "verse":    "BG 16.2",
        "definition": "Truthfulness in word and thought — saying what is real, beneficial, and kind.",
        "teaching": "Satyam is not blunt truth-telling. The scriptures say: truth that hurts "
                    "is not satyam in its highest sense. Speak truth that is beneficial, kind, "
                    "and necessary. And above all — be truthful with yourself.",
        "prompt":   "Reflect: Was I truthful today — to myself and to others? "
                    "Where did I shade or hide the truth, and why?",
        "quote":    "A heart filled with <strong>noble emotions</strong> like kindness, "
                    "compassion, mercy, truthfulness, honesty — such a heart is called a "
                    "<strong>pure heart</strong>.",
    },
    {
        "value":    "dānam",
        "english":  "Charity / Generosity",
        "devanagari": "दानम्",
        "verse":    "BG 16.1",
        "definition": "The spirit of giving — of time, attention, resources, knowledge, kindness.",
        "teaching": "True dāna is given without expectation of return, at the right time, "
                    "to the right person, in the right way. Dāna purifies the giver as much "
                    "as it helps the receiver. The act of giving releases attachment.",
        "prompt":   "Reflect: How did I give today — of myself, my time, my resources? "
                    "What is the inner motivation behind my giving?",
        "quote":    "Whatever you may offer — it doesn't matter. What Bhagavān sees is "
                    "the <strong>devotion</strong> with which you offer.",
    },
    {
        "value":    "tapas",
        "english":  "Austerity / Discipline",
        "devanagari": "तपस्",
        "verse":    "BG 16.1",
        "definition": "Voluntary discipline of body, speech, and mind for spiritual growth.",
        "teaching": "Tapas is not self-torture. It is the conscious choice to undertake "
                    "discipline that purifies and strengthens. It includes regularity in practice, "
                    "moderation in eating and speech, and gentleness in thought. Tapas burns away "
                    "the dross of impurities.",
        "prompt":   "Reflect: What sādhana did I undertake today? "
                    "Where did I choose discipline over comfort?",
        "quote":    "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!",
    },
]


def get_today_value():
    """Pick today's value based on day of year — rotates daily."""
    idx = date.today().toordinal() % len(DAILY_VALUES)
    return DAILY_VALUES[idx], idx


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#4A7C59,#6A9E78);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#2A5C3A,#4A7C59);transform:translateY(-2px);}

.page-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;
    color:#2A5C3A;text-align:center;margin:.5rem 0 .2rem;}
.page-subtitle{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#4A7C59;text-align:center;font-size:1.15rem;margin-bottom:2rem;}
.date-badge{text-align:center;font-family:'Lato',sans-serif;font-size:.85rem;
    color:#8B6914;font-weight:700;letter-spacing:1.5px;margin-bottom:1.5rem;}

.hero-value{background:linear-gradient(135deg,#EDF3EC 0%,#E4EDE4 50%,#EFF4EF 100%);
    border:2px solid #B8D4BC;border-radius:20px;padding:3rem 2rem;text-align:center;
    margin-bottom:2rem;box-shadow:0 4px 24px rgba(74,124,89,.10);position:relative;}
.hero-value::before{content:"🪷";position:absolute;top:-20px;left:50%;transform:translateX(-50%);
    background:#F8F9F5;border:2px solid #B8D4BC;border-radius:50%;width:50px;height:50px;
    display:flex;align-items:center;justify-content:center;font-size:1.5rem;}
.value-sanskrit{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:3.5rem;font-weight:700;color:#2A5C3A;line-height:1.1;margin-bottom:.3rem;}
.value-devanagari{font-family:'Cormorant Garamond',serif;font-size:1.8rem;
    color:#8B6914;margin-bottom:.5rem;}
.value-english{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
    color:#4A6B54;margin-bottom:.5rem;}
.value-verse{font-family:'Lato',sans-serif;font-size:.85rem;color:#8B6914;
    font-weight:700;letter-spacing:2px;text-transform:uppercase;}

.content-card{background:white;border:1.5px solid #B8D4BC;border-radius:14px;
    padding:1.8rem 2rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(74,124,89,.06);}
.card-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
    color:#2A5C3A;margin-bottom:.8rem;padding-bottom:.4rem;
    border-bottom:1.5px solid #B8D4BC;display:flex;align-items:center;gap:.6rem;}
.card-text{color:#1A3A28;font-size:.95rem;line-height:1.85;
    font-family:'Lato',sans-serif;}
.card-prompt{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.15rem;color:#2A4A38;line-height:1.75;
    padding:1rem 1.4rem;background:#EDF3EC;border-radius:10px;
    border-left:4px solid #8B6914;}

.swamiji-card{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);
    border:2px solid #B8D4BC;border-left:5px solid #4A7C59;
    border-radius:0 14px 14px 0;padding:1.5rem 1.8rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(74,124,89,.07);}
.swamiji-text{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.25rem;font-weight:700;color:#2A4A38;line-height:1.7;text-align:center;}
.swamiji-attr{font-family:'Playfair Display',serif;color:#4A7C59;
    font-size:1rem;font-weight:700;text-align:center;margin-top:.7rem;}

.cta-card{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);
    border:2px solid #B8D4BC;border-radius:14px;padding:1.5rem;text-align:center;
    margin-top:1rem;}
.cta-text{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#3A5040;font-size:1rem;margin-bottom:.8rem;}
</style>
""", unsafe_allow_html=True)

render_om_symbol()

# ── Page Title ─────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Value of the Day</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">A daily contemplation companion 🪷</div>',
            unsafe_allow_html=True)

today_value, today_idx = get_today_value()
st.markdown(f'<div class="date-badge">{date.today().strftime("%A, %B %d, %Y")} · '
            f'Day {today_idx + 1} of {len(DAILY_VALUES)}</div>',
            unsafe_allow_html=True)

# ── Hero — Today's Value ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-value">
    <div class="value-sanskrit">{today_value['value']}</div>
    <div class="value-devanagari">{today_value['devanagari']}</div>
    <div class="value-english">{today_value['english']}</div>
    <div class="value-verse">📖 {today_value['verse']}</div>
</div>
""", unsafe_allow_html=True)

# ── Definition ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="content-card">
    <div class="card-title">🪷 Meaning</div>
    <div class="card-text">{today_value['definition']}</div>
</div>
""", unsafe_allow_html=True)

# ── Teaching ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="content-card">
    <div class="card-title">📿 Teaching</div>
    <div class="card-text">{today_value['teaching']}</div>
</div>
""", unsafe_allow_html=True)

# ── Swamiji's Quote ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="swamiji-card">
    <div class="swamiji-text">&ldquo;{today_value['quote']}&rdquo;</div>
    <div class="swamiji-attr">— Swāmī Aparājitānandajī</div>
</div>
""", unsafe_allow_html=True)

# ── Reflection Prompt ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="content-card">
    <div class="card-title">✍️ Today's Reflection</div>
    <div class="card-prompt">{today_value['prompt']}</div>
</div>
""", unsafe_allow_html=True)

# ── Call to Action ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-card">
    <div class="cta-text">
        Want to write your reflection on this value?
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📔 Open Reflection Journal", use_container_width=True):
        st.switch_page("pages/10_Reflection_Journal.py")
with col2:
    if st.button("💬 Ask About This Value", use_container_width=True):
        st.session_state["pending_question"] = (
            f"What does Swamiji teach about {today_value['value']} "
            f"({today_value['english']})?"
        )
        st.switch_page("pages/2_Indispensable_Values_QA.py")

# ── Browse Other Values Section ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🌿 Explore another value"):
    st.markdown(
        "<p style='color:#3A5040;font-size:.9rem;margin-bottom:.8rem;'>"
        "Browse all 20 values from Bhagavad Gītā Chapters 13 &amp; 16. "
        "Click any to see its full contemplation.</p>",
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, v in enumerate(DAILY_VALUES):
        with cols[i % 2]:
            label = f"{v['value']} — {v['english']}"
            if st.button(label, key=f"v_{i}", use_container_width=True):
                st.session_state["selected_value_idx"] = i
                st.rerun()

# ── If a specific value was selected from browse ──────────────────────────────
if "selected_value_idx" in st.session_state:
    sel_idx = st.session_state["selected_value_idx"]
    if sel_idx != today_idx:
        sel = DAILY_VALUES[sel_idx]
        st.divider()
        st.markdown(f"<h3 style='text-align:center;'>📖 {sel['value']} — {sel['english']}</h3>",
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="hero-value">
            <div class="value-sanskrit">{sel['value']}</div>
            <div class="value-devanagari">{sel['devanagari']}</div>
            <div class="value-english">{sel['english']}</div>
            <div class="value-verse">📖 {sel['verse']}</div>
        </div>
        <div class="content-card">
            <div class="card-title">🪷 Meaning</div>
            <div class="card-text">{sel['definition']}</div>
        </div>
        <div class="content-card">
            <div class="card-title">📿 Teaching</div>
            <div class="card-text">{sel['teaching']}</div>
        </div>
        <div class="swamiji-card">
            <div class="swamiji-text">&ldquo;{sel['quote']}&rdquo;</div>
            <div class="swamiji-attr">— Swāmī Aparājitānandajī</div>
        </div>
        <div class="content-card">
            <div class="card-title">✍️ Reflection Prompt</div>
            <div class="card-prompt">{sel['prompt']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗙 Close this view"):
            del st.session_state["selected_value_idx"]
            st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#4A6B54;font-size:.85rem;font-family:'Cormorant Garamond',serif;
    font-style:italic;padding:1rem;border-top:1.5px solid #B8D4BC;margin-top:2rem;">
    🪷 &nbsp; A new value appears each day. &nbsp; 🪷<br>
    Spend a few moments today contemplating its meaning in your life.
</div>
""", unsafe_allow_html=True)
