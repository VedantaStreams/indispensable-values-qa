"""
pages/4_Value_of_the_Day.py — Daily contemplation page.
Auto-rotates through 20 values from Bhagavad Gītā Chapters 13 & 16.
Each value has 4 prompts that rotate daily for richer contemplation.
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

# ══════════════════════════════════════════════════════════════════════════════
# 20 Values — each with 4 rotating prompts
# ══════════════════════════════════════════════════════════════════════════════
DAILY_VALUES = [
    {
        "value":      "amānitvam",
        "english":    "Humility",
        "devanagari": "अमानित्वम्",
        "verse":      "BG 13.7",
        "definition": "Absence of self-glorification, of the desire for recognition, or seeking honor and respect from others.",
        "teaching":   "Humility is not low self-esteem. It is the natural state of one who has seen the infinite Self and recognizes the same Self in all beings. True humility arises from the understanding that whatever talents or accomplishments we possess have been given by Īśvara.",
        "prompts": [
            "Where did I seek recognition or praise today? Can I dedicate my actions and accomplishments to the Lord?",
            "When did I feel offended that someone didn't acknowledge me? What does this reveal about my ego?",
            "Whose contribution did I overlook today? How can I express gratitude?",
            "If no one was watching, would I still do my good deeds with the same energy?",
        ],
        "quote": "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!",
    },
    {
        "value":      "adambhitvam",
        "english":    "Absence of Pretense",
        "devanagari": "अदम्भित्वम्",
        "verse":      "BG 13.7",
        "definition": "The quality of not displaying or showing off one's qualifications, wealth, status, or spiritual practices.",
        "teaching":   "Where there is dambha (hypocrisy), there is a gap between what we are inside and what we project outside. The seeker walks a path of inner-outer alignment — being the same in private as in public.",
        "prompts": [
            "Where am I projecting an image rather than being authentic?",
            "Did I exaggerate my achievements to impress someone today?",
            "In which relationship do I feel I must wear a mask? What would happen if I removed it?",
            "Where do I display rather than simply share?",
        ],
        "quote": "<strong>True happiness</strong> shouldn't be because of! <strong>True happiness</strong> should be in spite of!",
    },
    {
        "value":      "ahiṃsā",
        "english":    "Non-Injury",
        "devanagari": "अहिंसा",
        "verse":      "BG 13.7",
        "definition": "Not causing pain to any living being — by thought, word, or deed.",
        "teaching":   "Ahiṃsā is not merely avoiding physical violence. It includes harsh words, cutting remarks, hateful thoughts, and indifference to others' suffering. It is positive love and compassion, not just the absence of cruelty.",
        "prompts": [
            "Did I cause hurt today — by word, action, or thought?",
            "Whose pain did I notice today, and how did I respond — with compassion or indifference?",
            "Am I being harsh with myself in any way? Where can I extend kindness inward first?",
            "When did I speak unkindly today? What was happening inside me?",
        ],
        "quote": "A heart filled with <strong>noble emotions</strong> like kindness, compassion, mercy, truthfulness, honesty — such a heart is called a <strong>pure heart</strong>.",
    },
    {
        "value":      "kṣāntiḥ",
        "english":    "Forbearance",
        "devanagari": "क्षान्तिः",
        "verse":      "BG 13.7",
        "definition": "Patience, forgiveness, and forbearance in the face of provocation or injury.",
        "teaching":   "Kṣānti is not weakness or suppression. It is the strength to remain unaffected when wronged, knowing that anger only burns the one who holds it. The mighty one is not who can strike back, but who can forgive.",
        "prompts": [
            "What tested my patience today? Did I respond with peace or with reactivity?",
            "Whom have I not yet forgiven? What is the cost of holding this resentment?",
            "When I was wronged today, did I pause before reacting?",
            "What old hurt am I still carrying? Can I release a small piece of it today?",
        ],
        "quote": "Rate your <strong>spiritual progress</strong> with the <strong>intensity of Peace</strong> which you experience.",
    },
    {
        "value":      "ārjavam",
        "english":    "Simplicity / Straightforwardness",
        "devanagari": "आर्जवम्",
        "verse":      "BG 13.7",
        "definition": "Alignment of thought, word, and action — the absence of crookedness.",
        "teaching":   "Ārjavam is the simplicity of one whose inner and outer lives are unified. What is thought is spoken; what is spoken is acted upon. There is no duplicity, no hidden agenda, no double-dealing.",
        "prompts": [
            "Were my thoughts, words, and deeds aligned today?",
            "Was there a moment today where I said one thing but meant another?",
            "Where am I complicating something that could be simple?",
            "What untold truth, if spoken simply and kindly, would bring relief to my heart?",
        ],
        "quote": "God resides in the hearts of all. But only those <strong>blessed ones</strong> who have kept their <strong>heart pure</strong> can experience it.",
    },
    {
        "value":      "ācāryopāsanam",
        "english":    "Service to the Teacher",
        "devanagari": "आचार्योपासनम्",
        "verse":      "BG 13.7",
        "definition": "Devoted service and reverence to one's spiritual teacher (Guru).",
        "teaching":   "The Guru is the channel through which the eternal teaching flows. Upāsana means 'sitting near' — not just physically, but with surrender, attentiveness, and a heart ready to receive. Without a Guru, the scriptures remain mere words.",
        "prompts": [
            "How am I honoring my teachers — past and present?",
            "Which of Swamiji's teachings has touched me most deeply this week? How am I living it?",
            "Whom can I think of as my teacher in daily life — colleagues, family, even challenges?",
            "If I had ten minutes with my Guru today, what would I want to ask or share?",
        ],
        "quote": "Remember, in life, the <strong>only permanent relationship</strong> is our relationship with <strong>God</strong>.",
    },
    {
        "value":      "śaucam",
        "english":    "Purity",
        "devanagari": "शौचम्",
        "verse":      "BG 13.7",
        "definition": "Cleanliness — both external (body, surroundings) and internal (mind, thoughts).",
        "teaching":   "External cleanliness reflects inner cleanliness. The mind cleansed of raga (attachment), dveṣa (aversion), and ahaṅkāra (ego) becomes a fit vessel for higher knowledge. God resides in a pure heart.",
        "prompts": [
            "What is the state of my mind today — clear or cluttered?",
            "What media, conversations, or environments influenced my inner state today?",
            "Is there a corner of my home, life, or mind that needs cleansing?",
            "How did my external environment affect my internal state today?",
        ],
        "quote": "God is not someone who can be seen through the naked eyes. He is someone who can be experienced in a <strong>pure heart</strong>.",
    },
    {
        "value":      "sthairyam",
        "english":    "Steadfastness",
        "devanagari": "स्थैर्यम्",
        "verse":      "BG 13.7",
        "definition": "Steadiness and perseverance in spiritual practice, especially in difficulties.",
        "teaching":   "The path is long and the obstacles many. Sthairyam is the inner resolve that says — 'I will continue, whatever may come.' It is not enthusiasm of a moment but the quiet determination of a lifetime.",
        "prompts": [
            "Did I waver in my practice today? What strengthens my resolve?",
            "What spiritual practice have I been inconsistent with lately?",
            "When I felt like giving up today, what kept me going?",
            "Where am I demanding quick results when steady practice is what's needed?",
        ],
        "quote": "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!",
    },
    {
        "value":      "ātmavinigrahaḥ",
        "english":    "Self-Control",
        "devanagari": "आत्मविनिग्रहः",
        "verse":      "BG 13.7",
        "definition": "Control of the senses and mind — not allowing them to run unchecked.",
        "teaching":   "The senses by nature run outward, seeking objects of pleasure. Ātma-vinigraha is the conscious choice to direct them inward, toward the Self. Not by suppression, but by wisdom.",
        "prompts": [
            "Where did my senses pull me today? Did I respond with awareness or impulsively?",
            "Which sense-craving keeps returning despite knowing it doesn't satisfy?",
            "When did I act mindfully today versus on autopilot?",
            "What single sense-pleasure am I willing to moderate this week?",
        ],
        "quote": "Rate your <strong>spiritual progress</strong> with the <strong>intensity of Peace</strong> which you experience.",
    },
    {
        "value":      "vairāgyam",
        "english":    "Dispassion",
        "devanagari": "वैराग्यम्",
        "verse":      "BG 13.8",
        "definition": "Dispassion toward sense objects — not attachment to pleasures of body or world.",
        "teaching":   "Vairāgya is not hatred of the world or escapism. It is the wisdom to engage fully with life without being enslaved by its objects. Like a lotus untouched by water — present yet free.",
        "prompts": [
            "What do I cling to that brings me anxiety?",
            "What sense-pleasure am I overestimating right now?",
            "If I lost what I'm most attached to, who would I still be?",
            "Where is my mind running throughout the day? What is it seeking?",
        ],
        "quote": "<strong>True happiness</strong> shouldn't be because of! <strong>True happiness</strong> should be in spite of!",
    },
    {
        "value":      "anahaṅkāra",
        "english":    "Absence of Ego",
        "devanagari": "अनहङ्कारः",
        "verse":      "BG 13.8",
        "definition": "Freedom from the false sense of 'I' identifying with body, mind, and ego.",
        "teaching":   "The 'I' that takes credit, fears criticism, and seeks to be special — that is ahaṅkāra. The Self needs no recognition because it is already complete. Anahaṅkāra is the natural ease of one who knows this.",
        "prompts": [
            "Where did my ego assert itself today?",
            "When did I take personal credit for what was really collective effort or grace?",
            "What criticism stung me today? What does that reveal about my self-image?",
            "Can I do one small act today without anyone knowing?",
        ],
        "quote": "God resides in the hearts of all. But only those <strong>blessed ones</strong> who have kept their <strong>heart pure</strong> can experience it.",
    },
    {
        "value":      "asaktiḥ",
        "english":    "Non-Attachment",
        "devanagari": "असक्तिः",
        "verse":      "BG 13.9",
        "definition": "Freedom from clinging — to people, possessions, situations, outcomes.",
        "teaching":   "Asakti does not mean cold detachment. It means the freedom that allows us to love deeply without dependence. We hold our relationships and responsibilities with open hands, not clenched fists.",
        "prompts": [
            "What attachment is causing me suffering?",
            "Where is my happiness conditional on someone else behaving a certain way?",
            "What possession, relationship, or role do I cling to as my identity?",
            "Can I love someone fully today without expecting anything in return?",
        ],
        "quote": "Remember, in life, the <strong>only permanent relationship</strong> is our relationship with <strong>God</strong>.",
    },
    {
        "value":      "samacittatvam",
        "english":    "Equanimity",
        "devanagari": "समचित्तत्वम्",
        "verse":      "BG 13.9",
        "definition": "Evenness of mind in pleasant and unpleasant events, success and failure.",
        "teaching":   "Sama-citta is not indifference. It is the inner stability of one who knows that situations come and go, but the Self remains. Both praise and criticism are received with the same calm presence.",
        "prompts": [
            "Was I equally accepting of pleasant and unpleasant events today?",
            "What disturbed me most today? Where did the disturbance actually arise?",
            "What moment of elation and what moment of low did I have today?",
            "What if I greeted every event today as a teacher?",
        ],
        "quote": "Rate your <strong>spiritual progress</strong> with the <strong>intensity of Peace</strong> which you experience.",
    },
    {
        "value":      "bhakti avyabhicāriṇī",
        "english":    "Unswerving Devotion",
        "devanagari": "भक्तिरव्यभिचारिणी",
        "verse":      "BG 13.10",
        "definition": "Single-pointed, unwavering devotion to the Lord, without distraction.",
        "teaching":   "Bhakti is not emotional excitement. It is the steady flow of love and remembrance of God in all moments — in joy and sorrow, success and failure. Like oil poured continuously, unbroken.",
        "prompts": [
            "How did I remember the Divine today?",
            "When was I most aware of the Lord's presence today? When did I forget?",
            "What single act today can I offer up as worship?",
            "If God walked into my room right now, what would I want to feel or say?",
        ],
        "quote": "Whatever you may offer — it doesn't matter. What Bhagavān sees is the <strong>devotion</strong> with which you offer.",
    },
    {
        "value":      "viveka",
        "english":    "Discrimination",
        "devanagari": "विवेक",
        "verse":      "BG 13.11",
        "definition": "Discrimination between the real (eternal) and the unreal (transient).",
        "teaching":   "Viveka is the prime faculty of the seeker. Everything in this world is transient — relationships, success, body itself. Only the Self is eternal. The wise person constantly turns the mind toward the imperishable.",
        "prompts": [
            "Where did I confuse the temporary with the permanent today?",
            "What am I treating as a problem when it's just the nature of the world?",
            "If everything in this world is changing, what within me is unchanging?",
            "What did I assume was real today that, on reflection, was just a thought?",
        ],
        "quote": "That which is <strong>infinite, all-pervading</strong> cannot have a form. But for the sake of the devotee, Bhagawān <strong>takes up a form</strong>.",
    },
    {
        "value":      "abhayaṁ",
        "english":    "Fearlessness",
        "devanagari": "अभयम्",
        "verse":      "BG 16.1",
        "definition": "Freedom from fear — the first of the daivī sampat (divine qualities).",
        "teaching":   "Fear arises from a sense of separation — from God, from the Self, from the wholeness of existence. The realized one is fearless because they know nothing can be lost — the Self is forever full and eternal.",
        "prompts": [
            "What fear is holding me back today?",
            "What is the worst-case scenario I'm imagining? Even then, would the Self be untouched?",
            "Where is my fear pretending to be wisdom or caution?",
            "What truth do I know but am afraid to act upon?",
        ],
        "quote": "Remember, in life, the <strong>only permanent relationship</strong> is our relationship with <strong>God</strong>.",
    },
    {
        "value":      "sattva-saṁśuddhiḥ",
        "english":    "Purity of Mind",
        "devanagari": "सत्त्वसंशुद्धिः",
        "verse":      "BG 16.1",
        "definition": "Purity of inner antaḥkaraṇa (mind, intellect, ego) — established in sattva.",
        "teaching":   "When the mind is pure, it reflects the Self clearly — like a polished mirror reflecting the sun. Sattvic qualities — clarity, peace, contentment — emerge naturally.",
        "prompts": [
            "What thoughts dominated my mind today — peaceful, restless, or dull?",
            "What did I consume today — food, media, conversations — and what state of mind did it produce?",
            "Which of my habits foster clarity, and which dull or agitate my mind?",
            "What sattvic practice can I add tomorrow — silence, study, prayer, sattvic food, nature?",
        ],
        "quote": "God is not someone who can be seen through the naked eyes. He is someone who can be experienced in a <strong>pure heart</strong>.",
    },
    {
        "value":      "satyam",
        "english":    "Truthfulness",
        "devanagari": "सत्यम्",
        "verse":      "BG 16.2",
        "definition": "Truthfulness in word and thought — saying what is real, beneficial, and kind.",
        "teaching":   "Satyam is not blunt truth-telling. The scriptures say: truth that hurts is not satyam in its highest sense. Speak truth that is beneficial, kind, and necessary. And above all — be truthful with yourself.",
        "prompts": [
            "Was I truthful today — to myself and to others?",
            "What truth am I avoiding because it's uncomfortable to face?",
            "Was there a moment today when a small white lie felt easier? What was I protecting?",
            "How do I speak truth that is also kind and necessary, not just blunt?",
        ],
        "quote": "A heart filled with <strong>noble emotions</strong> like kindness, compassion, mercy, truthfulness, honesty — such a heart is called a <strong>pure heart</strong>.",
    },
    {
        "value":      "dānam",
        "english":    "Charity / Generosity",
        "devanagari": "दानम्",
        "verse":      "BG 16.1",
        "definition": "The spirit of giving — of time, attention, resources, knowledge, kindness.",
        "teaching":   "True dāna is given without expectation of return, at the right time, to the right person, in the right way. Dāna purifies the giver as much as it helps the receiver. The act of giving releases attachment.",
        "prompts": [
            "How did I give today — of myself, my time, my resources?",
            "Did I give expecting something in return — recognition, gratitude, future reciprocation?",
            "Whom around me needs my time or attention more than my money?",
            "What can I give today without telling anyone?",
        ],
        "quote": "Whatever you may offer — it doesn't matter. What Bhagavān sees is the <strong>devotion</strong> with which you offer.",
    },
    {
        "value":      "tapas",
        "english":    "Austerity / Discipline",
        "devanagari": "तपस्",
        "verse":      "BG 16.1",
        "definition": "Voluntary discipline of body, speech, and mind for spiritual growth.",
        "teaching":   "Tapas is not self-torture. It is the conscious choice to undertake discipline that purifies and strengthens. It includes regularity in practice, moderation in eating and speech, and gentleness in thought.",
        "prompts": [
            "What sādhana did I undertake today?",
            "What small daily discipline can I commit to this week?",
            "Where am I being indulgent in a way that weakens rather than serves me?",
            "What discomfort can I welcome today as a teacher rather than resist as an enemy?",
        ],
        "quote": "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!",
    },
]


def get_today_value():
    """Pick today's value AND today's prompt — both rotate."""
    today_ordinal = date.today().toordinal()
    value_idx     = today_ordinal % len(DAILY_VALUES)
    prompt_idx    = (today_ordinal // len(DAILY_VALUES)) % 4
    return DAILY_VALUES[value_idx], value_idx, prompt_idx


def get_prompt(value: dict, prompt_idx: int) -> str:
    prompts = value.get("prompts", [])
    if not prompts:
        return ""
    return prompts[prompt_idx % len(prompts)]


# ══════════════════════════════════════════════════════════════════════════════
# Page CSS — Royal Maroon
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#1A3A45;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#0A4A58!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #0A4A58;}
div[data-testid="stSidebar"] *{color:#1A3A45!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#1A7A8C,#2C95A8);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#0A4A58,#1A7A8C);transform:translateY(-2px);}

.page-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;
    color:#0A4A58;text-align:center;margin:.5rem 0 .2rem;}
.page-subtitle{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#1A7A8C;text-align:center;font-size:1.15rem;margin-bottom:2rem;}
.date-badge{text-align:center;font-family:'Lato',sans-serif;font-size:.85rem;
    color:#0A4A58;font-weight:700;letter-spacing:1.5px;margin-bottom:1.5rem;}

.hero-value{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);
    border:2px solid #0A4A58;border-radius:20px;padding:3rem 2rem;text-align:center;
    margin-bottom:2rem;box-shadow:0 4px 24px rgba(26,122,140,.20);position:relative;}
.value-sanskrit{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:3.5rem;font-weight:700;color:#1A7A8C;line-height:1.1;margin-bottom:.3rem;}
.value-devanagari{font-family:'Cormorant Garamond',serif;font-size:1.8rem;
    color:#0A4A58;margin-bottom:.5rem;}
.value-english{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
    color:#FF8C42;margin-bottom:.5rem;}
.value-verse{font-family:'Lato',sans-serif;font-size:.85rem;color:#0A4A58;
    font-weight:700;letter-spacing:2px;text-transform:uppercase;}

.content-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;
    padding:1.8rem 2rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(0,0,0,.3);}
.card-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
    color:#0A4A58;margin-bottom:.8rem;padding-bottom:.4rem;
    border-bottom:1.5px solid #88C5D0;display:flex;align-items:center;gap:.6rem;}
.card-text{color:#1A3A45;font-size:.95rem;line-height:1.85;font-family:'Lato',sans-serif;}
.card-prompt{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.15rem;color:#1A7A8C;line-height:1.75;
    padding:1rem 1.4rem;background:#D0EDF1;border-radius:10px;
    border-left:4px solid #0A4A58;}

.swamiji-card{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);
    border:2px solid #0A4A58;border-left:5px solid #1A7A8C;
    border-radius:0 14px 14px 0;padding:1.5rem 1.8rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(26,122,140,.20);}
.swamiji-text{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.25rem;font-weight:700;color:#1A3A45;line-height:1.7;text-align:center;}
.swamiji-attr{font-family:'Playfair Display',serif;color:#FF8C42;
    font-size:1rem;font-weight:700;text-align:center;margin-top:.7rem;}
</style>
""", unsafe_allow_html=True)

