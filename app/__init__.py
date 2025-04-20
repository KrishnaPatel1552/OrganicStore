import os
from flask import Flask
from config import Config


def create_app():
    # calculate absolute paths
    base_dir = os.path.abspath(os.path.dirname(__file__))  # .../refactored_flask_app/app
    template_dir = os.path.join(base_dir, 'templates')  # .../app/templates
    static_dir = os.path.join(base_dir, '..', 'static')  # .../static

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    app.config.from_object(Config)

    from .routes import main
    app.register_blueprint(main)

    from .db import close_db
    app.teardown_appcontext(close_db)

    return app
