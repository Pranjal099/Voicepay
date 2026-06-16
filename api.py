from fastapi import FastAPI, UploadFile, File, Form
import shutil
import subprocess
import os

from db import (
    create_user,
    get_user_by_phone,
    add_transaction,
    get_balance_by_phone,
    update_balance_by_phone,
    get_transactions_by_phone,
    get_total_transactions_by_phone,
    get_total_spent_by_phone,
    get_today_spent_by_phone,
)

from qr_payment import scan_qr, parse_upi
from voice_payment import process_voice_payment

app = FastAPI()


@app.get("/")
def root():
    return {"status": "VoicePay API Running"}


# -----------------------------
# SIGNUP
# -----------------------------
@app.post("/signup")
async def signup(
    name: str = Form(...),
    phone: str = Form(...),
    upi_id: str = Form(...),
    voice1: UploadFile = File(...),
    voice2: UploadFile = File(...),
    voice3: UploadFile = File(...)
):

    os.makedirs("voices", exist_ok=True)

    m4a_1 = f"voices/{phone}_1.m4a"
    m4a_2 = f"voices/{phone}_2.m4a"
    m4a_3 = f"voices/{phone}_3.m4a"

    wav_1 = f"voices/{phone}_1.wav"
    wav_2 = f"voices/{phone}_2.wav"
    wav_3 = f"voices/{phone}_3.wav"

    with open(m4a_1, "wb") as buffer:
        shutil.copyfileobj(voice1.file, buffer)

    with open(m4a_2, "wb") as buffer:
        shutil.copyfileobj(voice2.file, buffer)

    with open(m4a_3, "wb") as buffer:
        shutil.copyfileobj(voice3.file, buffer)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        m4a_1,
        wav_1
    ])

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        m4a_2,
        wav_2
    ])

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        m4a_3,
        wav_3
    ])

    create_user(
        name,
        phone,
        upi_id,
        wav_1,
        wav_2,
        wav_3
    )

    return {
        "status": "success",
        "message": "User registered with 3 voice samples"
    }


# -----------------------------
# LOGIN
# -----------------------------
@app.post("/login")
def login(
    phone: str = Form(...)
):

    user = get_user_by_phone(phone)

    if not user:
        return {
            "status": "failed",
            "message": "User not found"
        }

    return {
        "status": "success",
        "id": user[0],
        "name": user[1],
        "phone": user[2],
        "upi_id": user[3],
        "voice_file1": user[4],
        "voice_file2": user[5],
        "voice_file3": user[6],
        "balance": user[7]
    }


# -----------------------------
# VOICE PAYMENT
# -----------------------------
@app.post("/voice-payment")
async def voice_payment(
    phone: str = Form(...),
    voice: UploadFile = File(...)
):

    print("PHONE =", phone)
    print("VOICE FILE =", voice.filename)

    os.makedirs("temp", exist_ok=True)

    m4a_path = f"temp/{phone}.m4a"
    wav_path = f"temp/{phone}.wav"

    with open(m4a_path, "wb") as buffer:
        shutil.copyfileobj(
            voice.file,
            buffer
        )

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        m4a_path,
        wav_path
    ])

    result = process_voice_payment(
        phone,
        wav_path
    )

    print("RESULT =", result)

    # DO NOT deduct balance here
    # DO NOT save transaction here

    return result


# -----------------------------
# CONFIRM PAYMENT
# -----------------------------
@app.post("/confirm-payment")
def confirm_payment(
    phone: str = Form(...),
    receiver: str = Form(...),
    amount: int = Form(...)
):

    update_balance_by_phone(
        phone,
        amount
    )

    add_transaction(
        phone,
        receiver,
        amount,
        "success"
    )

    return {
        "status": "success",
        "message": "Payment Successful"
    }

# -----------------------------
# BALANCE
# -----------------------------
@app.get("/balance")
def balance(phone: str):

    return {
        "balance":
        get_balance_by_phone(phone)
    }


# -----------------------------
# HISTORY
# -----------------------------
@app.get("/history")
def history(phone: str):

    transactions = get_transactions_by_phone(phone)

    data = []

    for row in transactions:

        data.append({
            "receiver": row[0],
            "amount": row[1],
            "status": row[2],
            "timestamp": row[3]
        })

    return data


# -----------------------------
# STATS
# -----------------------------
@app.get("/stats")
def stats(phone: str):

    return {
        "total_transactions":
            get_total_transactions_by_phone(phone),

        "total_spent":
            get_total_spent_by_phone(phone),

        "today_spent":
            get_today_spent_by_phone(phone)
    }


# -----------------------------
# QR PAYMENT
# -----------------------------
@app.get("/qr-payment")
def qr_payment():

    qr_data = scan_qr("temp_qr.png")

    if not qr_data:
        return {
            "status": "failed"
        }

    details = parse_upi(qr_data)

    return {
        "status": "success",
        "upi_id": details.get("pa"),
        "name": details.get("pn"),
        "amount": details.get("am")
    }