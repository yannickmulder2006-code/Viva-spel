"""
models.py
---------
Lichte dataclasses die de belangrijkste entiteiten uit de database
representeren binnen de Python-code. Dit maakt de rest van de code
leesbaar en type-veilig, zonder dat we een zware ORM nodig hebben.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


def _decade_for_year(year: int) -> int:
    """Rond een jaartal af naar het decennium waartoe het behoort, bv. 1987 -> 1980."""
    return (year // 10) * 10


@dataclass
class Song:
    """Eén liedje in de spelbibliotheek."""

    id: Optional[str] = None
    title: str = ""
    artist: str = ""
    year: int = 1980
    decade: int = field(init=False, default=1980)
    spotify_track_id: Optional[str] = None
    spotify_url: Optional[str] = None
    album_art_url: Optional[str] = None
    audio_url: Optional[str] = None
    active: bool = True
    added_by: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self) -> None:
        self.decade = _decade_for_year(self.year)

    @property
    def has_playable_audio(self) -> bool:
        return bool(self.audio_url)

    @property
    def display_name(self) -> str:
        return f"{self.title} — {self.artist}"

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "Song":
        return cls(
            id=row.get("id"),
            title=row.get("title", ""),
            artist=row.get("artist", ""),
            year=int(row.get("year", 1980)),
            spotify_track_id=row.get("spotify_track_id"),
            spotify_url=row.get("spotify_url"),
            album_art_url=row.get("album_art_url"),
            audio_url=row.get("audio_url"),
            active=row.get("active", True),
            added_by=row.get("added_by"),
            created_at=row.get("created_at"),
        )

    def to_insert_dict(self) -> dict[str, Any]:
        """Dict klaar om als nieuwe rij in Supabase te worden ingevoegd."""
        return {
            "title": self.title.strip(),
            "artist": self.artist.strip(),
            "year": self.year,
            "decade": self.decade,
            "spotify_track_id": self.spotify_track_id,
            "spotify_url": self.spotify_url,
            "album_art_url": self.album_art_url,
            "audio_url": self.audio_url,
            "active": self.active,
            "added_by": self.added_by,
        }


@dataclass
class RoundResult:
    """Resultaat van één ronde binnen een spelsessie (nog niet per se opgeslagen)."""

    song: Song
    guess_center: int
    guess_low: int
    guess_high: int
    points: int
    message: str


@dataclass
class GameSession:
    id: Optional[str] = None
    group_name: str = ""
    total_rounds: int = 10
    total_score: int = 0
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "GameSession":
        return cls(
            id=row.get("id"),
            group_name=row.get("group_name") or "",
            total_rounds=row.get("total_rounds", 0),
            total_score=row.get("total_score", 0),
            started_at=row.get("started_at"),
            ended_at=row.get("ended_at"),
        )
