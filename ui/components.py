"""
ui/components.py
------------------
Herbruikbare visuele bouwstenen. Bevat ook twee eigen (auteursrechtvrije)
illustraties als inline SVG/CSS: een jukebox voor het startscherm en een
draaiende vinylplaat voor de raad-kaart - dit zijn zelf ontworpen vormen,
geen extern beeldmateriaal.
"""

from __future__ import annotations

import streamlit as st


def progress_dots(current: int, total: int) -> None:
    filled = "\u25CF" * current
    empty = "\u25CB" * max(total - current, 0)
    st.markdown(f'<div class="progress-dots">{filled}{empty}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center; font-weight:800; color:#5B5270;">'
        f"Liedje {current} van {total}</p>",
        unsafe_allow_html=True,
    )


def mystery_card() -> None:
    st.markdown(
        """
        <div class="mystery-card">
            <div class="vinyl-wrap">
                <div class="vinyl"></div>
                <div class="vinyl-note n1">&#9835;</div>
                <div class="vinyl-note n2">&#9834;</div>
            </div>
            <h3 style="margin-top:0.2rem; margin-bottom:0.3rem;">Luister goed mee!</h3>
            <p style="margin:0;">Uit welk jaar komt dit liedje?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def jukebox_illustration() -> None:
    """Eigen (auteursrechtvrije) jukebox-illustratie voor het startscherm."""
    st.markdown(
        """
        <div class="jukebox-wrap">
        <svg width="200" height="190" viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="jbBody" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#8B5CF6"/>
              <stop offset="100%" stop-color="#6633CC"/>
            </linearGradient>
            <linearGradient id="jbDome" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#FF6B57"/>
              <stop offset="100%" stop-color="#D6432F"/>
            </linearGradient>
          </defs>
          <ellipse cx="100" cy="178" rx="70" ry="8" fill="#2B2440" opacity="0.10"/>
          <path d="M35 90 a65 65 0 0 1 130 0 v70 a10 10 0 0 1 -10 10 h-110 a10 10 0 0 1 -10 -10 z" fill="url(#jbBody)"/>
          <path d="M45 90 a55 55 0 0 1 110 0 v8 h-110 z" fill="url(#jbDome)"/>
          <rect x="55" y="100" width="90" height="52" rx="12" fill="#FFF8F0"/>
          <circle cx="100" cy="126" r="20" fill="#2E2740"/>
          <circle cx="100" cy="126" r="7" fill="#FFB238"/>
          <rect x="55" y="163" width="16" height="14" rx="5" fill="#FFB238"/>
          <rect x="75" y="163" width="16" height="14" rx="5" fill="#17B8A6"/>
          <rect x="95" y="163" width="16" height="14" rx="5" fill="#FF6B57"/>
          <rect x="115" y="163" width="16" height="14" rx="5" fill="#8B5CF6"/>
          <text x="100" y="45" font-family="Fredoka, sans-serif" font-size="22" font-weight="700"
                text-anchor="middle" fill="#8B5CF6">&#9835;</text>
          <text x="140" y="30" font-family="Fredoka, sans-serif" font-size="18" font-weight="700"
                text-anchor="middle" fill="#17B8A6">&#9834;</text>
        </svg>
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
    if url:
        st.markdown(
            f'<img src="{url}" class="hero-image" style="width:100%;" alt="sfeerbeeld" />',
            unsafe_allow_html=True,
        )


def subtle_admin_link_button() -> bool:
    st.markdown('<div class="subtle-link">', unsafe_allow_html=True)
    clicked = st.button("\u2699\uFE0F Beheerder", key="admin_entry_button", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked
