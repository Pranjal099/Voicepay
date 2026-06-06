import sqlite3

conn = sqlite3.connect("voicepay.db")

cursor = conn.cursor()

cursor.execute(
    """
    UPDATE users
    SET balance = 10000
    WHERE id = 1
    """
)

conn.commit()

conn.close()

print("Balance reset to ₹10000")