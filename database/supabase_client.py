"""
database/supabase_client.py
----------------------------
Maakt één herbruikbare Supabase-client aan. We gebruiken Streamlit's
`st.cache_resource` zodat er niet bij elke herlaad-actie van de pagina
een nieuwe connectie wordt opgezet.
"""

from __future__ import annotations

import streamlit as st
from supabase import Client, create_client

from config import Settings


class SupabaseConnectionError(RuntimeError):
    """Wordt gegooid wanneer er geen verbinding met Supabase gemaakt kan worden."""


@st.cache_resource(show_spinner=False)
def get_supabase_client(supabase_url: str, supabase_key: str) -> Client:
    """
    Maak (of hergebruik) een Supabase-client.

    We geven url/key als losse parameters mee (in plaats van het Settings-object)
    omdat st.cache_resource de argumenten moet kunnen hashen — een dataclass met
    alleen strings/ints is prima te hashen, maar dit maakt de cache-sleutel expliciet.
    """
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as exc:  # pragma: no cover - defensieve foutafhandeling
        raise SupabaseConnectionError(
            "Kon geen verbinding maken met Supabase. Controleer of SUPABASE_URL "
            "en SUPABASE_KEY correct zijn ingesteld."
        ) from exc


def get_client(settings: Settings) -> Client:
    """Handige wrapper die direct het Settings-object accepteert."""
    return get_supabase_client(settings.supabase_url, settings.supabase_key)
