# TODO: Make sure all the http status response codes are correct

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from database import setup, teardown


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
teardown(db)
setup(db)


def init_app():
    """Initialise the core application"""

    # Configure application
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    Session(app)

    with app.app_context():
        from .auth import routes
        app.register_blueprint(routes.auth)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    @app.route("/")
    @login_required
    def index():
        """Show portfolio of stocks"""
        return apology("PORTFOLIO")

    @app.route("/buy", methods=["GET", "POST"])
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

    @app.route("/history")
    @login_required
    def history():
        """Show history of transactions"""
        return apology("TODO")

    @app.route("/quote", methods=["GET", "POST"])
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


    @app.route("/sell", methods=["GET", "POST"])
    @login_required
    def sell():
        """Sell shares of stock"""
        return apology("TODO")

    return app
