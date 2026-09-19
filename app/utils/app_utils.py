from typing import cast
from flask import current_app, Flask

import sqlalchemy as sa

import pandas as pd

from app.types.config.mediatunes_svc_config import MediatunesServiceConfig


def get_config(app: Flask) -> MediatunesServiceConfig:
    return cast(MediatunesServiceConfig, current_app.config["MEDIATUNES_SVC_CONFIG"])


def get_mediascan_db_connection(app: Flask) -> sa.Connection:
    return cast(sa.Connection, current_app.config["MEDIASCAN_DB_CONN"])


def get_mediascan_db_files(app: Flask) -> pd.DataFrame:
    return cast(pd.DataFrame, current_app.config["MEDIASCAN_DB_FILES"])


def get_mediascan_db_artists(app: Flask) -> pd.DataFrame:
    return cast(pd.DataFrame, current_app.config["MEDIASCAN_DB_ARTISTS"])


def get_mediascan_db_files_artists_joined(app: Flask) -> pd.DataFrame:
    return cast(pd.DataFrame, current_app.config["MEDIASCAN_DB_FILES_ARTISTS_JOINED"])
