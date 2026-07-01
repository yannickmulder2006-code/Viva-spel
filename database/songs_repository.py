"""
database/songs_repository.py
------------------------------
Alle databasetoegang voor de tabel `songs` is hier gebundeld. De rest van de
app praat nooit rechtstreeks met Supabase, maar altijd via deze functies.
Dat maakt het makkelijk om later bijvoorbeeld caching, logging of een andere
database toe te voegen zonder de UI-code te hoeven aanpassen.
"""

from __future__ import annotations

import random
import uuid
from typing import Optional

from supabase import Client

from models import Song

TABLE = "songs"


class SongRepositoryError(RuntimeError):
    """Nette foutklasse voor problemen bij het opslaan/ophalen van liedjes."""


class DuplicateSongError(SongRepositoryError):
    """Wordt gegooid wanneer een liedje al in de bibliotheek staat."""


def _normalise(text: str) -> str:
    """Maak titel/artiest vergelijkbaar: kleine letters, geen dubbele spaties."""
    return " ".join(text.strip().lower().split())


def find_existing_song(client: Client, title: str, artist: str) -> Song | None:
    """
    Zoek of er al een liedje met dezelfde titel + artiest bestaat.

    We vergelijken genormaliseerd (hoofdletterongevoelig, spaties opgeschoond)
    zodat 'Geef Mij Maar Amsterdam' en 'geef mij  maar amsterdam' als
    hetzelfde worden gezien. Ook uitgeschakelde liedjes tellen mee, zodat een
    liedje niet twee keer in de database belandt.
    """
    target = (_normalise(title), _normalise(artist))
    for song in get_all_songs(client, active_only=False):
        if (_normalise(song.title), _normalise(song.artist)) == target:
            return song
    return None


def get_all_songs(client: Client, active_only: bool = True) -> list[Song]:
    """Haal alle liedjes op, standaard alleen de actieve."""
    try:
        query = client.table(TABLE).select("*").order("decade").order("year")
        if active_only:
            query = query.eq("active", True)
        response = query.execute()
        return [Song.from_row(row) for row in (response.data or [])]
    except Exception as exc:
        raise SongRepositoryError(f"Kon liedjes niet ophalen: {exc}") from exc


def get_random_songs(
    client: Client,
    amount: int,
    decades: Optional[list[int]] = None,
) -> list[Song]:
    """
    Kies willekeurige, actieve liedjes, optioneel gefilterd op decennium.

    Supabase/PostgREST ondersteunt geen `ORDER BY random()` via de fluent API,
    dus we halen de (doorgaans beperkte) set actieve liedjes op en husselen
    die vervolgens in Python. Voor een bibliotheek van enkele honderden
    liedjes is dit ruim snel genoeg.
    """
    songs = get_all_songs(client, active_only=True)
    if decades:
        songs = [song for song in songs if song.decade in decades]

    if not songs:
        return []

    random.shuffle(songs)
    return songs[: min(amount, len(songs))]


def count_songs(client: Client, active_only: bool = True) -> int:
    return len(get_all_songs(client, active_only=active_only))


def add_song(client: Client, song: Song) -> Song:
    """
    Voeg een nieuw liedje toe aan de bibliotheek.

    Gooit DuplicateSongError als er al een liedje met dezelfde titel + artiest
    bestaat, zodat de bibliotheek schoon blijft.
    """
    existing = find_existing_song(client, song.title, song.artist)
    if existing is not None:
        raise DuplicateSongError(
            f"'{song.title}' van {song.artist} staat al in de bibliotheek."
        )
    try:
        response = client.table(TABLE).insert(song.to_insert_dict()).execute()
        rows = response.data or []
        if not rows:
            raise SongRepositoryError("Supabase gaf geen bevestiging terug na het toevoegen.")
        return Song.from_row(rows[0])
    except (SongRepositoryError, DuplicateSongError):
        raise
    except Exception as exc:
        raise SongRepositoryError(f"Kon liedje niet opslaan: {exc}") from exc


def update_song(client: Client, song_id: str, fields: dict) -> None:
    """Werk losse velden van een bestaand liedje bij (bv. audio_url of active)."""
    try:
        client.table(TABLE).update(fields).eq("id", song_id).execute()
    except Exception as exc:
        raise SongRepositoryError(f"Kon liedje niet bijwerken: {exc}") from exc


def set_song_active(client: Client, song_id: str, active: bool) -> None:
    update_song(client, song_id, {"active": active})


def delete_song(client: Client, song_id: str) -> None:
    """Verwijder een liedje definitief. Gebruik bij voorkeur set_song_active(False)."""
    try:
        client.table(TABLE).delete().eq("id", song_id).execute()
    except Exception as exc:
        raise SongRepositoryError(f"Kon liedje niet verwijderen: {exc}") from exc


def _upload_to_bucket(
    client: Client,
    bucket: str,
    file_bytes: bytes,
    original_filename: str,
    allowed_extensions: set[str],
    default_extension: str,
    content_type_prefix: str,
) -> str:
    """Generieke upload naar Supabase Storage; geeft de publieke URL terug."""
    extension = (
        original_filename.rsplit(".", 1)[-1].lower()
        if "." in original_filename
        else default_extension
    )
    safe_extension = extension if extension in allowed_extensions else default_extension
    storage_path = f"{uuid.uuid4().hex}.{safe_extension}"

    try:
        client.storage.from_(bucket).upload(
            storage_path,
            file_bytes,
            {"content-type": f"{content_type_prefix}/{safe_extension}"},
        )
        return client.storage.from_(bucket).get_public_url(storage_path)
    except Exception as exc:
        raise SongRepositoryError(f"Kon bestand niet uploaden: {exc}") from exc


def upload_audio_fragment(
    client: Client, bucket: str, file_bytes: bytes, original_filename: str
) -> str:
    """Upload een audiofragment en geef de publieke URL terug."""
    return _upload_to_bucket(
        client,
        bucket,
        file_bytes,
        original_filename,
        allowed_extensions={"mp3", "wav", "ogg", "m4a"},
        default_extension="mp3",
        content_type_prefix="audio",
    )


def upload_image(
    client: Client, bucket: str, file_bytes: bytes, original_filename: str
) -> str:
    """Upload een afbeelding (sfeerfoto/hoesje) en geef de publieke URL terug."""
    return _upload_to_bucket(
        client,
        bucket,
        file_bytes,
        original_filename,
        allowed_extensions={"jpg", "jpeg", "png", "webp"},
        default_extension="jpg",
        content_type_prefix="image",
    )

