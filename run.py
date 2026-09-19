import logging
import sys
from pathlib import Path

from app import create_app
from app.utils.config.mediatunes_svc_config_util import MediatunesServiceConfigUtil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mediatunes_svc")


def main():
    config_filepath = None
    if len(sys.argv) > 1:
        config_filepath = Path(sys.argv[1])
        logger.info("Loading configuration from file: %s", config_filepath)
    else:
        logger.warning("No config file specified, loading default configuration")

    try:
        config = MediatunesServiceConfigUtil().load_config(config_filepath)
    except Exception as ex:
        logger.error("Failed to load configuration from '%s': %s", config_filepath, ex)
        sys.exit(1)

    if config.flask_config.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    try:
        app = create_app(config)
    except Exception as ex:
        logger.error("Failed to initialize mediatunes-service application: %s", ex)
        sys.exit(1)

    if config_filepath is None:
        app.logger.warning(
            "No config file specified, running with default configuration"
        )
    else:
        app.logger.info("Loaded configuration from file: %s", config_filepath)

    try:
        app.run(
            debug=config.flask_config.debug,
            use_debugger=config.flask_config.use_debugger,
            use_reloader=config.flask_config.use_reloader,
            host=config.flask_config.host,
            port=config.flask_config.port,
        )
    except Exception as ex:
        logger.error("Error while running mediatunes-service: %s", ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
