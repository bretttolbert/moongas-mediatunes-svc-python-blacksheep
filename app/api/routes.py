"""
JSON API routes consumed by the mediatunes-service web frontend.

The frontend single-page application lives in a separate repo; these
endpoints expose the media library data as JSON so it can render pages
client-side. They reuse the filtering/counting logic in
app/utils/media_files_utils.py.
"""

import random
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, cast

from flask import abort, current_app, request

from app.api import bp
from app.types.arg_types import args_dict_to_str
from app.utils.app_utils import (
    get_config,
    get_mediascan_db_artists,
    get_mediascan_db_files_artists_joined,
)
from app.utils.media_files_utils import (
    MediaFile,
    get_albums,
    get_artist,
    get_artist_counts,
    get_country_code_name_map,
    get_cover_path,
    get_files_list,
    get_genre_counts,
    get_language_code_name_map,
    get_region_code_name_map,
    get_tracks,
    get_word_cloud_data_artists,
    get_word_cloud_data_genres,
)
from app.utils.request_args_utils import get_request_args


class ArtistRow(NamedTuple):
    """
    Typed view of an artist row, as returned by get_artist()
    (a pandas namedtuple built from the 'artist' table).
    """

    name: Any
    countrycode: Any
    regioncode: Any
    city: Any
    languagecode: Any


@bp.route("/config")
def config() -> Dict[str, Any]:
    """Client-facing configuration (playback methods, limits, feature flags)."""
    cfg = get_config(current_app)
    return {
        "playbackMethodLocalEnabled": cfg.playback_methods.local.enabled,
        "webSearchPlaybackMethods": [
            {"name": m.name, "searchQueryUrlFormat": m.search_query_url_format}
            for m in cfg.playback_methods.webSearch
            if m.enabled
        ],
        "ageVerification": cfg.age_verification,
        "limitBandwidth": cfg.limit_bandwidth,
        "maxResults": cfg.max_results,
        "maxResultsAlbumCovers": cfg.max_results_album_covers,
        "presentYear": datetime.now().year,
    }


@bp.route("/albums")
def albums() -> Dict[str, Any]:
    args = get_request_args(request)
    current_app.logger.debug("api/albums args=%s", args_dict_to_str(args))
    album_list = get_albums(
        current_app,
        get_mediascan_db_files_artists_joined(current_app),
        get_mediascan_db_artists(current_app),
        args,
    )
    return {
        "albums": [
            {
                "artist": album.artist,
                "album": album.album,
                "year": album.year,
                "coverPath": str(album.cover_path),
            }
            for album in album_list
        ]
    }


@bp.route("/tracks")
def tracks() -> Dict[str, Any]:
    args = get_request_args(request)
    current_app.logger.debug("api/tracks args=%s", args_dict_to_str(args))
    track_list: List[MediaFile] = get_tracks(
        current_app,
        get_mediascan_db_files_artists_joined(current_app),
        get_mediascan_db_artists(current_app),
        args,
    )
    cover_path: Path = Path()
    if len(track_list):
        cover_path = get_cover_path(get_config(current_app), track_list[0])
    return {
        "files": [asdict(t) for t in track_list],
        "coverPath": str(cover_path),
    }


@bp.route("/artists")
def artists() -> Dict[str, Any]:
    args = get_request_args(request)
    current_app.logger.debug("api/artists args=%s", args_dict_to_str(args))
    artist_counts = get_artist_counts(
        current_app,
        get_mediascan_db_files_artists_joined(current_app),
        get_mediascan_db_artists(current_app),
        args,
    )
    return {
        "artists": [
            {"name": name, "count": count} for name, count in artist_counts.items()
        ]
    }


@bp.route("/artist")
def artist() -> Dict[str, Any]:
    args = get_request_args(request)
    current_app.logger.debug("api/artist args=%s", args_dict_to_str(args))
    result = cast(
        ArtistRow | None,
        get_artist(
            current_app,
            get_mediascan_db_files_artists_joined(current_app),
            get_mediascan_db_artists(current_app),
            args,
        ),
    )
    if result is None:
        current_app.logger.error("Artist not found for request arguments: %s", args)
        abort(404)
    return {
        "artist": {
            "name": str(result.name),
            "countryCode": str(result.countrycode),
            "regionCode": str(result.regioncode),
            "city": str(result.city),
            "languageCode": str(result.languagecode),
        }
    }


