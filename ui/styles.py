"""
ui/styles.py
------------
Het volledige visuele ontwerpsysteem van de app.

Ontwerprichting (na feedback: "vrolijker, grotere knoppen, professioneler"):
  - Kahoot/SongPop-achtige zelfverzekerde kleurmomenten per scherm
  - Duolingo-achtige "3D-knoppen" met een dikke onderrand (voelt drukbaar)
  - Retro jukebox-sfeer (warme kleuren, eigen illustraties i.p.v. emoji)
  - Spotify Wrapped-achtige grote typografie op een zachte gradient-achtergrond

Knoppen krijgen hun kleur via Streamlit's automatische 'st-key-<key>'
CSS-klasse (elke widget met een key= krijgt deze klasse op zijn container).
Zo kan elk scherm een eigen kleurmoment krijgen zonder rommelig te worden:
dezelfde knop-stijl, maar een andere kleur per fase van het spel.
"""

from __future__ import annotations

import streamlit as st

_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700;800;900&display=swap');

    :root {
        --ink: #2B2440;
        --ink-soft: #5B5270;
        --card: #FFFFFF;
        --cream: #FFF8F0;

        --coral: #FF6B57;
        --coral-dark: #D6432F;
        --teal: #17B8A6;
        --teal-dark: #0E8377;
        --violet: #8B5CF6;
        --violet-dark: #6633CC;
        --gold: #FFB238;
        --gold-dark: #DB8B12;

        --shadow: rgba(43, 36, 64, 0.14);
    }

    /* ---------- Achtergrond: zachte gradient-mesh (professioneel, geen kinderlijke felle vlakken) ---------- */
    .stApp {
        background-color: var(--cream);
        background-image:
            radial-gradient(720px 480px at 8% 0%, rgba(255,107,87,0.16) 0%, rgba(255,107,87,0) 60%),
            radial-gradient(760px 520px at 100% 12%, rgba(23,184,166,0.16) 0%, rgba(23,184,166,0) 60%),
            radial-gradient(640px 480px at 50% 100%, rgba(139,92,246,0.14) 0%, rgba(139,92,246,0) 60%);
        background-attachment: fixed;
    }

    html, body, [class*="css"] {
        font-family: 'Nunito', -apple-system, sans-serif;
        font-size: 20px;
        color: var(--ink);
    }

    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 740px;
    }

    /* ---------- Typografie: Fredoka = zelfverzekerd + speels, niet kinderlijk ---------- */
    h1 {
        font-family: 'Fredoka', sans-serif !important;
        font-size: 2.9rem !important;
        font-weight: 700 !important;
        color: var(--ink);
        text-align: center;
        letter-spacing: -0.5px;
        line-height: 1.08;
        margin-bottom: 0.2rem;
    }

    h2 {
        font-family: 'Fredoka', sans-serif !important;
        font-size: 2.1rem !important;
        font-weight: 600 !important;
        color: var(--ink);
        text-align: center;
    }

    h3 {
        font-family: 'Fredoka', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: var(--ink);
    }

    p, li, label, .stMarkdown {
        font-size: 1.18rem !important;
        color: var(--ink-soft);
        line-height: 1.6;
    }

    /* ---------- Knoppen: dikke '3D'-knoppen a la Duolingo ---------- */
    .stButton > button {
        width: 100%;
        min-height: 4.4rem;
        font-family: 'Nunito', sans-serif;
        font-size: 1.4rem !important;
        font-weight: 800;
        border-radius: 20px;
        border: none;
        background: #FFFFFF;
        color: var(--ink);
        padding: 0.6rem 1.2rem;
        box-shadow:
            inset 0 -5px 0 rgba(43,36,64,0.10),
            0 2px 0 rgba(43,36,64,0.06);
        transition: transform 0.05s ease, box-shadow 0.12s ease, filter 0.12s ease;
        position: relative;
    }
    .stButton > button:hover { filter: brightness(1.03); }
    .stButton > button:active { transform: translateY(3px); }

    /* Grote, opvallende primaire knoppen - dikke 'keycap'-onderrand */
    .stButton > button[kind="primary"] {
        font-size: 1.65rem !important;
        font-weight: 900;
        min-height: 5.2rem;
        color: #FFFFFF;
        border-radius: 24px;
        background: linear-gradient(180deg, var(--coral) 0%, var(--coral) 78%, var(--coral-dark) 78%);
        box-shadow: 0 6px 0 var(--coral-dark), 0 14px 26px rgba(214,67,47,0.35);
        text-shadow: 0 2px 3px rgba(0,0,0,0.15);
    }
    .stButton > button[kind="primary"]:hover { filter: brightness(1.05); }
    .stButton > button[kind="primary"]:active {
        transform: translateY(5px);
        box-shadow: 0 1px 0 var(--coral-dark), 0 4px 10px rgba(214,67,47,0.3);
    }

    /* Kleurmomenten per spelfase, via Streamlit's automatische st-key-* klasse */
    [class*="st-key-rounds_"] button[kind="primary"],
    [class*="st-key-next_round"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--teal) 0%, var(--teal) 78%, var(--teal-dark) 78%) !important;
        box-shadow: 0 6px 0 var(--teal-dark), 0 14px 26px rgba(14,131,119,0.35) !important;
    }
    [class*="st-key-confirm_"] button[kind="primary"],
    [class*="st-key-play_again"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--violet) 0%, var(--violet) 78%, var(--violet-dark) 78%) !important;
        box-shadow: 0 6px 0 var(--violet-dark), 0 14px 26px rgba(102,51,204,0.35) !important;
    }
    [class*="st-key-to_ask_title"] button[kind="primary"],
    [class*="st-key-to_reveal_full"] button[kind="primary"],
    [class*="st-key-to_end"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--gold) 0%, var(--gold) 78%, var(--gold-dark) 78%) !important;
        box-shadow: 0 6px 0 var(--gold-dark), 0 14px 26px rgba(219,139,18,0.35) !important;
        color: #3A2A05 !important;
        text-shadow: none !important;
    }

    /* Kleine, rustige knoppen (terug/uitloggen/beheerder) */
    .subtle-link .stButton > button {
        box-shadow: none;
        border: 2px solid #E4D9CC;
        background: transparent;
        min-height: 2.9rem;
        font-size: 1rem !important;
        font-weight: 700;
        width: auto;
        color: var(--ink-soft);
    }

    .stLinkButton > a {
        min-height: 3.8rem;
        font-size: 1.25rem !important;
        font-weight: 800;
        border-radius: 20px !important;
        background: #1DB954 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 5px 0 #14883C, 0 12px 22px rgba(29,185,84,0.3) !important;
    }

    /* ---------- Schuifregelaar ---------- */
    [data-testid="stSlider"] [role="slider"] {
        width: 36px !important;
        height: 36px !important;
        background: var(--coral) !important;
        border: 4px solid #FFFFFF !important;
        box-shadow: 0 0 0 6px rgba(255,107,87,0.22), 0 4px 10px rgba(0,0,0,0.2) !important;
    }
    [data-testid="stSlider"] > div > div > div > div {
        background: var(--coral) !important;
    }
    [data-testid="stSlider"] > div > div > div {
        background: #EADFD0 !important;
        height: 10px !important;
        border-radius: 999px !important;
    }
    [data-testid="stSliderTickBarMin"],
    [data-testid="stSliderTickBarMax"],
    [data-testid="stThumbValue"] {
        display: none !important;
    }

    /* ---------- Kaarten ---------- */
    .card {
        background: var(--card);
        border-radius: 28px;
        padding: 2rem 1.6rem;
        box-shadow: 0 4px 0 #EADFD0, 0 16px 34px var(--shadow);
        margin-bottom: 1.4rem;
    }

    .mystery-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #FFF3E9 100%);
        border-radius: 28px;
        padding: 2.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 4px 0 #F3D9BE, 0 16px 34px var(--shadow);
        margin-bottom: 1.3rem;
    }

    .reveal-card {
        background: var(--card);
        border-radius: 28px;
        padding: 2rem 1.5rem 2.2rem;
        text-align: center;
        box-shadow: 0 4px 0 #EADFD0, 0 18px 38px var(--shadow);
        margin-bottom: 1.2rem;
    }

    .reveal-card img {
        border-radius: 18px;
        box-shadow: 0 10px 24px rgba(43,36,64,0.3);
    }

    .result-banner {
        border-radius: 26px;
        padding: 1.6rem 1rem;
        text-align: center;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 0 rgba(0,0,0,0.06), 0 16px 32px var(--shadow);
    }
    .result-good  { background: linear-gradient(160deg, #E9FBF3 0%, #D3F5E4 100%); }
    .result-close { background: linear-gradient(160deg, #FFF6DE 0%, #FFEBB8 100%); }
    .result-far   { background: linear-gradient(160deg, #FFF0EA 0%, #FFDFCF 100%); }

    .hero-year {
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 5.2rem;
        line-height: 1;
        margin: 0.4rem 0;
    }

    .score-badge {
        display: inline-block;
        background: linear-gradient(180deg, var(--gold) 0%, var(--gold-dark) 100%);
        color: #3A2A05;
        font-size: 1.5rem;
        font-weight: 900;
        padding: 0.6rem 1.8rem;
        border-radius: 999px;
        margin-top: 0.7rem;
        box-shadow: 0 4px 0 #A9660A, 0 8px 18px rgba(219,139,18,0.4);
    }

    .decade-badge {
        display: inline-block;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.05rem;
        padding: 0.35rem 1.2rem;
        border-radius: 999px;
        letter-spacing: 0.5px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.18);
    }

    .guess-window-label {
        text-align: center;
        font-family: 'Fredoka', sans-serif;
        font-size: 3.2rem !important;
        font-weight: 700;
        color: var(--coral-dark);
        margin: 0.3rem 0 0.8rem 0;
    }

    .progress-dots {
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 8px;
        margin-bottom: 0.4rem;
        color: var(--coral);
    }

    .kicker {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.85rem !important;
        font-weight: 800;
        color: var(--teal-dark);
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.28rem !important;
        color: var(--ink-soft);
        font-weight: 600;
    }

    .subtle-link {
        text-align: center;
        margin-top: 2.2rem;
        opacity: 0.75;
    }

    .hero-image {
        border-radius: 26px;
        box-shadow: 0 16px 34px var(--shadow);
        margin-bottom: 1.2rem;
    }

    .timeline-strip {
        height: 12px;
        border-radius: 999px;
        margin: 0.9rem 0 0.2rem 0;
        background: linear-gradient(90deg,
            #FF6B57, #FFB238, #17B8A6, #8B5CF6, #FF6B57);
        background-size: 200% 100%;
        opacity: 0.9;
    }

    /* ---------- Vinylplaat (draaiende illustratie op de raad-kaart) ---------- */
    .vinyl-wrap { position: relative; width: 190px; height: 190px; margin: 0.3rem auto 1.2rem auto; }
    .vinyl {
        width: 190px; height: 190px;
        border-radius: 50%;
        background:
            radial-gradient(circle at center, var(--coral) 0 17%, #201A2E 17% 19%, #2E2740 19% 100%);
        box-shadow: 0 16px 34px rgba(43,36,64,0.4);
        animation: spin 7s linear infinite;
        position: relative;
    }
    .vinyl::before {
        content: "";
        position: absolute; inset: 22px;
        border-radius: 50%;
        background: repeating-radial-gradient(circle at center, #3A3350 0 2px, #2E2740 2px 6px);
    }
    .vinyl::after {
        content: "";
        position: absolute; inset: 76px;
        border-radius: 50%;
        background: radial-gradient(circle at center, #FFF3E9 0 30%, var(--coral) 30% 100%);
        box-shadow: inset 0 0 0 3px rgba(0,0,0,0.2);
    }
    .vinyl-note {
        position: absolute;
        font-family: 'Fredoka', sans-serif;
        font-size: 1.8rem;
        animation: float 3s ease-in-out infinite;
    }
    .vinyl-note.n1 { top: -10px; right: 4px; color: var(--teal); animation-delay: 0s; }
    .vinyl-note.n2 { bottom: 6px; left: -14px; color: var(--violet); animation-delay: 1.2s; }
    @keyframes spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(-6deg); }
        50% { transform: translateY(-10px) rotate(6deg); }
    }
    @media (prefers-reduced-motion: reduce) {
        .vinyl, .vinyl-note { animation: none; }
    }

    /* ---------- Jukebox-illustratie (startscherm) ---------- */
    .jukebox-wrap { text-align: center; margin: 0.2rem 0 0.6rem 0; }

    /* ---------- Tabs (beheerscherm): pil-vormig, kleurrijk actief tabblad ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        background: #FFFFFF;
        padding: 0.4rem;
        border-radius: 999px;
        box-shadow: 0 3px 0 #EADFD0, 0 8px 18px var(--shadow);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        font-weight: 800;
        font-size: 1.02rem;
        color: var(--ink-soft);
        padding: 0.6rem 1.1rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, var(--violet) 0%, var(--violet-dark) 100%) !important;
        color: #FFFFFF !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ---------- Formuliervelden ---------- */
    input, textarea, [data-baseweb="select"] > div {
        font-size: 1.1rem !important;
        border-radius: 14px !important;
        border-color: #E4D9CC !important;
    }
    input:focus, textarea:focus {
        border-color: var(--coral) !important;
        box-shadow: 0 0 0 3px rgba(255,107,87,0.18) !important;
    }

    /* ---------- Containers met rand (bv. liedjesregels in beheerscherm) ---------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border-color: #EDE2D4 !important;
        box-shadow: 0 2px 0 #EADFD0, 0 6px 16px rgba(43,36,64,0.08);
    }

    /* ---------- Expander ---------- */
    [data-testid="stExpander"] {
        border-radius: 18px !important;
        border-color: #EDE2D4 !important;
    }
</style>
"""


def inject_custom_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
