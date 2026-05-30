
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import whisper
import re
import os

from rapidfuzz import process
from speechbrain.inference.speaker import SpeakerRecognition

# -----------------------------
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
    dtype='float32'
)

sd.wait()

audio = audio / np.max(np.abs(audio))

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
    exit()

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
# INTENT PARSING
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

# -----------------------------
# NAME EXTRACTION
# -----------------------------

name_candidate = words[0]

match = process.extractOne(
    name_candidate,
    known_users
)

matched_name = match[0]

# -----------------------------
# AMOUNT EXTRACTION
# -----------------------------

amount = 0

numbers = re.findall(r'\d+', text)

if numbers:
    amount = int("".join(numbers))

# -----------------------------
# FINAL PAYMENT OUTPUT
# -----------------------------

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

# Small smooth delay
time.sleep(1)

# -----------------------------
# CONFIRMATION PROMPT
# -----------------------------

print("\nPlease say yes to confirm the payment")

os.system('say "Please say yes to confirm the payment"')

# -----------------------------
# RECORD CONFIRMATION
# -----------------------------

confirm_audio = sd.rec(
    int(5 * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype='float32'
)

sd.wait()

confirm_audio = confirm_audio / np.max(np.abs(confirm_audio))

sf.write("confirm.wav", confirm_audio, samplerate)

print("\nConfirmation recorded!")

# -----------------------------
# CONFIRMATION SPEECH TO TEXT
# -----------------------------

confirm_result = model.transcribe(
    "confirm.wav",
    language="en",
    fp16=False
)

confirm_text = confirm_result["text"].lower()

print("\nConfirmation Text:")
print(confirm_text)

# -----------------------------
# FINAL PAYMENT CHECK
# -----------------------------

if "yes" in confirm_text:

    print("\n✅ PAYMENT SUCCESSFUL")

    os.system('say "Payment successful"')

else:

    print("\n❌ PAYMENT DECLINED")

    os.system('say "Payment declined"')

