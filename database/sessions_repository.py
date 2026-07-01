"""
database/sessions_repository.py
---------------------------------
Alle databasetoegang voor spelsessies (`game_sessions`) en individuele
rondes daarbinnen (`session_rounds`). Dit wordt gebruikt om na afloop een
overzicht van gespeelde sessies te kunnen tonen aan de begeleider, en is
tegelijk de basis voor eventuele latere statistiek-features
(bv. "welk decennium wordt het best herkend?").
"""

from __future__ import annotations

from typing import Optional

from supabase import Client

from models import GameSession, RoundResult

SESSIONS_TABLE = "game_sessions"
ROUNDS_TABLE = "session_rounds"


class SessionRepositoryError(RuntimeError):
    pass


def create_session(client: Client, group_name: str, total_rounds: int) -> GameSession:
    try:
        response = (
            client.table(SESSIONS_TABLE)
            .insert({"group_name": group_name or None, "total_rounds": total_rounds})
            .execute()
        )
        rows = response.data or []
        if not rows:
            raise SessionRepositoryError("Geen bevestiging ontvangen bij starten sessie.")
        return GameSession.from_row(rows[0])
    except SessionRepositoryError:
        raise
    except Exception as exc:
        raise SessionRepositoryError(f"Kon spelsessie niet starten: {exc}") from exc


def save_round(client: Client, session_id: str, round_number: int, result: RoundResult) -> None:
    try:
        client.table(ROUNDS_TABLE).insert(
            {
                "session_id": session_id,
                "song_id": result.song.id,
                "round_number": round_number,
                "guessed_year_low": result.guess_low,
                "guessed_year_high": result.guess_high,
                "actual_year": result.song.year,
                "points_earned": result.points,
            }
        ).execute()
    except Exception as exc:
        raise SessionRepositoryError(f"Kon ronde niet opslaan: {exc}") from exc


def finish_session(client: Client, session_id: str, total_score: int) -> None:
    try:
        client.table(SESSIONS_TABLE).update(
            {"total_score": total_score, "ended_at": "now()"}
        ).eq("id", session_id).execute()
    except Exception as exc:
        raise SessionRepositoryError(f"Kon spelsessie niet afronden: {exc}") from exc


def get_recent_sessions(client: Client, limit: int = 20) -> list[GameSession]:
    try:
        response = (
            client.table(SESSIONS_TABLE)
            .select("*")
            .order("started_at", desc=True)
            .limit(limit)
            .execute()
        )
        return [GameSession.from_row(row) for row in (response.data or [])]
    except Exception as exc:
        raise SessionRepositoryError(f"Kon speelgeschiedenis niet ophalen: {exc}") from exc
