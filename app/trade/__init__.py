from flask import Blueprint

trade = Blueprint(
    'trade',
    __name__,
    template_folder='templates'
)

from . import routes
