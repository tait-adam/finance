from flask import session, render_template
from helpers import apology, login_required, lookup, usd
from app.models import db, Transaction, User, Symbol

from . import portfolio


@portfolio.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    id = session["user_id"]
    transactions = []
    total = 0

    # Get cash holdings for user and add to total
    cash = db.session.execute(
        db.select(User.cash).filter_by(id=id)
    ).scalar()
    total += cash

    # Get transaction records for user
    records = db.session.execute(
        db.select(Transaction).filter_by(user_id=id)
    ).scalars()

    # Build transaction dicts for view
    for record in records:
        # Lookup current stock info
        record.symbol = db.session.execute(
            db.select(Symbol.symbol).filter_by(id=record.symbol_id)
        ).scalar()
        transaction = lookup(record.symbol)

        # Calculate transaction holding
        transaction['shares'] = record.shares
        current_value = record.shares * transaction['price']

        # Add current_value to total
        total += current_value

        # Format currencies to USD
        transaction['current_value'] = usd(current_value)
        transaction['price'] = usd(transaction['price'])
        transaction['paid'] = usd(record.price)

        # Add transaction to transactions array
        transactions.append(transaction)

    # return apology("PORTFOLIO")
    return render_template(
        "portfolio.html",
        transactions=transactions,
        cash=usd(cash),
        total=usd(total)
    )


@portfolio.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")
