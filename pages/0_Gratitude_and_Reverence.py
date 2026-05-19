"""
pages/0_Gratitude_and_Reverence.py — Wisdom Distiller style with Midnight Saffron.
Single Om inside the title box, all sections centered, larger circular photos.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

st.set_page_config(
    page_title="Gratitude & Reverence | Indispensable Values",
    page_icon="🙏", layout="wide"
)

ASSETS = Path(__file__).parent.parent / "assets" / "images"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#1A0F0A;color:#F5E6C8;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#D4AF37!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#2C1810,#4A2818)!important;border-right:2px solid #D4AF37;}
div[data-testid="stSidebar"] *{color:#F5E6C8!important;font-weight:600!important;}

/* ── Hero — Om inside title box, all centered ── */
.title-box{
    background:linear-gradient(135deg,#2C1810,#3D2418);
    border:2px solid #D4AF37;border-radius:20px;
    padding:2.5rem 2rem 2rem;text-align:center;
    max-width:760px;margin:0 auto 2rem;
    box-shadow:0 4px 24px rgba(0,0,0,.4);
}
.title-om{
    width:75px;height:75px;border-radius:14px;
    object-fit:contain;
    border:2px solid #D4AF37;
    box-shadow:0 4px 16px rgba(212,175,55,.20);
    margin-bottom:1.2rem;
}
.page-title{
    font-family:'Playfair Display',serif;
    font-size:2.4rem;font-weight:800;
    color:#FFD89A;
    margin:.3rem 0;
}
.page-title span{color:#FF8C42;}
.diamonds{color:#D4AF37;font-size:1.2rem;letter-spacing:10px;margin:.8rem 0 0;}

/* ── Centered section labels ── */
.section-label{
    font-family:'Lato',sans-serif;font-size:.75rem;font-weight:700;
    letter-spacing:4px;color:#D4AF37;text-transform:uppercase;
    margin:2rem 0 1rem;text-align:center;
}

/* ── Perfect circular photos — bigger ── */
[data-testid="stImage"] img {
    width:260px!important;
    height:260px!important;
    border-radius:50%!important;
    object-fit:cover!important;
    object-position:top center!important;
    border:5px solid transparent!important;
    background:linear-gradient(#1A0F0A,#1A0F0A) padding-box,
               linear-gradient(135deg,#D4AF37,#FF8C42,#D4AF37,#FFD89A) border-box!important;
    box-shadow:0 8px 30px rgba(255,140,66,.25)!important;
}

/* ── Photo captions — centered ── */
.photo-name{
    font-family:'Playfair Display',serif;font-size:1.35rem;font-weight:700;
    color:#FFD89A;text-align:center;margin:1rem 0 .2rem;
}
.photo-title{
    font-family:'Cormorant Garamond',serif;font-style:italic;color:#FF8C42;
    font-size:1rem;text-align:center;margin-bottom:.3rem;
}
.photo-sub{font-size:.85rem;color:#B8956B;font-style:italic;text-align:center;}

.gold-line{border:none;border-top:1.5px solid #5C3820;
    margin:2rem auto;max-width:500px;}

/* ── Gratitude text box ── */
.gratitude-box{
    background:#2C1810;border:1.5px solid #5C3820;border-left:5px solid #FF8C42;
    border-radius:14px;padding:2rem 2.5rem;margin:1.5rem auto;max-width:760px;
    box-shadow:0 4px 16px rgba(0,0,0,.3);text-align:left;
}
.gratitude-title{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
    color:#FFD89A;margin-bottom:1rem;text-align:center;}
.gratitude-para{color:#F5E6C8;font-size:.95rem;line-height:1.9;margin-bottom:.9rem;}
.gratitude-italic{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.05rem;color:#FFD89A;line-height:1.9;margin-bottom:.9rem;}

/* ── Quotes ── */
.swamiji-quote{background:#2C1810;border-left:5px solid #FF8C42;
    border-radius:0 14px 14px 0;padding:1.3rem 1.8rem;margin:1rem auto;max-width:760px;
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.1rem;font-weight:700;color:#F5E6C8;line-height:1.8;
    box-shadow:0 2px 8px rgba(0,0,0,.3);}
.swamiji-quote-attr{font-family:'Playfair Display',serif;font-style:normal;
    font-size:.95rem;font-weight:700;color:#FF8C42;margin-top:.6rem;}

/* ── Mantra box ── */
.mantra-box{
    background:linear-gradient(135deg,#2C1810,#3D2418);
    border:2px solid #D4AF37;border-radius:14px;
    padding:1.8rem 2rem;margin:1.5rem auto;max-width:760px;text-align:center;
}
.mantra-text{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.2rem;color:#FFD89A;line-height:2.2;font-weight:600;}
.mantra-meaning{color:#C9A961;font-size:.88rem;margin-top:.8rem;font-style:italic;}

/* No blank under images */
[data-testid="stImage"]{margin-bottom:-1rem!important;padding-bottom:0!important;}
</style>
""", unsafe_allow_html=True)

