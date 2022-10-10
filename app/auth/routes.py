from flask import Blueprint, request, redirect, render_template, session
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
from cs50 import SQL

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

# TODO: transition to sqlalchemy
db = SQL("sqlite:///finance.db")


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        def is_unique(user):
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?",
                user
            )
            return len(rows) != 1

        # Ensure username is not blank
        if not username:
            return apology("must provide a username", 403)

        # Ensure username is unique
        elif not is_unique(username):
            return apology("username already exists", 403)

        # Ensure password is not blank
        elif not password:
            return apology("must provide a password", 403)

        # Ensure password and confirmation match
        elif password != confirmation:
            return apology("password and confirmation must match", 403)

        else:
            hash = generate_password_hash(password)

            id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, hash
            )

            session["user_id"] = id

            return redirect("/")

    else:
        return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@auth.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
