from flask import session, render_template
from helpers import login_required, lookup, usd
from app.models import db, User, Transaction

from . import portfolio


@portfolio.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    id = session["user_id"]
    transactions = []
    total = 0

    # Get users transaction records grouped by symbol
    records = db.session.execute(
        db
        .select(Transaction, db.func.sum(Transaction.shares))
        .filter_by(user_id=id)
        .group_by(Transaction.symbol_id)
    ).all()

    # Add cash holdings to total
    cash = db.session.execute(
        db
        .select(User.cash)
        .filter_by(id=id)
    ).scalars().first()
    total += cash

    # Build transaction dicts for view
    for record in records:
        print("**************************************************************")
        print(record[0].symbol_id)
        print("**************************************************************")

        # Lookup current stock info
        transaction = lookup(record[0].symbol.symbol)

        # Calculate current valuation of holdings
        shares = record[1]
        transaction['shares'] = shares
        current_value = shares * transaction['price']

        # Add current_value to total
        total += current_value

        # Format currencies to USD
        transaction['current_value'] = usd(current_value)
        transaction['price'] = usd(transaction['price'])
        transaction['paid'] = usd(record[0].price)

        # Add transaction to transactions array
        if shares != 0:
            transactions.append(transaction)

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

    id = session["user_id"]
    transactions = []

    records = db.session.execute(
        db
        .select(Transaction)
        .filter_by(user_id=id)
    ).scalars().all()

    for record in records:
        # Build transaction object
        transaction = {}
        transaction['symbol'] = record.symbol.symbol

        # Determine Sale or Purchase
        if record.shares < 0:
            transaction['type'] = 'SALE'
        else:
            transaction['type'] = 'PURCHASE'

        transaction['shares'] = abs(record.shares)

        # Format currencies to USD
        transaction['paid'] = usd(record.price)

        # Format transaction date
        transaction['timestamp'] = record.timestamp.strftime(
            "%m/%d/%Y, %H:%M:%S"
        )

        # Add transaction to transactions array
        transactions.append(transaction)

    return render_template("history.html", transactions=transactions)
