# 🎵 Raad het Jaartal!

Een vriendelijk muziek-jaartallenspel voor de ouderenzorg. Bewoners horen of
zien een liedje en raden via een grote schuifregelaar in welk jaar het is
uitgekomen. Gebouwd met **Python + Streamlit** (interface), **Supabase**
(database & opslag) en klaar om te beheren via **GitHub**.

Deze README is de **technische installatiehandleiding** (voor wie de app
opzet/beheert). Ben je op zoek naar een eenvoudige uitleg om de app te
*gebruiken* tijdens een activiteit? Zie [`GEBRUIKSHANDLEIDING.md`](GEBRUIKSHANDLEIDING.md).

---

## Inhoudsopgave

1. [Wat doet deze app precies?](#1-wat-doet-deze-app-precies)
2. [Projectstructuur](#2-projectstructuur)
3. [Wat heb je nodig?](#3-wat-heb-je-nodig)
4. [Stap 1 — Supabase instellen](#stap-1--supabase-instellen)
5. [Stap 2 — Spotify instellen (optioneel maar aanbevolen)](#stap-2--spotify-instellen-optioneel-maar-aanbevolen)
6. [Stap 3 — Project op je eigen computer draaien](#stap-3--project-op-je-eigen-computer-draaien)
7. [Stap 4 — Voorbeeldliedjes inladen](#stap-4--voorbeeldliedjes-inladen)
8. [Stap 5 — Project op GitHub zetten](#stap-5--project-op-github-zetten)
9. [Stap 6 — Online zetten met Streamlit Community Cloud](#stap-6--online-zetten-met-streamlit-community-cloud)
10. [Nieuwe liedjes toevoegen](#10-nieuwe-liedjes-toevoegen)
11. [Waarom audio-uploads i.p.v. Spotify-previews?](#11-waarom-audio-uploads-ipv-spotify-previews)
12. [Beveiliging — lees dit even](#12-beveiliging--lees-dit-even)
13. [Problemen oplossen](#13-problemen-oplossen)
14. [De app uitbreiden](#14-de-app-uitbreiden)
15. [Auteursrecht & muziek](#15-auteursrecht--muziek)

---

## 1. Wat doet deze app precies?

- Een groep (bijvoorbeeld tijdens dagbesteding) speelt samen op één tablet
  of computer.
- Per ronde speelt de app een kort geluidsfragment af (titel/artiest blijven
  verborgen — dat mogen bewoners zelf herkennen!).
- De groep sleept een schuifregelaar naar het jaar waarin ze denken dat het
  liedje uitkwam en bevestigt. Raden binnen 1 jaar telt al als voltreffer.
- **Onthulling in drie rustige stappen:**
  1. Eerst zien jullie of het jaar goed was, plus het echte jaartal en de punten.
  2. Daarna verschijnt de vraag *"Weten jullie ook de titel en artiest?"* —
     puur om samen over te praten, er hoeft niets ingevuld te worden.
  3. Tot slot worden titel, artiest en hoesfoto onthuld, en speelt het liedje
     hier **automatisch** af zodat iedereen het herkent.
- Aan het eind volgt een leuke eindscore. Daarna kan er direct opnieuw
  gespeeld worden.
- Achter een beveiligd beheerscherm (pincode) kan een begeleider liedjes
  toevoegen (via Spotify-zoekfunctie of handmatig), geluidsfragmenten
  uploaden, liedjes uitschakelen/verwijderen, de app aankleden met een eigen
  sfeerfoto/tekst, en de speelgeschiedenis bekijken.
- **Dubbele liedjes worden automatisch geblokkeerd** met een nette melding.

## 2. Projectstructuur

```
raad-het-jaartal/
├── app.py                     # Startpunt van de app (routering)
├── config.py                  # Laden van environment variables
├── models.py                  # Song / GameSession / RoundResult dataclasses
├── utils.py                   # Kleine hulpfuncties
├── requirements.txt           # Python-dependencies
├── .env.example                # Voorbeeld environment variables
├── .gitignore
├── README.md                   # Dit bestand
├── GEBRUIKSHANDLEIDING.md      # Eenvoudige gebruikshandleiding voor begeleiders
├── database/
│   ├── supabase_client.py      # Verbinding met Supabase
│   ├── songs_repository.py     # CRUD voor liedjes + audio-uploads
│   └── sessions_repository.py  # CRUD voor spelsessies/geschiedenis
├── services/
│   ├── spotify_service.py      # Spotify-zoekfunctie (metadata)
│   └── scoring_service.py      # Puntentelling
├── ui/
│   ├── styles.py                # CSS voor grote, rustige interface
│   ├── components.py            # Herbruikbare UI-onderdelen
│   ├── game_view.py             # Schermen voor de spelers
│   └── admin_view.py            # Beheerscherm
├── data/
│   └── seed_songs.csv           # 33 voorbeeldliedjes jaren 50 t/m 90
├── scripts/
│   └── seed_database.py         # Script om voorbeelddata in te laden
└── supabase/
    └── schema.sql                # SQL om alle tabellen aan te maken
```

## 3. Wat heb je nodig?

- Een gratis [Supabase](https://supabase.com)-account.
- Een gratis [Spotify for Developers](https://developer.spotify.com/dashboard)-account
  (optioneel, maar maakt het toevoegen van liedjes veel makkelijker).
- Een [GitHub](https://github.com)-account.
- Python 3.10 of hoger op je computer, als je lokaal wilt testen.
- Voor het online hosten: een gratis account op
  [Streamlit Community Cloud](https://streamlit.io/cloud).

---

## Stap 1 — Supabase instellen

1. Ga naar [supabase.com](https://supabase.com) en maak een nieuw project
   aan (kies een naam, wachtwoord en regio, bijvoorbeeld West-Europa).
2. Wacht tot het project klaar is (dit duurt ongeveer 1-2 minuten).
3. Ga naar **SQL Editor** in het linkermenu → **New query**.
4. Open het bestand [`supabase/schema.sql`](supabase/schema.sql) uit dit
   project, kopieer de volledige inhoud, plak het in de SQL Editor en klik
   op **Run**. Dit maakt automatisch aan:
   - de tabel `songs` (de liedjesbibliotheek)
   - de tabel `game_sessions` (gespeelde sessies)
   - de tabel `session_rounds` (score per ronde)
   - de tabel `app_settings` (voor je eigen sfeerfoto en welkomsttekst)
   - een automatische berekening van het `decade`-veld uit het jaartal
   - een opslagmap (**Storage bucket**) genaamd `song-audio` voor de
     geüploade geluidsfragmentjes en sfeerfoto's

   > Had je de app al eerder opgezet met een oudere versie van dit schema?
   > Draai dan in plaats daarvan **`supabase/migration_v2.sql`** — dat voegt
   > alleen de nieuwe onderdelen toe zonder je bestaande liedjes te raken,
   > en lost meteen de bekende `decade`-foutmelding op.
5. Ga naar **Settings → API**. Hier vind je:
   - **Project URL** → dit wordt `SUPABASE_URL`
   - **service_role key** (onder "Project API keys", NIET de "anon/public"
     key!) → dit wordt `SUPABASE_KEY`

   > ⚠️ De `service_role` key geeft volledige toegang tot je database.
   > Deel deze nooit publiekelijk en zet 'm nooit in GitHub (zie
   > [Beveiliging](#12-beveiliging--lees-dit-even)).

Dat is alles — de tabellen en de opslagmap staan klaar.

## Stap 2 — Spotify instellen (optioneel maar aanbevolen)

Spotify wordt in deze app **alleen gebruikt om liedjes op te zoeken**
(titel, artiest, jaartal en hoesfoto worden automatisch ingevuld). Het
afspelen tijdens het spel gebeurt via eigen geüploade fragmentjes — lees
waarom in [hoofdstuk 11](#11-waarom-audio-uploads-ipv-spotify-previews).

1. Ga naar [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
   en log in met een (gratis) Spotify-account.
2. Klik op **Create app**.
   - App name: bijvoorbeeld "Raad het Jaartal"
   - App description: "Intern spel voor ouderenzorg"
   - Redirect URI: vul iets in zoals `http://localhost:8501` (wordt door
     deze app niet echt gebruikt, maar is verplicht om in te vullen)
   - Vink de API's aan die worden voorgesteld en accepteer de voorwaarden.
3. Open je nieuwe app → **Settings**. Hier vind je **Client ID** en
   **Client secret** (klik op "View client secret").
   - `Client ID` → dit wordt `SPOTIFY_CLIENT_ID`
   - `Client secret` → dit wordt `SPOTIFY_CLIENT_SECRET`

Wil je Spotify niet gebruiken? Geen probleem: laat deze twee velden leeg in
je `.env`-bestand. Liedjes toevoegen kan dan nog steeds, alleen handmatig
via het beheerscherm.

## Stap 3 — Project op je eigen computer draaien

Open een terminal (Opdrachtprompt/Terminal) in de projectmap en voer uit:

```bash
# 1. Maak een virtuele omgeving aan (aanbevolen)
python3 -m venv venv
source venv/bin/activate        # Op Windows: venv\Scripts\activate

# 2. Installeer alle benodigde packages
pip install -r requirements.txt

# 3. Maak je eigen .env bestand
cp .env.example .env
```

Open vervolgens `.env` in een teksteditor en vul de waarden in die je bij
Stap 1 en 2 hebt verzameld (`SUPABASE_URL`, `SUPABASE_KEY`,
`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`) en kies zelf een `ADMIN_PIN`.

Start de app met:

```bash
streamlit run app.py
```

Er opent automatisch een browservenster op `http://localhost:8501`.

## Stap 4 — Voorbeeldliedjes inladen

Dit project bevat 33 bekende Nederlandstalige liedjes (jaren 50 t/m 90),
zorgvuldig samengesteld met gecontroleerde releasejaren (o.a. Johnny
Jordaan, André Hazes, Doe Maar, Vader Abraham, Marco Borsato, BLØF).
Laad ze in met:

```bash
python -m scripts.seed_database
```

> Let op: dit script vult alleen titel/artiest/jaartal. Geluidsfragmenten
> mogen we om auteursrechtelijke redenen niet meeleveren — die voeg je zelf
> toe via het beheerscherm (zie [hoofdstuk 10](#10-nieuwe-liedjes-toevoegen)).

## Stap 5 — Project op GitHub zetten

1. Maak een nieuwe, **lege** (geen README/`.gitignore` aanvinken) repository
   aan op [github.com/new](https://github.com/new), bijvoorbeeld genaamd
   `raad-het-jaartal`.
2. Voer in de projectmap uit:

```bash
git init
git add .
git commit -m "Eerste versie van Raad het Jaartal"
git branch -M main
git remote add origin https://github.com/JOUW-GEBRUIKERSNAAM/raad-het-jaartal.git
git push -u origin main
```

Omdat `.env` in `.gitignore` staat, worden je geheime sleutels **nooit**
meegestuurd naar GitHub. Controleer dit gerust vooraf met `git status` —
je mag daar geen `.env` in zien staan.

## Stap 6 — Online zetten met Streamlit Community Cloud

1. Ga naar [share.streamlit.io](https://share.streamlit.io) en log in met
   je GitHub-account.
2. Klik op **Create app** → **Deploy a public app from GitHub**.
3. Kies je repository, branch `main`, en main file `app.py`.
4. Klik op **Advanced settings** → **Secrets** en plak daar (in dit exacte
   TOML-formaat, zonder aanhalingstekens rond de key-namen):

```toml
SUPABASE_URL = "https://jouwproject.supabase.co"
SUPABASE_KEY = "jouw-service-role-key"
SPOTIFY_CLIENT_ID = "jouw-spotify-client-id"
SPOTIFY_CLIENT_SECRET = "jouw-spotify-client-secret"
ADMIN_PIN = "1234"
```

5. Klik op **Deploy**. Na een paar minuten is je app publiek bereikbaar op
   een URL zoals `https://raad-het-jaartal.streamlit.app`.

> 💡 Elke keer dat je wijzigingen naar GitHub pusht (`git push`), werkt
> Streamlit Cloud de live-app automatisch bij.

---

## 10. Nieuwe liedjes toevoegen

De app is met opzet zo gebouwd dat je zelf, zonder code aan te passen,
liedjes kunt blijven toevoegen:

1. Open de app en klik rechtsonder op het kleine **⚙️ Beheerder**-knopje.
2. Voer je pincode in (die je in `.env`/Secrets hebt ingesteld als
   `ADMIN_PIN`).
3. Tabblad **➕ Liedje toevoegen**:
   - **Met Spotify:** typ een titel of artiest, klik op zoeken, en klik bij
     het juiste resultaat op "Toevoegen". Titel, artiest, jaartal en
     hoesfoto worden automatisch overgenomen.
   - **Handmatig:** vul titel, artiest en jaartal zelf in (bijvoorbeeld
     handig voor een heel specifieke, lokale of minder bekende titel).
4. Tabblad **🎶 Liedjes beheren**: hier zie je per liedje of er al een
   geluidsfragment is. Staat er "🔇 geen fragment"? Upload dan een kort
   mp3-bestandje (15–30 seconden is ruim voldoende) via de
   bestand-uploadknop die daar verschijnt.
5. Liedjes tijdelijk niet gebruiken? Klik op "Uitschakelen" in plaats van
   te verwijderen — zo kun je ze later makkelijk weer terugzetten.

## 11. Waarom audio-uploads i.p.v. Spotify-previews?

Spotify heeft sinds 27 november 2024 het 30-seconden-voorbeeldfragment
(`preview_url`) uit haar Web API gehaald voor alle nieuw aangemaakte
apps — dit is een bewuste keuze van Spotify zelf en geen beperking van
deze applicatie. Daardoor is het technisch niet meer betrouwbaar mogelijk
om via de Spotify API automatisch een fragment af te spelen zonder daarbij
ook titel en artiest in beeld te krijgen (de officiële Spotify-widget toont
dat namelijk altijd).

Om toch aan de kernwens te voldoen — **alleen geluid, titel/artiest pas
onthullen ná het raden** — uploadt de beheerder daarom zelf een kort
fragment per liedje naar Supabase Storage. Dat fragment staat volledig
onder eigen controle van de app, dus kunnen we titel en artiest netjes
verbergen tot het onthullingsmoment. Na de onthulling krijgt de speler
een link om het hele nummer alsnog op Spotify te beluisteren.

**Praktische tip:** neem voor elk liedje bijvoorbeeld met een telefoon een
fragmentje van 15-30 seconden op vanaf een cd, radio of Spotify (voor eigen
gebruik binnen de instelling), of gebruik een online tool om een kort
fragment uit een muziekbestand te knippen.

## 12. Beveiliging — lees dit even

- Deze app heeft geen volwaardig login-systeem met gebruikersaccounts —
  het beheerscherm is beveiligd met één gedeelde pincode (`ADMIN_PIN`).
  Dat is een bewuste, eenvoudige keuze passend bij een intern hulpmiddel
  voor één instelling/team. Deel de pincode alleen met begeleiders.
- De app gebruikt de Supabase **service_role key**, die nooit in de
  browser terechtkomt (Streamlit-code draait server-side) maar wél
  volledige databasetoegang geeft. Zet deze dus nooit in code of GitHub,
  alleen in `.env` (lokaal) of Streamlit Secrets (online).
- Wil je de app niet voor de hele wereld toegankelijk maken? Streamlit
  Community Cloud biedt de optie om een app **privé** te zetten
  (alleen zichtbaar voor uitgenodigde e-mailadressen) via de
  app-instellingen — erg aan te raden voor dit soort interne tools.
- Rijbeveiliging (Row Level Security) staat aan op alle Supabase-tabellen,
  waardoor de database standaard afgesloten is voor iedereen die niet via
  de service_role key binnenkomt.

## 13. Problemen oplossen

| Probleem | Mogelijke oplossing |
|---|---|
| "Verplichte environment variable ontbreekt" | Controleer of `.env` bestaat en alle waarden uit `.env.example` zijn ingevuld. |
| "Kon geen verbinding maken met Supabase" | Controleer `SUPABASE_URL` en `SUPABASE_KEY` (gebruik de **service_role** key, niet de anon key). |
| "Nog geen liedjes gevonden" in het spel | Voer `python -m scripts.seed_database` uit, of voeg handmatig liedjes toe via het beheerscherm. |
| Zoeken op Spotify geeft een foutmelding | Controleer `SPOTIFY_CLIENT_ID`/`SPOTIFY_CLIENT_SECRET`, en of je Spotify-app actief is in het Developer Dashboard. |
| Geüpload geluidsfragment speelt niet af | Controleer of de storage-bucket `song-audio` bestaat en op "public" staat (stap 4 van `schema.sql` regelt dit automatisch). |
| Wijzigingen op GitHub verschijnen niet online | Controleer of je naar de juiste branch (`main`) hebt gepusht en of de Streamlit Cloud-app daaraan gekoppeld is. |

## 14. De app uitbreiden

Dit project is bewust modulair opgezet. Enkele ideeën voor vervolgstappen:

- **Statistieken-dashboard**: `session_rounds` bevat per ronde de gok en
  het echte jaar — hiermee kun je bijvoorbeeld tonen welk decennium het
  best herkend wordt.
- **Moeilijkheidsgraad**: voeg een kolom `difficulty` toe aan `songs` en
  laat begeleiders vooraf een niveau kiezen.
- **Meerdere spelmodi**: bijvoorbeeld "raad het decennium" (nog
  eenvoudiger) of "raad de artiest" als variatie.
- **Spotify Connect-afspelen**: voor instellingen met een Spotify
  Premium-account is het mogelijk (met de Authorization Code-flow i.p.v.
  Client Credentials) om muziek op een gekoppelde speaker te laten spelen
  via de Spotify Connect-API — dit vraagt wel een uitgebreidere
  OAuth-koppeling dan in deze eerste versie is meegenomen.
- **Eigen gebruikersaccounts** per begeleider i.p.v. één gedeelde pincode,
  via Supabase Auth.

## 15. Auteursrecht & muziek

De titels, artiesten en jaartallen in `data/seed_songs.csv` zijn publiek
beschikbare feitelijke informatie. Er worden **geen** muziekbestanden of
songteksten met dit project meegeleverd. Zorg dat je voor de
geluidsfragmenten die je zelf uploadt toestemming/rechten hebt passend bij
gebruik binnen je eigen instelling (bijvoorbeeld via een reeds aanwezige
muzieklicentie, of fragmenten die je zelf hebt opgenomen/aangeschaft).
