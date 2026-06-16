def process_voice_payment(phone, input_file):

    import whisper
    import re
    from db import get_user_by_phone
    from rapidfuzz import process
    from speechbrain.inference.speaker import SpeakerRecognition

    print("Using uploaded audio file")

    # -----------------------------
    # SPEAKER VERIFICATION
    # -----------------------------

    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir="pretrained_models"
    )

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

    score1, _ = verification.verify_files(
        voice1,
        input_file
    )

    score2, _ = verification.verify_files(
        voice2,
        input_file
    )

    score3, _ = verification.verify_files(
        voice3,
        input_file
    )

    score_value = max(
        score1.item(),
        score2.item(),
        score3.item()
    )

    print("Similarity Score 1 =", score1.item())
    print("Similarity Score 2 =", score2.item())
    print("Similarity Score 3 =", score3.item())
    print("Best Similarity Score =", score_value)

    threshold = 0.55

    if score_value <= threshold:

        return {
            "status": "failed",
            "message": "Voice not verified",
            "score": score_value
        }

    print("Voice Verified")

    # -----------------------------
    # WHISPER
    # -----------------------------

    model = whisper.load_model("small")

    result = model.transcribe(
        input_file,
        language="en",
        fp16=False
    )

    text = result["text"].lower()

    print("Detected Text =", text)

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

    matched_name = None

    for user_name in known_users:

        if user_name in text:
            matched_name = user_name
            break

    if matched_name is None:

        match = process.extractOne(
            text,
            known_users
        )

        if match:
            matched_name = match[0]
        else:
            matched_name = "unknown"

    # -----------------------------
    # AMOUNT EXTRACTION
    # -----------------------------

    numbers = re.findall(
        r"\d+",
        text
    )

    if len(numbers) > 0:
        amount = int(numbers[0])
    else:
        amount = 0

    print("Receiver =", matched_name)
    print("Amount =", amount)

    return {
        "status": "success",
        "receiver": matched_name,
        "amount": amount,
        "text": text,
        "score": score_value
    }


if __name__ == "__main__":

    result = process_voice_payment(
        "8210552036",
        "voices/8210552036.wav"
    )

    print(result)