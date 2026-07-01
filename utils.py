"""
utils.py
--------
Kleine, generieke hulpfuncties die op meerdere plekken in de app worden gebruikt.
"""

from __future__ import annotations


def decade_label(decade: int) -> str:
    """Geeft een leesbaar label voor een decennium, bv. 1980 -> 'Jaren 80'."""
    return f"Jaren {str(decade)[-2:]}"


# Kleurcodering per decennium (geïnspireerd op Hitster, maar met warmere,
# rustigere tinten passend bij de doelgroep). Wordt gebruikt om het
# onthulde jaartal en de decennium-badges visueel te onderscheiden.
_DECADE_COLORS: dict[int, str] = {
    1950: "#B5654A",  # terracotta
    1960: "#C98A2B",  # oker
    1970: "#8A7B3A",  # olijf/mosterd
    1980: "#7A6BB0",  # gedempt paars
    1990: "#3E8E7E",  # groenblauw
    2000: "#4A7BA6",  # blauw
    2010: "#9E4E6E",  # oudroze/bordeaux
    2020: "#5B7C6B",  # salie
}


def decade_color(decade: int) -> str:
    """Geef een rustige, warme kleur die bij een decennium hoort."""
    return _DECADE_COLORS.get(decade, "#9E4E1E")


def clamp(value: int, minimum: int, maximum: int) -> int:
    """Houd een waarde binnen een minimum en maximum."""
    return max(minimum, min(maximum, value))


def format_year_range(low: int, high: int) -> str:
    return f"{low} – {high}"


def guess_distance(actual_year: int, guess_low: int, guess_high: int) -> int:
    """
    Bereken hoe ver het echte jaar buiten de geraden 3-jaars-bandbreedte ligt.
    0 betekent: het echte jaar valt binnen de gok (voltreffer).
    """
    if guess_low <= actual_year <= guess_high:
        return 0
    if actual_year < guess_low:
        return guess_low - actual_year
    return actual_year - guess_high


def initials(name: str) -> str:
    """Geeft initialen van een naam, gebruikt voor eenvoudige weergave."""
    parts = [p for p in name.strip().split() if p]
    if not parts:
        return "?"
    return "".join(p[0].upper() for p in parts[:2])
