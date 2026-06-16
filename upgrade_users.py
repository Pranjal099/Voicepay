import sqlite3

conn = sqlite3.connect("voicepay.db")
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS users
""")

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    upi_id TEXT,
    voice_file TEXT,
    balance REAL
)
""")

conn.commit()
conn.close()

print("Users table upgraded")