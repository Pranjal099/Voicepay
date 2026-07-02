import shutil
import os
from logger import PAYMENT_DIR, timestamp, write_csv
from db import get_transactions_by_phone
from intent_parser import detect_intent
from payment_parser import parse_payment
import time
from spoof_detector import detect_spoof
import whisper
print("Loading Whisper...")
model = whisper.load_model("small")
print("Whisper Loaded")

def process_voice_payment(phone, input_file):
    from db import (
    get_user_by_phone,
    get_balance_by_phone,
    get_transactions_by_phone,
    get_total_transactions_by_phone,
    get_total_spent_by_phone,
    get_today_spent_by_phone,
    )
    from speaker_verify import verify_speaker

    print("Using uploaded audio file")
    # ---------------------------------
    # Save payment audio permanently
    # ---------------------------------

    user_folder = os.path.join(PAYMENT_DIR, phone)
    os.makedirs(user_folder, exist_ok=True)

    saved_payment_audio = os.path.join(
        user_folder,
        f"{timestamp()}.wav"
    )

    shutil.copy(
        input_file,
        saved_payment_audio
    )

    print("Payment voice saved:", saved_payment_audio)
    start_total = time.perf_counter()
    user = get_user_by_phone(phone)

    if not user:
        return {
            "status": "failed",
            "message": "User not found"
        }

    voice1 = user[4]
    voice2 = user[5]
    voice3 = user[6]

    print("Voice 1:", voice1)
    print("Voice 2:", voice2)
    print("Voice 3:", voice3)

    print("Input File:", input_file)

    start_ecapa = time.perf_counter()
    score1 = verify_speaker(
        voice1,
        input_file
    )
    score2 = verify_speaker(
        voice2,
        input_file
    )
    score3 = verify_speaker(
        voice3,
        input_file
    )
    score_value = max(
        score1,
        score2,
        score3
    )

    print("Best Similarity Score =", score_value)
    ecapa_time = time.perf_counter() - start_ecapa
    print(f"ECAPA Time : {ecapa_time:.3f} sec")

    threshold = 0.40

    if score_value <= threshold:

        write_csv(
            "payments.csv",
            {
                "timestamp": timestamp(),
                "phone": phone,
                "status": "failed",
                "reason": "voice_not_verified",
                "similarity_score": round(score_value, 4),
                "threshold": threshold,
                "audio_file": saved_payment_audio
            }
        )

        return {
            "status": "failed",
            "message": "Voice not verified",
            "score": score_value
        }

    print("Voice Verified")

    start_aasist = time.perf_counter()
    print("Running Anti-Spoofing...")

    is_live = detect_spoof(input_file)

    if not is_live:

        write_csv(
            "payments.csv",
            {
                "timestamp": timestamp(),
                "phone": phone,
                "status": "failed",
                "reason": "spoof_detected",
                "audio_file": saved_payment_audio
            }
        )

        return {
            "status": "failed",
            "message": "Spoof voice detected"
        }

    print("Live Voice Verified")
    aasist_time = time.perf_counter() - start_aasist
    print(f"AASIST Time : {aasist_time:.3f} sec")

    start_whisper = time.perf_counter()
    result = model.transcribe(
        input_file,
        language="en",
        fp16=False
    )

    text = result["text"].lower()
    whisper_time = time.perf_counter() - start_whisper
    print(f"Whisper Time : {whisper_time:.3f} sec")

    print("Detected Text =", text)

    # -----------------------------
    # Intent Detection
    # -----------------------------

    intent = detect_intent(text)

    print("Intent =", intent)

    if intent == "payment":

        payment = parse_payment(text)

        receiver = payment["receiver"]
        amount = payment["amount"]

        print("Receiver =", receiver)
        print("Amount =", amount)

        total_time = time.perf_counter() - start_total
        write_csv(
            "payments.csv",
            {
                "timestamp": timestamp(),
                "phone": phone,
                "intent": intent,
                "audio_file": saved_payment_audio,
                "receiver": receiver,
                "amount": amount,
                "transcription": text,
                "similarity_score": round(score_value, 4),
                "threshold": threshold,
                "verified": score_value > threshold,
                "spoof": is_live,
                "status": "success",
                "ecapa_time": round(ecapa_time, 3),
                "aasist_time": round(aasist_time, 3),
                "whisper_time": round(whisper_time, 3),
                "total_time": round(total_time, 3)
            }
        )



        return {
            "status": "success",
            "intent": intent,
            "receiver": receiver,
            "amount": amount,
            "text": text,
            "score": score_value,
            "latency": {
                "ecapa": round(ecapa_time, 3),
                "aasist": round(aasist_time, 3),
                "whisper": round(whisper_time, 3),
                "total": round(total_time, 3)
            }
        }

    elif intent == "balance":

        balance = get_balance_by_phone(phone)

        total_time = time.perf_counter() - start_total

        speech = f"Your current wallet balance is {balance} rupees."

        return {
            "status": "success",
            "intent": "balance",
            "balance": balance,
            "speech": speech,
            "text": text,
            "latency": {
                "ecapa": round(ecapa_time, 3),
                "aasist": round(aasist_time, 3),
                "whisper": round(whisper_time, 3),
                "total": round(total_time, 3)
            }
        }

    elif intent == "history":

        transactions = get_transactions_by_phone(phone)

        total_time = time.perf_counter() - start_total

        history = []

        for row in transactions:

            history.append({
                "receiver": row[0],
                "amount": row[1],
                "status": row[2],
                "timestamp": row[3]
            })

        if len(history) == 0:

            speech = "You have no transactions."

        else:

            latest = history[0]

            speech = (
                f"You have {len(history)} transactions. "
                f"Your latest payment was {latest['amount']} rupees "
                f"to {latest['receiver']}."
            )

        return {
            "status": "success",
            "intent": "history",
            "transactions": history,
            "speech": speech,
            "text": text,
            "latency": {
                "ecapa": round(ecapa_time, 3),
                "aasist": round(aasist_time, 3),
                "whisper": round(whisper_time, 3),
                "total": round(total_time, 3)
            }
        }

    elif intent == "qr":

        total_time = time.perf_counter() - start_total

        speech = "Opening QR scanner. Please scan the merchant QR code."

        return {
            "status": "success",
            "intent": "qr",
            "open_qr": True,
            "speech": speech,
            "text": text,
            "latency": {
                "ecapa": round(ecapa_time, 3),
                "aasist": round(aasist_time, 3),
                "whisper": round(whisper_time, 3),
                "total": round(total_time, 3)
            }
        }

    elif intent == "profile":

        user = get_user_by_phone(phone)

        total_time = time.perf_counter() - start_total

        speech = (
            f"Welcome {user[1]}. "
            f"Your registered phone number is {user[2]}. "
            f"Your UPI ID is {user[3]}. "
            f"Your current balance is {user[7]} rupees."
        )

        return {
            "status": "success",
            "intent": "profile",
            "name": user[1],
            "phone": user[2],
            "upi_id": user[3],
            "balance": user[7],
            "speech": speech,
            "text": text,
            "latency": {
                "ecapa": round(ecapa_time, 3),
                "aasist": round(aasist_time, 3),
                "whisper": round(whisper_time, 3),
                "total": round(total_time, 3)
            }
        }

    elif intent == "stats":

        total_transactions = get_total_transactions_by_phone(phone)
        total_spent = get_total_spent_by_phone(phone)
        today_spent = get_today_spent_by_phone(phone)

        total_time = time.perf_counter() - start_total

        speech = (
            f"You have completed {total_transactions} transactions. "
            f"Your total spending is {total_spent} rupees. "
            f"Today you spent {today_spent} rupees."
        )

        return {
            "status": "success",
            "intent": "stats",
            "total_transactions": total_transactions,
            "total_spent": total_spent,
            "today_spent": today_spent,
            "speech": speech,
            "text": text,
            "latency": {
                "ecapa": round(ecapa_time, 3),
                "aasist": round(aasist_time, 3),
                "whisper": round(whisper_time, 3),
                "total": round(total_time, 3)
            }
        }

    else:

        write_csv(
            "payments.csv",
            {
                "timestamp": timestamp(),
                "phone": phone,
                "status": "failed",
                "reason": "unknown_intent",
                "transcription": text,
                "audio_file": saved_payment_audio
            }
        )

        return {
            "status": "failed",
            "intent": "unknown",
            "text": text,
            "message": "Command not recognized"
        }
if __name__ == "__main__":

    result = process_voice_payment(
        "8210552036",
        "voices/8210552036.wav"
    )

    print(result)