@bp.route("/genres")
def genres() -> Dict[str, Any]:
    sort: str = ""
    value = request.args.get("sort")
    if value:
        sort = value
    genre_counts = get_genre_counts(
        get_mediascan_db_files_artists_joined(current_app), sort=sort
    )
    return {
        "genres": [
            {"genre": genre, "count": count} for genre, count in genre_counts.items()
        ]
    }


def _artist_geo_counts(kind: str) -> List[Dict[str, Any]]:
    """
    Count artists by a geo attribute and return user-facing names plus the
    filter criteria (so the client can build its own router links).
    """
    artists_df = get_mediascan_db_artists(current_app)

    country_map = get_country_code_name_map(current_app)
    region_map = get_region_code_name_map(current_app)
    language_map = get_language_code_name_map(current_app)

    # uniq_key -> [display_value, criteria_dict, count]
    counts: Dict[str, List[Any]] = {}
    name = ""
    for row in artists_df.itertuples():
        cc = str(row.countrycode)
        rc = str(row.regioncode)
        city = str(row.city)
        lc = str(row.languagecode)
        criteria: Dict[str, str] = {}
        if kind == "countries":
            name = "Country"
            if cc not in country_map:
                current_app.logger.error("Failed to find name for countrycode=%s", cc)
                continue
            value = country_map[cc]
            criteria = {"countryCode": cc}
        elif kind == "regions":
            name = "Region"
            if rc not in region_map:
                current_app.logger.error("Failed to find name for regioncode=%s", rc)
                continue
            value = region_map[rc]
            criteria = {"regionCode": rc}
        elif kind == "languages":
            name = "Language"
            if lc not in language_map:
                current_app.logger.error("Failed to find name for languagecode=%s", lc)
                continue
            value = language_map[lc]
            criteria = {"languageCode": lc}
        elif kind == "cities":
            name = "City"
            qualifiers: List[str] = []
            if rc in region_map:
                qualifiers.append(region_map[rc])
            if cc in country_map:
                qualifiers.append(country_map[cc])
            value = city
            if len(qualifiers):
                value = f"{city} ({', '.join(qualifiers)})"
            criteria = {"city": city, "regionCode": rc, "countryCode": cc}
        else:
            abort(404)

        uniq_key = f"{value}|{sorted(criteria.items())}"
        if uniq_key in counts:
            counts[uniq_key][2] += 1
        else:
            counts[uniq_key] = [value, criteria, 1]

    # default sort: by count (descending)
    items = sorted(counts.values(), key=lambda item: item[2], reverse=True)
    return [
        {"name": name, "value": value, "criteria": criteria, "count": count}
        for value, criteria, count in items
    ]


@bp.route("/artist-geo/<kind>")
def artist_geo(kind: str) -> Dict[str, Any]:
    """kind is one of: countries, regions, cities, languages"""
    if kind not in ("countries", "regions", "cities", "languages"):
        abort(404)
    return {"items": _artist_geo_counts(kind)}


@bp.route("/wordcloud/genres")
def wordcloud_genres() -> Dict[str, Any]:
    return {
        "words": get_word_cloud_data_genres(
            get_mediascan_db_files_artists_joined(current_app)
        )
    }


@bp.route("/wordcloud/artists")
def wordcloud_artists() -> Dict[str, Any]:
    return {
        "words": get_word_cloud_data_artists(
            current_app,
            get_mediascan_db_files_artists_joined(current_app),
            get_mediascan_db_artists(current_app),
            get_request_args(request),
        )
    }


@bp.route("/random-track")
def random_track() -> Dict[str, Any]:
    """
    Same behavior as main.api_track (/api/track on the main blueprint):
    returns a single random track matching the filter args.
    """
    cfg = get_config(current_app)
    args = get_request_args(request)
    current_app.logger.debug("api/random-track args=%s", args_dict_to_str(args))
    files_list: List[MediaFile] = get_files_list(
        current_app,
        get_mediascan_db_files_artists_joined(current_app),
        get_mediascan_db_artists(current_app),
        args,
    )
    if not len(files_list):
        abort(404)
    file = random.choice(files_list)
    cover_path = get_cover_path(cfg, file)
    return {
        "path": file.path,
        "coverPath": str(cover_path),
        "artist": file.artist,
        "album": file.album,
        "title": file.title,
        "genre": file.genre,
        "year": file.year,
        "countryCode": file.countryCode,
        "regionCode": file.regionCode,
        "city": file.city,
        "languageCode": file.languageCode,
    }
