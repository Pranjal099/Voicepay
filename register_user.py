import sqlite3

def register_user(
    name,
    phone,
    upi_id,
    voice_file
):

    conn = sqlite3.connect("voicepay.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            phone,
            upi_id,
            voice_file,
            balance
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            upi_id,
            voice_file,
            5000
        )
    )

    conn.commit()
    conn.close()