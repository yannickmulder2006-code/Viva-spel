"""
ui/assets.py
-------------
Laadt lokale afbeeldingen (in de map assets/) en zet ze om naar base64
data-URI's, zodat ze direct in CSS/HTML gebruikt kunnen worden.

Waarom geen Streamlit static-file-serving (de 'static/' map + enableStaticServing)?
Die functie bestaat en werkt, maar hangt af van een exacte mapnaam en een
losse configuratie-instelling die op afstand lastig te controleren is als
er iets misgaat. Deze aanpak leest de bestanden gewoon in met normale
Python-bestandstoegang: geen aparte instelling nodig, werkt identiek lokaal
en op Streamlit Cloud, en kan nooit "per ongeluk uitstaan".

De afbeeldingen zijn met matige kwaliteit (JPEG ~84%) en beperkte afmetingen
opgeslagen zodat de pagina snel blijft laden.
"""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


@st.cache_data(show_spinner=False)
def get_data_uri(filename: str) -> str | None:
    """
    Geef een 'data:image/...;base64,...'-string voor een bestand in assets/.
    Geeft None terug als het bestand niet bestaat, zodat de UI-code netjes
    kan terugvallen op een alternatief (bv. geen decoratieve foto tonen).
    """
    path = ASSETS_DIR / filename
    if not path.exists():
        return None

    mime = _MIME_TYPES.get(path.suffix.lower(), "image/jpeg")
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"
