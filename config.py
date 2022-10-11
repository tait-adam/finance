import os
basedir = os.path.abspath(os.path.dirname(__file__))

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


class Config:
    """ Set Flask config variables """

    # General Config
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = 'development'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    TEMPLATES_AUTO_RELOAD = True

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'finance.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
