"""
ui/game_view.py
-----------------
Alle schermen die de BEWONERS/SPELERS zien. De spelflow is een status-machine
op basis van st.session_state.view. Per liedje doorloopt de groep:

    play           -> raad het jaar met de schuif, bevestig
    reveal_year    -> goed/fout + het echte jaar + punten
    ask_title      -> "Weten jullie ook de titel en artiest?" (alleen bespreken)
    reveal_full    -> titel + artiest + hoesje, liedje speelt HIER automatisch af

Volledige flow:
    home -> setup -> play -> reveal_year -> ask_title -> reveal_full
         -> (play -> ...) -> end -> setup
"""

from __future__ import annotations

import random

import streamlit as st
from supabase import Client

from config import Settings
from database import app_settings_repository, sessions_repository, songs_repository
from models import RoundResult
from services.scoring_service import calculate_score
from utils import decade_color, decade_label
from ui.components import (
    big_spacer,
    hero_image,
    jukebox_illustration,
    mystery_card,
    polaroid_photo,
    progress_dots,
    score_badge,
    sticker_badge,
    subtle_admin_link_button,
)

ROUND_CHOICES = [5, 10, 15]


# ----------------------------------------------------------------------
# State
# ----------------------------------------------------------------------
def _ensure_state() -> None:
    defaults = {
        "view": "home",
        "group_name": "",
        "selected_decades": [],
        "num_rounds": 10,
        "session_id": None,
        "round_songs": [],
        "round_index": 0,
        "total_score": 0,
        "round_results": [],
        "app_settings": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _get_app_settings(client: Client) -> dict:
    if st.session_state.app_settings is None:
        st.session_state.app_settings = app_settings_repository.get_all_settings(client)
    return st.session_state.app_settings


def _reset_for_new_game() -> None:
    st.session_state.session_id = None
    st.session_state.round_songs = []
    st.session_state.round_index = 0
    st.session_state.total_score = 0
    st.session_state.round_results = []
    st.session_state.pop("play_side_photo", None)


def _start_game(client: Client, num_rounds: int) -> None:
    decades = st.session_state.selected_decades or None
    songs = songs_repository.get_random_songs(client, num_rounds, decades=decades)

    if not songs:
        st.session_state.view = "no_songs"
        return

    _reset_for_new_game()
    st.session_state.round_songs = songs
    st.session_state.num_rounds = len(songs)

    try:
        session = sessions_repository.create_session(
            client, st.session_state.group_name, len(songs)
        )
        st.session_state.session_id = session.id
    except Exception:
        st.session_state.session_id = None

    st.session_state.view = "play"


# ----------------------------------------------------------------------
# Schermen
# ----------------------------------------------------------------------
def _render_home(client: Client) -> None:
    cfg = _get_app_settings(client)

    big_spacer(0.4)

    if cfg.get("hero_image_url"):
        col_l, col_r = st.columns([1, 1])
        with col_l:
            jukebox_illustration()
        with col_r:
            hero_image(cfg["hero_image_url"])
    else:
        # Compositie zoals in de referentiemockup: jukebox links, sfeerfoto rechts.
        # De foto-keuze wordt één keer per sessie vastgezet (in session_state), anders
        # zou hij bij elke rerun (elke klik) willekeurig kunnen wisselen.
        if "home_street_photo" not in st.session_state:
            st.session_state.home_street_photo = random.choice(
                ["street_scene_a.jpg", "street_scene_b.jpg", "canal_scene.jpg"]
            )
        col_l, col_mid, col_r = st.columns([1, 0.15, 1])
        with col_l:
            jukebox_illustration()
        with col_r:
            polaroid_photo(st.session_state.home_street_photo, width=150, rotate=4)

    st.markdown('<p class="kicker">Muziek van vroeger</p>', unsafe_allow_html=True)
    st.markdown(
        f"<h1 class='script'>{cfg.get('welcome_title') or 'Raad het Jaartal!'}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="subtitle">{cfg.get("welcome_subtitle") or "Herkent u de liedjes van vroeger?"}</p>',
        unsafe_allow_html=True,
    )
    big_spacer(1.2)

    if st.button("Start het spel", type="primary", key="home_start"):
        st.session_state.view = "setup"
        st.rerun()

    if subtle_admin_link_button():
        st.session_state.view = "admin_login"
        st.rerun()


def _render_no_songs() -> None:
    big_spacer(2)
    st.markdown("<h2>Nog geen liedjes gevonden</h2>", unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;">Er staan nog geen (bijpassende) liedjes klaar. '
        "Vraag de beheerder om eerst een aantal liedjes toe te voegen.</p>",
        unsafe_allow_html=True,
    )
    if st.button("\u2B05\uFE0F Terug naar start"):
        st.session_state.view = "home"
        st.rerun()


def _render_setup(client: Client) -> None:
    col_l, col_mid, col_r = st.columns([1, 1, 1])
    with col_mid:
        polaroid_photo("record_player_corner.jpg", width=110, rotate=-4)
    st.markdown('<p class="kicker">Even instellen</p>', unsafe_allow_html=True)
    st.markdown("<h2>Hoeveel liedjes?</h2>", unsafe_allow_html=True)
    big_spacer(0.5)

    cols = st.columns(len(ROUND_CHOICES))
    for col, amount in zip(cols, ROUND_CHOICES):
        with col:
            if st.button(f"{amount} liedjes", key=f"rounds_{amount}", type="primary"):
                _start_game(client, amount)
                st.rerun()

    big_spacer(1.2)
    with st.expander("Meer opties (optioneel)"):
        st.session_state.group_name = st.text_input(
            "Naam van de groep of activiteit (optioneel)",
            value=st.session_state.group_name,
            placeholder="Bijvoorbeeld: Huiskamer 2, dinsdagmiddag",
        )
        st.write("Alleen liedjes uit bepaalde jaren?")
        decade_options = {
            "Jaren 50": 1950,
            "Jaren 60": 1960,
            "Jaren 70": 1970,
            "Jaren 80": 1980,
            "Jaren 90": 1990,
        }
        chosen = st.multiselect(
            "Laat leeg voor alle jaren", options=list(decade_options.keys()), default=[]
        )
        st.session_state.selected_decades = [decade_options[c] for c in chosen]

    big_spacer(0.5)
    if st.button("\u2B05\uFE0F Terug naar start", key="setup_back"):
        st.session_state.view = "home"
        st.rerun()


def _render_play(client: Client, settings: Settings) -> None:
    songs = st.session_state.round_songs
    index = st.session_state.round_index
    song = songs[index]

    progress_dots(index + 1, len(songs))

    # Brede tv-compositie: platenspeler-foto links, speelkaart in het midden,
    # sfeerfoto rechts (net als in de referentiemockup). Op smallere schermen
    # stapelt Streamlit deze kolommen vanzelf netjes onder elkaar.
    col_left, col_mid, col_right = st.columns([1, 2.2, 1])

    with col_left:
        polaroid_photo("record_player_corner.jpg", width=210, rotate=-5)

    with col_right:
        if "play_side_photo" not in st.session_state:
            st.session_state.play_side_photo = random.choice(
                ["street_scene_a.jpg", "street_scene_b.jpg", "canal_scene.jpg"]
            )
        polaroid_photo(st.session_state.play_side_photo, width=210, rotate=5)

    with col_mid:
        mystery_card()

        if song.has_playable_audio:
            st.audio(song.audio_url)
        else:
            st.info(
                "\U0001F508 Er is nog geen geluidsfragment voor dit liedje. "
                "Vraag de begeleider dit liedje af te spelen, en gebruik dan de balk."
            )

        big_spacer(0.5)
        st.markdown(
            "<h3 style='text-align:center;'>Naar welk jaar wijst uw gevoel?</h3>",
            unsafe_allow_html=True,
        )

        default_value = (settings.min_year + settings.max_year) // 2
        guess_year = st.slider(
            "Sleep de balk naar het jaar",
            min_value=settings.min_year,
            max_value=settings.max_year,
            value=default_value,
            step=1,
            key=f"guess_slider_{index}",
            label_visibility="collapsed",
        )
        st.markdown(f'<div class="guess-window-label">{guess_year}</div>', unsafe_allow_html=True)

        big_spacer(0.5)
        confirmed = st.button("\u2705 Dit is ons antwoord", type="primary", key=f"confirm_{index}")

    if confirmed:
        outcome = calculate_score(song.year, guess_year)
        result = RoundResult(
            song=song,
            guess_center=guess_year,
            guess_low=guess_year,
            guess_high=guess_year,
            points=outcome.points,
            message=outcome.message,
        )
        st.session_state.round_results.append(result)
        st.session_state.total_score += outcome.points

        if st.session_state.session_id:
            try:
                sessions_repository.save_round(
                    client, st.session_state.session_id, index + 1, result
                )
            except Exception:
                pass

        st.session_state.view = "reveal_year"
        st.rerun()


def _render_reveal_year() -> None:
    result = st.session_state.round_results[-1]
    song = result.song
    diff = abs(result.guess_center - song.year)
    color = decade_color(song.decade)

    if diff == 0:
        banner_class, headline = "result-good", "Precies goed! \U0001F3AF"
    elif diff <= 3:
        banner_class, headline = "result-good", "Heel dichtbij! \U0001F44F"
    elif diff <= 7:
        banner_class, headline = "result-close", "Goed gegokt! \U0001F44D"
    else:
        banner_class, headline = "result-far", "Een eind ernaast \U0001F642"

    if result.points >= 70:
        st.balloons()

    st.markdown(
        f"""
        <div class="result-banner {banner_class}">
            <h3 style="margin:0 0 0.3rem 0;">{headline}</h3>
            <p style="margin:0;">Uw antwoord was <strong>{result.guess_center}</strong></p>
            <p style="margin:0.6rem 0 0 0;">Het juiste jaar is</p>
            <div class="hero-year" style="color:{color};">{song.year}</div>
            <span class="decade-badge" style="background:{color};">{decade_label(song.decade)}</span>
            <div class="timeline-strip"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    score_badge(result.points)

    big_spacer(1)
    if st.button("\u27A1\uFE0F Verder", type="primary", key="to_ask_title"):
        st.session_state.view = "ask_title"
        st.rerun()


def _render_ask_title() -> None:
    st.markdown(
        """
        <div class="mystery-card">
            <div class="vinyl-hang"></div>
            <span class="note-accent" style="top:-6px; left:14%;">&#9835;</span>
            <span class="note-accent" style="top:6px; right:16%;">&#9834;</span>
            <h3 class="script-heading" style="font-family:'Pacifico',cursive; font-size:1.8rem; font-weight:400; margin-top:0.6rem; margin-bottom:0.4rem;">Weten jullie ook...</h3>
            <p style="font-size:1.35rem !important; font-weight:700; color:#3D2E1F; margin:0;">
                Welk liedje is dit?<br>En welke artiest?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="text-align:center;">Overleg samen... en kijk dan of jullie gelijk hadden!</p>',
        unsafe_allow_html=True,
    )

    big_spacer(1)
    if st.button("Toon het antwoord", type="primary", key="to_reveal_full"):
        st.session_state.view = "reveal_full"
        st.rerun()


def _render_reveal_full() -> None:
    result = st.session_state.round_results[-1]
    song = result.song
    is_last = st.session_state.round_index + 1 >= len(st.session_state.round_songs)

    st.markdown('<div class="reveal-card">', unsafe_allow_html=True)
    if song.album_art_url:
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            st.image(song.album_art_url, use_container_width=True)
    st.markdown(f"<h2 style='margin-bottom:0.2rem;'>{song.title}</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:1.4rem !important; font-weight:700; color:#C0632B;'>{song.artist}</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='font-size:1.2rem;'>uit <strong>{song.year}</strong></p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<span class="decade-badge" style="background:{decade_color(song.decade)};">'
        f"{decade_label(song.decade)}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Speel het liedje op dit onthulscherm automatisch af.
    # We gebruiken de NATIVE st.audio(..., autoplay=True). Autoplay via
    # st.markdown(<audio autoplay>) werkt niet betrouwbaar omdat Streamlit de
    # HTML sanitized. Omdat elk liedje een eigen audio-URL heeft, krijgt elke
    # ronde bovendien een eigen widget-identiteit, zodat autoplay opnieuw start.
    # Autoplay is toegestaan omdat de gebruiker net op een knop heeft geklikt.
    if song.has_playable_audio:
        st.audio(song.audio_url, autoplay=True)

    if song.spotify_url:
        st.link_button(
            "\U0001F3A7 Beluister het hele nummer op Spotify",
            song.spotify_url,
            use_container_width=True,
        )

    big_spacer(0.8)
    if is_last:
        if st.button("\U0001F3C6 Bekijk de eindscore", type="primary", key="to_end"):
            st.session_state.view = "end"
            st.rerun()
    else:
        if st.button("\u27A1\uFE0F Volgende liedje", type="primary", key="next_round"):
            st.session_state.round_index += 1
            st.session_state.view = "play"
            st.rerun()


def _render_end(client: Client) -> None:
    results = st.session_state.round_results
    total = st.session_state.total_score
    max_possible = len(results) * 100
    average = total / len(results) if results else 0

    if st.session_state.session_id:
        try:
            sessions_repository.finish_session(client, st.session_state.session_id, total)
            st.session_state.session_id = None
        except Exception:
            pass

    big_spacer(0.5)
    col_l, col_mid, col_r = st.columns([1, 1, 1])
    with col_mid:
        sticker_badge("Goed<br>gedaan!")
    st.markdown('<p class="kicker">Het is gelukt</p>', unsafe_allow_html=True)
    st.markdown("<h1 class='script'>Goed gedaan!</h1>", unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitle" style="font-weight:800; color:#A1663A;">'
        f"{total} van de {max_possible} punten</p>",
        unsafe_allow_html=True,
    )

    if average >= 80:
        closing = "Wat een muzikaal geheugen hebben jullie! \U0001F31F"
    elif average >= 50:
        closing = "Goed geraden! Dat waren mooie herinneringen. \U0001F3B6"
    else:
        closing = "Leuk gespeeld! Muziek van vroeger blijft lastig te plaatsen. \U0001F60A"

    st.markdown(f'<p class="subtitle">{closing}</p>', unsafe_allow_html=True)

    big_spacer(0.8)
    with st.expander("Bekijk alle liedjes van dit spel"):
        for i, result in enumerate(results, start=1):
            st.markdown(
                f"**{i}. {result.song.title}** — {result.song.artist} ({result.song.year}) "
                f"· uw gok: {result.guess_center} · +{result.points} punten"
            )

    big_spacer(1)
    if st.button("\U0001F504 Nog een keer spelen", type="primary", key="play_again"):
        st.session_state.view = "setup"
        st.rerun()
    if st.button("\U0001F3E0 Terug naar start", key="end_home"):
        st.session_state.view = "home"
        st.rerun()


# ----------------------------------------------------------------------
# Entrypoint
# ----------------------------------------------------------------------
def render(client: Client, settings: Settings) -> None:
    _ensure_state()
    view = st.session_state.view

    if view == "home":
        _render_home(client)
    elif view == "no_songs":
        _render_no_songs()
    elif view == "setup":
        _render_setup(client)
    elif view == "play":
        _render_play(client, settings)
    elif view == "reveal_year":
        _render_reveal_year()
    elif view == "ask_title":
        _render_ask_title()
    elif view == "reveal_full":
        _render_reveal_full()
    elif view == "end":
        _render_end(client)
    else:
        st.session_state.view = "home"
        st.rerun()
