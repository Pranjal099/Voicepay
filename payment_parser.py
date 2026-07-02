from rapidfuzz import process
import re

KNOWN_USERS = [
    "rahul",
    "aman",
    "aditya",
    "priya",
    "mummy",
    "papa"
]

NUMBER_WORDS = {
    "zero":0,
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9,
    "ten":10,

    "ek":1,
    "do":2,
    "teen":3,
    "char":4,
    "paanch":5,
    "cheh":6,
    "saat":7,
    "aath":8,
    "nau":9,
    "das":10,

    "hundred":100,
    "thousand":1000,
    "sau":100,
    "hazaar":1000
}


def parse_payment(text):

    text = text.lower()

    receiver = None
    amount = 0

    # -----------------------
    # Receiver
    # -----------------------

    words = re.findall(r"[a-zA-Z]+", text)

    best_score = 0

    for word in words:

        match = process.extractOne(word, KNOWN_USERS)

        if match and match[1] > best_score:
            best_score = match[1]
            receiver = match[0]

    # -----------------------
    # Digits
    # -----------------------

    numbers = re.findall(r"\d+", text)

    if numbers:
        amount = int(numbers[0])

    # -----------------------
    # Hindi / English Words
    # -----------------------

    if amount == 0:

        words = text.split()

        for i in range(len(words)):

            word = words[i]

            if word not in NUMBER_WORDS:
                continue

            value = NUMBER_WORDS[word]

            if i + 1 < len(words):

                nxt = words[i + 1]

                if nxt in ["hundred", "sau"]:
                    amount = value * 100
                    break

                if nxt in ["thousand", "hazaar"]:
                    amount = value * 1000
                    break

            amount = value

    return {
        "receiver": receiver,
        "amount": amount
    }