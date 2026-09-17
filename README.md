# moongas-py-mediaserver

Web application for browsing and playing media library files, with advanced search filtering. The frontend is a Vue 3 + TypeScript single-page application built with Vite and served by a plain `Deno.serve` server; the Flask backend serves a JSON API plus the media files themselves.

- A component of the `moongas` ecosystem of media library tools

- [moongas-py-mediaserver](https://github.com/bretttolbert/moongas-py-mediaserver) [![CI](https://github.com/bretttolbert/moongas-py-mediaserver/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediaserver/actions/workflows/ci.yml) - Flask Web App to serve Moongas media collections enabling users to browse, search (various streaming services) and (optionally) play local media files
- [moongas-collection-demo](https://github.com/bretttolbert/moongas-collection-demo) [![CI](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml) - Example Moongas media collection (metadata only)
- [moongas-py-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) [![CI](https://github.com/bretttolbert/moongas-py-mediascan/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediascan/actions/workflows/ci.yml) - Python package for loading Moongas database and Yaml
- [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan) [![CI](https://github.com/bretttolbert/moongas-go-mediascan/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-go-mediascan/actions/workflows/ci.yml) - Golang module to scan media collections and Moongas Yaml metatadata, outputs Moongas database
- [moongas-py-mediatest](https://github.com/bretttolbert/moongas-py-mediatest) [![CI](https://github.com/bretttolbert/moongas-py-mediatest/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediatest/actions/workflows/ci.yml) - Python tool for enforcing media collection rules (implemented with `pytest`)

Uses related projects [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan) and [moongas-py-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) for scanning music library files to an sqlite database and then loading the database, respectively.

## [mediaserver Live Demo (aka _Brettify_)](https://bretttolbert.com/mediaserver)

### Filter by year range

[bretttolbert.com/mediaserver/albums?minYear=1990&maxYear=2004](https://bretttolbert.com/mediaserver/albums?minYear=1990&maxYear=2004)

### Filter by year range and genre(s)

[bretttolbert.com/mediaserver/player?minYear=1960&maxYear=2024&genre=Industrial+Metal&genre=Punk&genre=Punk+Rock&genre=Heavy+Metal&genre=Hip+Hop&genre=Urbano&genre=Thrash+Metal&genre=Nu+Metal&genre=Rock+en+español&genre=Funk+Metal&genre=Hip-Hop+français](https://bretttolbert.com/mediaserver/player?minYear=1960&maxYear=2024&genre=Industrial+Metal&genre=Punk&genre=Punk+Rock&genre=Heavy+Metal&genre=Hip+Hop&genre=Urbano&genre=Thrash+Metal&genre=Nu+Metal&genre=Rock+en+español&genre=Funk+Metal&genre=Hip-Hop+français)

### Filter by artist, album and title

[bretttolbert.com/mediaserver/player?artist=Rush&album=Grace%20Under%20Pressure&title=The%20Body%20Electric](https://bretttolbert.com/mediaserver/player?artist=Rush&album=Grace%20Under%20Pressure&title=The%20Body%20Electric)

## Screenshots

[Screenshots](./doc/screenshots/README.md)

## Vue + TypeScript frontend (Deno + Vite)

The web UI is a single-page application built with [Deno](https://deno.com/), [Vite](https://vite.dev/), [Vue 3](https://vuejs.org/) and TypeScript:

- `client/` — the Vue SPA (all TypeScript; uses npm `d3` + `d3-cloud` for the word clouds). Routes mirror the API paths (`/albums`, `/tracks`, `/artists`, `/player`, `/genres-cloud`, etc.).
- `app/api/` — Flask JSON API blueprint consumed by the SPA (`/api/config`, `/api/albums`, `/api/tracks`, `/api/artists`, `/api/artist`, `/api/genres`, `/api/artist-geo/<kind>`, `/api/wordcloud/*`, `/api/random-track`).
- `server/main.ts` — plain `Deno.serve` production server: serves the Vite build from `client/dist`, proxies `/api/*` and `/getfile/*` to Flask, and falls back to `index.html` for client-side routes.

### Development

```sh
# 1. Start the Flask backend (serves the JSON API and media files)
python run.py mediaserver-config.yml

# 2. In another shell, start the Vite dev server (proxies /api and /getfile to Flask)
deno task install   # first time only
deno task dev       # http://localhost:5173
```

If your Flask config sets `flaskConfig.urlPrefix` (e.g. `/mediaserver`), export `FLASK_URL_PREFIX=/mediaserver` (and `FLASK_BACKEND_URL` if not `http://127.0.0.1:5000`) so the dev proxy rewrites correctly.

### Production

```sh
deno task build     # builds client/ to client/dist
deno task serve     # http://localhost:8000 (env: PORT, FLASK_BACKEND_URL, FLASK_URL_PREFIX)
```

### Type checking

```sh
deno task check     # runs vue-tsc on client/ and deno check on server/
```

### Runtimes

- **Node 24+** runs the client toolchain: `deno task install` (dependency install), `dev`, `build`, and `check` (vue-tsc) all execute under Node. (Earlier Node/Deno combinations logged a noisy `AbortError` stack whenever the browser cancelled an in-flight proxied API request; Node 24 handles these cleanly.)
- **Deno** runs the production web server, `server/main.ts` (`deno task serve`).



## Features

- Simple minimalist web interface
- Perfect for a party jukebox hosted on your home WiFi network
- Multiple playback options (configurable):
    1. Play local media files in the browser (using HTML5 `<audio>` tag)
    2. "Play" by opening YouTube search for _"(artist) (album) (title) video"_ (configurable)
        - Great for finding music videos of your favorite music
        - Great for creating YouTube playlists of music videos meeting certain filter criteria (e.g. 80s New Wave music videos for your 80s party)
        - IMHO mediaserver + YouTube premium (no ads) is better than YouTube Music or Spotify
    3. (Default) Display both options
- Album art displayed at a beautiful `1000x1000px` resolution
    - (bandwidth optimized by converting to `.webp` at 80% quality if hosted by yours truly)
- Continuous shuffle playback with filtering options
- Fast (tested with a library of 20,000+ music files)
- Versatile filtering and sorting via a common set of intuitive url parameters
- Comprehensive browsing options--browse by _artist_, _album_, _genre_, _year_, _year range_, and more
- _Name That Tune_--plays a song without displaying the info, but offering hints, challenging the user to name the artist/tune
- Direct download of music files via hyperlinks
- Accessible from mobile devices (tested in Chrome on Android)


## Limitations

- Doesn't work with some `.m4a` files
    - Error: html5 audio element can't decode
- Requires that your music library be scanned with [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan)
    - `moongas-go-mediascan/cmd/scantodb` scans your music library and outputs a `mediascan.db` file
    - This must be repeated to update the music library (e.g. add new files)
    - Album art may be extracted (and converted to .webp) using the mediascan copy covers script
    - I cannot share my music files, of course, as they are copyrighted, but I can share my mediascan database with over 20,000+ tracks, allowing you to browse my extensive and painstakingly organized music library (with accurate tags, genre and year) and _play_ any track by opening a YouTube search for it. 
- Requires that music library be organized with the directory and file structure that Moongas expects
    - For example:
        - Artist folders containing album folders with `cover.jpg` (or `cover.webp`) files
        - Music filenames do not contain prohibited characters such as `+`
    - You can enforce these requirements by testing your music library with [moongas-py-mediatest](https://github.com/bretttolbert/moongas-py-mediatest)

## Coming soon

- Play entire albums
- Playlists
- Back button to go back to previous track(s) in player
- Sort by modified time

## Dependencies

- [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan) A simple and fast Go (golang) command-line utility to recursively scan a directory for media files, extract metadata (including ID3v2 tags from both MP3 and M4A files), and save the output in an sqlite3 database e.g. [mediascan.db](https://github.com/bretttolbert/mediascan/blob/main/out/mediascan.db)
- [moongas-py-mediascan] a Python library with data classes for working with the database output by `mediascan.go`

## Installation

### Install bretttolbert/moongas-py-mediascan from GitHub source 
- Install the Moongas `mediascan` python package
```bash
pip install git+https://github.com/bretttolbert/moongas-py-mediascan.git
```
- Modify the mediascan config (`mediascan-config.yml`) values (`mediadirs` etc.) as needed
- Run the `scantodb` command (requires [go](https://go.dev/doc/install))
```bash
cd moongas-go-mediascan
go run cmd/scantodb/main.go mediascan-config.yml ../mediascan.db
```

### Install bretttolbert/moongas-py-mediaserver from GitHub source 
- Clone the repo
```bash
git clone git@github.com:bretttolbert/moongas-py-mediaserver.git
cd moongas-py-mediaserver
python -m pip install .
```
- Configure `mediaPath`, etc. in the [`mediaserver-config.yml`](./mediaserver-config.yml)
- Run mediaserver
```bash
cd moongas-py-mediaserver
mediaserver mediaserver-config.yml
```

### Automatically start and run as a SystemD service

Two systemd units are provided:

- [`mediaserver.service`](./mediaserver.service) — the Flask backend (JSON API + media files)
- [`mediaserver-web.service`](./mediaserver-web.service) — the Deno web frontend (serves the Vue SPA and proxies to the backend)

To set them up:

- Customize the .service files as required
- Create a compatible Python virtual environment with the necessary dependencies
- Activate it and install mediaserver
- Update [`mediaserver.service`](./mediaserver.service) to point to your virtual environment
- Build the frontend with `deno task build` (so `client/dist` exists)
- Update [`mediaserver-web.service`](./mediaserver-web.service): set `ExecStart` to the output of `which deno` on the host, and `FLASK_BACKEND_URL` / `FLASK_URL_PREFIX` to match `mediaserver-config.yml`
- Copy both `.service` files into the systemd system folder to install them as systemd services
```bash
sudo cp mediaserver.service mediaserver-web.service /etc/systemd/system/
cd /etc/systemd/system
sudo chmod 644 mediaserver.service mediaserver-web.service
```
- Enable the services with `systemctl enable`: 
```bash
$ sudo systemctl enable mediaserver.service mediaserver-web.service
Created symlink /etc/systemd/system/multi-user.target.wants/mediaserver.service → /etc/systemd/system/mediaserver.service.
Created symlink /etc/systemd/system/multi-user.target.wants/mediaserver-web.service → /etc/systemd/system/mediaserver-web.service.
``
- Start the services (the web unit starts after the backend via `After=`)
```bash
systemctl start mediaserver.service
systemctl start mediaserver-web.service
```
- Use `systemctl status` to verify that mediaserver is running
```bash
$ systemctl status mediaserver
● mediaserver.service - mediaserver
     Loaded: loaded (/etc/systemd/system/mediaserver.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-09-07 10:25:00 CDT; 2s ago
   Main PID: 24056 (python)
      Tasks: 8 (limit: 38397)
     Memory: 181.9M (peak: 182.1M)
        CPU: 1.812s
     CGroup: /system.slice/mediaserver.service
             └─24056 /home/brett/Git/bretttolbert/moongas/env/bin/python run.py ../mediaserver-config.yml

Sep 07 10:25:00 pentatonic systemd[1]: Started mediaserver.service - mediaserver.
Sep 07 10:25:02 pentatonic python[24056]: Loading configuration from file ../mediaserver-config.yml
Sep 07 10:25:02 pentatonic python[24056]:  * Serving Flask app 'app'
Sep 07 10:25:02 pentatonic python[24056]:  * Debug mode: on
Sep 07 10:25:02 pentatonic python[24056]: WARNING: This is a development server. Do not use it in a production deployment. Use a produc>
Sep 07 10:25:02 pentatonic python[24056]:  * Running on all addresses (0.0.0.0)
Sep 07 10:25:02 pentatonic python[24056]:  * Running on http://127.0.0.1:5000
Sep 07 10:25:02 pentatonic python[24056]:  * Running on http://192.168.0.85:5000
Sep 07 10:25:02 pentatonic python[24056]: Press CTRL+C to quit
```
- If you make changes to a unit file, use the `systemctl daemon-reload` command to force systemd to reload it
```bash
systemctl daemon-reload
systemctl restart mediaserver mediaserver-web
```
- Once you have it set up to run as a service, re-scanning your library is as easy as this:
```bash
cd moongas-go-mediascan
go run cmd/scantodb/main.go mediascan-conf.yml ../mediascan.db
sudo systemctl restart mediaserver mediaserver-web
journalctl -b -f -u mediaserver
```
- Use `-u` to specify the unit by name (`mediaserver`)
- Use `-f` to follow the log so you can watch the server startup
- Use `-b` to only show output since last boot (avoids showing old output)

### Recommended directory structure for moongas

Recommendations:
- Create a `moongas` root directory and then clone the various components (such as `moongas-py-mediaserver`) inside it
- Put the active config files (`mediaserver-config.yml`, `mediascan-config.yml`) in this root directory. 
- Don't use the subproject default config files _in-place_, copy them to `moongas` root dir
- Run commands such that output files (i.e. `mediascan.db`) reside in `moongas` root directory

```bash
brett@pentatonic:~/Git/bretttolbert/moongas$ tree -L 1
.
├── env -> env-py314
├── env-py314
├── mediascan-artists.yml
├── mediascan-config.yml
├── mediascan.db
├── mediascan-files.yml
├── mediaserver-config.yml
├── moongas-go-mediascan
├── moongas-java-mediaserver
├── moongas-py-mediascan
├── moongas-py-mediaserver
├── moongas-py-mediatest
├── rename-album-files -> moongas-py-mediascan/scripts/rename_album_files.py
├── restart-local-mediaserver -> moongas-py-mediaserver/dev/scripts/restart_local_mediaserver.sh
├── restart-remote-mediaserver -> moongas-py-mediaserver/dev/scripts/restart_remote_mediaserver.sh
├── run-mediascan-scanartistsyaml -> moongas-py-mediaserver/dev/scripts/run_mediascan_scanartistsyaml.sh
├── run-mediascan-scanfilesyaml -> moongas-py-mediaserver/dev/scripts/run_mediascan_scanfilesyaml.sh
├── run-mediascan-scantodb -> moongas-py-mediaserver/dev/scripts/run_mediascan_scantodb.sh
├── run-mediatest -> moongas-py-mediaserver/dev/scripts/run_mediatest.sh
├── update-covers -> moongas-py-mediaserver/dev/scripts/update_covers.sh
├── update-everything -> moongas-py-mediaserver/dev/scripts/update_everything.sh
├── upload-covers -> moongas-py-mediaserver/dev/scripts/upload_covers.sh
├── upload-mediascandb -> moongas-py-mediaserver/dev/scripts/upload_mediascandb.sh
├── upload-moongas-py-mediascan -> moongas-py-mediaserver/dev/scripts/upload_moongas-py-mediascan.sh
└── upload-moongas-py-mediaserver -> moongas-py-mediaserver/dev/scripts/upload_moongas-py-mediaserver.sh

```
