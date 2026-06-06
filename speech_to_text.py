import whisper

print("Loading Whisper Model...")

model = whisper.load_model("small")


def transcribe_audio(audio_file):

    result = model.transcribe(
        audio_file,
        fp16=False
    )

    text = result["text"]

    print(
        "RAW WHISPER TEXT =",
        repr(text)
    )

    return text.lower().strip()