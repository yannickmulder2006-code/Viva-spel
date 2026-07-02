"""
utils.py
--------
Kleine, generieke hulpfuncties die op meerdere plekken in de app worden gebruikt.
"""

from __future__ import annotations


def decade_label(decade: int) -> str:
    """Geeft een leesbaar label voor een decennium, bv. 1980 -> 'Jaren 80'."""
    return f"Jaren {str(decade)[-2:]}"


# Kleurcodering per decennium, exact overgenomen uit het aangeleverde
# vintage-kleurenpalet (salie, terracotta, bruin, gedempt paars, petrol).
_DECADE_COLORS: dict[int, str] = {
    1950: "#74411E",  # bruin
    1960: "#A1663A",  # warme oker-bruin
    1970: "#E08E51",  # terracotta
    1980: "#7F6578",  # gedempt paars
    1990: "#476F78",  # petrol
    2000: "#64846D",  # salie
    2010: "#5B4856",  # donker paars
    2020: "#334F56",  # donker petrol
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
