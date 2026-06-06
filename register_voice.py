from record import record_audio

print("Recording owner voice...")

record_audio(
    "owner.wav",
    duration=10
)

print("Owner voice saved!")