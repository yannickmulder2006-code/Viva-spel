"""
scripts/seed_database.py
---------------------------
Eenmalig (of herhaaldelijk, dat kan geen kwaad) uit te voeren script dat de
voorbeeld-liedjes uit data/seed_songs.csv in de Supabase-database zet.

Gebruik (vanuit de hoofdmap van het project):

    python -m scripts.seed_database

Vereist dat SUPABASE_URL en SUPABASE_KEY zijn ingesteld (.env bestand).

Let op: dit script vult alleen titel, artiest en jaartal. Er worden geen
geluidsfragmenten meegeleverd (dat mogen we vanwege auteursrecht niet
bijleveren) — voeg die later toe via het beheerscherm in de app.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

# Zorg dat de hoofdmap van het project op het pad staat, ook als dit
# script direct wordt aangeroepen vanuit de scripts/-map.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import load_settings  # noqa: E402
from database.songs_repository import DuplicateSongError, add_song, get_all_songs  # noqa: E402
from database.supabase_client import get_client  # noqa: E402
from models import Song  # noqa: E402

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "seed_songs.csv"


def main() -> None:
    print("Instellingen laden...")
    settings = load_settings()
    client = get_client(settings)

    print("Bestaande liedjes ophalen om dubbele invoer te voorkomen...")
    existing = get_all_songs(client, active_only=False)
    existing_keys = {(s.title.strip().lower(), s.artist.strip().lower()) for s in existing}

    added, skipped = 0, 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            title = row["title"].strip()
            artist = row["artist"].strip()
            key = (title.lower(), artist.lower())

            if key in existing_keys:
                skipped += 1
                continue

            song = Song(
                title=title,
                artist=artist,
                year=int(row["year"]),
                spotify_url=row.get("spotify_url") or None,
                album_art_url=row.get("album_art_url") or None,
                added_by="seed-script",
            )
            try:
                add_song(client, song)
                added += 1
                print(f"  + {title} — {artist} ({song.year})")
            except DuplicateSongError:
                skipped += 1
            except Exception as exc:  # noqa: BLE001
                print(f"  ! Overgeslagen wegens fout: {title} — {artist}: {exc}")

    print(f"\nKlaar! {added} liedjes toegevoegd, {skipped} al aanwezig.")
    print(
        "Vergeet niet: ga naar het beheerscherm in de app om bij elk liedje "
        "een kort geluidsfragment te uploaden, zodat ze speelbaar zijn."
    )


if __name__ == "__main__":
    main()
