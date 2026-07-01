-- =====================================================================
-- supabase/schema.sql
-- =====================================================================
-- Voer dit volledige bestand één keer uit in de Supabase SQL Editor
-- (Dashboard -> SQL Editor -> New query -> plak dit bestand -> Run).
--
-- Dit maakt aan:
--   1. Tabel songs            -> de liedjesbibliotheek
--   2. Tabel game_sessions    -> één rij per gespeelde sessie
--   3. Tabel session_rounds   -> één rij per geraden liedje binnen een sessie
--   4. Een publieke Storage-bucket 'song-audio' voor geüploade fragmenten
--
-- Rijbeveiliging (RLS) staat AAN op alle tabellen, maar er zijn bewust
-- geen policies toegevoegd. De Streamlit-app gebruikt de Supabase
-- "service_role" key (zie .env.example), die RLS altijd omzeilt vanaf de
-- server. Zo blijft de database standaard afgesloten voor iedereen die
-- rechtstreeks met de (publieke) anon-key zou proberen te verbinden.
-- =====================================================================

-- Nodig voor gen_random_uuid()
create extension if not exists pgcrypto;

-- ---------------------------------------------------------------------
-- 1. songs
-- ---------------------------------------------------------------------
create table if not exists songs (
    id                uuid primary key default gen_random_uuid(),
    title             text not null,
    artist            text not null,
    year              integer not null check (year between 1900 and 2100),
    decade            integer not null,
    spotify_track_id  text,
    spotify_url       text,
    album_art_url     text,
    audio_url         text,
    active            boolean not null default true,
    added_by          text,
    created_at        timestamptz not null default now()
);

create index if not exists idx_songs_active on songs (active);
create index if not exists idx_songs_decade on songs (decade);

alter table songs enable row level security;

-- ---------------------------------------------------------------------
-- 2. game_sessions
-- ---------------------------------------------------------------------
create table if not exists game_sessions (
    id            uuid primary key default gen_random_uuid(),
    group_name    text,
    total_rounds  integer not null default 0,
    total_score   integer not null default 0,
    started_at    timestamptz not null default now(),
    ended_at      timestamptz
);

alter table game_sessions enable row level security;

-- ---------------------------------------------------------------------
-- 3. session_rounds
-- ---------------------------------------------------------------------
create table if not exists session_rounds (
    id                 uuid primary key default gen_random_uuid(),
    session_id         uuid not null references game_sessions (id) on delete cascade,
    song_id            uuid references songs (id) on delete set null,
    round_number       integer not null,
    guessed_year_low   integer not null,
    guessed_year_high  integer not null,
    actual_year        integer not null,
    points_earned      integer not null,
    created_at         timestamptz not null default now()
);

create index if not exists idx_session_rounds_session on session_rounds (session_id);

alter table session_rounds enable row level security;

-- ---------------------------------------------------------------------
-- 4. app_settings (personalisatie: sfeerfoto, welkomsttekst)
-- ---------------------------------------------------------------------
create table if not exists app_settings (
    key         text primary key,
    value       text,
    updated_at  timestamptz not null default now()
);

alter table app_settings enable row level security;

-- ---------------------------------------------------------------------
-- 5. Automatisch 'decade' berekenen uit 'year'
-- ---------------------------------------------------------------------
-- Hierdoor hoeft 'decade' nooit handmatig meegestuurd te worden - niet bij
-- een CSV-import en niet vanuit de app. De trigger vult 'm altijd correct in.
alter table songs alter column decade drop not null;

create or replace function set_song_decade()
returns trigger as $$
begin
    new.decade := (new.year / 10) * 10;
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_set_song_decade on songs;
create trigger trg_set_song_decade
    before insert or update on songs
    for each row execute function set_song_decade();

-- ---------------------------------------------------------------------
-- 6. Storage-bucket voor geuploade audiofragmenten en sfeerfoto's
-- ---------------------------------------------------------------------
-- 'public = true' zorgt dat afgespeelde fragmenten direct via een publieke
-- URL beschikbaar zijn (nodig voor st.audio() in de app). Dit is voor dit
-- gebruik (korte, niet-gevoelige muziekfragmentjes) een prima afweging.
insert into storage.buckets (id, name, public)
values ('song-audio', 'song-audio', true)
on conflict (id) do nothing;
