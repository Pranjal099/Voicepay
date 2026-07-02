import csv
import os
from datetime import datetime

# Root folder
ROOT = "voicepay_dataset"

# Subfolders
LOG_DIR = os.path.join(ROOT, "logs")
VOICE_DIR = os.path.join(ROOT, "voices")

ENROLL_DIR = os.path.join(VOICE_DIR, "enrollment")
PAYMENT_DIR = os.path.join(VOICE_DIR, "payment")
CONFIRM_DIR = os.path.join(VOICE_DIR, "confirmation")

RECEIPT_DIR = os.path.join(ROOT, "receipts")

# Create folders automatically
for folder in [
    ROOT,
    LOG_DIR,
    VOICE_DIR,
    ENROLL_DIR,
    PAYMENT_DIR,
    CONFIRM_DIR,
    RECEIPT_DIR
]:
    os.makedirs(folder, exist_ok=True)


def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def write_csv(filename, row):

    filepath = os.path.join(LOG_DIR, filename)

    exists = os.path.exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=row.keys()
        )

        if not exists:
            writer.writeheader()

        writer.writerow(row)