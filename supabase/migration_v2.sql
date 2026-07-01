-- =====================================================================
-- supabase/migration_v2.sql
-- =====================================================================
-- Draai dit ALLEEN als je de app al eerder had opgezet met de eerste versie
-- van schema.sql. Het voegt de nieuwe onderdelen toe zonder je bestaande
-- liedjes/sessies aan te raken:
--   * app_settings-tabel (voor sfeerfoto + welkomsttekst)
--   * automatische 'decade'-berekening (lost de bekende decade-foutmelding op)
--
-- Begin je helemaal opnieuw? Dan hoef je dit NIET te draaien - gebruik dan
-- gewoon het volledige schema.sql.
-- =====================================================================

-- 1. app_settings-tabel
create table if not exists app_settings (
    key         text primary key,
    value       text,
    updated_at  timestamptz not null default now()
);
alter table app_settings enable row level security;

-- 2. 'decade' voortaan automatisch laten berekenen
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

-- 3. Vul ontbrekende decennia in voor liedjes die er al staan
update songs set decade = (year / 10) * 10 where decade is null;
