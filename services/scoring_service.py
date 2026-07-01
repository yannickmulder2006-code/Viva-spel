"""
services/scoring_service.py
------------------------------
Bepaalt hoeveel punten een gok oplevert. De scoring is bewust vergevingsgezind
opgezet: ook een gok die er flink naast zit levert nog iets op, zodat spelers
altijd een succeservaring overhouden - dit is een expliciete eis vanuit de
ouderenzorg-context van deze app.

De speler kiest via een schuifregelaar EEN jaartal. Omdat exact het juiste
jaar raden lastig is, is er een kleine marge ingebouwd (tot 1 jaar ernaast
telt nog als voltreffer - dit sluit aan bij de oorspronkelijke wens van een
"bandbreedte van 3 jaar"). Scoring op basis van hoeveel jaar de gok van het
echte jaar afligt:

    * 0-1 jaar ernaast   -> 100 punten ("Precies goed!")
    * 2-3 jaar ernaast   ->  70 punten ("Heel dichtbij!")
    * 4-7 jaar ernaast   ->  40 punten ("Goed gegokt!")
    * 8-15 jaar ernaast  ->  20 punten ("Een eind ernaast")
    * meer dan 15 jaar   ->   5 punten (troostpunten)
"""

from __future__ import annotations

from dataclasses import dataclass

BULLSEYE_MARGIN = 1  # tot en met 1 jaar ernaast telt nog als voltreffer


@dataclass(frozen=True)
class ScoreOutcome:
    points: int
    distance: int
    message: str


# (maximale afstand, punten, boodschap) - eerste passende rij wint
_TIERS: list[tuple[int, int, str]] = [
    (BULLSEYE_MARGIN, 100, "Precies goed! Wat een geheugen!"),
    (3, 70, "Heel dichtbij! Bijna raak!"),
    (7, 40, "Goed gegokt, niet ver ernaast!"),
    (15, 20, "Een eind ernaast, maar knap geprobeerd!"),
]
_CONSOLATION_POINTS = 5
_CONSOLATION_MESSAGE = "Deze was pittig! Volgende keer beter."


def calculate_score(actual_year: int, guess_center: int) -> ScoreOutcome:
    """Bereken score op basis van het echte jaar en het geraden jaar."""
    distance = abs(actual_year - guess_center)

    for max_distance, points, message in _TIERS:
        if distance <= max_distance:
            return ScoreOutcome(points=points, distance=distance, message=message)

    return ScoreOutcome(points=_CONSOLATION_POINTS, distance=distance, message=_CONSOLATION_MESSAGE)
