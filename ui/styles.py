"""
ui/styles.py
------------
Warme, nostalgische en rustige huisstijl voor de app. Bewust seniorvriendelijk:
grote leesbare tekst, grote knoppen, hoog contrast en een zachte, huiselijke
sfeer (warme creme/terracotta tinten) in plaats van het standaard "kale"
Streamlit-uiterlijk.

Sfeerbeelden en een eventueel eigen logo worden NIET meegeleverd - die kan de
instelling zelf toevoegen via het beheerscherm (Instellingen). Zo blijft de
app juridisch schoon en toch te personaliseren.
"""

from __future__ import annotations

import streamlit as st

_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Nunito:wght@400;600;700;800&display=swap');

    :root {
        --bg: #F4E9D8;
        --bg-soft: #FBF3E7;
        --card: #FFFDF9;
        --ink: #3A2E24;
        --ink-soft: #6B5B4B;
        --primary: #C0632B;
        --primary-dark: #9E4E1E;
        --accent: #2E6E5A;
        --gold: #D9A441;
        --shadow: rgba(74, 52, 30, 0.16);
    }

    .stApp {
        background:
            radial-gradient(1200px 500px at 50% -10%, #FBEFD9 0%, rgba(251,239,217,0) 60%),
            linear-gradient(180deg, #F4E9D8 0%, #EFE0C9 100%);
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
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }

    h1 {
        font-family: 'Fraunces', Georgia, serif !important;
        font-size: 2.9rem !important;
        font-weight: 700 !important;
        color: var(--ink);
        text-align: center;
        letter-spacing: -0.5px;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    h2 {
        font-family: 'Fraunces', Georgia, serif !important;
        font-size: 2.1rem !important;
        font-weight: 600 !important;
        color: var(--ink);
        text-align: center;
    }

    h3 {
        font-family: 'Nunito', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--ink);
    }

    p, li, label, .stMarkdown {
        font-size: 1.18rem !important;
        color: var(--ink-soft);
        line-height: 1.65;
    }

    .stButton > button {
        width: 100%;
        min-height: 4rem;
        font-family: 'Nunito', sans-serif;
        font-size: 1.35rem !important;
        font-weight: 800;
        border-radius: 20px;
        border: 2px solid var(--gold);
        background: var(--card);
        color: var(--ink);
        padding: 0.6rem 1rem;
        transition: transform 0.06s ease, box-shadow 0.18s ease, background 0.18s ease;
        box-shadow: 0 4px 0 var(--shadow);
    }

    .stButton > button:hover {
        border-color: var(--primary);
        background: #FFF8EE;
        box-shadow: 0 6px 16px rgba(192, 99, 43, 0.22);
    }

    .stButton > button:active {
        transform: translateY(3px);
        box-shadow: 0 1px 0 var(--shadow);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-color: var(--primary-dark);
        color: #FFFFFF;
        font-size: 1.55rem !important;
        min-height: 4.6rem;
        box-shadow: 0 5px 0 rgba(120, 58, 20, 0.4);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(180deg, #CE6E33 0%, var(--primary) 100%);
        box-shadow: 0 7px 20px rgba(158, 78, 30, 0.4);
    }

    .stLinkButton > a {
        min-height: 3.6rem;
        font-size: 1.25rem !important;
        font-weight: 700;
        border-radius: 18px !important;
        background: #1DB954 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        width: 34px !important;
        height: 34px !important;
        background: var(--primary) !important;
        box-shadow: 0 0 0 7px rgba(192, 99, 43, 0.18) !important;
    }

    [data-testid="stSlider"] > div > div > div > div {
        background: var(--primary) !important;
    }

    [data-testid="stSlider"] > div > div > div {
        background: #E7D3B3 !important;
        height: 8px !important;
    }

    [data-testid="stSliderTickBarMin"],
    [data-testid="stSliderTickBarMax"],
    [data-testid="stThumbValue"] {
        display: none !important;
    }

    .card {
        background: var(--card);
        border-radius: 28px;
        padding: 2rem 1.6rem;
        border: 1px solid #EAD9BE;
        box-shadow: 0 10px 30px var(--shadow);
        margin-bottom: 1.4rem;
    }

    .mystery-card {
        background: linear-gradient(135deg, #FFF3DE 0%, #F6DEB6 100%);
        border-radius: 28px;
        padding: 2.2rem 1.5rem;
        text-align: center;
        border: 2px solid #E7C77E;
        box-shadow: 0 10px 30px var(--shadow);
        margin-bottom: 1.3rem;
    }

    .mystery-card .icon {
        font-size: 4rem;
        line-height: 1;
        filter: saturate(0.9);
    }

    .reveal-card {
        background: var(--card);
        border-radius: 28px;
        padding: 2rem 1.5rem 2.2rem;
        text-align: center;
        border: 1px solid #EAD9BE;
        box-shadow: 0 12px 34px var(--shadow);
        margin-bottom: 1.2rem;
    }

    .reveal-card img {
        border-radius: 16px;
        box-shadow: 0 8px 22px rgba(74, 52, 30, 0.28);
    }

    .result-banner {
        border-radius: 22px;
        padding: 1.4rem 1rem;
        text-align: center;
        margin-bottom: 1.2rem;
        border: 2px solid;
    }
    .result-good   { background: #E4F0E4; border-color: #7FB07F; }
    .result-close  { background: #FBF0D8; border-color: #E7C77E; }
    .result-far    { background: #F3E7DC; border-color: #D2B79A; }

    .result-year {
        font-family: 'Fraunces', serif;
        font-size: 3.4rem;
        font-weight: 700;
        color: var(--primary-dark);
        line-height: 1;
        margin: 0.3rem 0;
    }

    .score-badge {
        display: inline-block;
        background: var(--gold);
        color: #4A3418;
        font-size: 1.4rem;
        font-weight: 800;
        padding: 0.55rem 1.6rem;
        border-radius: 999px;
        margin-top: 0.6rem;
        box-shadow: 0 4px 12px rgba(217, 164, 65, 0.4);
    }

    .guess-window-label {
        text-align: center;
        font-family: 'Fraunces', serif;
        font-size: 3rem !important;
        font-weight: 700;
        color: var(--primary-dark);
        margin: 0.3rem 0 0.8rem 0;
        letter-spacing: 1px;
    }

    .progress-dots {
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 8px;
        margin-bottom: 0.4rem;
        color: var(--primary);
    }

    .kicker {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.85rem !important;
        font-weight: 800;
        color: var(--accent);
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.25rem !important;
        color: var(--ink-soft);
    }

    .subtle-link {
        text-align: center;
        margin-top: 2.5rem;
        opacity: 0.5;
    }
    .subtle-link .stButton > button {
        box-shadow: none;
        border: 1px solid #D8C5A6;
        background: transparent;
        min-height: 2.8rem;
        font-size: 0.95rem !important;
        font-weight: 600;
        width: auto;
    }

    .hero-image {
        border-radius: 24px;
        box-shadow: 0 12px 34px var(--shadow);
        margin-bottom: 1.2rem;
    }

    /* ---------- Vinylplaat (Hitster-inspiratie: draaiende plaat) ---------- */
    .vinyl {
        width: 190px;
        height: 190px;
        margin: 0.5rem auto 1.2rem auto;
        border-radius: 50%;
        background:
            radial-gradient(circle at center,
                #C0632B 0 18%,
                #1a1a1a 18% 20%,
                #2b2b2b 20% 100%);
        position: relative;
        box-shadow: 0 14px 34px rgba(0,0,0,0.35);
        animation: spin 6s linear infinite;
    }
    .vinyl::before {
        /* groeven */
        content: "";
        position: absolute; inset: 24px;
        border-radius: 50%;
        background: repeating-radial-gradient(
            circle at center,
            #333 0 2px, #262626 2px 5px);
    }
    .vinyl::after {
        /* label in het midden */
        content: "";
        position: absolute; inset: 74px;
        border-radius: 50%;
        background: radial-gradient(circle at center, #F4E9D8 0 32%, #C0632B 32% 100%);
        box-shadow: inset 0 0 0 3px rgba(0,0,0,0.25);
    }
    @keyframes spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }

    @media (prefers-reduced-motion: reduce) {
        .vinyl { animation: none; }
    }

    /* ---------- Decennium-badge (kleurcodering) ---------- */
    .decade-badge {
        display: inline-block;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.05rem;
        padding: 0.35rem 1.1rem;
        border-radius: 999px;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.18);
    }

    /* Groot onthuld jaartal met decennium-kleur (via inline style gezet) */
    .hero-year {
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 5rem;
        line-height: 1;
        margin: 0.4rem 0;
    }

    /* Tijdlijn-lint als subtiele verwijzing naar Hitster's timeline */
    .timeline-strip {
        height: 10px;
        border-radius: 999px;
        margin: 0.8rem 0 0.2rem 0;
        background: linear-gradient(90deg,
            #B5654A, #C98A2B, #8A7B3A, #7A6BB0, #3E8E7E, #4A7BA6);
        opacity: 0.85;
    }
</style>
"""


def inject_custom_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
