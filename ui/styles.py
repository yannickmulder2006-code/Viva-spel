"""
ui/styles.py
------------
Visueel ontwerpsysteem, herbouwd op basis van de vintage-scrapbook-mockups
die zijn aangeleverd als inspiratie. Kleuren zijn 1-op-1 overgenomen (met
een pipet) uit het aangeleverde kleurenpalet: salie, crème, terracotta,
bruin, gedempt paars, petrol.

Ontwerpprincipes uit de mockups:
  - Sierlijk script-lettertype ALLEEN voor korte koppen ("Luister goed mee!");
    alle functionele tekst (instructies, knoppen, cijfers) blijft in een
    rustig, goed leesbaar schreefloos lettertype - belangrijk voor de
    doelgroep.
    De opdrachtgever gaf zelf aan dat leesbaarheid hier iets minder zwaar
    hoeft te wegen omdat de app onder begeleiding wordt gebruikt, maar uit
    zorgvuldigheid houden we dit onderscheid toch aan.
  - Foto's/illustraties met een 'polaroid'-lijstje en lichte kanteling
  - Organische, zachte vormen i.p.v. felle vlakke kleurblokken
  - Leren/stoffen knoppen met een zachte "ingedrukt"-schaduw
"""

from __future__ import annotations

import streamlit as st

from ui.assets import get_data_uri

