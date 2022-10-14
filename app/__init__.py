# TODO: Make sure all the http status response codes errors are handled
# TODO: Define UNIQUE indexes on any fields that should be unique.
# TODO: Define (non-UNIQUE) indexes on any fields via which you will search
#       (as via SELECT with WHERE).
# TODO: Decide if we need tempfile/mkdtemp
# TODO: Decide if I'm happy with all my db calls

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from helpers import usd, apology

# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()


def init_app():
    """Initialise the core application"""

    # Configure application
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    with app.app_context():
        register_blueprints(app)
        initialise_extensions(app, db)
        configure_logging(app)
        register_error_handlers(app)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app


# Helper Functions
def register_blueprints(app):
    from app.auth import auth
    from app.trade import trade
    from app.portfolio import portfolio
    app.register_blueprint(auth)
    app.register_blueprint(trade)
    app.register_blueprint(portfolio)


def initialise_extensions(app, db):
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)


def configure_logging(app):
    # https://towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery-90281349fb7a
    pass


def register_error_handlers(app):
    """
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    1xx informational response
    2xx success
    3xx redirection
    4xx client error
    5xx server error
    """

    @app.errorhandler(404)
    def page_not_found(e):
        return apology('Page Not Found', 404)
