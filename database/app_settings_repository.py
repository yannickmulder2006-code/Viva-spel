"""
database/app_settings_repository.py
-------------------------------------
Kleine key-value opslag voor personalisatie-instellingen van de app, zoals:
  - welcome_title      : de titel op het startscherm
  - welcome_subtitle   : de ondertitel op het startscherm
  - hero_image_url     : sfeerfoto op het startscherm (zelf te uploaden)
  - reveal_image_url   : optionele sfeerfoto op het onthulscherm

Zo kan de instelling (bv. een zorglocatie) de app opfleuren met EIGEN
materiaal (eigen sfeerfoto's, eigen tekst), zonder dat er extern beschermd
beeld- of merkmateriaal in de broncode zit.
"""

from __future__ import annotations

from supabase import Client

TABLE = "app_settings"


class AppSettingsError(RuntimeError):
    pass


DEFAULTS: dict[str, str] = {
    "welcome_title": "Raad het Jaartal!",
    "welcome_subtitle": "Herkent u de liedjes van vroeger?",
    "hero_image_url": "",
    "reveal_image_url": "",
}


def get_all_settings(client: Client) -> dict[str, str]:
    """Haal alle instellingen op als dict, aangevuld met standaardwaarden."""
    result = dict(DEFAULTS)
    try:
        response = client.table(TABLE).select("*").execute()
        for row in response.data or []:
            key = row.get("key")
            if key:
                result[key] = row.get("value") or ""
    except Exception:
        # Als de tabel (nog) niet bestaat, val netjes terug op de standaarden.
        pass
    return result


def set_setting(client: Client, key: str, value: str) -> None:
    """Sla één instelling op (insert of update)."""
    try:
        client.table(TABLE).upsert({"key": key, "value": value}).execute()
    except Exception as exc:
        raise AppSettingsError(f"Kon instelling '{key}' niet opslaan: {exc}") from exc
