"""
Non-Jinja routes kept for the Vue SPA frontend:

- /getfile/<path>  serves media files and album covers from disk
- /api/track       returns a single random track matching the filter args
                   (this route predates the app/api blueprint and is kept
                   for backwards compatibility)

All server-rendered Jinja page routes were removed; the SPA (client/)
renders pages client-side using the JSON API in app/api/routes.py.
"""

import os
import random
from pathlib import Path
from typing import Dict, List

from flask import (
    abort,
    current_app,
    request,
    send_from_directory,
    Response,
)

from app.main import bp
from app.types.arg_types import args_dict_to_str
from app.utils.request_args_utils import get_request_args
from app.utils.media_files_utils import (
    MediaFile,
    get_cover_path,
    get_files_list,
)
from app.utils.app_utils import (
    get_config,
    get_mediascan_db_artists,
    get_mediascan_db_files_artists_joined,
)


@bp.route("/getfile/<path:path>")
def getfile(path: str) -> Response:
    config = get_config(current_app)

    # path_prefix = /var/www/html/Covers/
    # path = /var/www/html/Covers/MusicOther/Johnny Cash/With His Hot and Blue Guitar [1957]/cover.jpg
    # path_without_prefix = MusicOther/Johnny Cash/With His Hot and Blue Guitar [1957]/cover.jpg

    if not path.startswith("/"):
        path = "/" + path
    path_prefix = config.playback_methods.local.media_path
    if path.startswith(config.album_covers_path):
        path_prefix = config.album_covers_path

    if not Path(path).exists():
        # if it's a jpg, try looking for webp instead of jpg
        # in case someone (me) converted the original jpgs to webp
        root, ext = os.path.splitext(path)
        if ext != ".jpg":
            current_app.logger.error('File not found (and not a jpg): "%s"', path)
            abort(404)
        oldpath = path
        path = root + ".webp"
        current_app.logger.warning(
            "Couldn't find file, trying different file extension:\noldpath=%s\nnewpath=%s",
            oldpath,
            path,
        )
    if not Path(path).exists():
        current_app.logger.error('File not found: "%s"', path)
        abort(404)
    else:
        current_app.logger.debug("File exists: %s", path)

    if not path_prefix.endswith("/"):
        path_prefix = path_prefix + "/"
    if path.startswith(path_prefix):
        path_without_prefix = path[len(path_prefix) :]
        current_app.logger.debug(
            '/getfile/ path="%s" path_prefix="%s" path_without_prefix="%s"',
            path,
            path_prefix,
            path_without_prefix,
        )
        current_app.logger.debug(
            'send_from_directory("%s", "%s")', path_prefix, path_without_prefix
        )
        return send_from_directory(path_prefix, path_without_prefix)
    else:
        current_app.logger.warning(
            "path (%s) doesn't match expected media path prefix (%s), refusing to serve it",
            path,
            path_prefix,
        )
        abort(404)


@bp.route("/api/track")
def api_track() -> Dict[str, object]:
    config = get_config(current_app)
    args = get_request_args(request)
    current_app.logger.debug("api/track args=%s", args_dict_to_str(args))
    files_list: List[MediaFile] = get_files_list(
        current_app,
        get_mediascan_db_files_artists_joined(current_app),
        get_mediascan_db_artists(current_app),
        args,
    )
    if not len(files_list):
        abort(404)
    file = random.choice(files_list)
    cover_path = get_cover_path(config, file)
    return {
        "path": file.path,
        "cover_path": str(cover_path),
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
