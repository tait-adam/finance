# TODO: Make sure all the http status response codes are correct

from cs50 import SQL
from flask import Flask, flash
from flask_session import Session
from tempfile import mkdtemp

from helpers import usd
from database import setup, teardown


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
teardown(db)
setup(db)


def init_app():
    """Initialise the core application"""

    # Configure application
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    Session(app)

    with app.app_context():
        from . import auth
        from . import trade
        from . import portfolio
        app.register_blueprint(auth.auth)
        app.register_blueprint(trade.trade)
        app.register_blueprint(portfolio.portfolio)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app
