import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import random
import sys
from pathlib import Path
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_page_quote

st.set_page_config(
    page_title="Kids Corner | Indispensable Values",
    page_icon="🌱",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@400;700;900&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap');

.kids-header{background:linear-gradient(135deg,#FFFFFF 0%,#D0EDF1 50%,#FFFFFF 100%);
    border:2px solid #88C5D0;border-radius:20px;padding:2rem 2.5rem;
    text-align:center;margin-bottom:1.5rem;box-shadow:0 4px 20px rgba(0,0,0,.08);}
.kids-header-title{font-family:'Playfair Display',serif;font-size:2.4rem;
    font-weight:800;color:#062E3A;margin-bottom:.3rem;}
.kids-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.1rem;color:#0D5C6B;}

.activity-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;
    padding:1.4rem 1.6rem;margin-bottom:1rem;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.activity-title{font-family:'Playfair Display',serif;font-size:1.15rem;
    font-weight:700;color:#062E3A;margin-bottom:.6rem;}

.quiz-question{font-family:'Lato',sans-serif;font-size:1rem;font-weight:700;
    color:#062E3A;margin-bottom:.8rem;line-height:1.6;}
.quiz-correct{background:#D4EDDA;border:1.5px solid #28A745;border-radius:10px;
    padding:.6rem 1rem;color:#155724;font-weight:700;margin:.3rem 0;}
.quiz-wrong{background:#F8D7DA;border:1.5px solid #DC3545;border-radius:10px;
    padding:.6rem 1rem;color:#721C24;font-weight:700;margin:.3rem 0;}
.quiz-score{background:linear-gradient(135deg,#D0EDF1,#FFFFFF);
    border:2px solid #1A7A8C;border-radius:14px;padding:1.2rem 1.8rem;
    text-align:center;font-family:'Playfair Display',serif;font-size:1.3rem;
    font-weight:800;color:#062E3A;margin-top:1rem;}

.word-grid{font-family:'Lato',sans-serif;font-size:1rem;font-weight:700;
    letter-spacing:.15rem;line-height:2;color:#062E3A;
    background:#F0FAFC;border:1.5px solid #88C5D0;border-radius:10px;
    padding:1rem 1.5rem;display:inline-block;}
.word-list{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.8rem;}
.word-badge{background:#D0EDF1;border:1.5px solid #062E3A;color:#062E3A;
    border-radius:20px;padding:.3rem .9rem;font-size:.88rem;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:700;}

.match-item{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:10px;
    padding:.6rem 1rem;margin:.3rem 0;font-size:.92rem;color:#062E3A;
    font-family:'Lato',sans-serif;}
.match-correct{border-color:#28A745;background:#D4EDDA;color:#155724;}
.match-wrong{border-color:#DC3545;background:#F8D7DA;color:#721C24;}

.stButton>button{background:linear-gradient(135deg,#FFFFFF,#D0EDF1)!important;
    color:#062E3A!important;border:1.5px solid #062E3A!important;
    border-radius:10px!important;font-weight:600!important;
    font-family:'Lato',sans-serif!important;transition:all .2s!important;}
.stButton>button:hover{background:linear-gradient(135deg,#0D5C6B,#2C95A8)!important;
    color:white!important;transform:translateY(-1px)!important;}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kids-header">
    <div class="kids-header-title">🌱 Kids Corner</div>
    <div class="kids-header-sub">
        Explore the Indispensable Values through quizzes, puzzles and games
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
for key in ["quiz_started", "quiz_answers", "quiz_submitted",
            "match_selections", "match_submitted", "ws_found"]:
    if key not in st.session_state:
        if key in ["quiz_answers", "match_selections", "ws_found"]:
            st.session_state[key] = {}
        else:
            st.session_state[key] = False

# Seed for random question selection per age group
for age in ["6-10", "10-14", "14-18"]:
    seed_key = f"quiz_seed_{age}"
    if seed_key not in st.session_state:
        st.session_state[seed_key] = random.randint(0, 9999)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── QUIZ DATA ──────────────────────────────────────────────────────────────────
QUIZZES = {
    "6-10": [
        {"q": "Ahiṃsā means which of the following?",
         "opts": ["Hurting others", "Not hurting anyone", "Being angry", "Telling lies"],
         "ans": "Not hurting anyone",
         "explain": "Ahiṃsā means not hurting any living being — in thoughts, words, or actions! 🌸"},
        {"q": "Amānitvam means which of the following?",
         "opts": ["Boasting a lot", "Not asking for praise or showing off", "Being loud", "Being greedy"],
         "ans": "Not asking for praise or showing off",
         "explain": "Amānitvam means humility — not demanding that others praise or admire you. It is one of the most beautiful values! 🪷"},
        {"q": "Satyam means which of the following?",
         "opts": ["Telling the truth", "Eating sweets", "Playing games", "Being lazy"],
         "ans": "Telling the truth",
         "explain": "Satyam means truthfulness — always saying what is true! ✨"},
        {"q": "Dayā bhūteṣu means which of the following?",
         "opts": ["Being unkind", "Being kind and compassionate to everyone", "Being greedy", "Being proud"],
         "ans": "Being kind and compassionate to everyone",
         "explain": "Dayā bhūteṣu means compassion towards all beings — feeling love and care for everyone around us! 💕"},
        {"q": "Ācāryopāsanam means which of the following?",
         "opts": ["Ignoring your teacher", "Loving and serving your teacher with gratitude", "Arguing with elders", "Sleeping in class"],
         "ans": "Loving and serving your teacher with gratitude",
         "explain": "Ācāryopāsanam means devotion to the teacher — feeling deep gratitude for those who teach us! 🙏"},
        {"q": "Śaucam means which of the following?",
         "opts": ["Being messy", "Being clean and pure inside and outside", "Being loud", "Being sleepy"],
         "ans": "Being clean and pure inside and outside",
         "explain": "Śaucam means purity — keeping our body, words and thoughts clean and good! 🌼"},
        {"q": "Akrodhaḥ means which of the following?",
         "opts": ["Getting angry easily", "Staying calm and free from anger", "Being greedy", "Being proud"],
         "ans": "Staying calm and free from anger",
         "explain": "Akrodhaḥ means freedom from anger — choosing to stay calm even when things upset us! 🧘"},
        {"q": "Dānam means which of the following?",
         "opts": ["Taking from others", "Giving to others with a happy heart", "Eating a lot", "Sleeping late"],
         "ans": "Giving to others with a happy heart",
         "explain": "Dānam means giving — sharing what we have with others freely and joyfully! 🌸"},
        {"q": "Abhayam means which of the following?",
         "opts": ["Being scared of everything", "Being brave and fearless", "Being angry", "Being sad"],
         "ans": "Being brave and fearless",
         "explain": "Abhayam means fearlessness — facing life with courage and trust! 🦁"},
        {"q": "Adambhitvam means which of the following?",
         "opts": ["Pretending to be good when you are not", "Being genuine and not showing off", "Being lazy", "Telling lies"],
         "ans": "Being genuine and not showing off",
         "explain": "Adambhitvam means no hypocrisy — being real, not pretending to be better than you are! 🌿"},
        {"q": "Kṣamā means which of the following?",
         "opts": ["Getting revenge", "Forgiving others", "Being greedy", "Being proud"],
         "ans": "Forgiving others",
         "explain": "Kṣamā means forgiveness — letting go of hurt and choosing peace instead! 🕊️"},
        {"q": "Śāntiḥ means which of the following?",
         "opts": ["Feeling noisy inside", "Feeling peaceful and calm inside", "Feeling angry", "Feeling sad"],
         "ans": "Feeling peaceful and calm inside",
         "explain": "Śāntiḥ means inner peace — a quiet, happy feeling inside that does not go away easily! 🕊️"},
        {"q": "Svādhyāyaḥ means which of the following?",
         "opts": ["Avoiding books", "Studying and learning with love every day", "Watching television all day", "Being lazy"],
         "ans": "Studying and learning with love every day",
         "explain": "Svādhyāyaḥ means self-study — reading, learning and nourishing the mind with good knowledge every day! 📖"},
        {"q": "Mārdavam means which of the following?",
         "opts": ["Being harsh and rough", "Being gentle and soft with others", "Being greedy", "Being loud"],
         "ans": "Being gentle and soft with others",
         "explain": "Mārdavam means gentleness — speaking and acting softly, with kindness and care for others! 🌸"},
        {"q": "Tapas means which of the following?",
         "opts": ["Eating spicy food", "Working hard and staying disciplined", "Playing all day", "Being lazy"],
         "ans": "Working hard and staying disciplined",
         "explain": "Tapas means austerity — doing the hard work needed to grow and become our best selves! 🔥"},
        {"q": "Asaktiḥ means which of the following?",
         "opts": ["Clinging tightly to things", "Not being too attached to people or things", "Being greedy", "Being proud"],
         "ans": "Not being too attached to people or things",
         "explain": "Asaktiḥ means non-attachment — loving people without clinging to them or being possessive! 🌿"},
        {"q": "Tejaḥ means which of the following?",
         "opts": ["Being dull and dim", "Shining with energy, confidence and goodness", "Being scared", "Being lazy"],
         "ans": "Shining with energy, confidence and goodness",
         "explain": "Tejaḥ means vigour and radiance — shining brightly with energy and goodness! ✨"},
        {"q": "Aloluptvam means which of the following?",
         "opts": ["Always wanting more and more", "Being happy with what you have and not being greedy", "Being angry", "Being proud"],
         "ans": "Being happy with what you have and not being greedy",
         "explain": "Aloluptvam means non-greediness — feeling content and not always wanting more! 🌼"},
        {"q": "Dhṛtiḥ means which of the following?",
         "opts": ["Giving up when things get hard", "Staying strong and not giving up", "Being greedy", "Being angry"],
         "ans": "Staying strong and not giving up",
         "explain": "Dhṛtiḥ means fortitude — staying committed and strong even when life feels difficult! 💎"},
        {"q": "Nātimānitā means which of the following?",
         "opts": ["Demanding a lot of respect from everyone", "Not expecting too much praise or importance", "Being greedy", "Being angry"],
         "ans": "Not expecting too much praise or importance",
         "explain": "Nātimānitā means absence of excessive pride — not demanding that everyone treats you as special. This goes hand in hand with humility! 🪷"},
    ],
    "10-14": [
        {"q": "Amānitvam and adambhitvam are both values about humility. What is the difference between them?",
         "opts": ["They mean exactly the same thing",
                  "Amānitvam is about not demanding respect; adambhitvam is about not pretending or showing off",
                  "Amānitvam is about anger; adambhitvam is about greed",
                  "They are from different chapters"],
         "ans": "Amānitvam is about not demanding respect; adambhitvam is about not pretending or showing off",
         "explain": "Together they build authentic humility — not craving admiration (amānitvam) and not faking goodness (adambhitvam)! 🪷"},
        {"q": "Ācāryopāsanam is a value about gratitude. What does it specifically mean?",
         "opts": ["Ignoring teachers", "Devotion and service to one's teacher with gratitude",
                  "Studying alone without a teacher", "Memorising scripture"],
         "ans": "Devotion and service to one's teacher with gratitude",
         "explain": "Ācāryopāsanam means the teacher is not just respected — they are served with love and deep gratitude, because they open the door to wisdom! 🙏"},
        {"q": "Abhayam is the first of the 26 values in BG Ch.16. Why is fearlessness so important?",
         "opts": ["It makes you physically strong",
                  "Without fearlessness you cannot inquire honestly or surrender to truth",
                  "It is the easiest value to practise",
                  "It was Arjuna's special quality"],
         "ans": "Without fearlessness you cannot inquire honestly or surrender to truth",
         "explain": "Abhayam is listed first because fear blocks everything — honest inquiry, devotion, and surrender all require a fearless heart! 🦁"},
        {"q": "Ahiṃsā appears in both BG Ch.13 and Ch.16. In which chapter is it described as a condition for Self-knowledge?",
         "opts": ["Ch.16 only", "Ch.13 only", "Neither chapter", "Both chapters describe it identically"],
         "ans": "Ch.13 only",
         "explain": "In Ch.13, ahiṃsā is among the jñāna sādhana values — prerequisites for Self-knowledge. In Ch.16 it belongs to the daivī sampat — divine qualities! ✨"},
        {"q": "Svādhyāyaḥ means self-study. Which chapter of the Bhagavad Gītā lists it as a value?",
         "opts": ["Ch.13 only", "Ch.16 only", "Both Ch.13 and Ch.16", "Neither chapter"],
         "ans": "Ch.16 only",
         "explain": "Svādhyāyaḥ is one of the 26 daivī sampat values in BG 16.01 — daily scriptural study nourishes the mind and keeps it oriented toward truth! 📖"},
        {"q": "Dayā bhūteṣu means compassion to all beings. Which chapter lists it?",
         "opts": ["Ch.13", "Ch.16", "Both", "Neither"],
         "ans": "Ch.16",
         "explain": "Dayā bhūteṣu is one of the 26 daivī sampat values in BG 16.02 — feeling genuine compassion for the suffering of all living beings! 💕"},
        {"q": "Kṣamā means forgiveness. Which chapter lists it?",
         "opts": ["Ch.13", "Ch.16", "Both", "Neither"],
         "ans": "Ch.16",
         "explain": "Kṣamā is among the six values of BG 16.03 — forgiveness is a divine quality that frees both the one who forgives and the one forgiven! 🕊️"},
        {"q": "Asaktiḥ and anabhiṣvaṅga both deal with detachment. What is the difference?",
         "opts": ["They mean the same thing",
                  "Asaktiḥ is general non-attachment; anabhiṣvaṅga is specifically about family attachment",
                  "Asaktiḥ is from Ch.16; anabhiṣvaṅga is from Ch.13",
                  "Anabhiṣvaṅga is about material wealth"],
         "ans": "Asaktiḥ is general non-attachment; anabhiṣvaṅga is specifically about family attachment",
         "explain": "Both are from Ch.13 — together they teach us to love our family deeply without clinging possessively to them! 🌸"},
        {"q": "Tattva-jñānārtha-darśanam is the 20th value in Ch.13. What does it mean?",
         "opts": ["Daily ritual worship", "Seeing liberation as the ultimate goal of life",
                  "Memorising Sanskrit", "Physical austerity"],
         "ans": "Seeing liberation as the ultimate goal of life",
         "explain": "This value orients everything — it asks us to see mokṣa (liberation) as the true purpose of human life, not just worldly success! 🪷"},
        {"q": "Damaḥ and indriyārtheṣu vairāgyam both deal with the senses. What is the key difference?",
         "opts": ["They are the same",
                  "Damaḥ is outer restraint of the senses; vairāgyam is inner dispassion toward sense objects",
                  "Damaḥ is from Ch.16; vairāgyam is from Ch.13",
                  "Vairāgyam is physical exercise"],
         "ans": "Damaḥ is outer restraint of the senses; vairāgyam is inner dispassion toward sense objects",
         "explain": "Damaḥ (Ch.16) restrains the senses through will; vairāgyam (Ch.13) is the deeper inner dispassion that makes restraint effortless! 🧘"},
        {"q": "Nātimānitā is the 26th and last of the Ch.16 values. What does it mean?",
         "opts": ["Demanding great honour and respect",
                  "Absence of excessive pride — not demanding more honour than is due",
                  "Complete self-degradation",
                  "Silence in all situations"],
         "ans": "Absence of excessive pride — not demanding more honour than is due",
         "explain": "Nātimānitā completes the 26 divine values — humility in how we carry ourselves, without ego or false modesty! 🪷"},
        {"q": "Śaucam appears in both Ch.13 and Ch.16. What does it mean?",
         "opts": ["Only outer physical cleanliness",
                  "Purity of body and mind — inner and outer cleanliness",
                  "Ritual bathing only",
                  "Vegetarian diet"],
         "ans": "Purity of body and mind — inner and outer cleanliness",
         "explain": "Śaucam covers both — a clean body and a clean mind, free of impure thoughts, jealousy and ill-will! 🌼"},
        {"q": "Tapas is listed in Ch.16. Which of the following best describes it?",
         "opts": ["Eating spicy food", "Self-discipline and austerity in body, speech and mind",
                  "Physical punishment", "Fasting from water"],
         "ans": "Self-discipline and austerity in body, speech and mind",
         "explain": "Tapas means choosing discomfort over comfort in order to grow — disciplining our body, speech and mind toward higher values! 🔥"},
        {"q": "Apaiśunam is one of the Ch.16 values. What does it mean?",
         "opts": ["Speaking harshly", "Absence of fault-finding and not speaking ill of others",
                  "Loud recitation of prayers", "Isolation from society"],
         "ans": "Absence of fault-finding and not speaking ill of others",
         "explain": "Apaiśunam means non-slander — refraining from gossip, criticism and backbiting. Our words should build up, not tear down! 🌿"},
        {"q": "Bhakti avyabhicāriṇī is described as 'unswerving devotion'. What makes devotion swerve?",
         "opts": ["Too much study",
                  "Mixing devotion with desire for worldly results",
                  "Attending too many temples",
                  "Chanting too loudly"],
         "ans": "Mixing devotion with desire for worldly results",
         "explain": "Avyabhicāriṇī means undivided — devotion that is pure and unconditional, not bargaining with God for outcomes! 🙏"},
        {"q": "Viviktadeśa-sevitvam is a Ch.13 value. What does it promote?",
         "opts": ["Living in a busy city",
                  "Seeking solitude and quiet places for spiritual practice",
                  "Attending large social gatherings",
                  "Loud communal worship"],
         "ans": "Seeking solitude and quiet places for spiritual practice",
         "explain": "The mind needs quietness to turn inward — this value asks us to value solitude as a friend, not a punishment! 🌿"},
        {"q": "Tyāgaḥ is listed in Ch.16. What does it mean?",
         "opts": ["Accumulating wealth", "Renunciation — giving up selfish attachment to results",
                  "Loud generosity", "Physical austerity only"],
         "ans": "Renunciation — giving up selfish attachment to results",
         "explain": "Tyāgaḥ means letting go — acting rightly without clinging to what we get in return! 🙏"},
        {"q": "Samacittatvam is a Ch.13 value. In what situations must we maintain equanimity?",
         "opts": ["Only during meditation",
                  "In pleasure and pain, success and failure equally",
                  "Only during hardship",
                  "Only during worship"],
         "ans": "In pleasure and pain, success and failure equally",
         "explain": "Samacittatvam is evenness of mind in all circumstances — not swinging between highs and lows but remaining steady! 🧘"},
        {"q": "Adhyātma-jñāna-nityatvam is a Ch.13 value. What does nityatvam mean here?",
         "opts": ["Occasional reading", "Constancy — unbroken daily orientation toward Self-knowledge",
                  "Memorisation only", "Physical discipline"],
         "ans": "Constancy — unbroken daily orientation toward Self-knowledge",
         "explain": "Nityatvam means perpetual — our pursuit of Self-knowledge should be an unbroken daily commitment, not occasional! 📖"},
        {"q": "Dānam is listed in Ch.16. How is it different from ordinary giving?",
         "opts": ["It is giving only to temples",
                  "It is giving without expectation of return — purely out of love and gratitude",
                  "It is giving only money",
                  "It is giving only to family"],
         "ans": "It is giving without expectation of return — purely out of love and gratitude",
         "explain": "Dānam in BG 16.01 is the highest form of giving — an expression of gratitude and love, not a transaction! 🌸"},
    ],
    "14-18": [
        {"q": "Amānitvam is listed first among the 20 jñāna sādhana values of BG 13.7. Why does humility precede all other values?",
         "opts": ["It is the easiest value to practise",
                  "Pride is the primary veil over the intellect — without humility, no genuine inquiry or learning is possible",
                  "It was Arjuna's special strength",
                  "It is alphabetically first in Sanskrit"],
         "ans": "Pride is the primary veil over the intellect — without humility, no genuine inquiry or learning is possible",
         "explain": "In Vedānta, the ego (ahaṅkāra) is the fundamental obstacle to Self-knowledge. Amānitvam dissolves the arrogance that says 'I already know' — the prerequisite of all learning! 🪷"},
        {"q": "Ācāryopāsanam is listed among the 20 jñāna values of BG Ch.13. Why is the guru-śiṣya relationship described as indispensable for Self-knowledge?",
         "opts": ["Teachers can grant mokṣa directly",
                  "Vedāntic knowledge is not mere information — it requires a realised teacher to guide the student past the limitations of the conditioned mind",
                  "It is a social tradition only",
                  "Books alone are sufficient for realisation"],
         "ans": "Vedāntic knowledge is not mere information — it requires a realised teacher to guide the student past the limitations of the conditioned mind",
         "explain": "The guru does not just transmit information — they transmit a living understanding that cannot be captured in books. Gratitude and service to the teacher (ācāryopāsanam) keeps this channel open! 🙏"},
        {"q": "Adambhitvam (BG 13.7) and amānitvam both address humility. How do they differ functionally?",
         "opts": ["They are synonyms",
                  "Amānitvam addresses how we receive honour; adambhitvam addresses how we present ourselves to others",
                  "Adambhitvam is from Ch.16",
                  "Amānitvam deals with anger; adambhitvam deals with greed"],
         "ans": "Amānitvam addresses how we receive honour; adambhitvam addresses how we present ourselves to others",
         "explain": "Together they cover both dimensions of ego — the inward craving for respect (amānitvam) and the outward performance of false virtue (adambhitvam)! 🌿"},
        {"q": "Abhayam opens the list of 26 daivī sampat values in BG 16.01. What specific kind of fear is being addressed?",
         "opts": ["Fear of physical danger only",
                  "The existential fear of loss, death and the unknown that drives all ego-protective behaviour",
                  "Fear of snakes and animals",
                  "Fear of public speaking"],
         "ans": "The existential fear of loss, death and the unknown that drives all ego-protective behaviour",
         "explain": "Abhayam addresses the root fear — the fear of annihilation of the ego-self. All spiritual progress requires facing this fear with trust in the Lord and clarity from Vedānta! 🦁"},
        {"q": "Ahiṃsā appears in both BG 13.7 and BG 16.02. What is the conceptual difference in its placement?",
         "opts": ["No difference — the same meaning in both",
                  "In Ch.13 it is a prerequisite for jñāna; in Ch.16 it is a fruit of daivī nature — the same value seen from different angles",
                  "Ch.16 ahiṃsā is physical only",
                  "Ch.13 ahiṃsā applies only to brahmins"],
         "ans": "In Ch.13 it is a prerequisite for jñāna; in Ch.16 it is a fruit of daivī nature — the same value seen from different angles",
         "explain": "The same value plays two roles — as a condition for inquiry (Ch.13) and as evidence of a purified character (Ch.16). This dual presence shows ahiṃsā's centrality in Kṛṣṇa's teaching! ✨"},
        {"q": "Sattva-saṁśuddhiḥ (BG 16.01) means purification of one's being. What does this purification specifically target?",
         "opts": ["Physical body only",
                  "The entire configuration of one's character — thoughts, motivations, emotions and habitual responses",
                  "Dietary choices only",
                  "Speech only"],
         "ans": "The entire configuration of one's character — thoughts, motivations, emotions and habitual responses",
         "explain": "Sattva-saṁśuddhiḥ is holistic inner purification — not surface behaviour but the deep patterns of the mind that determine how we actually respond to life! 🌼"},
        {"q": "Jñāna-yoga-vyavasthitiḥ (BG 16.01) describes steadfastness in both knowledge and yoga. Why must both be held together?",
         "opts": ["They can be practised separately",
                  "Knowledge without practice remains theoretical; practice without knowledge lacks direction — both together lead to realisation",
                  "Yoga here means only physical postures",
                  "Jñāna is for monks; yoga is for householders"],
         "ans": "Knowledge without practice remains theoretical; practice without knowledge lacks direction — both together lead to realisation",
         "explain": "This value captures the Vedāntic insistence on both śravaṇa-manana (study) and nididhyāsana (contemplative practice) — neither alone is sufficient! 🧘"},
        {"q": "Tattva-jñānārtha-darśanam is the culminating 20th value of BG Ch.13. What does it add that the previous 19 values do not?",
         "opts": ["A new spiritual practice",
                  "It orients all the preceding values — they are only meaningful when aimed at liberation as the ultimate goal",
                  "It is a repetition of svādhyāyaḥ",
                  "It applies only at the end of life"],
         "ans": "It orients all the preceding values — they are only meaningful when aimed at liberation as the ultimate goal",
         "explain": "Without this final value, the other 19 could be practised for social approval or worldly success. Tattva-jñānārtha-darśanam ensures they are all in service of mokṣa! 🪷"},
        {"q": "Nātimānitā is the 26th and final value of BG Ch.16. What is its relationship to amānitvam in Ch.13?",
         "opts": ["They are unrelated",
                  "Both address the same root — ego-inflation — but amānitvam is a prerequisite for knowledge while nātimānitā is the fruit of a purified daivī character",
                  "Nātimānitā is stronger than amānitvam",
                  "Amānitvam is for monks; nātimānitā is for householders"],
         "ans": "Both address the same root — ego-inflation — but amānitvam is a prerequisite for knowledge while nātimānitā is the fruit of a purified daivī character",
         "explain": "The Gītā bookends its value teaching with humility — first as a condition (Ch.13) and finally as a fruit (Ch.16). Ego-dissolution is both the starting point and the destination! 🪷"},
        {"q": "Dānam (BG 16.01) is listed alongside yajñaḥ and svādhyāyaḥ. What do these three share?",
         "opts": ["They all involve physical effort",
                  "They are all outward expressions of gratitude — giving, worship and study are all ways of acknowledging what we have received",
                  "They are only for wealthy people",
                  "They are optional for advanced seekers"],
         "ans": "They are all outward expressions of gratitude — giving, worship and study are all ways of acknowledging what we have received",
         "explain": "Dānam (giving), yajñaḥ (worship) and svādhyāyaḥ (study) together express gratitude to society, the divine and the tradition of knowledge respectively! 🙏"},
        {"q": "Indriyārtheṣu vairāgyam (BG 13.8) and damaḥ (BG 16.01) both relate to the senses. Philosophically, which is deeper and why?",
         "opts": ["Damaḥ is deeper because it involves more effort",
                  "Vairāgyam is deeper — it is the inner dispassion from which damaḥ flows naturally, rather than restraint through willpower alone",
                  "They are equally deep",
                  "Damaḥ is from a later chapter so it is more advanced"],
         "ans": "Vairāgyam is deeper — it is the inner dispassion from which damaḥ flows naturally, rather than restraint through willpower alone",
         "explain": "Willpower-based restraint (damaḥ) is necessary but effortful. When vairāgyam matures — genuine dispassion — the senses naturally lose their pull. The Gītā values both but points toward the deeper! 🧘"},
        {"q": "Apaiśunam (BG 16.02) means non-slander. How does this value protect the spiritual community?",
         "opts": ["It keeps conversations polite superficially",
                  "Fault-finding and gossip fracture the trust and mutual respect that spiritual community depends on — apaiśunam protects this sacred space",
                  "It applies only to speech about teachers",
                  "It means total silence"],
         "ans": "Fault-finding and gossip fracture the trust and mutual respect that spiritual community depends on — apaiśunam protects this sacred space",
         "explain": "In Vedānta, satsaṅg (company of seekers) is precious. Apaiśunam protects this environment by ensuring we speak of others' faults only when genuinely necessary — never casually or maliciously! 🌿"},
        {"q": "Bhakti avyabhicāriṇī (BG 13.10) is specifically described as unswerving. What causes devotion to swerve?",
         "opts": ["Too much scriptural study",
                  "Desire contamination — when devotion is mixed with personal agendas or worldly desires, it loses its purity and power",
                  "Insufficient temple attendance",
                  "Excessive fasting"],
         "ans": "Desire contamination — when devotion is mixed with personal agendas or worldly desires, it loses its purity and power",
         "explain": "Avyabhicāriṇī means non-adulterated — devotion that is not transactional. When we love the Lord without agenda, the heart purifies itself naturally! 🙏"},
        {"q": "Asaktiḥ (BG 13.9) and anabhiṣvaṅga (BG 13.9) both address detachment. Why does the Gītā need two separate values for this?",
         "opts": ["It is repetition for emphasis",
                  "Asaktiḥ addresses the broad tendency to cling to anything; anabhiṣvaṅga specifically targets family attachment — the hardest arena for most seekers",
                  "They apply to different castes",
                  "Anabhiṣvaṅga is from Ch.16"],
         "ans": "Asaktiḥ addresses the broad tendency to cling to anything; anabhiṣvaṅga specifically targets family attachment — the hardest arena for most seekers",
         "explain": "The Gītā is practical — it knows family attachment is the last and most tenacious attachment for most people. Anabhiṣvaṅga names it specifically so we cannot pretend we are non-attached while clinging to our children! 🌸"},
        {"q": "Samacittatvam (BG 13.9) asks for equanimity in iṣṭa-aniṣṭa — pleasant and unpleasant events. How is this different from indifference?",
         "opts": ["They are the same — equanimity means not caring",
                  "Equanimity means remaining centred in one's values regardless of outer events — full engagement with life, undisturbed by its fluctuations",
                  "It means suppressing emotions",
                  "It applies only during meditation"],
         "ans": "Equanimity means remaining centred in one's values regardless of outer events — full engagement with life, undisturbed by its fluctuations",
         "explain": "Samacittatvam is not emotional flatness — it is the stability of someone whose identity is not dependent on outer circumstances. They laugh, grieve and care — but are not destabilised! 🧘"},
        {"q": "Viviktadeśa-sevitvam (BG 13.10) means love of solitude. How does this value interact with dayā bhūteṣu (compassion)?",
         "opts": ["They contradict each other — solitude means avoiding people",
                  "Solitude replenishes the inner resources from which genuine compassion flows — without inner quietness, service becomes burnout",
                  "They apply to different seekers",
                  "Viviktadeśa-sevitvam applies only to monks"],
         "ans": "Solitude replenishes the inner resources from which genuine compassion flows — without inner quietness, service becomes burnout",
         "explain": "The Gītā is holistic — it knows that genuine compassion (dayā bhūteṣu) requires an inner depth that only solitude and contemplation can develop. Outer service and inner stillness support each other! 🌿"},
        {"q": "Śaucam appears in both BG 13.7 and BG 16.03. What does its presence in both chapters suggest?",
         "opts": ["It is a mistake or repetition",
                  "Purity is foundational to both the pursuit of knowledge (Ch.13) and the expression of divine character (Ch.16) — it pervades the entire spiritual life",
                  "The two śaucams have entirely different meanings",
                  "Ch.16 śaucam is physical only"],
         "ans": "Purity is foundational to both the pursuit of knowledge (Ch.13) and the expression of divine character (Ch.16) — it pervades the entire spiritual life",
         "explain": "By placing śaucam in both lists, Kṛṣṇa signals that purity is not one value among many — it is a thread running through all of spiritual life, from the first step to the last! 🌼"},
        {"q": "Adhyātma-jñāna-nityatvam (BG 13.11) uses the word nityatvam — constancy. Why is constancy specifically emphasised over intensity?",
         "opts": ["Intensity is more important than constancy",
                  "Sporadic intense practice cannot build the deep mental grooves (saṃskāras) that steady daily orientation creates — constancy transforms character",
                  "Nityatvam means doing one practice only",
                  "Intensity and constancy are the same"],
         "ans": "Sporadic intense practice cannot build the deep mental grooves (saṃskāras) that steady daily orientation creates — constancy transforms character",
         "explain": "A river carves a canyon not through occasional floods but through steady daily flow. Nityatvam captures this wisdom — unbroken daily orientation is what reshapes the mind! 📖"},
        {"q": "Janma-mṛtyu-jarā-vyādhi-duḥkha-doṣānudarśanam (BG 13.8) asks us to see sorrow in birth, death, old age and disease. How does this lead to liberation rather than despair?",
         "opts": ["It leads to despair and is meant to motivate renunciation by fear",
                  "Seeing the inherent duḥkha of saṃsāra turns the seeking impulse toward the only permanent solution — Self-knowledge — rather than endlessly rearranging temporary comforts",
                  "It is only for elderly people to contemplate",
                  "It means avoiding hospitals and funerals"],
         "ans": "Seeing the inherent duḥkha of saṃsāra turns the seeking impulse toward the only permanent solution — Self-knowledge — rather than endlessly rearranging temporary comforts",
         "explain": "This is the Vedāntic parallel to the Buddha's first noble truth — clear seeing of impermanence is not pessimism but the beginning of wisdom. It redirects our energy toward mokṣa! 🧘"},
        {"q": "Anahaṅkāra (BG 13.8) means absence of ego. In Vedānta, what exactly is the ahaṅkāra and why must it be transcended?",
         "opts": ["Ahaṅkāra is self-confidence, which is always negative",
                  "Ahaṅkāra is the false identification of pure Consciousness with the body-mind — the root error that generates all suffering and the sense of separation",
                  "Ahaṅkāra is healthy self-esteem",
                  "Ahaṅkāra is desire for material objects only"],
         "ans": "Ahaṅkāra is the false identification of pure Consciousness with the body-mind — the root error that generates all suffering and the sense of separation",
         "explain": "Anahaṅkāra is not self-negation — it is the recognition that the true Self (Ātman) is not the ego-identity we constructed. Dissolving the false frees the Real! 🪷"},
    ],
}
# ── WORD SEARCH DATA ───────────────────────────────────────────────────────────
WORD_SEARCHES = {
    "6-10": {
        "title": "Find the Values!",
        "words": ["AHIMSA", "TRUTH", "PEACE", "PURE", "CALM", "KIND", "GIVE"],
        "grid": [
            "A H I M S A T R",
            "T B C A L M R U",
            "R K I N D P E T",
            "U G I V E A P H",
            "T P E A C E U Q",
            "H X W Z L R R S",
            "M P U R E F E V",
            "Y Z A B C G D W",
        ],
        "hint": "Look across → and down ↓ for the hidden values!",
    },
    "10-14": {
        "title": "Sanskrit Values Word Search",
        "words": ["ABHAYAM", "SATYAM", "DANAM", "TAPAS", "SHANTI", "DAMA", "TYAGA"],
        "grid": [
            "A B H A Y A M T",
            "S D A N A M P Y",
            "A R C T A P A S",
            "T S H A N T I A",
            "Y E D A M A Q G",
            "A Z W B C T R A",
            "M T Y A G A P M",
            "X D A M A B C Y",
        ],
        "hint": "Find all 7 values hidden across → and down ↓!",
    },
    "14-18": {
        "title": "Sanskrit Values — Advanced Search",
        "words":["AMANITVA", "AHIMSA", "KSAMA", "DHRITI", "TYAGA", "ABHAYAM", "SATYAM"],
        "grid": [
            "A M A N I T V A",
            "B S A T Y A M H",
            "H X A H I M S A",
            "A Z K S A M A B",
            "Y D H R I T I Y",
            "A T Y A G A C A",
            "M P Q R W S X M",
            "A B C D E F G Z",
        ],
        "hint": "Find all 7 values — look across → and down ↓!",
    },
}

# ── MATCH DATA ─────────────────────────────────────────────────────────────────
MATCHES = {
    "6-10": [
        ("Ahiṃsā",        "Not hurting anyone"),
        ("Satyam",        "Always telling the truth"),
        ("Śāntiḥ",        "Feeling peaceful inside"),
        ("Dānam",         "Giving to others"),
        ("Śaucam",        "Being clean and pure"),
    ],
    "10-14": [
        ("Abhayam",       "Fearlessness"),
        ("Akrodhaḥ",      "Freedom from anger"),
        ("Kṣamā",         "Forgiveness"),
        ("Tapas",         "Austerity and self-discipline"),
        ("Svādhyāyaḥ",    "Self-study and scriptural reading"),
        ("Dānam",         "Generous giving"),
    ],
    "14-18": [
        ("Amānitvam",             "Absence of pride — not demanding respect"),
        ("Adambhitvam",           "Absence of hypocrisy and ostentation"),
        ("Jñāna-yoga-vyavasthitiḥ", "Steadfastness in knowledge and yoga"),
        ("Anabhiṣvaṅga",          "Freedom from blind attachment to family"),
        ("Nātimānitā",            "Absence of excessive pride"),
        ("Tattva-jñānārtha-darśanam", "Seeing liberation as the goal of life"),
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def render_quiz(age_key: str):
    all_questions = QUIZZES[age_key]
    quiz_key      = f"quiz_{age_key}"
    ans_key       = f"ans_{age_key}"
    sub_key       = f"sub_{age_key}"
    seed_key      = f"quiz_seed_{age_key}"

    if ans_key not in st.session_state:
        st.session_state[ans_key] = {}
    if sub_key not in st.session_state:
        st.session_state[sub_key] = False

    # Pick 5 random questions using the stored seed
    rng       = random.Random(st.session_state[seed_key])
    questions = rng.sample(all_questions, 5)

    st.markdown('<div class="activity-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="activity-title">🎯 Quiz — Test Your Knowledge! '
        '<span style="font-size:.8rem;font-weight:400;color:#0D5C6B;">'
        f'(5 of {len(all_questions)} questions — randomly selected)</span></div>',
        unsafe_allow_html=True,
    )

    for idx, q in enumerate(questions):
        st.markdown(f'<div class="quiz-question">Q{idx+1}. {q["q"]}</div>',
                    unsafe_allow_html=True)
        choice = st.radio(
            label=f"q{idx}",
            options=q["opts"],
            key=f"{quiz_key}_q{idx}_{st.session_state[seed_key]}",
            label_visibility="collapsed",
        )
        st.session_state[ans_key][idx] = choice

        if st.session_state[sub_key]:
            if choice == q["ans"]:
                st.markdown(
                    f'<div class="quiz-correct">✅ Correct! {q["explain"]}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="quiz-wrong">❌ Not quite. The answer is '
                    f'<strong>{q["ans"]}</strong>. {q["explain"]}</div>',
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("✅ Submit", key=f"submit_{quiz_key}",
                     use_container_width=True):
            st.session_state[sub_key] = True
            st.rerun()
    with col2:
        if st.button("🔄 Try 5 More", key=f"more_{quiz_key}",
                     use_container_width=True):
            st.session_state[sub_key]  = False
            st.session_state[ans_key]  = {}
            st.session_state[seed_key] = random.randint(0, 9999)
            st.rerun()
    with col3:
        if st.button("↩️ Reset", key=f"reset_{quiz_key}",
                     use_container_width=True):
            st.session_state[sub_key]  = False
            st.session_state[ans_key]  = {}
            st.session_state[seed_key] = random.randint(0, 9999)
            st.rerun()

    if st.session_state[sub_key]:
        score = sum(
            1 for idx, q in enumerate(questions)
            if st.session_state[ans_key].get(idx) == q["ans"]
        )
        total = len(questions)
        emoji = "🏆" if score == total else "🌸" if score >= total // 2 else "🪷"
        msg   = ("Perfect score — wonderful!" if score == total
                 else "Great effort — try 5 more!" if score >= total // 2
                 else "Keep exploring — you're learning! 🪷")
        st.markdown(
            f'<div class="quiz-score">{emoji} You scored {score} out of {total}! {msg}</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_word_search(age_key: str):
    ws   = WORD_SEARCHES[age_key]
    st.markdown('<div class="activity-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="activity-title">🔤 Word Search — {ws["title"]}</div>',
                unsafe_allow_html=True)
    st.caption(ws["hint"])

    # Grid display
    grid_html = '<div class="word-grid">'
    for row in ws["grid"]:
        grid_html += row + "<br>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown("<br>**Find these words:**", unsafe_allow_html=True)
    badges = "".join(
        f'<span class="word-badge">{w}</span>' for w in ws["words"]
    )
    st.markdown(f'<div class="word-list">{badges}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    found_key = f"ws_found_{age_key}"
    if found_key not in st.session_state:
        st.session_state[found_key] = []

    st.markdown("**Tick the words you've found:**")
    cols = st.columns(4)
    for i, word in enumerate(ws["words"]):
        with cols[i % 4]:
            checked = st.checkbox(word, key=f"ws_{age_key}_{i}")
            if checked and word not in st.session_state[found_key]:
                st.session_state[found_key].append(word)

    found = len([w for w in ws["words"]
                 if st.session_state.get(f"ws_{age_key}_{ws['words'].index(w)}", False)])
    total = len(ws["words"])
    if found == total:
        st.success(f"🏆 Amazing! You found all {total} words!")
    elif found > 0:
        st.info(f"🌸 Found {found} of {total} — keep looking!")
    st.markdown('</div>', unsafe_allow_html=True)


def render_match(age_key: str):
    pairs    = MATCHES[age_key]
    values   = [p[0] for p in pairs]
    meanings = [p[1] for p in pairs]
    sub_key  = f"match_sub_{age_key}"
    sel_key  = f"match_sel_{age_key}"

    if sub_key not in st.session_state:
        st.session_state[sub_key] = False
    if sel_key not in st.session_state:
        st.session_state[sel_key] = {}

    correct_map = {p[0]: p[1] for p in pairs}

    st.markdown('<div class="activity-card">', unsafe_allow_html=True)
    st.markdown('<div class="activity-title">🔗 Match the Value — Pair each value to its meaning!</div>',
                unsafe_allow_html=True)

    shuffled_meanings = meanings.copy()
    # Use a stable shuffle seeded on age_key so it doesn't reshuffle on rerun
    rng = random.Random(age_key)
    rng.shuffle(shuffled_meanings)

    for i, val in enumerate(values):
        choice = st.selectbox(
            label=val,
            options=["— select meaning —"] + shuffled_meanings,
            key=f"match_{age_key}_{i}",
        )
        st.session_state[sel_key][val] = choice

        if st.session_state[sub_key] and choice != "— select meaning —":
            if choice == correct_map[val]:
                st.markdown(
                    f'<div class="match-item match-correct">✅ {val} → {choice}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="match-item match-wrong">❌ {val} → correct: '
                    f'{correct_map[val]}</div>',
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("✅ Check Answers", key=f"match_submit_{age_key}",
                     use_container_width=True):
            st.session_state[sub_key] = True
            st.rerun()
    with col2:
        if st.button("🔄 Reset", key=f"match_reset_{age_key}",
                     use_container_width=True):
            st.session_state[sub_key] = False
            st.session_state[sel_key] = {}
            st.rerun()

    if st.session_state[sub_key]:
        score = sum(
            1 for val in values
            if st.session_state[sel_key].get(val) == correct_map[val]
        )
        total = len(values)
        emoji = "🏆" if score == total else "🌸" if score >= total // 2 else "🪷"
        st.markdown(
            f'<div class="quiz-score">{emoji} {score} of {total} correct! '
            f'{"All matched — excellent!" if score == total else "Try again — you\'re learning!"}'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN — Three Age Group Tabs
# ══════════════════════════════════════════════════════════════════════════════

tab_young, tab_mid, tab_teen = st.tabs([
    "🌱 Little Seekers (6–10)",
    "🌸 Young Explorers (10–14)",
    "🔥 Teen Wisdom (14–18)",
])

# ── Tab 1: Little Seekers (6–10) ───────────────────────────────────────────────
with tab_young:
    st.markdown("""
    <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
        padding:1rem 1.4rem;margin-bottom:1rem;border-left:5px solid #0D5C6B;">
        <div style="font-family:'Playfair Display',serif;font-weight:700;
            color:#062E3A;font-size:1rem;margin-bottom:.2rem;">
            🌱 Welcome, Little Seeker!
        </div>
        <div style="font-size:.88rem;color:#1A3A45;line-height:1.6;">
            Learn about the beautiful values that make us kind, honest and peaceful.
            Try the quiz, find words in the puzzle, and match values to their meanings!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Quiz")
    render_quiz("6-10")

    st.markdown("### 🔤 Word Search")
    render_word_search("6-10")

    st.markdown("### 🔗 Match the Value")
    render_match("6-10")

# ── Tab 2: Young Explorers (10–14) ────────────────────────────────────────────
with tab_mid:
    st.markdown("""
    <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
        padding:1rem 1.4rem;margin-bottom:1rem;border-left:5px solid #0D5C6B;">
        <div style="font-family:'Playfair Display',serif;font-weight:700;
            color:#062E3A;font-size:1rem;margin-bottom:.2rem;">
            🌸 Welcome, Young Explorer!
        </div>
        <div style="font-size:.88rem;color:#1A3A45;line-height:1.6;">
            Dive deeper into the 46 Indispensable Values from the Bhagavad Gītā.
            These values were taught by Pūjya Swāmī Aparājitānanda to help us live
            a meaningful and joyful life.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Quiz")
    render_quiz("10-14")

    st.markdown("### 🔤 Word Search")
    render_word_search("10-14")

    st.markdown("### 🔗 Match the Value")
    render_match("10-14")

# ── Tab 3: Teen Wisdom (14–18) ────────────────────────────────────────────────
with tab_teen:
    st.markdown("""
    <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
        padding:1rem 1.4rem;margin-bottom:1rem;border-left:5px solid #0D5C6B;">
        <div style="font-family:'Playfair Display',serif;font-weight:700;
            color:#062E3A;font-size:1rem;margin-bottom:.2rem;">
            🔥 Welcome, Teen Wisdom Seeker!
        </div>
        <div style="font-size:.88rem;color:#1A3A45;line-height:1.6;">
            Explore the deeper meanings of the Indispensable Values as taught in
            Bhagavad Gītā Chapters 13 and 16. These questions will challenge you
            to think carefully about what each value really means.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Quiz")
    render_quiz("14-18")

    st.markdown("### 🔤 Word Search")
    render_word_search("14-18")

    st.markdown("### 🔗 Match the Value")
    render_match("14-18")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#0D5C6B;font-size:.88rem;
    font-family:'Cormorant Garamond',serif;font-style:italic;
    margin-top:2rem;padding:1rem;border-top:1.5px solid #88C5D0;">
    🪷 &nbsp; Learning values is the greatest gift you can give yourself &nbsp; 🪷<br>
    <span style="font-size:.78rem;">— Inspired by the teachings of Pūjya Swāmī Aparājitānanda</span>
</div>
""", unsafe_allow_html=True)
