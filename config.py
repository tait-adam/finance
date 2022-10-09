import os

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

class Config:
    """ Set Flask config variables """
    FLASK_ENV = 'development'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
