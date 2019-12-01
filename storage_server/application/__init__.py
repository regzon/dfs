import logging
import logging.config

from flask import Flask

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    logging.config.fileConfig(
        'logging.conf',
        disable_existing_loggers=False,
    )

    @app.route('/')
    def hello_world():
        return "Hello world"

    return app
