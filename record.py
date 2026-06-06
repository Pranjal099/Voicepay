import sounddevice as sd
import soundfile as sf
import numpy as np
import time


def record_audio(filename, duration=4):

    samplerate = 16000

    print("Get ready...")
    time.sleep(1)

    print("Speak now...")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = audio / np.max(np.abs(audio))

    sf.write(
        filename,
        audio,
        samplerate
    )

    print(
        f"Audio saved as {filename}"
    )