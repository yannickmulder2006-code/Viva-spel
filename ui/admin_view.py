"""
ui/admin_view.py
------------------
Beheerscherm voor de begeleider (achter een pincode). Vier tabbladen:
  1. Liedje toevoegen  - via Spotify-zoeken of handmatig
  2. Liedjes beheren   - overzicht met hoesjes, audio uploaden, aan/uit, verwijderen
  3. Aankleding        - eigen sfeerfoto en welkomsttekst instellen
  4. Speelgeschiedenis - overzicht van gespeelde sessies
"""

from __future__ import annotations

import streamlit as st
from supabase import Client

from config import Settings
from database import app_settings_repository, sessions_repository, songs_repository
from database.songs_repository import DuplicateSongError, SongRepositoryError
from models import Song
from services.spotify_service import SpotifyServiceError, get_spotify_service
from utils import decade_label


def _ensure_state() -> None:
    defaults = {
        "admin_authenticated": False,
        "spotify_search_results": [],
        "confirm_delete_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _render_login(settings: Settings) -> None:
    st.markdown("<h2>Beheerder</h2>", unsafe_allow_html=True)
    pin = st.text_input("Pincode", type="password", key="admin_pin_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Inloggen", type="primary"):
            if pin == settings.admin_pin:
                st.session_state.admin_authenticated = True
                st.session_state.view = "admin"
                st.rerun()
            else:
                st.error("Onjuiste pincode.")
    with col2:
        if st.button("\u2B05\uFE0F Terug"):
            st.session_state.view = "home"
            st.rerun()


def _clear_settings_cache() -> None:
    """Zorg dat het startscherm de nieuwe aankleding oppikt."""
    st.session_state.app_settings = None


# ----------------------------------------------------------------------
# Tab 1: toevoegen
# ----------------------------------------------------------------------
def _render_add_song_tab(client: Client, settings: Settings) -> None:
    st.subheader("Liedje zoeken via Spotify")

    if not settings.spotify_configured:
        st.info(
            "Spotify is nog niet gekoppeld. Je kunt hieronder wel handmatig "
            "liedjes toevoegen."
        )
    else:
        query = st.text_input(
            "Zoek op titel en/of artiest",
            placeholder="Bijvoorbeeld: Geef mij maar Amsterdam",
            key="spotify_query",
        )
        if st.button("\U0001F50D Zoeken op Spotify"):
            try:
                service = get_spotify_service(
                    settings.spotify_client_id, settings.spotify_client_secret
                )
                st.session_state.spotify_search_results = service.search_tracks(query)
                if not st.session_state.spotify_search_results:
                    st.warning("Geen resultaten gevonden. Probeer een andere zoekterm.")
            except SpotifyServiceError as exc:
                st.error(str(exc))

        for track in st.session_state.spotify_search_results:
            with st.container(border=True):
                cols = st.columns([1, 3, 1])
                with cols[0]:
                    if track.album_art_url:
                        st.image(track.album_art_url, width=72)
                with cols[1]:
                    st.markdown(f"**{track.title}**")
                    st.caption(f"{track.artist} \u00B7 {track.year}")
                with cols[2]:
                    if st.button("\u2795 Voeg toe", key=f"add_spotify_{track.spotify_track_id}"):
                        song = Song(
                            title=track.title,
                            artist=track.artist,
                            year=track.year,
                            spotify_track_id=track.spotify_track_id,
                            spotify_url=track.spotify_url,
                            album_art_url=track.album_art_url,
                            added_by="beheerder (Spotify)",
                        )
                        try:
                            songs_repository.add_song(client, song)
                            st.success(f"'{song.title}' is toegevoegd!")
                        except DuplicateSongError as exc:
                            st.warning(f"\u26A0\uFE0F {exc}")
                        except SongRepositoryError as exc:
                            st.error(str(exc))

    st.divider()
    st.subheader("Of handmatig toevoegen")
    with st.form("manual_add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Titel")
        with col2:
            artist = st.text_input("Artiest")
        year = st.number_input(
            "Jaartal", min_value=settings.min_year, max_value=settings.max_year, value=1980
        )
        album_art_url = st.text_input("Link naar hoesfoto (optioneel)")
        audio_file = st.file_uploader(
            "Geluidsfragment (mp3, optioneel - kan ook later)",
            type=["mp3", "wav", "ogg", "m4a"],
        )
        submitted = st.form_submit_button("\u2795 Liedje toevoegen", type="primary")

        if submitted:
            if not title or not artist:
                st.error("Vul minimaal een titel en artiest in.")
            else:
                try:
                    audio_url = None
                    if audio_file is not None:
                        audio_url = songs_repository.upload_audio_fragment(
                            client, settings.audio_bucket, audio_file.read(), audio_file.name
                        )
                    song = Song(
                        title=title,
                        artist=artist,
                        year=int(year),
                        album_art_url=album_art_url or None,
                        audio_url=audio_url,
                        added_by="beheerder (handmatig)",
                    )
                    songs_repository.add_song(client, song)
                    st.success(f"'{title}' is toegevoegd!")
                except DuplicateSongError as exc:
                    st.warning(f"\u26A0\uFE0F {exc}")
                except SongRepositoryError as exc:
                    st.error(str(exc))


# ----------------------------------------------------------------------
# Tab 2: beheren
# ----------------------------------------------------------------------
def _render_manage_songs_tab(client: Client, settings: Settings) -> None:
    st.subheader("Alle liedjes")
    try:
        songs = songs_repository.get_all_songs(client, active_only=False)
    except SongRepositoryError as exc:
        st.error(str(exc))
        return

    if not songs:
        st.info("Er zijn nog geen liedjes toegevoegd.")
        return

    decades = sorted({song.decade for song in songs})
    labels = [decade_label(d) for d in decades]
    decade_filter = st.selectbox("Filter op decennium", options=["Alle"] + labels)
    if decade_filter != "Alle":
        target = decades[labels.index(decade_filter)]
        songs = [s for s in songs if s.decade == target]

    st.caption(f"{len(songs)} liedje(s)")

    for song in songs:
        with st.container(border=True):
            cols = st.columns([1, 3, 1.3])
            with cols[0]:
                if song.album_art_url:
                    st.image(song.album_art_url, width=64)
                else:
                    st.markdown(
                        '<div style="width:64px;height:64px;border-radius:10px;'
                        'background:#EFE0C9;display:flex;align-items:center;'
                        'justify-content:center;font-size:1.6rem;">\U0001F3B5</div>',
                        unsafe_allow_html=True,
                    )
            with cols[1]:
                status = "\u2705 actief" if song.active else "\U0001F6AB uit"
                audio_status = "\U0001F50A" if song.has_playable_audio else "\U0001F507 geen geluid"
                st.markdown(f"**{song.title}**")
                st.caption(f"{song.artist} \u00B7 {song.year} \u00B7 {status} \u00B7 {audio_status}")
            with cols[2]:
                toggle_label = "Uitzetten" if song.active else "Aanzetten"
                if st.button(toggle_label, key=f"toggle_{song.id}"):
                    songs_repository.set_song_active(client, song.id, not song.active)
                    st.rerun()
                if st.session_state.confirm_delete_id == song.id:
                    if st.button("Zeker weten?", key=f"confirm_del_{song.id}", type="primary"):
                        songs_repository.delete_song(client, song.id)
                        st.session_state.confirm_delete_id = None
                        st.rerun()
                else:
                    if st.button("\U0001F5D1\uFE0F", key=f"del_{song.id}"):
                        st.session_state.confirm_delete_id = song.id
                        st.rerun()

            if not song.has_playable_audio:
                uploaded = st.file_uploader(
                    "Geluidsfragment toevoegen",
                    type=["mp3", "wav", "ogg", "m4a"],
                    key=f"audio_upload_{song.id}",
                )
                if uploaded is not None:
                    try:
                        url = songs_repository.upload_audio_fragment(
                            client, settings.audio_bucket, uploaded.read(), uploaded.name
                        )
                        songs_repository.update_song(client, song.id, {"audio_url": url})
                        st.success("Geluidsfragment toegevoegd!")
                        st.rerun()
                    except SongRepositoryError as exc:
                        st.error(str(exc))


# ----------------------------------------------------------------------
# Tab 3: aankleding
# ----------------------------------------------------------------------
def _render_appearance_tab(client: Client, settings: Settings) -> None:
    st.subheader("Aankleding van het startscherm")
    st.caption(
        "Personaliseer de app met een eigen sfeerfoto en tekst. Tip: gebruik "
        "een warme, herkenbare foto (bijvoorbeeld van de eigen woonkamer of "
        "een nostalgisch tafereel) waarvan je zelf de rechten hebt."
    )

    current = app_settings_repository.get_all_settings(client)

    with st.form("appearance_form"):
        welcome_title = st.text_input("Titel op startscherm", value=current.get("welcome_title", ""))
        welcome_subtitle = st.text_input("Ondertitel", value=current.get("welcome_subtitle", ""))
        hero_file = st.file_uploader(
            "Sfeerfoto voor het startscherm (jpg/png)", type=["jpg", "jpeg", "png", "webp"]
        )
        if current.get("hero_image_url"):
            st.image(current["hero_image_url"], caption="Huidige sfeerfoto", width=280)

        saved = st.form_submit_button("\U0001F4BE Opslaan", type="primary")
        if saved:
            try:
                app_settings_repository.set_setting(client, "welcome_title", welcome_title)
                app_settings_repository.set_setting(client, "welcome_subtitle", welcome_subtitle)
                if hero_file is not None:
                    url = songs_repository.upload_image(
                        client, settings.audio_bucket, hero_file.read(), hero_file.name
                    )
                    app_settings_repository.set_setting(client, "hero_image_url", url)
                _clear_settings_cache()
                st.success("Aankleding opgeslagen! Het startscherm is bijgewerkt.")
            except Exception as exc:
                st.error(f"Kon aankleding niet opslaan: {exc}")


# ----------------------------------------------------------------------
# Tab 4: geschiedenis
# ----------------------------------------------------------------------
def _render_history_tab(client: Client) -> None:
    st.subheader("Speelgeschiedenis")
    try:
        sessions = sessions_repository.get_recent_sessions(client, limit=30)
    except Exception as exc:
        st.error(f"Kon geschiedenis niet ophalen: {exc}")
        return

    if not sessions:
        st.info("Er is nog niet gespeeld.")
        return

    for session in sessions:
        name = session.group_name or "(geen groepsnaam)"
        st.markdown(
            f"**{name}** \u2014 {session.total_rounds} liedjes \u2014 "
            f"score: {session.total_score} \u2014 {session.started_at}"
        )


def render(client: Client, settings: Settings) -> None:
    _ensure_state()

    if not st.session_state.admin_authenticated:
        _render_login(settings)
        return

    st.markdown("<h2>Beheerscherm</h2>", unsafe_allow_html=True)
    if st.button("\U0001F6AA Uitloggen en terug naar spel"):
        st.session_state.admin_authenticated = False
        st.session_state.view = "home"
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["\u2795 Toevoegen", "\U0001F3B6 Beheren", "\U0001F3A8 Aankleding", "\U0001F4CA Geschiedenis"]
    )
    with tab1:
        _render_add_song_tab(client, settings)
    with tab2:
        _render_manage_songs_tab(client, settings)
    with tab3:
        _render_appearance_tab(client, settings)
    with tab4:
        _render_history_tab(client)
