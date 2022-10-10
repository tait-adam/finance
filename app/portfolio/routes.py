from helpers import apology, login_required

from . import portfolio


@portfolio.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("PORTFOLIO")


@portfolio.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")
