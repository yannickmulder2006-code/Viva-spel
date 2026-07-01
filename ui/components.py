"""
ui/components.py
------------------
Kleine, herbruikbare visuele bouwstenen die op meerdere schermen worden
gebruikt. Door dit hier te bundelen blijven de view-bestanden overzichtelijk.
"""

from __future__ import annotations

import streamlit as st


def progress_dots(current: int, total: int) -> None:
    """Toon voortgang als bolletjes, bv. filled/empty, plus 'Liedje 3 van 10'."""
    filled = "\u25CF" * current
    empty = "\u25CB" * max(total - current, 0)
    st.markdown(f'<div class="progress-dots">{filled}{empty}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center; font-weight:700; color:#6B5B4B;">'
        f"Liedje {current} van {total}</p>",
        unsafe_allow_html=True,
    )


def mystery_card() -> None:
    st.markdown(
        """
        <div class="mystery-card">
            <div class="vinyl"></div>
            <h3 style="margin-top:0.3rem; margin-bottom:0.3rem;">Luister goed mee!</h3>
            <p style="margin:0;">Uit welk jaar komt dit liedje?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_badge(points: int, label: str = "punten") -> None:
    st.markdown(
        f'<div style="text-align:center;"><span class="score-badge">+{points} {label}</span></div>',
        unsafe_allow_html=True,
    )


def big_spacer(height_rem: float = 1.0) -> None:
    st.markdown(f'<div style="height:{height_rem}rem;"></div>', unsafe_allow_html=True)


def hero_image(url: str) -> None:
    """Toon een sfeerbeeld bovenaan (indien ingesteld door de beheerder)."""
    if url:
        st.markdown(
            f'<img src="{url}" class="hero-image" style="width:100%;" alt="sfeerbeeld" />',
            unsafe_allow_html=True,
        )


def subtle_admin_link_button() -> bool:
    """Klein, onopvallend knopje onderaan het startscherm voor de beheerder."""
    st.markdown('<div class="subtle-link">', unsafe_allow_html=True)
    clicked = st.button("\u2699\uFE0F Beheerder", key="admin_entry_button", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked
