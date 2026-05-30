import whisper
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

print("Loading model...")

model = whisper.load_model("small")

prompt = (
    "Indian payment command in Hindi and Hinglish. "
    "Examples: राहुल को पांच सौ रुपये भेजो."
)

result = model.transcribe(
    "myvoice.wav",
    language="hi",
    fp16=False,
    initial_prompt=prompt
)

hindi_text = result["text"]

# Transliterate Hindi → Hinglish
hinglish_text = transliterate(
    hindi_text,
    sanscript.DEVANAGARI,
    sanscript.ITRANS
)

# Clean Hinglish formatting
hinglish_text = hinglish_text.replace("A", "a")
hinglish_text = hinglish_text.replace(".n", "n")
hinglish_text = hinglish_text.replace("M", "m")
hinglish_text = hinglish_text.replace("H", "h")

print("\nHindi Output:")
print(hindi_text)

print("\nHinglish Output:")
print(hinglish_text.lower())