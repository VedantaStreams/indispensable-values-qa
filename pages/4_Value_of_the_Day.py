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
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#0A1E28;font-weight:500;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#062E3A!important;font-weight:800!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #062E3A;}
div[data-testid="stSidebar"] *{color:#0A1E28!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#0D5C6B,#2C95A8);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#062E3A,#0D5C6B);transform:translateY(-2px);}

.page-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;
    color:#062E3A;text-align:center;margin:.5rem 0 .2rem;}
.page-subtitle{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#062E3A;text-align:center;font-size:1.15rem;margin-bottom:2rem;}
.date-badge{text-align:center;font-family:'Lato',sans-serif;font-size:.85rem;
    color:#062E3A;font-weight:700;letter-spacing:1.5px;margin-bottom:1.5rem;}

.hero-value{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);
    border:2px solid #062E3A;border-radius:20px;padding:3rem 2rem;text-align:center;
    margin-bottom:2rem;box-shadow:0 4px 24px rgba(26,122,140,.20);position:relative;}
.value-sanskrit{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:3.5rem;font-weight:700;color:#062E3A;line-height:1.1;margin-bottom:.3rem;}
.value-devanagari{font-family:'Cormorant Garamond',serif;font-size:1.8rem;
    color:#062E3A;margin-bottom:.5rem;}
.value-english{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
    color:#FF8C42;margin-bottom:.5rem;}
.value-verse{font-family:'Lato',sans-serif;font-size:.85rem;color:#062E3A;
    font-weight:700;letter-spacing:2px;text-transform:uppercase;}

.content-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;
    padding:1.8rem 2rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(26,122,140,.08);}
.card-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
    color:#062E3A;margin-bottom:.8rem;padding-bottom:.4rem;
    border-bottom:1.5px solid #88C5D0;display:flex;align-items:center;gap:.6rem;}
.card-text{color:#0A1E28;font-size:.95rem;line-height:1.85;font-weight:500;font-family:'Lato',sans-serif;}
.card-prompt{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.15rem;color:#062E3A;line-height:1.75;
    padding:1rem 1.4rem;background:#D0EDF1;border-radius:10px;
    border-left:4px solid #062E3A;}

.swamiji-card{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);
    border:2px solid #062E3A;border-left:5px solid #0D5C6B;
    border-radius:0 14px 14px 0;padding:1.5rem 1.8rem;margin-bottom:1.5rem;
    box-shadow:0 2px 12px rgba(26,122,140,.20);}
.swamiji-text{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.25rem;font-weight:700;color:#0A1E28;line-height:1.7;text-align:center;}
.swamiji-attr{font-family:'Playfair Display',serif;color:#FF8C42;
    font-size:1rem;font-weight:700;text-align:center;margin-top:.7rem;}

.om-box-pg{
    background:linear-gradient(135deg,#D0EDF1,#B8E4EC);
    border:2px solid #1A7A8C;border-radius:16px;
    width:90px;height:90px;
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:.8rem;
    box-shadow:0 4px 16px rgba(26,122,140,.15);
}
.om-box-pg img{width:70px;height:70px;object-fit:contain;border-radius:10px;}
.swamiji-quote-pg{
    text-align:center;max-width:780px;margin:.5rem auto 1.8rem;
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.35rem;font-weight:700;color:#03202A;
    line-height:1.75;padding:0 1.5rem;
}
.swamiji-quote-pg-attr{display:block;font-family:'Playfair Display',serif;
    font-style:normal;font-size:1rem;font-weight:700;
    color:#0D5C6B;margin-top:.7rem;}

</style>
""", unsafe_allow_html=True)


# ── Page Title ─────────────────────────────────────────────────────────────────
st.markdown(f'''
<div style="background:linear-gradient(135deg,#D0EDF1 0%,#B8E4EC 50%,#C8EAF0 100%);
    border:2px solid #1A7A8C;border-radius:20px;
    padding:2.2rem 3rem 1.8rem;text-align:center;
    margin-bottom:1rem;
    box-shadow:0 4px 24px rgba(26,122,140,.12);width:100%;">
    <div class="om-box-pg"><img src="data:image/jpeg;base64,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" alt="Om"/></div><br>
    <div class="page-title">Value of the Day</div>
    <div class="page-subtitle">A daily contemplation companion 🪷</div>
</div>
''', unsafe_allow_html=True)

today_value, today_idx, prompt_idx = get_today_value()
today_prompt = get_prompt(today_value, prompt_idx)

st.markdown(
    f'<div class="date-badge">{date.today().strftime("%A, %B %d, %Y")} · '
    f'Day {today_idx + 1} of {len(DAILY_VALUES)}</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="swamiji-quote-pg">
    &ldquo;Rate your <strong>spiritual progress</strong> with the <strong>intensity of Peace</strong> which you experience.&rdquo;
    <span class="swamiji-quote-pg-attr">— Swāmī Aparājitānanda</span>
</div>
""", unsafe_allow_html=True)

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
    <div class="swamiji-attr">— Pūjya Swāmī Aparājitānanda</div>
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
            <div class="swamiji-attr">— Pūjya Swāmī Aparājitānanda</div>
        </div>
        <div class="content-card">
            <div class="card-title">✍️ Reflection Prompt</div>
            <div class="card-prompt">{sel_prompt}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗙 Close this view"):
            del st.session_state["selected_value_idx"]
            st.rerun()
