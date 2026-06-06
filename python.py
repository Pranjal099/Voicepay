from speech_to_text import transcribe_audio

text = transcribe_audio("qr_confirm.wav")

print("RESULT =", repr(text))