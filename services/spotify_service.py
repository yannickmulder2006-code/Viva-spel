"""
services/spotify_service.py
-----------------------------
Integratie met de Spotify Web API (Client Credentials flow).

BELANGRIJK — waarom we Spotify alléén gebruiken voor het OPZOEKEN van
liedjes (titel, artiest, jaartal, hoesfoto) en niet voor het afspelen:

Sinds 27 november 2024 geeft de Spotify Web API voor NIEUWE apps geen
`preview_url` (het korte 30-seconden fragment) meer terug — dit veld komt
altijd leeg (null) terug. Spotify heeft dit zelf aangekondigd en dit is
niet iets wat wij kunnen omzeilen. Zie:
https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api

Daarom werkt deze app als volgt:
1. De beheerder zoekt een liedje op via Spotify (deze module) om snel en
   foutloos de juiste titel, artiest, jaartal en hoesfoto binnen te halen.
2. Voor het daadwerkelijk afspelen tijdens het spel uploadt de beheerder
   zelf een kort audiofragment (mp3), dat via Supabase Storage wordt
   opgeslagen (zie database/songs_repository.py::upload_audio_fragment).
   Zo blijft de audio volledig binnen onze eigen controle — inclusief het
   verbergen van titel/artiest tijdens het raden.
3. Na het raden kan de speler via de "Luister op Spotify"-link het hele
   nummer beluisteren in de Spotify-app.

Dit is geen tijdelijke workaround maar de aanbevolen, robuuste aanpak
gegeven de huidige beperkingen van de Spotify API.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import requests
import streamlit as st

TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"


class SpotifyServiceError(RuntimeError):
    pass


@dataclass
class SpotifyTrack:
    spotify_track_id: str
    title: str
    artist: str
    year: int
    album_art_url: str | None
    spotify_url: str


class SpotifyService:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token: str | None = None
        self._token_expires_at: float = 0.0

    # ------------------------------------------------------------------
    # Authenticatie
    # ------------------------------------------------------------------
    def _get_access_token(self) -> str:
        """Haal een access token op (Client Credentials flow) en cache 'm tot vervaldatum."""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token

        try:
            response = requests.post(
                TOKEN_URL,
                data={"grant_type": "client_credentials"},
                auth=(self._client_id, self._client_secret),
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SpotifyServiceError(
                "Kon niet inloggen bij Spotify. Controleer SPOTIFY_CLIENT_ID en "
                "SPOTIFY_CLIENT_SECRET, en je internetverbinding."
            ) from exc

        payload = response.json()
        self._access_token = payload["access_token"]
        # Trek 30 seconden van de geldigheidsduur af als veiligheidsmarge.
        self._token_expires_at = time.time() + payload.get("expires_in", 3600) - 30
        return self._access_token

    # ------------------------------------------------------------------
    # Zoeken
    # ------------------------------------------------------------------
    def search_tracks(self, query: str, limit: int = 8) -> list[SpotifyTrack]:
        """Zoek nummers op titel/artiest en geef de belangrijkste metadata terug."""
        if not query.strip():
            return []

        token = self._get_access_token()
        try:
            response = requests.get(
                SEARCH_URL,
                headers={"Authorization": f"Bearer {token}"},
                params={"q": query, "type": "track", "limit": limit, "market": "NL"},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SpotifyServiceError(f"Zoeken op Spotify is mislukt: {exc}") from exc

        items = response.json().get("tracks", {}).get("items", [])
        results: list[SpotifyTrack] = []
        for item in items:
            year = _parse_release_year(item.get("album", {}).get("release_date", ""))
            images = item.get("album", {}).get("images", [])
            album_art_url = images[0]["url"] if images else None
            artists = ", ".join(a["name"] for a in item.get("artists", []))
            results.append(
                SpotifyTrack(
                    spotify_track_id=item["id"],
                    title=item.get("name", "Onbekende titel"),
                    artist=artists or "Onbekende artiest",
                    year=year,
                    album_art_url=album_art_url,
                    spotify_url=item.get("external_urls", {}).get("spotify", ""),
                )
            )
        return results


def _parse_release_year(release_date: str) -> int:
    """Spotify geeft 'YYYY', 'YYYY-MM' of 'YYYY-MM-DD' terug — pak altijd het jaar."""
    if not release_date:
        return 1980
    try:
        return int(release_date[:4])
    except ValueError:
        return 1980


@st.cache_resource(show_spinner=False)
def get_spotify_service(client_id: str, client_secret: str) -> SpotifyService:
    """Cache één SpotifyService-instantie per client_id/secret combinatie."""
    return SpotifyService(client_id, client_secret)
