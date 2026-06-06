
def process_voice_payment():

    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    import time
    import whisper
    import re
    import os

    from rapidfuzz import process
    from speechbrain.inference.speaker import SpeakerRecognition

    # -----------------------------ß
    # RECORD USER VOICE
    # -----------------------------

    samplerate = 16000
    duration = 6

    print("Get ready...")
    time.sleep(1)

    print("Speak now...")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    max_audio = np.max(np.abs(audio))

    if max_audio > 0:
        audio = audio / max_audio

    sf.write("input.wav", audio, samplerate)

    print("\n✅ Voice recorded successfully!")

    # -----------------------------
    # SPEAKER VERIFICATION
    # -----------------------------

    print("\nLoading Speaker Verification Model...")

    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir="pretrained_models"
    )

    print("\nComparing Voices...")

    score, prediction = verification.verify_files(
        "owner.wav",
        "input.wav"
    )

    score_value = score.item()

    print("\nSimilarity Score:")
    print(score_value)

    threshold = 0.55

    if score_value > threshold:

        print("\n✅ Voice Verified")

    else:

        print("\n❌ Voice Not Verified")

        os.system('say "Voice not verified"')

        return {
            "status": "failed",
            "score": score_value
        }

    # -----------------------------
    # SPEECH TO TEXT
    # -----------------------------

    print("\nLoading Whisper Model...")

    model = whisper.load_model("small")

    prompt = (
        "Indian Hinglish payment commands. "
        "Examples: Rahul ko 500 bhejo. "
        "Aditya ko 2000 transfer karo."
    )

    result = model.transcribe(
        "input.wav",
        language="en",
        initial_prompt=prompt,
        fp16=False
    )

    text = result["text"].lower()

    print("\nDetected Text:")
    print(text)

    # -----------------------------
    # USER LIST
    # -----------------------------

    known_users = [
        "rahul",
        "aditya",
        "aman",
        "priya",
        "mummy",
        "papa"
    ]

    words = text.split()

    if len(words) == 0:

        return {
            "status": "declined",
            "receiver": "unknown",
            "amount": 0
        }

    # -----------------------------
    # NAME EXTRACTION
    # -----------------------------

    # -----------------------------
# NAME EXTRACTION
# -----------------------------

    matched_name = None

    for user in known_users:

        if user in text:
            matched_name = user
            break

    if matched_name is None:

        match = process.extractOne(
            text,
            known_users
        )

        matched_name = match[0]

    # -----------------------------
    # AMOUNT EXTRACTION
    # -----------------------------

    amount = 0

    # -----------------------------
# AMOUNT EXTRACTION
# -----------------------------

    amount = 0

    numbers = re.findall(r"\d+", text)

    if len(numbers) > 0:
        amount = int(numbers[0])
    else:
        amount = 0

    print("RAW TEXT =", text)
    print("NUMBERS FOUND =", numbers)
    print("EXTRACTED AMOUNT =", amount)

    print("\n========================")
    print("PAYMENT INTENT DETECTED")
    print("========================")

    print(f"\nReceiver: {matched_name}")
    print(f"Amount: ₹{amount}")

    print(f"\n✅ Ready to send ₹{amount} to {matched_name}")

    # -----------------------------
    # VOICE RESPONSE
    # -----------------------------

    os.system(
        f'say "Voice verified. Ready to send {amount} rupees to {matched_name}"'
    )

    time.sleep(1)

    # -----------------------------
    # CONFIRMATION PROMPT
    # -----------------------------

    print("\nPlease say yes to confirm the payment")

    os.system(
        'say "Please say yes to confirm the payment"'
    )

    # -----------------------------
    # RECORD CONFIRMATION
    # -----------------------------

    confirm_audio = sd.rec(
        int(5 * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    max_confirm = np.max(np.abs(confirm_audio))

    if max_confirm > 0:
        confirm_audio = confirm_audio / max_confirm

    sf.write("confirm.wav", confirm_audio, samplerate)

    print("\nConfirmation recorded!")

    # -----------------------------
    # CONFIRMATION STT
    # -----------------------------
    print("STEP 1")
    confirm_result = model.transcribe(
        "confirm.wav",
        language="en",
        fp16=False
    )

    confirm_text = confirm_result["text"].lower()
    print("STEP 2")
    print("\nConfirmation Text:")
    print(confirm_text)

    # -----------------------------
    # FINAL CHECK
    # -----------------------------
    print("STEP 3")
    if "yes" in confirm_text.strip():

        print("\n✅ PAYMENT SUCCESSFUL")

        os.system('say "Payment successful"')
        print("STEP 4")
        return {
            "status": "success",
            "receiver": matched_name,
            "amount": amount
        }

    else:

        print("\n❌ PAYMENT DECLINED")

        os.system('say "Payment declined"')
        print("STEP 5")
        return {
            "status": "declined",
            "receiver": matched_name,
            "amount": amount
        }

