import sqlite3
from datetime import datetime
DB_NAME = "voicepay.db"


def get_balance():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE id=1"
    )

    balance = cursor.fetchone()[0]

    conn.close()

    return balance


def update_balance(amount):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET balance = balance - ?
        WHERE id=1
        """,
        (amount,)
    )

    conn.commit()

    conn.close()


def add_transaction(receiver, amount, status):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions
        (receiver, amount, status)
        VALUES (?, ?, ?)
        """,
        (receiver, amount, status)
    )

    conn.commit()

    conn.close()


def get_transactions():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT receiver,
               amount,
               status,
               timestamp
        FROM transactions
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_total_transactions():

    conn = sqlite3.connect("voicepay.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_total_spent():

    conn = sqlite3.connect("voicepay.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM transactions"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0

def get_today_spent():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn = sqlite3.connect("voicepay.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE timestamp LIKE ?
        """,
        (f"{today}%",)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0

from datetime import datetime


def get_total_transactions():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_total_spent():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM transactions"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0


def get_today_spent():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE timestamp LIKE ?
        """,
        (f"{today}%",)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0