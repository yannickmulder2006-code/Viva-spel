"""
ui/components.py
------------------
Herbruikbare visuele bouwstenen. Combineert eigen SVG-tekenwerk (jukebox,
vinylplaat) met de aangeleverde vintage sfeerfoto's (via ui/assets.py).

Belangrijk: alle HTML wordt als EEN ENKELE regel zonder inspringing aan
st.markdown meegegeven. Streamlit's markdown-parser interpreteert ingesprongen
regels namelijk als codeblok, waardoor losse sluit-tags (</div>) als platte
tekst zichtbaar worden. Enkele regel zonder witruimte voorkomt dat.
"""

from __future__ import annotations

import streamlit as st

from ui.assets import get_data_uri


def progress_dots(current: int, total: int) -> None:
    filled = "\u25CF" * current
    empty = "\u25CB" * max(total - current, 0)
    st.markdown(f'<div class="progress-dots">{filled}{empty}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center; font-weight:800; color:#6B5C4D;">Liedje {current} van {total}</p>',
        unsafe_allow_html=True,
    )


def mystery_card() -> None:
    """De 'luister mee'-kaart met een hangende vinylplaat en muzieknoot-accenten."""
    html = (
        '<div class="mystery-card">'
        '<div class="vinyl-hang"></div>'
        '<span class="note-accent" style="top:-6px; left:14%;">&#9835;</span>'
        '<span class="note-accent" style="top:6px; right:16%;">&#9834;</span>'
        '<h3 class="script-heading" style="font-family:\'Pacifico\',cursive; font-size:2.2rem; '
        'font-weight:400; margin-top:0.6rem; margin-bottom:0.3rem;">Luister goed mee!</h3>'
        '<p style="margin:0;">Uit welk jaar komt dit liedje?</p>'
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def polaroid_photo(filename: str, caption: str = "", width: int = 150, rotate: int = -4) -> None:
    """Toon een vintage sfeerfoto in een polaroid-lijstje, licht gekanteld."""
    uri = get_data_uri(filename)
    if not uri:
        return
    cap = (
        f'<div style="text-align:center; font-size:0.9rem; color:#6B5C4D; padding:6px 0 2px;">{caption}</div>'
        if caption
        else '<div style="height:14px;"></div>'
    )
    html = (
        f'<div style="text-align:center; transform:rotate({rotate}deg); margin:0.4rem 0;">'
        f'<div class="polaroid">'
        f'<img src="{uri}" style="width:{width}px; height:{width}px; object-fit:cover;" />'
        f"{cap}"
        f"</div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def sticker_badge(text: str) -> None:
    st.markdown(
        f'<div style="text-align:center;"><span class="sticker-badge">{text}</span></div>',
        unsafe_allow_html=True,
    )


def jukebox_illustration() -> None:
    """Eigen jukebox-illustratie (SVG), herkleurd naar het vintage palet."""
    svg = (
        '<div style="text-align:center; margin:0.2rem 0 0.6rem 0;">'
        '<svg width="210" height="200" viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<linearGradient id="jbBody" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="#7F6578"/><stop offset="100%" stop-color="#5B4856"/></linearGradient>'
        '<linearGradient id="jbDome" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="#E08E51"/><stop offset="100%" stop-color="#A1663A"/></linearGradient>'
        '</defs>'
        '<ellipse cx="100" cy="178" rx="70" ry="8" fill="#3D2E1F" opacity="0.10"/>'
        '<path d="M35 90 a65 65 0 0 1 130 0 v70 a10 10 0 0 1 -10 10 h-110 a10 10 0 0 1 -10 -10 z" fill="url(#jbBody)"/>'
        '<path d="M45 90 a55 55 0 0 1 110 0 v8 h-110 z" fill="url(#jbDome)"/>'
        '<rect x="55" y="100" width="90" height="52" rx="12" fill="#FBF4E9"/>'
        '<circle cx="100" cy="126" r="20" fill="#3D2E1F"/><circle cx="100" cy="126" r="7" fill="#E08E51"/>'
        '<rect x="55" y="163" width="16" height="14" rx="5" fill="#E08E51"/>'
        '<rect x="75" y="163" width="16" height="14" rx="5" fill="#64846D"/>'
        '<rect x="95" y="163" width="16" height="14" rx="5" fill="#476F78"/>'
        '<rect x="115" y="163" width="16" height="14" rx="5" fill="#7F6578"/>'
        '</svg></div>'
    )
    st.markdown(svg, unsafe_allow_html=True)


def score_badge(points: int, label: str = "punten") -> None:
    st.markdown(
        f'<div style="text-align:center;"><span class="score-badge">+{points} {label}</span></div>',
        unsafe_allow_html=True,
    )


def big_spacer(height_rem: float = 1.0) -> None:
    st.markdown(f'<div style="height:{height_rem}rem;"></div>', unsafe_allow_html=True)


def hero_image(url: str) -> None:
    if url:
        st.markdown(
            f'<img src="{url}" style="width:100%; border-radius:20px; '
            f'box-shadow:0 14px 30px rgba(61,46,31,0.2); margin-bottom:1rem;" alt="sfeerbeeld" />',
            unsafe_allow_html=True,
        )


def subtle_admin_link_button() -> bool:
    st.markdown('<div class="subtle-link">', unsafe_allow_html=True)
    clicked = st.button("\u2699\uFE0F Beheerder", key="admin_entry_button", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked
