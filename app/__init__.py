from typing import Optional
import logging
import os
from pathlib import Path
from flask import Flask
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

from app.types.config.mediaserver_config import MediaServerConfig

logger = logging.getLogger(__name__)


def register_blueprint(
    app: Flask, config: MediaServerConfig, url_prefix: Optional[str] = None
):
    from app.main import bp
    from app.api import bp as api_bp

    if url_prefix is None:
        app.register_blueprint(bp)
        app.register_blueprint(api_bp, url_prefix="/api")
    else:
        app.register_blueprint(bp, url_prefix=url_prefix)
        app.register_blueprint(api_bp, url_prefix=f"{url_prefix}/api")


def create_app(config: MediaServerConfig) -> Flask:
    root_path = config.flask_config.root_path
    url_prefix = config.flask_config.url_prefix
    static_url_path = config.flask_config.static_url_path
    app = Flask(__name__, root_path=root_path, static_url_path=static_url_path)
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
    register_blueprint(app, config, url_prefix)
    return app
