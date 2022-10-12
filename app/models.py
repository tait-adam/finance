from datetime import datetime
from app import db


class User(db.Model):
    """Data model for user accounts"""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    username = db.Column(
        db.Text,
        nullable=False
    )
    hash = db.Column(
        db.Text,
        nullable=False
    )
    cash = db.Column(
        db.Float,
        nullable=False,
        default=10000
    )


class Symbol(db.Model):
    """Data model for stock symbols"""

    __tablename__ = 'symbols'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    symbol = db.Column(
        db.String(10),
        nullable=False
    )


class Transaction(db.Model):
    """Data model for transactions"""

    __tablename__ = 'transactions'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    symbol_id = db.Column(
        db.Integer,
        db.ForeignKey(Symbol.id),
        nullable=False,
    )
    price = db.Column(
        db.Float,
        nullable=False
    )
    shares = db.Column(
        db.Integer,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False,
    )