_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:wght@400;600;700;800;900&display=swap');

    :root {
        --sage: #64846D;      --sage-dark: #485F4E;
        --cream: #F6EAD8;     --cream-light: #FBF4E9;
        --terracotta: #E08E51; --terracotta-dark: #A1663A; --terracotta-darker: #7B4E2C;
        --brown: #74411E;     --brown-dark: #532E15;
        --purple: #7F6578;    --purple-dark: #5B4856;
        --teal: #476F78;      --teal-dark: #334F56;
        --ink: #3D2E1F;
        --ink-soft: #6B5C4D;
        --card: #FFFDF9;
        --shadow: rgba(61, 46, 31, 0.16);
    }

    .stApp {
        background-color: var(--cream-light);
        background-image:
            radial-gradient(900px 500px at 8% -8%, rgba(100,132,109,0.14) 0%, rgba(100,132,109,0) 60%),
            radial-gradient(800px 500px at 100% 8%, rgba(224,142,81,0.14) 0%, rgba(224,142,81,0) 60%);
        background-attachment: fixed;
    }

    html, body, [class*="css"] {
        font-family: 'Nunito', -apple-system, sans-serif;
        font-size: 20px;
        color: var(--ink);
    }

    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

    .block-container { padding-top: 1.3rem; padding-bottom: 3rem; max-width: 740px; }

    /* ---------- Typografie ---------- */
    h1.script, .script-heading {
        font-family: 'Pacifico', cursive !important;
        font-weight: 400 !important;
        font-size: 2.7rem !important;
        color: var(--ink);
        text-align: center;
        line-height: 1.25;
        margin: 0.2rem 0 0.3rem 0;
    }
    h2 { font-family: 'Nunito', sans-serif !important; font-size: 1.7rem !important; font-weight: 800 !important; color: var(--ink); text-align: center; }
    h3 { font-family: 'Nunito', sans-serif !important; font-size: 1.4rem !important; font-weight: 800 !important; color: var(--ink); }
    p, li, label, .stMarkdown { font-size: 1.16rem !important; color: var(--ink-soft); line-height: 1.6; }

    /* ---------- Knoppen: leren/stoffen 'ingedrukt' effect ---------- */
    .stButton > button {
        width: 100%;
        min-height: 4.3rem;
        font-family: 'Nunito', sans-serif;
        font-size: 1.32rem !important;
        font-weight: 800;
        border-radius: 18px;
        border: none;
        background: var(--card);
        color: var(--ink);
        padding: 0.6rem 1.1rem;
        box-shadow: inset 0 -4px 0 rgba(61,46,31,0.08), 0 3px 8px var(--shadow);
        transition: transform 0.05s ease, filter 0.12s ease;
    }
    .stButton > button:hover { filter: brightness(1.03); }
    .stButton > button:active { transform: translateY(2px); }

    .stButton > button[kind="primary"] {
        font-size: 1.5rem !important;
        font-weight: 800;
        min-height: 4.8rem;
        color: #FFFFFF;
        border-radius: 999px;
        background: linear-gradient(180deg, var(--terracotta) 0%, var(--terracotta-dark) 100%);
        box-shadow: 0 5px 0 var(--terracotta-darker), 0 12px 24px rgba(123,78,44,0.35);
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(4px);
        box-shadow: 0 1px 0 var(--terracotta-darker), 0 4px 10px rgba(123,78,44,0.3);
    }

    /* Kleurmomenten per spelfase (via Streamlit's automatische st-key-* klasse) */
    [class*="st-key-rounds_"] button[kind="primary"],
    [class*="st-key-next_round"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--sage) 0%, var(--sage-dark) 100%) !important;
        box-shadow: 0 5px 0 #37483B, 0 12px 24px rgba(72,95,78,0.35) !important;
    }
    [class*="st-key-confirm_"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--teal) 0%, var(--teal-dark) 100%) !important;
        box-shadow: 0 5px 0 #273D42, 0 12px 24px rgba(51,79,86,0.35) !important;
        border-radius: 16px !important;
    }
    [class*="st-key-to_ask_title"] button[kind="primary"],
    [class*="st-key-to_reveal_full"] button[kind="primary"],
    [class*="st-key-to_end"] button[kind="primary"],
    [class*="st-key-play_again"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--purple) 0%, var(--purple-dark) 100%) !important;
        box-shadow: 0 5px 0 #453742, 0 12px 24px rgba(91,72,86,0.35) !important;
    }

    .subtle-link .stButton > button {
        box-shadow: none;
        border: 2px solid #E3D4BE;
        background: transparent;
        min-height: 2.9rem;
        font-size: 1rem !important;
        font-weight: 700;
        width: auto;
        color: var(--ink-soft);
        border-radius: 999px;
    }

    .stLinkButton > a {
        min-height: 3.7rem;
        font-size: 1.22rem !important;
        font-weight: 800;
        border-radius: 999px !important;
        background: #1DB954 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 0 #14883C, 0 10px 20px rgba(29,185,84,0.3) !important;
    }

    /* ---------- Schuifregelaar ---------- */
    [data-testid="stSlider"] [role="slider"] {
        width: 32px !important; height: 32px !important;
        background: var(--terracotta) !important;
        border: 4px solid #FFFFFF !important;
        box-shadow: 0 0 0 5px rgba(224,142,81,0.25), 0 3px 8px rgba(0,0,0,0.2) !important;
    }
    [data-testid="stSlider"] > div > div > div > div { background: var(--terracotta) !important; }
    [data-testid="stSlider"] > div > div > div { background: #E3D4BE !important; height: 8px !important; border-radius: 999px !important; }
    [data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"], [data-testid="stThumbValue"] { display: none !important; }

    /* ---------- Kaarten ---------- */
    .card {
        background: var(--card); border-radius: 24px; padding: 2rem 1.6rem;
        box-shadow: 0 3px 0 #E3D4BE, 0 14px 30px var(--shadow); margin-bottom: 1.3rem;
    }
    .mystery-card {
        background: var(--card); border-radius: 26px; padding: 2.1rem 1.5rem 1.7rem;
        text-align: center; box-shadow: 0 3px 0 #E3D4BE, 0 14px 30px var(--shadow);
        margin-bottom: 1.2rem; position: relative; margin-top: 2.8rem;
    }
    .reveal-card {
        background: var(--card); border-radius: 26px; padding: 2rem 1.5rem 2.1rem;
        text-align: center; box-shadow: 0 3px 0 #E3D4BE, 0 16px 34px var(--shadow); margin-bottom: 1.1rem;
    }
    .reveal-card img { border-radius: 16px; box-shadow: 0 8px 20px rgba(61,46,31,0.28); }

    .result-banner { border-radius: 24px; padding: 1.5rem 1rem; text-align: center; margin-bottom: 1.1rem; box-shadow: 0 3px 0 rgba(0,0,0,0.05), 0 14px 28px var(--shadow); }
    .result-good  { background: linear-gradient(160deg, #EEF4EC 0%, #DCEAD7 100%); }
    .result-close { background: linear-gradient(160deg, #FBF1DE 0%, #F5E1BC 100%); }
    .result-far   { background: linear-gradient(160deg, #F7ECE3 0%, #EFDACB 100%); }

    .hero-year { font-family: 'Nunito', sans-serif; font-weight: 900; font-size: 4.6rem; line-height: 1; margin: 0.4rem 0; }

    .score-badge {
        display: inline-block; background: linear-gradient(180deg, var(--terracotta) 0%, var(--terracotta-dark) 100%);
        color: #FFFFFF; font-size: 1.4rem; font-weight: 800; padding: 0.55rem 1.6rem; border-radius: 999px;
        margin-top: 0.6rem; box-shadow: 0 4px 0 var(--terracotta-darker), 0 8px 16px rgba(123,78,44,0.35);
    }
    .decade-badge { display: inline-block; color: #FFFFFF; font-weight: 800; font-size: 1.02rem; padding: 0.3rem 1.1rem; border-radius: 999px; box-shadow: 0 3px 6px rgba(0,0,0,0.16); }
    .guess-window-label { text-align: center; font-family: 'Nunito', sans-serif; font-size: 2.9rem !important; font-weight: 900; color: var(--terracotta-dark); margin: 0.2rem 0 0.7rem 0; }
    .progress-dots { text-align: center; font-size: 1.15rem; letter-spacing: 8px; margin-bottom: 0.3rem; color: var(--terracotta); }
    .kicker { text-align: center; text-transform: uppercase; letter-spacing: 3px; font-size: 0.82rem !important; font-weight: 800; color: var(--teal); margin-bottom: 0.1rem; }
    .subtitle { text-align: center; font-size: 1.24rem !important; color: var(--ink-soft); font-weight: 600; }
    .subtle-link { text-align: center; margin-top: 2rem; opacity: 0.8; }
    .timeline-strip { height: 10px; border-radius: 999px; margin: 0.8rem 0 0.2rem 0; background: linear-gradient(90deg, var(--sage), var(--terracotta), var(--purple), var(--teal)); opacity: 0.85; }

    /* ---------- Vintage polaroid-foto (decoratief, gebruikersfoto's) ---------- */
    .polaroid {
        background: #FFFDF9; padding: 10px 10px 34px 10px; border-radius: 4px;
        box-shadow: 0 10px 24px rgba(61,46,31,0.28); display: inline-block;
    }
    .polaroid img { display: block; border-radius: 2px; }

    /* ---------- Vinylplaat 'hangend' bovenaan de raad-kaart ---------- */
    .vinyl-hang {
        width: 108px; height: 108px; border-radius: 50%; position: absolute;
        top: -42px; left: 50%; transform: translateX(-50%) rotate(-8deg);
        background: radial-gradient(circle at center, var(--terracotta) 0 20%, #201A14 20% 22%, #2E2620 22% 100%);
        box-shadow: 0 10px 22px rgba(0,0,0,0.38);
    }
    .vinyl-hang::after {
        content: ""; position: absolute; inset: 44px; border-radius: 50%;
        background: radial-gradient(circle at center, #FBF4E9 0 32%, var(--terracotta) 32% 100%);
    }

    /* ---------- Kleine muzieknoot-accenten ---------- */
    .note-accent { position: absolute; font-family: 'Nunito', sans-serif; font-size: 1.4rem; opacity: 0.55; }

    /* ---------- Decoratieve hoekfoto (klein, gekanteld) ---------- */
    .corner-photo {
        position: absolute; border-radius: 4px; box-shadow: 0 8px 20px rgba(61,46,31,0.3);
        border: 6px solid #FFFDF9;
    }

    /* ---------- Sticker-badge ('Veel plezier!'-stijl) ---------- */
    .sticker-badge {
        display: inline-block; background: var(--cream-light); border: 2px dashed var(--terracotta);
        border-radius: 50%; width: 92px; height: 92px; text-align: center;
        font-weight: 800; font-size: 0.92rem; color: var(--terracotta-dark);
        display: flex; align-items: center; justify-content: center; line-height: 1.2;
        box-shadow: 0 6px 14px var(--shadow); transform: rotate(6deg);
    }

    /* ---------- Tabs (beheerscherm) ---------- */
    .stTabs [data-baseweb="tab-list"] { gap: 0.4rem; background: #FFFFFF; padding: 0.4rem; border-radius: 999px; box-shadow: 0 3px 0 #E3D4BE, 0 8px 18px var(--shadow); }
    .stTabs [data-baseweb="tab"] { border-radius: 999px; font-weight: 800; font-size: 1rem; color: var(--ink-soft); padding: 0.6rem 1.1rem; }
    .stTabs [aria-selected="true"] { background: linear-gradient(180deg, var(--purple) 0%, var(--purple-dark) 100%) !important; color: #FFFFFF !important; }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

    input, textarea, [data-baseweb="select"] > div { font-size: 1.1rem !important; border-radius: 12px !important; border-color: #E3D4BE !important; }
    input:focus, textarea:focus { border-color: var(--terracotta) !important; box-shadow: 0 0 0 3px rgba(224,142,81,0.2) !important; }

    [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 18px !important; border-color: #EEE2CE !important; box-shadow: 0 2px 0 #E3D4BE, 0 6px 16px rgba(61,46,31,0.08); }
    [data-testid="stExpander"] { border-radius: 16px !important; border-color: #EEE2CE !important; }
</style>
"""


def inject_custom_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def bg_photo_style(filename: str, opacity: float = 1.0) -> str:
    """Geef een CSS background-image url() voor een asset, of lege string als het ontbreekt."""
    uri = get_data_uri(filename)
    if not uri:
        return ""
    return f"background-image: url('{uri}'); background-size: cover; background-position: center; opacity: {opacity};"
