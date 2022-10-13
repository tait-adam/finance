from flask import request, redirect, render_template, session
from helpers import apology, login_required, lookup, is_pos_int
from app.models import db, User, Transaction, Symbol

from . import trade


@trade.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not quote:
            return apology("Symbol not recognised", 404)
        else:
            return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@trade.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = lookup(symbol)
        id = session["user_id"]
        cash_available = db.one_or_404(
            db.select(User.cash).filter_by(id=id)
        )

        # Ensure symbol is not blank...
        if not symbol:
            return apology("Symbol cannot be blank!", 403)
        # ... and exists
        elif not quote:
            return apology("Symbol does not exist", 403)

        # Ensure number of shares is a positive integer
        elif not is_pos_int(shares):
            return apology("Must be a positive integer!", 403)

        # Ensure user can afford the purchase
        elif (shares * quote["price"]) > cash_available:
            return apology("You can't afford it homeboy", 403)

        else:
            # Get symbol id or generate new one
            record = db.session.execute(
                db.select(Symbol.id).filter_by(symbol=symbol)
            ).first()

            if record is not None:
                symbol_id = record[0]
            else:
                new_symbol = Symbol(
                    symbol=symbol.upper()
                )
                db.session.add(new_symbol)
                db.session.commit()
                symbol_id = new_symbol.id

            # Define the transaction table entry
            transaction = Transaction(
                symbol_id=symbol_id,
                price=quote["price"],
                shares=shares,
                user_id=id
            )

            # Work out how much cash user will have after transaction
            cash_remaining = cash_available - shares * quote["price"]

            # Fetch user record to update
            user = db.session.execute(
                db.select(User).filter_by(id=id)
            ).first()[0]

            # Add the transaction and update the users cash
            db.session.add(transaction)
            user.cash = cash_remaining
            db.session.commit()

            return redirect('/')

    # User reached route via GET (clicking link or entering url)
    else:
        return render_template("buy.html")


@trade.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    id = session["user_id"]
    stocks_held = []

    # Get users transaction records grouped by symbol
    records = db.session.execute(
        db
        .select(Transaction, db.func.sum(Transaction.shares))
        .filter_by(user_id=id)
        .group_by(Transaction.symbol_id)
    ).all()

    for record in records:
        symbol = record[0].symbol.symbol
        shares = record[1]
        if shares != 0:
            stock = {
                'symbol': symbol,
                'shares': shares
            }
            stocks_held.append(stock)

    if request.method == "POST":
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        # Check stock selected
        if not symbol:
            return apology("Need to select a share")
        # Check we own stock
        elif not any(stock['symbol'] == symbol for stock in stocks_held):
            return apology(f"You don't hold {symbol} shares")
        # Check number of share to sell is +ve int
        elif not is_pos_int(shares):
            return apology("Must be a positive integer!", 403)

        # Look up symbol id
        symbol_id = db.session.execute(
            db.select(Symbol.id).filter_by(symbol=symbol)
        ).first()[0]

        # Look up market price
        market = lookup(symbol)

        # Build transaction entry
        transaction = Transaction(
            price=market["price"],
            shares=-shares,
            symbol_id=symbol_id,
            user_id=id
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect("/")

    # if request.method="GET"
    else:
        return render_template("sell.html", stocks=stocks_held)
