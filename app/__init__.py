import os
import yaml
from flask import Flask, send_from_directory
from dynaconf import FlaskDynaconf
from pathlib import Path
import logging
import logging.config

def create_app():
    """Initialize the Flask app instance"""

    app = Flask(__name__)
    dynaconf = FlaskDynaconf(extensions_list=True)

    with app.app_context():
        # route for favicon
        @app.route('/favicon.ico')
        def favicon():
            try:
                app.logger.info("Favicon requested")
                return send_from_directory(
                    os.path.join(app.root_path, 'static', 'images'), 'favicon.ico', mimetype="image/vnd.microsoft.icon"
                )
            except Exception as e:
                app.logger.error(f"Error serving favicon: {e}")
                raise
        
        # initialize plugins
        os.environ["ROOT_PATH_FOR_DYNACONF"] = app.root_path
        dynaconf.init_app(app)

        #app.config["SECRET_KEY"] = bytearray(app.config["SECRET_KEY"], "UTF-8")

        _configure_logging(app, dynaconf)

        # import the routes
        from . import intro

        # register the blueprints
        app.register_blueprint(intro.intro_bp)

        return app
    
def _configure_logging(app, dynaconf):
    logging_config_path = Path(app.root_path).parent / "logging_config.yaml"
    with open(logging_config_path, "r") as fh:
        logging_config = yaml.safe_load(fh.read())
        env_logging_level = dynaconf.settings.get("logging_level", "INFO").upper()
        logging_level = logging.INFO if env_logging_level == "INFO" else logging.DEBUG
        logging_config["handlers"]["console"]["level"] = logging_level
        logging_config["loggers"][""]["level"] = logging_level
        logging.config.dictConfig(logging_config)
