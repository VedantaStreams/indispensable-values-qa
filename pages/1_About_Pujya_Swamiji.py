"""
pages/1_About_Pujya_Swamiji.py — About page with hero box, centered photo, books, YouTube.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

st.set_page_config(page_title="About Pūjya Swamiji | Indispensable Values",
                   page_icon="📖", layout="wide")

ASSETS = Path(__file__).parent.parent / "assets" / "images"
APARAJITA = ASSETS / "swamiji_aparajitananda.jpg"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#1A3A45;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#0A4A58!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #0A4A58;}
div[data-testid="stSidebar"] *{color:#1A3A45!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#1A7A8C,#2C95A8);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.5rem 1.2rem;}

/* ── Hero — Om in box like other pages ── */
.hero-block{
    background:linear-gradient(135deg,#FFFFFF 0%,#D0EDF1 50%,#A8D8E0 100%);
    border:2px solid #0A4A58;border-radius:20px;
    padding:2.5rem 3rem 2rem;text-align:center;
    margin-bottom:1.5rem;
    box-shadow:0 4px 24px rgba(26,122,140,.20);
    width:100%;
}
.om-box{
    background:linear-gradient(135deg,#FFFFFF,#D0EDF1);
    border:2px solid #0A4A58;border-radius:16px;
    width:90px;height:90px;
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:.8rem;
    box-shadow:0 4px 16px rgba(212,175,55,.20);
}
.om-img{width:70px;height:70px;object-fit:contain;border-radius:10px;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.5rem;font-weight:800;line-height:1.2;color:#0A4A58;margin-bottom:.3rem;}
.hero-title .accent{color:#FF8C42;}
.hero-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:#FF8C42;}

/* ── Centered quote below hero ── */
.intro-quote{
    text-align:center;max-width:780px;margin:.5rem auto 1.8rem;
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.4rem;font-weight:700;color:#0A4A58;line-height:1.7;padding:0 1.5rem;
}
.intro-quote-attr{display:block;font-family:'Playfair Display',serif;font-style:normal;
    font-size:1rem;font-weight:700;color:#FF8C42;margin-top:.7rem;}

/* ── Centered photo block ── */
.photo-wrapper{
    text-align:center;margin:0 auto 1.5rem;
}
.photo-name{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:800;color:#0A4A58;
    text-align:center;margin:1rem 0 .2rem;}
.photo-loc-main{font-family:'Cormorant Garamond',serif;font-style:italic;color:#FF8C42;
    font-size:1.1rem;text-align:center;}
.photo-loc-sub{font-size:.95rem;color:#3A5C68;text-align:center;margin:.1rem 0;}
.photo-email{font-size:.88rem;text-align:center;margin:.4rem 0;}
.photo-email a{color:#FF8C42;text-decoration:none;}
.photo-tag{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.05rem;font-weight:700;color:#0A4A58;text-align:center;margin:.6rem 0;
    padding:.4rem 1rem;background:#FFFFFF;display:inline-block;border-radius:20px;
    border:1.5px solid #0A4A58;}

/* For st.image centered photo */
[data-testid="stImage"] img {
    width:280px!important;
    height:280px!important;
    border-radius:16px!important;
    object-fit:cover!important;
    object-position:top center!important;
    border:5px solid transparent!important;
    background:linear-gradient(#E8F4F6,#E8F4F6) padding-box,
               linear-gradient(135deg,#0A4A58,#1A7A8C,#0A4A58,#0A4A58) border-box!important;
    box-shadow:0 8px 30px rgba(26,122,140,.25)!important;
    margin:0 auto!important;display:block!important;
}
[data-testid="stImage"]{margin-bottom:-.5rem!important;padding-bottom:0!important;
    display:flex!important;justify-content:center!important;}

.bio-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;padding:2rem;
    box-shadow:0 4px 12px rgba(26,122,140,.08);margin-bottom:1.5rem;}
.bio-para{color:#1A3A45;font-size:.97rem;line-height:1.9;margin-bottom:.9rem;}
.bio-para:last-child{margin-bottom:0;}

.quote-block{background:#FFFFFF;border-left:5px solid #1A7A8C;
    border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin:1.2rem 0;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;
    color:#0A4A58;line-height:1.8;}

.swamiji-quote{background:#FFFFFF;border-left:5px solid #1A7A8C;
    border-radius:0 14px 14px 0;padding:1.2rem 1.8rem;margin:1rem 0;
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.1rem;font-weight:700;color:#1A3A45;line-height:1.8;}
.swamiji-quote-attr{font-family:'Playfair Display',serif;font-style:normal;font-size:.95rem;
    font-weight:700;color:#FF8C42;margin-top:.6rem;}

.section-title{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;color:#0A4A58;
    margin:2rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #0A4A58;}

.milestone{display:flex;align-items:flex-start;gap:1rem;background:#FFFFFF;
    border:1.5px solid #88C5D0;border-radius:12px;padding:1.1rem 1.4rem;
    margin-bottom:.8rem;}
.milestone-year{font-family:'Playfair Display',serif;font-size:1rem;font-weight:800;
    color:#FF8C42;min-width:58px;}
.milestone-text{color:#1A3A45;font-size:.92rem;line-height:1.65;}

.value-section{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;padding:1.8rem;
    margin-bottom:1rem;}
.value-section-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
    color:#0A4A58;margin-bottom:.8rem;padding-bottom:.4rem;border-bottom:1.5px solid #88C5D0;}
.value-item{display:flex;align-items:flex-start;margin-bottom:.55rem;}
.value-bullet{color:#FF8C42;font-size:1rem;margin-right:.6rem;flex-shrink:0;}
.value-text{color:#1A3A45;font-size:.9rem;line-height:1.6;}
.value-name{font-weight:700;color:#0A4A58;font-family:'Cormorant Garamond',serif;font-style:italic;}

.yt-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-left:5px solid #CC0000;
    border-radius:10px;padding:1rem 1.4rem;margin-bottom:.8rem;
    display:flex;align-items:center;gap:1rem;}
.yt-icon{font-size:1.8rem;}
.yt-content{flex:1;}
.yt-channel{font-family:'Playfair Display',serif;font-weight:700;color:#0A4A58;font-size:1rem;}
.yt-url a{color:#FF8C42;text-decoration:none;font-size:.85rem;}
.yt-url a:hover{text-decoration:underline;}
</style>
""", unsafe_allow_html=True)

