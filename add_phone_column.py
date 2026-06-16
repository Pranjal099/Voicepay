import sqlite3

conn = sqlite3.connect("voicepay.db")

cursor = conn.cursor()

cursor.execute(
    """
    ALTER TABLE transactions
    ADD COLUMN phone TEXT
    """
)

conn.commit()

conn.close()

print("phone column added")