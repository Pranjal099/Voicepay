import sounddevice as sd

print(sd.query_devices())
print("Default:", sd.default.device)

sd.rec(16000, samplerate=16000, channels=1)
sd.wait()

print("Mic works")