# ── Hero — Om + Title + Subtitle ──────────────────────────────────────────────
st.markdown('''
<div class="hero-block">
    <div class="om-box">
        <img class="om-img" src="data:image/jpeg;base64,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" alt="Om"/>
    </div><br>
    <div class="hero-title">
        About <span class="accent">Pūjya Swamiji</span>
    </div>
    <div class="hero-sub">Swāmī Aparājitānanda · Chinmaya Mission Chicago</div>
</div>
''', unsafe_allow_html=True)

# ── Quote below hero ──────────────────────────────────────────────────────────
st.markdown('''
<div class="intro-quote">
    &ldquo;<strong>True happiness</strong> shouldn't be because of!
    <strong>True happiness</strong> should be in spite of!&rdquo;
    <span class="intro-quote-attr">— Swāmī Aparājitānanda</span>
</div>
''', unsafe_allow_html=True)

# ── Centered Photo + Name + Details ───────────────────────────────────────────
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if APARAJITA.exists():
        st.image(str(APARAJITA))
    else:
        st.markdown('<div style="font-size:5rem;text-align:center;">🙏</div>',
                    unsafe_allow_html=True)
    st.markdown('''
    <div class="photo-name">Swāmī Aparājitānanda</div>
    <div class="photo-loc-main">Chinmaya Mission Chicago</div>
    <div class="photo-loc-sub">Yamunotri Center</div>
    <div class="photo-email">
        <a href="mailto:swamiaparajitananda@gmail.com">swamiaparajitananda@gmail.com</a>
    </div>
    <div style="text-align:center;margin-top:.8rem;">
        <span class="photo-tag">Exponent of Advaita Vedānta</span>
    </div>
    ''', unsafe_allow_html=True)

# ── Bio Card ──────────────────────────────────────────────────────────────────
st.markdown('''
<div class="bio-card">
    <div class="bio-para">Pūjya <strong>Swāmī Aparājitānanda</strong> is a profound
    spiritual teacher whose journey from the world of electronics engineering to the
    sacred path of Vedānta is both inspiring and transformative. His life stands as a
    shining example of dedication to the pursuit of intelligent living as envisioned
    by Chinmaya Mission.</div>
    <div class="bio-para">Before embracing the spiritual path, Swamiji was an
    <strong>Electronics and Communication Engineer</strong> who served as a Professor
    at an engineering college in Bengaluru. Guided by a higher calling and inspired
    by the vision of <strong>Pūjya Gurudev Swāmī Chinmayānanda</strong>, he chose
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
''', unsafe_allow_html=True)

# ── Journey ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Swamiji\'s Journey</div>',
            unsafe_allow_html=True)

milestones = [
    ("Pre-2005","Electronics and Communication Engineer; Professor at an engineering college in Bengaluru."),
    ("2005","Joined <em>Sandeepany Sadhanalaya</em>, Mumbai — intensive residential Vedānta course."),
    ("2005–18","Served Chinmaya Mission centres across Karnataka including <strong>Chinmaya Mission Mangalore</strong>."),
    ("2018","Initiated into <strong>Sanyāsa</strong> — total dedication to renunciation, teaching, and service."),
    ("2022","Published <em>Indispensable Values</em> — 37 values from Bhagavad Gītā Chapters 13 and 16."),
    ("2023–","Serving <strong>Chinmaya Mission Chicago · Yamunotri Center</strong> — visiting 30+ US centres, Vedānta Residential Retreats, Jñāna Yajnas."),
]
for year, txt in milestones:
    st.markdown(f"""<div class="milestone">
        <div class="milestone-year">{year}</div>
        <div class="milestone-text">{txt}</div>
    </div>""", unsafe_allow_html=True)

