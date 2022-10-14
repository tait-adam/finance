from flask import flash, request, redirect, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology

from . import auth
from app.models import db, User


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        def already_exists(user):
            exists = db.session.execute(
                db.select(User.id).filter_by(username=username)
            ).first() is not None

            return exists

        # Ensure username is not blank
        if not username:
            return apology("must provide a username", 403)

        # Ensure username is unique
        elif already_exists(username):
            return apology("username already exists", 403)

        # Ensure password is not blank
        elif not password:
            return apology("must provide a password", 403)

        # Ensure password and confirmation match
        elif password != confirmation:
            return apology("password and confirmation must match", 403)

        else:
            hash = generate_password_hash(password)
            new_user = User(
                username=username,
                hash=hash
            )
            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            flash('You were successfully registered')

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
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        record = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar()

        # Ensure username exists and password is correct
        if not record or not check_password_hash(record.hash, password):
            return apology("invalid username and/or password", 403)
        else:
            # Remember which user has logged in
            session["user_id"] = record.id
            flash('You were successfully logged in')

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
