import sounddevice as sd

print(sd.query_devices())

print("Recording...")

audio = sd.rec(
    16000 * 3,
    samplerate=16000,
    channels=1,
    dtype="float32"
)

sd.wait()

print("Success")