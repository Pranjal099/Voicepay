from record import record_audio

print("Recording test voice...")

record_audio(
    "input.wav",
    duration=5
)

print("Test voice saved!")