# ── Title Box — single Om + title together, centered ───────────────────────────
st.markdown(f'''
<div class="title-box">
    <img class="title-om" src="data:image/jpeg;base64,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" alt="Om"/>
    <div class="page-title">With <span>Reverence &amp; Gratitude</span></div>
    <div class="diamonds">❖ &nbsp; ❖ &nbsp; ❖</div>
</div>
''', unsafe_allow_html=True)

# ── Opening Mantra ────────────────────────────────────────────────────────────
st.markdown('''<div class="mantra-box">
    <div class="mantra-text">gurur brahmā gurur viṣṇuḥ gurur devo maheśvaraḥ<br>
    guruḥ sākṣāt paraṃ brahma tasmai śrī gurave namaḥ</div>
    <div class="mantra-meaning">The Guru is Brahma, the Guru is Vishnu, the Guru is Shiva.<br>
    The Guru is verily the Supreme Brahman — salutations to that revered Guru.</div>
</div>''', unsafe_allow_html=True)

# ── Gurudev — centered, bigger circle ──────────────────────────────────────────
st.markdown('<div class="section-label">In Devotion &amp; Remembrance</div>',
            unsafe_allow_html=True)

g_path = ASSETS / "swamiji_chinmayananda.jpg"
_, cg, _ = st.columns([1.2, 1, 1.2])
with cg:
    if g_path.exists():
        st.image(str(g_path))
    else:
        st.markdown('<div style="font-size:5rem;text-align:center;">🪷</div>',
                    unsafe_allow_html=True)

st.markdown('''
<div class="photo-name">Pūjya Swāmī Chinmayānandajī</div>
<div class="photo-title">Founder · Chinmaya Mission</div>
<div class="photo-sub">May his eternal light guide all seekers</div>
<hr class="gold-line"/>
''', unsafe_allow_html=True)

# ── Swami Aparajitananda — centered, bigger circle ─────────────────────────────
st.markdown('<div class="section-label">With Deep Gratitude &amp; Humble Pranāms</div>',
            unsafe_allow_html=True)

a_path = ASSETS / "swamiji_aparajitananda.jpg"
_, ca, _ = st.columns([1.2, 1, 1.2])
with ca:
    if a_path.exists():
        st.image(str(a_path))
    else:
        st.markdown('<div style="font-size:4rem;text-align:center;">🙏</div>',
                    unsafe_allow_html=True)

st.markdown('''
<div class="photo-name">Swāmī Aparājitānandajī</div>
<div class="photo-title">Chinmaya Mission</div>
''', unsafe_allow_html=True)

# ── Gratitude Text ────────────────────────────────────────────────────────────
st.markdown('''<div class="gratitude-box">
    <div class="gratitude-title">🙏 Pranāms &amp; Gratitude</div>
    <div class="gratitude-para">With deep reverence and devotion, we offer our humble
    pranāms and heartfelt gratitude to <strong>Pūjya Gurudev Swāmī Chinmayānandajī</strong>,
    whose tireless vision brought the light of Vedanta to millions of seekers across the world.</div>
    <div class="gratitude-para">To <strong>Swāmī Aparājitānandajī</strong>, we offer sincere
    gratitude for his extraordinary ability to unfold the profound truths of Vedānta with
    remarkable clarity and simplicity. His tireless dedication inspires deeper inquiry,
    reflection, and understanding in every seeker.</div>
    <div class="gratitude-italic">This humble initiative is offered as a small sevā at their
    holy feet — so that more seekers may listen (śravaṇa), reflect (manana), and internalise
    these sacred teachings (nididhyāsana) with greater ease, devotion, and depth.</div>
</div>''', unsafe_allow_html=True)

# ── Quotes ────────────────────────────────────────────────────────────────────
st.markdown('''
<div class="swamiji-quote">
    &ldquo;God is not someone who can be seen through the <strong>naked eyes</strong>.
    He is someone who can be known through a <strong>pure heart</strong> —
    experienced in a <strong>pure heart</strong>.&rdquo;
    <div class="swamiji-quote-attr">— Swāmī Aparājitānandajī</div>
</div>
<div class="swamiji-quote">
    &ldquo;A heart filled with <strong>noble emotions</strong> like kindness, compassion, mercy,
    truthfulness, honesty — such a heart is called a <strong>pure heart</strong>.&rdquo;
    <div class="swamiji-quote-attr">— Swāmī Aparājitānandajī</div>
</div>
''', unsafe_allow_html=True)

# ── Closing Mantras ───────────────────────────────────────────────────────────
st.markdown('''<div class="mantra-box">
    <div class="mantra-text">asato mā sadgamaya · tamaso mā jyotirgamaya<br>
    mṛtyor mā amṛtaṃ gamaya · Oṃ śāntiḥ śāntiḥ śāntiḥ</div>
    <div class="mantra-meaning">Lead me from untruth to Truth · From darkness to Light<br>
    From mortality to Immortality · Om Peace Peace Peace</div>
</div>
<div style="text-align:center;margin-top:1rem;color:#FF8C42;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;">
    🪷 &nbsp; Hari Om &nbsp; 🪷
</div>''', unsafe_allow_html=True)
