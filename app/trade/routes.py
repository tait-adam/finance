from flask import request, redirect, render_template, session
from helpers import apology, login_required, lookup
from cs50 import SQL

from . import trade

# TODO: transition to sqlalchemy
db = SQL("sqlite:///finance.db")


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
        rows = db.execute("SELECT cash FROM users WHERE id=?", id)
        cash_available = rows[0]["cash"]

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
            row = db.execute(
                "SELECT id FROM transaction_type WHERE type = 'PURCHASE'"
            )
            type_id = row[0]["id"]
            cash_remaining = cash_available - shares * quote["price"]

            db.execute(
                """
                INSERT INTO transactions (
                    transaction_type_id,
                    symbol,
                    price,
                    shares,
                    user_id
                )
                VALUES (?, ?, ?, ?, ?)
                """, type_id, symbol, quote["price"], shares, id
            )
            db.execute(
                """
                UPDATE users
                SET cash = ?
                WHERE id = ?
                """, cash_remaining, id
            )

            return redirect('/')

    # User reached route via GET (clicking link or entering url)
    else:
        return render_template("buy.html")


@trade.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
