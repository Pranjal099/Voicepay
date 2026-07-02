def detect_intent(text):

    text = text.lower()

    # -----------------------------
    # PAYMENT
    # -----------------------------

    payment_keywords = [
        "pay",
        "send",
        "transfer",
        "give",
        "bhejo",
        "bhejna",
        "de do",
        "money",
        "payment"
    ]

    # -----------------------------
    # BALANCE
    # -----------------------------

    balance_keywords = [
        "balance",
        "wallet",
        "account balance",
        "check balance",
        "kitna balance",
        "mera balance"
    ]

    # -----------------------------
    # HISTORY
    # -----------------------------

    history_keywords = [
        "history",
        "transactions",
        "transaction",
        "recent payments",
        "payment history"
    ]

    # -----------------------------
    # QR
    # -----------------------------

    qr_keywords = [
        "qr",
        "scan qr",
        "scan code",
        "scanner"
    ]

    # -----------------------------
    # PROFILE
    # -----------------------------

    profile_keywords = [
        "profile",
        "account",
        "my profile"
    ]

    # -----------------------------
    # STATS
    # -----------------------------

    stats_keywords = [
        "stats",
        "statistics",
        "today",
        "spent",
        "expense"
    ]

    if any(word in text for word in payment_keywords):
        return "payment"

    if any(word in text for word in balance_keywords):
        return "balance"

    if any(word in text for word in history_keywords):
        return "history"

    if any(word in text for word in qr_keywords):
        return "qr"

    if any(word in text for word in profile_keywords):
        return "profile"

    if any(word in text for word in stats_keywords):
        return "stats"

    return "unknown"

if __name__ == "__main__":

    while True:

        text = input("Speak: ")

        print(detect_intent(text))