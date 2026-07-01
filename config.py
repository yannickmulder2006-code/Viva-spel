"""
config.py
---------
Centrale plek voor alle configuratie en environment variables.

Alle geheime sleutels (Supabase, Spotify, admin-pin) worden NOOIT hardcoded
in de code, maar altijd geladen uit environment variables. Lokaal gebruik je
daarvoor een .env bestand (zie .env.example), op Streamlit Cloud gebruik je
de ingebouwde "Secrets"-manager.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Laad variabelen uit een lokaal .env bestand (indien aanwezig).
# Op Streamlit Cloud worden secrets automatisch als environment variables
# beschikbaar gemaakt, dus deze regel is dan onschadelijk (er is geen .env).
load_dotenv()


def _get_env(key: str, default: str | None = None, required: bool = False) -> str | None:
    """Haal een environment variable op, met nette foutmelding indien verplicht."""
    value = os.environ.get(key, default)
    if required and not value:
        raise RuntimeError(
            f"Verplichte environment variable '{key}' ontbreekt.\n"
            f"Maak een .env bestand aan (zie .env.example) of stel dit in "
            f"via Streamlit Secrets bij het deployen."
        )
    return value


@dataclass(frozen=True)
class Settings:
    # --- Supabase ---
    supabase_url: str
    supabase_key: str

    # --- Spotify (Client Credentials flow, alleen voor zoeken/metadata) ---
    spotify_client_id: str | None
    spotify_client_secret: str | None

    # --- Beveiliging beheerscherm ---
    admin_pin: str

    # --- Spelinstellingen ---
    min_year: int = 1950
    max_year: int = 2025
    default_rounds: int = 10
    audio_bucket: str = "song-audio"

    @property
    def spotify_configured(self) -> bool:
        return bool(self.spotify_client_id and self.spotify_client_secret)


def load_settings() -> Settings:
    """Laad en valideer alle instellingen. Wordt één keer aangeroepen vanuit app.py."""
    return Settings(
        supabase_url=_get_env("SUPABASE_URL", required=True),
        supabase_key=_get_env("SUPABASE_KEY", required=True),
        spotify_client_id=_get_env("SPOTIFY_CLIENT_ID"),
        spotify_client_secret=_get_env("SPOTIFY_CLIENT_SECRET"),
        admin_pin=_get_env("ADMIN_PIN", default="1234"),
        min_year=int(_get_env("APP_MIN_YEAR", default="1950")),
        max_year=int(_get_env("APP_MAX_YEAR", default="2025")),
        default_rounds=int(_get_env("APP_DEFAULT_ROUNDS", default="10")),
    )