# ── Two Quotes ────────────────────────────────────────────────────────────────
st.markdown('''
<div class="swamiji-quote">
    &ldquo;Remember, in life, the <strong>only permanent relationship</strong>
    is our relationship with <strong>God</strong>. All other relationships are impermanent.&rdquo;
    <div class="swamiji-quote-attr">— Swāmī Aparājitānanda</div>
</div>
''', unsafe_allow_html=True)

# ── Published Works (corrected years) ─────────────────────────────────────────
st.markdown('<div class="section-title">Published Works (2016–2022)</div>',
            unsafe_allow_html=True)
st.markdown('''
<div class="bio-card">
    <div class="bio-para" style="margin-bottom:.5rem;">
        Pūjya Swāmī Aparājitānanda has authored several books over the years:
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:.8rem;">
        <div style="background:#D0EDF1;border:1.5px solid #88C5D0;border-radius:10px;padding:.8rem 1rem;">
            <div style="font-family:\'Playfair Display\',serif;font-weight:700;color:#0A4A58;font-size:.95rem;">📖 Read Daily, Live Fully</div>
            <div style="font-size:.82rem;color:#3A5C68;margin-top:.2rem;"><strong>2016</strong> · A daily spiritual companion</div>
        </div>
        <div style="background:#D0EDF1;border:1.5px solid #88C5D0;border-radius:10px;padding:.8rem 1rem;">
            <div style="font-family:\'Playfair Display\',serif;font-weight:700;color:#0A4A58;font-size:.95rem;">📖 Gurudev\'s Quotes — Volume I</div>
            <div style="font-size:.82rem;color:#3A5C68;margin-top:.2rem;"><strong>2019</strong> · Selected quotes from Gurudev</div>
        </div>
        <div style="background:#D0EDF1;border:1.5px solid #88C5D0;border-radius:10px;padding:.8rem 1rem;">
            <div style="font-family:\'Playfair Display\',serif;font-weight:700;color:#0A4A58;font-size:.95rem;">📖 Gurudev\'s Quotes — Volume II</div>
            <div style="font-size:.82rem;color:#3A5C68;margin-top:.2rem;"><strong>2021</strong> · Selected quotes from Gurudev</div>
        </div>
        <div style="background:#D0EDF1;border:1.5px solid #88C5D0;border-radius:10px;padding:.8rem 1rem;">
            <div style="font-family:\'Playfair Display\',serif;font-weight:700;color:#0A4A58;font-size:.95rem;">📖 Gurudev\'s Quotes — Volume III</div>
            <div style="font-size:.82rem;color:#3A5C68;margin-top:.2rem;"><strong>2021</strong> · Selected quotes from Gurudev</div>
        </div>
        <div style="background:#D0EDF1;border:1.5px solid #88C5D0;border-radius:10px;padding:.8rem 1rem;grid-column:1/-1;border-left:5px solid #0A4A58;">
            <div style="font-family:\'Playfair Display\',serif;font-weight:700;color:#0A4A58;font-size:1.05rem;">📖 Indispensable Values</div>
            <div style="font-size:.85rem;color:#3A5C68;margin-top:.2rem;"><strong>2022</strong> · Central Chinmaya Mission Trust · 37 values from Bhagavad Gītā Chapters 13 &amp; 16</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# ── YouTube Channels ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">YouTube Channels</div>', unsafe_allow_html=True)
st.markdown('''
<div class="yt-card">
    <div class="yt-icon">📺</div>
    <div class="yt-content">
        <div class="yt-channel">Vedanta Madhuryam</div>
        <div class="yt-url"><a href="https://www.youtube.com/@vedantamadhuryam" target="_blank">https://www.youtube.com/@vedantamadhuryam</a></div>
    </div>
</div>
<div class="yt-card">
    <div class="yt-icon">📺</div>
    <div class="yt-content">
        <div class="yt-channel">Chinmaya Mission Yamunotri</div>
        <div class="yt-url"><a href="https://www.youtube.com/@ChinmayaMissionYamunotri" target="_blank">https://www.youtube.com/@ChinmayaMissionYamunotri</a></div>
    </div>
</div>
''', unsafe_allow_html=True)

# ── 20 Values ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">The 20 Indispensable Values — Bhagavad Gītā 13.7–11</div>',
            unsafe_allow_html=True)

values_l = [
    ("amānitvam","Humility — absence of pride"),
    ("adambhitvam","Absence of hypocrisy and show-off"),
    ("ahiṃsā","Non-injury in thought, word and deed"),
    ("kṣāntiḥ","Forgiveness and forbearance"),
    ("ārjavam","Simplicity"),
    ("ācāryopāsanam","Devotion and service to one\'s teacher"),
    ("śaucam","Purity of body and mind"),
    ("sthairyam","Steadfastness"),
    ("ātmavinigrahaḥ","Self-control over the senses"),
    ("indriyārtheṣu vairāgyam","Dispassion towards sense objects"),
]
values_r = [
    ("anahaṅkāra","Absence of ego"),
    ("janma-mṛtyu darśanam","Seeing sorrow in birth, death, old age, disease"),
    ("asaktiḥ","Non-attachment to people and things"),
    ("anabhiṣvaṅga","Absence of blind attachment to family"),
    ("samacittatvam","Equanimity"),
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
