# The design of the database tables needs to facilitate:
# 1. the ability to list all users transactions
# 2. the ability to calculate held position from transactions, which is
#    perhaps better stored separately, although that duplicates data.

def teardown(db):
    db.execute("DROP TABLE IF EXISTS transactions;")
    db.execute("DROP TABLE IF EXISTS users;")
    db.execute("DROP TABLE IF EXISTS transaction_type;")


def setup(db):
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            hash TEXT NOT NULL,
            cash NUMERIC NOT NULL DEFAULT 10000.00
        );
        """
    )
    db.execute(
        """
        CREATE UNIQUE INDEX username ON users (username);
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            price NUMERIC NOT NULL,
            shares NUMERIC NOT NULL,
            timestamp CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id)
        );
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS transaction_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            UNIQUE(type)
        );
        """
    )
    db.execute(
        """
        INSERT INTO transaction_type (type)
        VALUES
            ('PURCHASE'),
            ('SALE');
        """
    )
