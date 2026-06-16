
import sqlite3
from datetime import datetime
DB_NAME = "voicepay.db"





def add_transaction(phone, receiver, amount, status):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions
        (phone, receiver, amount, status)
        VALUES (?, ?, ?, ?)
        """,
        (phone, receiver, amount, status)
    )

    conn.commit()
    conn.close()

    def add_transaction(
    phone,
    receiver,
    amount,
    status
):

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO transactions
            (
                phone,
                receiver,
                amount,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                phone,
                receiver,
                amount,
                status
            )
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




def create_user(
    name,
    phone,
    upi_id,
    voice_file1,
    voice_file2,
    voice_file3
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            phone,
            upi_id,
            voice_file1,
            voice_file2,
            voice_file3,
            balance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            upi_id,
            voice_file1,
            voice_file2,
            voice_file3,
            5000
        )
    )

    conn.commit()

    conn.close()


def get_user_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE phone=?
        """,
        (phone,)
    )

    user = cursor.fetchone()

    conn.close()

    return user

def get_user_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE phone=?
        """,
        (phone,)
    )

    user = cursor.fetchone()

    conn.close()

    return user

def get_balance_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT balance
        FROM users
        WHERE phone=?
        """,
        (phone,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return 0

    return user[0]


def update_balance_by_phone(
    phone,
    amount
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET balance = balance - ?
        WHERE phone=?
        """,
        (
            amount,
            phone
        )
    )

    conn.commit()

    conn.close()

def get_transactions_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT receiver,
            amount,
            status,
            timestamp
        FROM transactions
        WHERE phone=?
        ORDER BY id DESC
        """,
        (phone,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_total_transactions_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE phone=?
        """,
        (phone,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_total_spent_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE phone=?
        """,
        (phone,)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0

def get_today_spent_by_phone(phone):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE phone=?
        AND timestamp LIKE ?
        """,
        (
            phone,
            f"{today}%"
        )
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0

