from flask import Blueprint

portfolio = Blueprint(
    'portfolio',
    __name__,
    template_folder='templates'
)

from app.portfolio import routes