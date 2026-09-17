from pathlib import Path
import sqlite3

import pytest
from flask import Flask

from app import create_app
from app.types.config.mediaserver_config import MediaServerConfig


@pytest.fixture()
def app(tmp_path: Path) -> Flask:
    db_file = tmp_path / "api_test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("""
        CREATE TABLE mediafile (
            id INTEGER PRIMARY KEY,
            path TEXT,
            artistpath TEXT,
            title TEXT,
            artist TEXT,
            albumartist TEXT,
            album TEXT,
            genre TEXT,
            year TEXT
        )
        """)
    conn.execute("""
        CREATE TABLE artist (
            path TEXT PRIMARY KEY,
            name TEXT,
            countrycode TEXT,
            regioncode TEXT,
            city TEXT,
            languagecode TEXT
        )
        """)
    conn.execute(
        "INSERT INTO artist (path, name, countrycode, regioncode, city, languagecode) "
        "VALUES ('/data/Music/A/Artist One', 'Artist One', 'US', 'US-AL', 'Huntsville', 'en')"
    )
    conn.execute(
        "INSERT INTO mediafile (id, path, artistpath, title, artist, albumartist, album, genre, year) "
        "VALUES (1, '/data/Music/A/Artist One/Album [2000]/01 - Track 1.mp3', "
        "'/data/Music/A/Artist One', 'Track 1', 'Artist One', 'Artist One', 'Album', 'Rock', '2000')"
    )
    conn.commit()
    conn.close()

    config = MediaServerConfig(mediascan_database_file_path=f"sqlite:///{db_file}")
    return create_app(config)


def test_api_config(app: Flask):
    client = app.test_client()
    resp = client.get("/api/config")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "playbackMethodLocalEnabled" in data
    assert "webSearchPlaybackMethods" in data
    assert "presentYear" in data


def test_api_tracks(app: Flask):
    client = app.test_client()
    resp = client.get("/api/tracks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["files"]) == 1
    assert data["files"][0]["title"] == "Track 1"
    assert data["files"][0]["genre"] == "Rock"


def test_api_tracks_filtered(app: Flask):
    client = app.test_client()
    resp = client.get("/api/tracks?genre=Jazz")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["files"]) == 0


def test_api_albums(app: Flask):
    client = app.test_client()
    resp = client.get("/api/albums")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["albums"]) == 1
    assert data["albums"][0]["album"] == "Album"
    assert data["albums"][0]["year"] == 2000


def test_api_artists(app: Flask):
    client = app.test_client()
    resp = client.get("/api/artists")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["artists"] == [{"name": "Artist One", "count": 1}]


def test_api_artist(app: Flask):
    client = app.test_client()
    resp = client.get("/api/artist?artist=Artist One")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["artist"]["name"] == "Artist One"
    assert data["artist"]["countryCode"] == "US"


def test_api_artist_not_found(app: Flask):
    client = app.test_client()
    resp = client.get("/api/artist?artist=Nobody")
    assert resp.status_code == 404


def test_api_genres(app: Flask):
    client = app.test_client()
    resp = client.get("/api/genres")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["genres"] == [{"genre": "Rock", "count": 1}]


def test_api_artist_geo(app: Flask):
    client = app.test_client()
    resp = client.get("/api/artist-geo/countries")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Country"
    assert data["items"][0]["value"] == "United States"
    assert data["items"][0]["criteria"] == {"countryCode": "US"}
    assert data["items"][0]["count"] == 1

    resp = client.get("/api/artist-geo/cities")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["items"][0]["value"] == "Huntsville (Alabama, United States)"
    assert data["items"][0]["criteria"]["city"] == "Huntsville"

    resp = client.get("/api/artist-geo/bogus")
    assert resp.status_code == 404


def test_api_wordcloud(app: Flask):
    client = app.test_client()
    resp = client.get("/api/wordcloud/genres")
    assert resp.status_code == 200
    assert resp.get_json()["words"] == [{"text": "Rock"}]

    resp = client.get("/api/wordcloud/artists")
    assert resp.status_code == 200
    assert resp.get_json()["words"] == [{"text": "Artist One"}]


def test_api_random_track(app: Flask):
    client = app.test_client()
    resp = client.get("/api/random-track")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["title"] == "Track 1"
    assert data["artist"] == "Artist One"
    assert "coverPath" in data

    resp = client.get("/api/random-track?genre=Jazz")
    assert resp.status_code == 404
