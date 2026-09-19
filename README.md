# moongas-py-mediatunes-svc

> 🚧 **Status: Work in Progress (WIP)**  
> This project is currently under active development. Features, APIs, and documentation are subject to change.

---

## Overview

**Python+BlackSheep API service for Moongas hybrid media collections--backend for the `moongas-mediatunes-web` application**

### A component of the `moongas` ecosystem of media library tools

- [moongas-mediatunes-web](https://github.com/bretttolbert/moongas-mediatunes-web) [![CI](https://github.com/bretttolbert/moongas-py-mediaserver/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediatunes-web/actions/workflows/ci.yml) - A Deno-tooled TypeScript/Vue SPA for Moongas hybrid media collections, pairing with the separate moongas-py-mediatunes-svc backend to seemlessly blend offline and streaming playback
- [moongas-py-mediatunes-svc](https://github.com/bretttolbert/moongas-py-mediatunes-svc) [![CI](https://github.com/bretttolbert/moongas-py-mediaserver/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediatunes-svc/actions/workflows/ci.yml) - Python+BlackSheep API service for Moongas hybrid media collections—backend for moongas-mediatunes-web application
- [moongas-collection-demo](https://github.com/bretttolbert/moongas-collection-demo) [![CI](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml) - Example Moongas media collection (metadata only)
- [moongas-py-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) [![CI](https://github.com/bretttolbert/moongas-py-mediascan/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediascan/actions/workflows/ci.yml) - Python package for loading Moongas database and Yaml
- [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan) [![CI](https://github.com/bretttolbert/moongas-go-mediascan/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-go-mediascan/actions/workflows/ci.yml) - Golang module to scan media collections and Moongas Yaml metatadata, outputs Moongas database
- [moongas-py-mediatest](https://github.com/bretttolbert/moongas-py-mediatest) [![CI](https://github.com/bretttolbert/moongas-py-mediatest/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediatest/actions/workflows/ci.yml) - Python tool for enforcing media collection rules (implemented with `pytest`)

## Dependencies

- [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan) - used for: scanning music library files into a Moongas sqlite3 database
- [moongas-py-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) - used for: loading the Moongas database

## Live Demos
- [Live Demo (hosted on bretttolbert.com)](https://bretttolbert.com/mediaserver)
- [Live Demo (hosted on moongas.org)](https://moongas.org/mediaserver)

### Filter by year range

[bretttolbert.com/mediatunes-service/albums?minYear=1990&maxYear=2004](https://bretttolbert.com/mediatunes-service/albums?minYear=1990&maxYear=2004)

### Filter by year range and genre(s)

[bretttolbert.com/mediatunes-service/player?minYear=1960&maxYear=2024&genre=Industrial+Metal&genre=Punk&genre=Punk+Rock&genre=Heavy+Metal&genre=Hip+Hop&genre=Urbano&genre=Thrash+Metal&genre=Nu+Metal&genre=Rock+en+español&genre=Funk+Metal&genre=Hip-Hop+français](https://bretttolbert.com/mediatunes-service/player?minYear=1960&maxYear=2024&genre=Industrial+Metal&genre=Punk&genre=Punk+Rock&genre=Heavy+Metal&genre=Hip+Hop&genre=Urbano&genre=Thrash+Metal&genre=Nu+Metal&genre=Rock+en+español&genre=Funk+Metal&genre=Hip-Hop+français)

### Filter by artist, album and title

[bretttolbert.com/mediatunes-service/player?artist=Rush&album=Grace%20Under%20Pressure&title=The%20Body%20Electric](https://bretttolbert.com/mediatunes-service/player?artist=Rush&album=Grace%20Under%20Pressure&title=The%20Body%20Electric)

## Screenshots

[Screenshots](./doc/screenshots/README.md)

## Web frontend

The web UI single-page application (Vue 3 + TypeScript, built with Vite) has moved to a separate repo. It consumes this backend's JSON API (`app/api/` — `/api/config`, `/api/albums`, `/api/tracks`, `/api/artists`, `/api/artist`, `/api/genres`, `/api/artist-geo/<kind>`, `/api/wordcloud/*`, `/api/random-track`) and the media files via `/getfile/*`.

### Running the backend

```sh
python run.py mediatunes-config.yml
```

## Features

- Simple minimalist web interface
- Perfect for a party jukebox hosted on your home WiFi network
- Multiple playback options (configurable):
    1. Play local media files in the browser (using HTML5 `<audio>` tag)
    2. "Play" by opening YouTube search for _"(artist) (album) (title) video"_ (configurable)
        - Great for finding music videos of your favorite music
        - Great for creating YouTube playlists of music videos meeting certain filter criteria (e.g. 80s New Wave music videos for your 80s party)
        - IMHO mediatunes-service + YouTube premium (no ads) is better than YouTube Music or Spotify
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

### Install bretttolbert/moongas-py-mediatunes-service from GitHub source 
- Clone the repo
```bash
git clone git@github.com:bretttolbert/moongas-py-mediatunes-service.git
cd moongas-py-mediatunes-service
python -m pip install .
```
- Configure `mediaPath`, etc. in the [`mediatunes-config.yml`](./mediatunes-config.yml)
- Run mediatunes-service
```bash
cd moongas-py-mediatunes-service
mediatunes-service mediatunes-config.yml
```

### Automatically start and run as a SystemD service

A systemd unit is provided:

- [`mediatunes-svc.service`](./mediatunes-svc.service) — the BlackSheep backend (JSON API + media files)

To set it up:

- Customize the .service file as required
- Create a compatible Python virtual environment with the necessary dependencies
- Activate it and install mediatunes-service
- Update [`mediatunes-service.service`](./mediatunes-service.service) to point to your virtual environment
- Copy the `.service` file into the systemd system folder to install it as a systemd service
```bash
sudo cp mediatunes-service.service /etc/systemd/system/
cd /etc/systemd/system
sudo chmod 644 mediatunes-service.service
```
- Enable the service with `systemctl enable`: 
```bash
$ sudo systemctl enable mediatunes-service.service
Created symlink /etc/systemd/system/multi-user.target.wants/mediatunes-service.service → /etc/systemd/system/mediatunes-service.service.
```
- Start the service
```bash
systemctl start mediatunes-service.service
```
- Use `systemctl status` to verify that mediatunes-service is running
```bash
$ systemctl status mediatunes-service
● mediatunes-service.service - mediatunes-service
     Loaded: loaded (/etc/systemd/system/mediatunes-service.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-09-07 10:25:00 CDT; 2s ago
   Main PID: 24056 (python)
      Tasks: 8 (limit: 38397)
     Memory: 181.9M (peak: 182.1M)
        CPU: 1.812s
     CGroup: /system.slice/mediatunes-service.service
             └─24056 /home/brett/Git/bretttolbert/moongas/env/bin/python run.py ../mediatunes-config.yml

Sep 07 10:25:00 pentatonic systemd[1]: Started mediatunes-service.service - mediatunes-service.
Sep 07 10:25:02 pentatonic python[24056]: Loading configuration from file ../mediatunes-config.yml
Sep 07 10:25:02 pentatonic python[24056]: INFO:     Started server process [24056]
Sep 07 10:25:02 pentatonic python[24056]: INFO:     Waiting for application startup.
Sep 07 10:25:02 pentatonic python[24056]: INFO:     Application startup complete.
Sep 07 10:25:02 pentatonic python[24056]: INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```
- If you make changes to a unit file, use the `systemctl daemon-reload` command to force systemd to reload it
```bash
systemctl daemon-reload
systemctl restart mediatunes-service
```
- Once you have it set up to run as a service, re-scanning your library is as easy as this:
```bash
cd moongas-go-mediascan
go run cmd/scantodb/main.go mediascan-conf.yml ../mediascan.db
sudo systemctl restart mediatunes-service
journalctl -b -f -u mediatunes-service
```
- Use `-u` to specify the unit by name (`mediatunes-service`)
- Use `-f` to follow the log so you can watch the server startup
- Use `-b` to only show output since last boot (avoids showing old output)

### Recommended directory structure for moongas

Recommendations:
- Create a `moongas` root directory and then clone the various components (such as `moongas-py-mediatunes-service`) inside it
- Put the active config files (`mediatunes-config.yml`, `mediascan-config.yml`) in this root directory. 
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
├── mediatunes-config.yml
├── moongas-go-mediascan
├── moongas-java-mediatunes-service
├── moongas-py-mediascan
├── moongas-py-mediatunes-service
├── moongas-py-mediatest
├── rename-album-files -> moongas-py-mediascan/scripts/rename_album_files.py
├── restart-local-mediatunes-service -> moongas-py-mediatunes-service/dev/scripts/restart_local_mediaserver.sh
├── restart-remote-mediatunes-service -> moongas-py-mediatunes-service/dev/scripts/restart_remote_mediaserver.sh
├── run-mediascan-scanartistsyaml -> moongas-py-mediatunes-service/dev/scripts/run_mediascan_scanartistsyaml.sh
├── run-mediascan-scanfilesyaml -> moongas-py-mediatunes-service/dev/scripts/run_mediascan_scanfilesyaml.sh
├── run-mediascan-scantodb -> moongas-py-mediatunes-service/dev/scripts/run_mediascan_scantodb.sh
├── run-mediatest -> moongas-py-mediatunes-service/dev/scripts/run_mediatest.sh
├── update-covers -> moongas-py-mediatunes-service/dev/scripts/update_covers.sh
├── update-everything -> moongas-py-mediatunes-service/dev/scripts/update_everything.sh
├── upload-covers -> moongas-py-mediatunes-service/dev/scripts/upload_covers.sh
├── upload-mediascandb -> moongas-py-mediatunes-service/dev/scripts/upload_mediascandb.sh
├── upload-moongas-py-mediascan -> moongas-py-mediatunes-service/dev/scripts/upload_moongas-py-mediascan.sh
└── upload-moongas-py-mediatunes-service -> moongas-py-mediatunes-service/dev/scripts/upload_moongas-py-mediaserver.sh

```
