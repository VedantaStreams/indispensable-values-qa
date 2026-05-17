"""
pages/1_About_Pujya_Swamiji.py — Clean rewrite. Uses st.image() only.
"""
import streamlit as st
from pathlib import Path

import sys
from pathlib import Path
import sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_om_symbol, render_page_quote

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="About Pūjya Swamiji | Indispensable Values",
                   page_icon="📖", layout="wide")

render_om_symbol()

ASSETS = Path(__file__).parent.parent / "assets" / "images"
APARAJITA = ASSETS / "swamiji_aparajitananda.jpg"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap');

[data-testid="stImage"] {
    margin-bottom:-1.5rem!important;
    padding-bottom:0!important;
    line-height:0!important;
}
[data-testid="stImage"] img {
    display:block!important;
}

html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}

/* ── Pink-gold border on photo ── */
[data-testid="stImage"] img {
    border-radius:16px!important;
    object-fit:cover!important;
    object-position:top center!important;
    border:5px solid transparent!important;
    background:linear-gradient(white,white) padding-box,
               linear-gradient(135deg,#B8D4BC,#8B6914,#4A7C59,#B8D4BC) border-box!important;
    box-shadow:0 8px 30px rgba(74,124,89,.20)!important;
}

.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;
    border-radius:18px;padding:2.5rem;text-align:center;margin-bottom:2rem;
    box-shadow:0 4px 20px rgba(74,124,89,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:#4A7C59;}

.bio-name{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;color:#2A5C3A;
    text-align:center;margin:.8rem 0 .1rem;}
.bio-title{font-family:'Cormorant Garamond',serif;font-style:italic;color:#4A7C59;
    font-size:1rem;text-align:center;}
.bio-loc{font-size:.85rem;color:#4A6B54;text-align:center;margin:.1rem 0;}

.bio-card{background:white;border:2px solid #B8D4BC;border-radius:16px;padding:2rem;
    box-shadow:0 4px 16px rgba(74,124,89,.08);margin-bottom:1.5rem;}
.bio-para{color:#1A3A28;font-size:.97rem;line-height:1.9;margin-bottom:.9rem;}
.bio-para:last-child{margin-bottom:0;}

.quote-block{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);border-left:5px solid #4A7C59;
    border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin:1.2rem 0;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;
    color:#2A5C3A;line-height:1.8;}

.swamiji-quote{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);border-left:5px solid #4A7C59;
    border-radius:0 14px 14px 0;padding:1.2rem 1.8rem;margin:1rem 0;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.05rem;
    color:#2A4A38;line-height:1.8;box-shadow:0 2px 8px rgba(74,124,89,.07);}
.swamiji-quote-attr{font-family:'Lato',sans-serif;font-style:normal;font-size:.75rem;
    font-weight:700;color:#4A7C59;letter-spacing:.5px;margin-top:.5rem;text-transform:uppercase;}

.tag{display:inline-block;background:#EDF3EC;border:1.5px solid #B8D4BC;color:#2A5C3A;
    border-radius:20px;padding:.25rem .85rem;font-size:.85rem;margin:.2rem;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;}

.milestone{display:flex;align-items:flex-start;gap:1rem;background:white;
    border:1.5px solid #B8D4BC;border-radius:12px;padding:1.1rem 1.4rem;
    margin-bottom:.8rem;box-shadow:0 2px 8px rgba(74,124,89,.05);}
.milestone-year{font-family:'Playfair Display',serif;font-size:1rem;font-weight:800;
    color:#4A7C59;min-width:58px;}
.milestone-text{color:#1A3A28;font-size:.92rem;line-height:1.65;}

.value-section{background:white;border:1.5px solid #B8D4BC;border-radius:14px;padding:1.8rem;
    margin-bottom:1rem;box-shadow:0 2px 10px rgba(74,124,89,.06);}
.value-section-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
    color:#2A5C3A;margin-bottom:.8rem;padding-bottom:.4rem;border-bottom:1.5px solid #B8D4BC;}
.value-item{display:flex;align-items:flex-start;margin-bottom:.55rem;}
.value-bullet{color:#4A7C59;font-size:1rem;margin-right:.6rem;flex-shrink:0;}
.value-text{color:#1A3A28;font-size:.9rem;line-height:1.6;}
.value-name{font-weight:700;color:#2A5C3A;font-family:'Cormorant Garamond',serif;font-style:italic;}

.section-title{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;
    color:#2A5C3A;margin:2rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #B8D4BC;}
</style>
""", unsafe_allow_html=True)


render_page_quote(
    "<strong>True happiness</strong> shouldn't be because of! <strong>True happiness</strong> should be in spite of!"
)
# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div style="font-size:2rem;margin-bottom:.3rem;">🪷</div>
    <div class="page-header-title">About Pūjya Swamiji</div>
    <div class="page-header-sub">Swāmī Aparājitānandajī · Chinmaya Mission</div>
</div>
""", unsafe_allow_html=True)

# ── Photo + Intro ─────────────────────────────────────────────────────────────
col_photo, col_intro = st.columns([1, 2])

with col_photo:
    if APARAJITA.exists():
        st.image(str(APARAJITA), width=260)
    else:
        st.markdown('<div style="font-size:5rem;text-align:center;">🙏</div>',
                    unsafe_allow_html=True)
    st.markdown("""
    <div class="bio-name">Swāmī Aparājitānandajī</div>
    <div class="bio-title">Chinmaya Mission</div>
    <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
        color:#3A5040;font-size:.92rem;text-align:center;margin:.2rem 0;">
        Chinmaya Mission Chicago</div>
    <div style="font-size:.85rem;color:#4A6B54;text-align:center;margin:.1rem 0;">
        Yamunotri Center</div>
    <div style="font-size:.82rem;text-align:center;margin:.3rem 0;">
        <a href="mailto:swamiaparajitananda@gmail.com" style="color:#4A7C59;
        text-decoration:none;">swamiaparajitananda@gmail.com</a>
    </div>
    <div style="text-align:center;margin-top:.6rem;">
        <span class="tag">Bhagavad Gītā</span><span class="tag">Vedānta</span>
        <span class="tag">Bhāgavatam</span><span class="tag">Upaniṣads</span>
    </div>
    """, unsafe_allow_html=True)

with col_intro:
    st.markdown("""
    <div class="bio-card">
        <div class="bio-para">Pūjya <strong>Swāmī Aparājitānandajī</strong> is a profound
        spiritual teacher whose journey from the world of electronics engineering to the
        sacred path of Vedānta is both inspiring and transformative. His life stands as a
        shining example of dedication to the pursuit of intelligent living as envisioned
        by Chinmaya Mission.</div>
        <div class="bio-para">Before embracing the spiritual path, Swamiji was an
        <strong>Electronics and Communication Engineer</strong> who served as a Professor
        at an engineering college in Bengaluru. Guided by a higher calling and inspired
        by the vision of <strong>Pūjya Gurudev Swāmī Chinmayānandajī</strong>, he chose
        to dedicate his life entirely to spiritual study and service.</div>
        <div class="bio-para">In <strong>2005</strong>, he joined the prestigious
        <strong>Sandeepany Sadhanalaya in Mumbai</strong>, immersing himself deeply in the
        scriptures and the traditional Guru–Śiṣya Paramparā.</div>
        <div class="quote-block">"His presence is a source of inspiration,
        his words a source of clarity, and his teachings a source of inner transformation."</div>
        <div class="bio-para">Widely admired for his <strong>powerful oratory, remarkable
        clarity, and extraordinary ability to make even the most subtle Vedāntic concepts
        accessible</strong> — from children's summer camps to advanced spiritual aspirants.</div>
    </div>
    """, unsafe_allow_html=True)

# ── Journey ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Swamiji\'s Journey</div>', unsafe_allow_html=True)

milestones = [
    ("Pre-2005","Electronics and Communication Engineer; Professor at an engineering college in Bengaluru. Inspired by Pūjya Gurudev's vision of intelligent living."),
    ("2005","Joined <em>Sandeepany Sadhanalaya</em>, Mumbai — intensive residential Vedānta course under the traditional Guru–Śiṣya Paramparā."),
    ("2005–18","Served Chinmaya Mission centres across Karnataka — Bengaluru, Mysuru, Shimoga — and nearly a decade at <strong>Chinmaya Mission Mangalore</strong>."),
    ("2018","Initiated into <strong>Sanyāsa</strong> — marking total dedication to a life of renunciation, teaching, and spiritual service."),
    ("2022","Published <em>Indispensable Values</em> — covering 37 values from Bhagavad Gītā Chapters 13 and 16. Primary source for this knowledge base."),
    ("2023–","Serving <strong>Chinmaya Mission Chicago · Yamunotri Center</strong> — visiting 30+ US centres, Winter Vedānta Residential Retreats, Jñāna Yajnas."),
]
for year, text in milestones:
    st.markdown(f"""<div class="milestone">
        <div class="milestone-year">{year}</div>
        <div class="milestone-text">{text}</div>
    </div>""", unsafe_allow_html=True)

# ── Quotes ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="swamiji-quote">
    True happiness shouldn't be <em>because of</em>! True happiness should be <em>in spite of</em>!
    <div class="swamiji-quote-attr">— Swāmī Aparājitānandajī</div>
</div>
<div class="swamiji-quote">
    Remember, in life, the only permanent relationship is our relationship with God.
    All other relationships are impermanent. Our only permanent relationship is with God.
    <div class="swamiji-quote-attr">— Swāmī Aparājitānandajī</div>
</div>
""", unsafe_allow_html=True)

# ── 20 Values ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">The 20 Indispensable Values — Bhagavad Gītā 13.7–11</div>',
            unsafe_allow_html=True)

values_l = [
    ("amānitvam","Humility — absence of pride"),
    ("adambhitvam","Absence of hypocrisy and show-off"),
    ("ahiṃsā","Non-injury in thought, word and deed"),
    ("kṣāntiḥ","Forgiveness and forbearance"),
    ("ārjavam","Simplicity — thought, word, deed in one line"),
    ("ācāryopāsanam","Devotion and service to one's teacher"),
    ("śaucam","Purity of body and mind"),
    ("sthairyam","Steadfastness — never giving up"),
    ("ātmavinigrahaḥ","Self-control over the senses"),
    ("indriyārtheṣu vairāgyam","Dispassion towards sense objects"),
]
values_r = [
    ("anahaṅkāra","Absence of ego — sense of doership"),
    ("janma-mṛtyu darśanam","Seeing sorrow in birth, death, old age, disease"),
    ("asaktiḥ","Non-attachment to people and things"),
    ("anabhiṣvaṅga","Absence of blind attachment to family"),
    ("samacittatvam","Equanimity in pleasant and unpleasant events"),
    ("bhakti avyabhicāriṇī","Unswerving devotion to the Lord"),
    ("viviktadeśa-sevitvam","Love of solitude for spiritual practice"),
    ("aratir janasaṃsadi","Disinterest in worldly gatherings"),
    ("adhyātma-jñāna-nityatvam","Constancy in spiritual knowledge"),
    ("tattva-jñānārtha-darśanam","Seeing liberation as the goal of life"),
]

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="value-section"><div class="value-section-title">Values 1–10</div>',
                unsafe_allow_html=True)
    for name, desc in values_l:
        st.markdown(f"""<div class="value-item">
            <div class="value-bullet">🪷</div>
            <div class="value-text"><span class="value-name">{name}</span> — {desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="value-section"><div class="value-section-title">Values 11–20</div>',
                unsafe_allow_html=True)
    for name, desc in values_r:
        st.markdown(f"""<div class="value-item">
            <div class="value-bullet">🪷</div>
            <div class="value-text"><span class="value-name">{name}</span> — {desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;padding:1.5rem;
    border-top:2px solid #B8D4BC;color:#4A6B54;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.95rem;
    background:linear-gradient(135deg,#EDF3EC,#F8F9F5);border-radius:12px;">
    🪷 &nbsp; Hari Om &nbsp; 🪷 <br>
    <em>We are blessed to have Swāmī Aparājitānandajī's teachings illumine our path.</em>
</div>
""", unsafe_allow_html=True)
