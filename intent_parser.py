from rapidfuzz import process
import re

# Known users
known_users = [
    "rahul",
    "aman",
    "priya",
    "mummy",
    "papa"
]

# Example ASR text
text = "rahula ko paanch sau bhejo"

print("Original Text:")
print(text)

# -----------------------------
# STEP 1: Extract possible name
# -----------------------------

words = text.split()

name_candidate = words[0]

# Fuzzy match with known users
match = process.extractOne(
    name_candidate,
    known_users
)

matched_name = match[0]

print("\nMatched Name:")
print(matched_name)

# -----------------------------
# STEP 2: Hindi Number Mapping
# -----------------------------

number_map = {
    "ek": 1,
    "do": 2,
    "teen": 3,
    "char": 4,
    "paanch": 5,
    "cheh": 6,
    "saat": 7,
    "aath": 8,
    "nau": 9,
    "das": 10,
    "sau": 100,
    "hazaar": 1000
}

# -----------------------------
# STEP 3: Extract Amount
# -----------------------------

amount = 0

for i in range(len(words)):

    if words[i] in number_map:

        current = number_map[words[i]]

        # Handle paanch sau
        if i + 1 < len(words):

            next_word = words[i + 1]

            if next_word == "sau":
                amount = current * 100

            elif next_word == "hazaar":
                amount = current * 1000

print("\nDetected Amount:")
print(amount)

# -----------------------------
# FINAL PAYMENT INTENT
# -----------------------------

print("\nPayment Intent:")
print(f"Send ₹{amount} to {matched_name}")