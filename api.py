import shutil
import os

from logger import (
    ENROLL_DIR,
    CONFIRM_DIR,
    timestamp,
    write_csv
)
from amount_parser import parse_amount
from payment_parser import parse_payment
from voice_confirmation import verify_confirmation
from fastapi import FastAPI, UploadFile, File, Form
import shutil
import subprocess
import os
import time

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
from intent_parser import detect_intent
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

    # ---------------------------------
    # Save enrollment voices
    # ---------------------------------

    user_folder = os.path.join(ENROLL_DIR, phone)
    os.makedirs(user_folder, exist_ok=True)

    sample1 = os.path.join(user_folder, "sample1.wav")
    sample2 = os.path.join(user_folder, "sample2.wav")
    sample3 = os.path.join(user_folder, "sample3.wav")

    shutil.copy(wav_1, sample1)
    shutil.copy(wav_2, sample2)
    shutil.copy(wav_3, sample3)

    print("Enrollment voices saved.")

    write_csv(
        "enrollment.csv",
        {
            "timestamp": timestamp(),
            "name": name,
            "phone": phone,
            "upi_id": upi_id,
            "sample1": sample1,
            "sample2": sample2,
            "sample3": sample3
        }
    )


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


@app.post("/voice-confirmation")
async def voice_confirmation(
    phone: str = Form(...),
    receiver: str = Form(...),
    amount: int = Form(...),
    voice: UploadFile = File(...)
):

    os.makedirs("temp", exist_ok=True)

    m4a_path = f"temp/{phone}_confirm.m4a"
    wav_path = f"temp/{phone}_confirm.wav"

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

    # ---------------------------------
    # Save confirmation audio permanently
    # ---------------------------------

    user_folder = os.path.join(CONFIRM_DIR, phone)
    os.makedirs(user_folder, exist_ok=True)

    saved_confirm_audio = os.path.join(
        user_folder,
        f"{timestamp()}.wav"
    )

    shutil.copy(
        wav_path,
        saved_confirm_audio
    )

    print("Confirmation audio saved:", saved_confirm_audio)

    decision = verify_confirmation(wav_path)
    write_csv(
        "confirmation.csv",
        {
            "timestamp": timestamp(),
            "phone": phone,
            "receiver": receiver,
            "amount": amount,
            "decision": decision,
            "audio_file": saved_confirm_audio
        }
    )
    if decision != "confirm":

        write_csv(
            "confirmation.csv",
            {
                "timestamp": timestamp(),
                "phone": phone,
                "receiver": receiver,
                "amount": amount,
                "decision": decision,
                "status": "cancelled",
                "audio_file": saved_confirm_audio
            }
        )

        return {
            "status": "failed",
            "message": "Payment Cancelled"
        }
    transaction_id = f"TXN{int(time.time())}"
    update_balance_by_phone(
    phone,
    amount
)
    balance = get_balance_by_phone(phone)

    add_transaction(
        phone,
        receiver,
        amount,
        "success"
    )

    speech = (
    f"Payment successful. "
    f"{amount} rupees has been sent to {receiver}. "
    f"Your remaining balance is {balance} rupees."
    )   
    return {
        "status": "success",
        "transaction_id": transaction_id,
        "message": "Payment Successful",
        "receiver": receiver,
        "amount": amount,
        "balance": balance,
        "speech": speech
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
            "status": "failed",
            "message": "No QR code detected"
        }

    details = parse_upi(qr_data)

    return {
        "status": "success",
        **details
    }


@app.post("/parse-command")
def parse_command(text: str = Form(...)):

    intent = detect_intent(text)

    response = {
        "text": text,
        "intent": intent
    }

    if intent == "payment":

        payment = parse_payment(text)

        response["receiver"] = payment["receiver"]
        response["amount"] = payment["amount"]

    return response
# -----------------------------
# VOICE AMOUNT
# -----------------------------
@app.post("/voice-amount")
def voice_amount(
    text: str = Form(...),
    merchant: str = Form(...)
):

    amount = parse_amount(text)

    return {
        "status": "success",
        "merchant": merchant,
        "amount": amount,
        "need_confirmation": True,
        "speech": (
            f"You are about to pay "
            f"{amount} rupees to {merchant}. "
            f"Please say Confirm."
        )
    }