render_om_symbol()

# ── Page Title ─────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Value of the Day</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">A daily contemplation companion 🪷</div>',
            unsafe_allow_html=True)

today_value, today_idx, prompt_idx = get_today_value()
today_prompt = get_prompt(today_value, prompt_idx)

st.markdown(
    f'<div class="date-badge">{date.today().strftime("%A, %B %d, %Y")} · '
    f'Day {today_idx + 1} of {len(DAILY_VALUES)}</div>',
    unsafe_allow_html=True,
)

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
    <div class="swamiji-attr">— Pūjya Swāmī Aparājitānandajī</div>
</div>
""", unsafe_allow_html=True)

# ── Reflection Prompt ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="content-card">
    <div class="card-title">✍️ Today's Reflection</div>
    <div class="card-prompt">{today_prompt}</div>
</div>
""", unsafe_allow_html=True)

# ── Action Buttons ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    if st.button("📔 Open Reflection Journal", use_container_width=True):
        st.switch_page("pages/3_Reflection_Journal.py")
with col2:
    if st.button("💬 Ask About This Value", use_container_width=True):
        st.session_state["pending_question"] = (
            f"What does Swamiji teach about {today_value['value']} "
            f"({today_value['english']})?"
        )
        st.switch_page("pages/2_Indispensable_Values_QA.py")

# ── Browse Other Values ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🌿 Explore another value"):
    cols = st.columns(2)
    for i, v in enumerate(DAILY_VALUES):
        with cols[i % 2]:
            if st.button(f"{v['value']} — {v['english']}",
                         key=f"v_{i}", use_container_width=True):
                st.session_state["selected_value_idx"] = i
                st.rerun()

# ── Selected value view ────────────────────────────────────────────────────────
if "selected_value_idx" in st.session_state:
    sel_idx = st.session_state["selected_value_idx"]
    if sel_idx != today_idx:
        sel = DAILY_VALUES[sel_idx]
        sel_prompt = get_prompt(sel, prompt_idx)
        st.divider()
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
            <div class="swamiji-attr">— Pūjya Swāmī Aparājitānandajī</div>
        </div>
        <div class="content-card">
            <div class="card-title">✍️ Reflection Prompt</div>
            <div class="card-prompt">{sel_prompt}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗙 Close this view"):
            del st.session_state["selected_value_idx"]
            st.rerun()
