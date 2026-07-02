import whisper

print("Loading Confirmation Model...")

confirmation_model = whisper.load_model("small")

print("Confirmation Model Loaded")


def verify_confirmation(audio_file):

    result = confirmation_model.transcribe(
        audio_file,
        language="en",
        fp16=False
    )

    text = result["text"].lower().strip()

    print("Confirmation Text:", text)

    positive = [
        "confirm",
        "yes",
        "okay",
        "ok",
        "proceed"
    ]

    negative = [
        "cancel",
        "no",
        "stop"
    ]

    for word in positive:
        if word in text:
            return "confirm"

    for word in negative:
        if word in text:
            return "cancel"

    return "unknown"