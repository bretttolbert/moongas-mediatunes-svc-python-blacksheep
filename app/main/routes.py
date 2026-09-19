"""
Non-Jinja routes kept for the web frontend (which lives in a separate repo):

- /getfile/<path>  serves media files and album covers from disk
- /api/track       returns a single random track matching the filter args
                   (this route predates the app/api router and is kept
                   for backwards compatibility)

All server-rendered page routes were removed; the frontend
single-page application renders pages client-side using the JSON API in
app/api/routes.py.
"""

import mimetypes
import os
import random
from pathlib import Path
from typing import List

from blacksheep import Application, Request, Response, file, json
from blacksheep.exceptions import NotFound

from app.types.arg_types import args_dict_to_str
from app.utils.app_utils import (
    get_config,
    get_mediascan_db_artists,
    get_mediascan_db_files_artists_joined,
)
from app.utils.media_files_utils import (
    MediaFile,
    get_cover_path,
    get_files_list,
)
from app.utils.request_args_utils import get_request_args


def register_routes(app: Application, url_prefix: str = "") -> None:
    @app.router.get(url_prefix + "/getfile/{path:path}")
    async def getfile(request: Request, path: str) -> Response:
        config = get_config(app)

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
                app.logger.error('File not found (and not a jpg): "%s"', path)
                raise NotFound()
            oldpath = path
            path = root + ".webp"
            app.logger.warning(
                "Couldn't find file, trying different file extension:\noldpath=%s\nnewpath=%s",
                oldpath,
                path,
            )
        if not Path(path).exists():
            app.logger.error('File not found: "%s"', path)
            raise NotFound()
        else:
            app.logger.debug("File exists: %s", path)

        if not path_prefix.endswith("/"):
            path_prefix = path_prefix + "/"
        if not path.startswith(path_prefix):
            app.logger.warning(
                "path (%s) doesn't match expected media path prefix (%s), refusing to serve it",
                path,
                path_prefix,
            )
            raise NotFound()

        app.logger.debug('/getfile/ serving file: "%s"', path)
        content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
        return file(path, content_type)

    @app.router.get(url_prefix + "/api/track")
    async def api_track(request: Request) -> Response:
        config = get_config(app)
        args = get_request_args(request)
        app.logger.debug("api/track args=%s", args_dict_to_str(args))
        files_list: List[MediaFile] = get_files_list(
            app,
            get_mediascan_db_files_artists_joined(app),
            get_mediascan_db_artists(app),
            args,
        )
        if not len(files_list):
            raise NotFound()
        media_file = random.choice(files_list)
        cover_path = get_cover_path(config, media_file)
        return json(
            {
                "path": media_file.path,
                "cover_path": str(cover_path),
                "artist": media_file.artist,
                "album": media_file.album,
                "title": media_file.title,
                "genre": media_file.genre,
                "year": media_file.year,
                "countryCode": media_file.countryCode,
                "regionCode": media_file.regionCode,
                "city": media_file.city,
                "languageCode": media_file.languageCode,
            }
        )
