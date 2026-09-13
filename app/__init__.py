from typing import Any, Iterable, Optional, cast
from datetime import datetime
import logging
import os
from pathlib import Path
from urllib.parse import quote_plus
from flask import Flask
import flask_jsglue
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

from app.types.config.mediaserver_config import MediaServerConfig

logger = logging.getLogger(__name__)


def format_results_string(l: Iterable[Any], max_results: int):
    L = len(list(l))
    return f"{L:,}{'+' if L >= max_results else ''} {'result' if L == 1 else 'results'}"


def register_filters(app: Flask, config: MediaServerConfig):
    filters = cast(dict[str, Any], cast(Any, app.jinja_env).filters)

    def format_results(l: Iterable[Any]) -> str:
        return format_results_string(l, config.max_results)

    filters["result_or_results"] = format_results

    def format_album_covers_results(l: Iterable[Any]) -> str:
        return format_results_string(l, config.max_results_album_covers)

    filters["result_or_results_album_covers"] = format_album_covers_results
    filters["quote_plus"] = quote_plus

    def make_list(s: Iterable[Any]) -> list[Any]:
        return list(s)

    filters["make_list"] = make_list


def set_globals(
    app: Flask,
    config: MediaServerConfig,
):
    globals_ = cast(dict[str, Any], cast(Any, app.jinja_env).globals)

    globals_["PRESENT_YEAR"] = datetime.now().year
    globals_["PLAYBACK_METHOD_LOCAL_ENABLED"] = config.playback_methods.local.enabled

    globals_["WEB_SEARCH_PLAYBACK_METHODS"] = [
        method for method in config.playback_methods.webSearch if method.enabled
    ]

    globals_["AGE_VERIFICATION"] = config.age_verification

    globals_["LIMIT_BANDWIDTH"] = config.limit_bandwidth


def register_blueprint(
    app: Flask, config: MediaServerConfig, url_prefix: Optional[str] = None
):
    from app.main import bp

    globals_ = cast(dict[str, Any], cast(Any, app.jinja_env).globals)

    if url_prefix is None:
        app.register_blueprint(bp)
        globals_["URL_PREFIX"] = ""
    else:
        app.register_blueprint(bp, url_prefix=url_prefix)
        globals_["URL_PREFIX"] = url_prefix


def create_app(config: MediaServerConfig) -> Flask:
    root_path = config.flask_config.root_path
    url_prefix = config.flask_config.url_prefix
    static_url_path = config.flask_config.static_url_path
    app = Flask(__name__, root_path=root_path, static_url_path=static_url_path)
    flask_jsglue.init(app, url_prefix)
    app.logger.debug("flask_config.root_path: %s", root_path)
    app.logger.debug("flask_config.url_prefix: %s", url_prefix)
    app.logger.debug("flask_config.static_url_path: %s", static_url_path)
    app.config["MEDIASERVER_CONFIG"] = config

    db_path = config.mediascan_database_file_path
    if not db_path:
        error_msg = "No mediascan database file path configured in mediaserver config."
        app.logger.error(error_msg)
        raise ValueError(error_msg)

    # Validate SQLite database file path if applicable
    if db_path.startswith("sqlite:///"):
        sqlite_file_str = db_path[len("sqlite:///") :]
        if sqlite_file_str and sqlite_file_str != ":memory:":
            sqlite_path = Path(sqlite_file_str).expanduser()
            resolved_sqlite_path = sqlite_path.resolve()
            app.logger.info(
                "Configured SQLite database path: '%s' (resolved: '%s')",
                db_path,
                resolved_sqlite_path,
            )
            if not resolved_sqlite_path.exists():
                error_msg = (
                    f"SQLite database file not found at '{resolved_sqlite_path}' "
                    f"(from config: '{db_path}', current directory: '{os.getcwd()}'). "
                    "Please verify that the database path in your config is correct and that the database file exists."
                )
                app.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            if resolved_sqlite_path.stat().st_size == 0:
                error_msg = (
                    f"SQLite database file at '{resolved_sqlite_path}' is empty (0 bytes). "
                    "Please populate the database using mediascan before running mediaserver."
                )
                app.logger.error(error_msg)
                raise ValueError(error_msg)
    else:
        app.logger.info("Configured database URL: '%s'", db_path)

    try:
        engine = create_engine(db_path)
        app.config["ENGINE"] = engine
    except Exception as ex:
        app.logger.error("Failed to create SQLAlchemy engine for '%s': %s", db_path, ex)
        raise

    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        app.logger.debug("Discovered database tables: %s", table_names)

        required_tables = ["mediafile", "artist"]
        missing_tables = [t for t in required_tables if t not in table_names]
        if missing_tables:
            error_msg = (
                f"Database '{db_path}' is missing required table(s): {missing_tables}. "
                f"Tables found in database: {table_names}. "
                "Please verify that this is a valid mediascan database."
            )
            app.logger.error(error_msg)
            raise ValueError(error_msg)
    except (SQLAlchemyError, ValueError):
        raise
    except Exception as ex:
        app.logger.error("Failed to inspect tables in database '%s': %s", db_path, ex)
        raise

    try:
        with engine.connect() as conn:
            app.config["MEDIASCAN_DB_CONN"] = conn
            app.logger.info("Loading 'mediafile' table from database...")
            files_df = pd.read_sql_query("SELECT * FROM mediafile", conn)
            app.config["MEDIASCAN_DB_FILES"] = files_df

            app.logger.info("Loading 'artist' table from database...")
            artists_df = pd.read_sql_query("SELECT * FROM artist", conn)
            app.config["MEDIASCAN_DB_ARTISTS"] = artists_df

            app.logger.info("Joining media files and artists...")
            joined_df = pd.read_sql_query(
                "SELECT * FROM mediafile LEFT JOIN artist ON mediafile.artistpath = artist.path",
                conn,
            )
            app.config["MEDIASCAN_DB_FILES_ARTISTS_JOINED"] = joined_df

            app.logger.info(
                "Successfully loaded %d media files and %d artists from database.",
                len(files_df),
                len(artists_df),
            )
    except SQLAlchemyError as ex:
        app.logger.error(
            "SQLAlchemy error executing queries on database '%s': %s",
            db_path,
            ex,
        )
        raise
    except Exception as ex:
        app.logger.error(
            "Unexpected error loading data from database '%s': %s", db_path, ex
        )
        raise

    app.debug = config.flask_config.debug
    register_filters(app, config)
    set_globals(app, config)
    register_blueprint(app, config, url_prefix)
    return app
