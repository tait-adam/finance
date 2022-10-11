# TODO: Make sure all the http status response codes errors are handled

from flask import Flask
from flask_session import Session
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy

from helpers import usd
# from .seed import transaction_types as seed_data


# Globally accessible libraries
db = SQLAlchemy()
# TODO: Add flask-migrate so I can seed db


def init_app():
    """Initialise the core application"""

    # Configure application
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialise Plugins
    db.init_app(app)
    Session(app)

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    with app.app_context():
        from app.auth import auth
        from app.trade import trade
        from app.portfolio import portfolio
        app.register_blueprint(auth)
        app.register_blueprint(trade)
        app.register_blueprint(portfolio)
        db.create_all()

        # TODO: Seed transaction_types
        # from app.models import TransactionType

        # db.engine.execute(
        #     TransactionType.__table__.insert(),
        #     seed_data
        # )

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app
