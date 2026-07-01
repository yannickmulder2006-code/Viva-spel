"""
app.py
------
Startpunt van de applicatie. Start lokaal met:

    streamlit run app.py

Dit bestand doet drie dingen:
1. De paginaconfiguratie en styling instellen.
2. Instellingen (environment variables) en de Supabase-verbinding laden,
   met nette foutmeldingen wanneer dat niet lukt.
3. Op basis van `st.session_state.view` bepalen of het spelscherm of het
   beheerscherm getoond moet worden.
"""

from __future__ import annotations

import streamlit as st

from config import Settings, load_settings
from database.supabase_client import SupabaseConnectionError, get_client
from ui import admin_view, game_view
from ui.styles import inject_custom_css

st.set_page_config(
    page_title="Raad het Jaartal!",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_custom_css()

ADMIN_VIEWS = {"admin_login", "admin"}


def _load_settings_safely() -> Settings | None:
    try:
        return load_settings()
    except RuntimeError as exc:
        st.markdown("## ⚠️ De app kan niet starten")
        st.error(str(exc))
        st.markdown(
            "**Wat te doen:** kopieer `.env.example` naar `.env` en vul de "
            "ontbrekende waarden in. Zie het `README.md` bestand voor een "
            "stap-voor-stap uitleg. Draai je de app op Streamlit Cloud, "
            "stel deze waarden dan in via *Settings → Secrets*."
        )
        return None


def main() -> None:
    settings = _load_settings_safely()
    if settings is None:
        return

    try:
        client = get_client(settings)
    except SupabaseConnectionError as exc:
        st.markdown("## ⚠️ Kan geen verbinding maken met de database")
        st.error(str(exc))
        return

    if "view" not in st.session_state:
        st.session_state.view = "home"

    if st.session_state.view in ADMIN_VIEWS:
        admin_view.render(client, settings)
    else:
        game_view.render(client, settings)


if __name__ == "__main__":
    main()
