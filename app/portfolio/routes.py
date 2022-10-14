from flask import session, render_template
from helpers import apology, login_required, lookup, usd
from app.models import db, Transaction, User

from . import portfolio


@portfolio.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    id = session["user_id"]
    transactions = []
    total = 0

    # Get all users transactions
    records = db.session.execute(
        db
        .select(Transaction)
        .filter_by(user_id=id)
    ).scalars().all()

    # Add cash holdings to total
    # If there have been no transactions get users cash
    if not records:
        cash = db.session.execute(
            db
            .select(User.cash)
            .filter_by(id=id)
        ).scalars().first()
        total += cash
    # If there are transactions, no need for a separate call to user
    else:
        cash = records[0].user.cash
        total += cash

    # Build transaction dicts for view
    for record in records:
        # Lookup current stock info
        transaction = lookup(record.symbol.symbol)

        # Calculate current valuation of holdings
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
