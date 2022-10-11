from flask import request, redirect, render_template, session
from helpers import apology, login_required, lookup
from app.models import db, User, Transaction, TransactionType

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

        def is_pos_int(n):
            return isinstance(n, int) and n > 0

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
            # Find the id for a purchase transaction
            type_id = db.session.execute(
                db.select(TransactionType.id).filter_by(type='PURCHASE')
            ).first()[0]

            # Define the transaction table entry
            transaction = Transaction(
                transaction_type_id=type_id,
                symbol=symbol,
                price=quote["price"],
                shares=shares,
                user_id=id
            )

            # Work out how much cash user will have after transaction
            cash_remaining = cash_available - shares * quote["price"]

            # Fetch record to update
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
    return apology("TODO")
