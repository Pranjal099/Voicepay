import re

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


def parse_amount(text):

    text = text.lower()

    # -----------------------
    # Digits
    # -----------------------

    digits = re.findall(r"\d+", text)

    if digits:
        return int(digits[0])

    # -----------------------
    # Hindi / English
    # -----------------------

    words = text.split()

    for i, word in enumerate(words):

        if word not in NUMBER_WORDS:
            continue

        value = NUMBER_WORDS[word]

        if i + 1 < len(words):

            nxt = words[i + 1]

            if nxt in ["hundred", "sau"]:
                return value * 100

            if nxt in ["thousand", "hazaar"]:
                return value * 1000

        return value

    return 0
if __name__ == "__main__":

    while True:

        text = input("Amount: ")

        print(parse_amount(text))