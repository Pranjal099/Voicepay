import sounddevice as sd
import soundfile as sf
import numpy as np
import time

samplerate = 16000
duration = 6

print("Get ready...")
time.sleep(2)

print("Speak now...")

audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype='float32'
)

sd.wait()

# Normalize audio
audio = audio / np.max(np.abs(audio))

# Save clean WAV
sf.write("myvoice.wav", audio, samplerate)

print("Audio saved successfully!")