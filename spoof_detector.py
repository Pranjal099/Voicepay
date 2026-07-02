import os
import torch
import torchaudio

from aasist.models.AASIST import Model
from aasist.data_utils import pad

from aasist.models.AASIST import Model
print("Loading AASIST...")
CONFIG = {
    "architecture": "AASIST",
    "nb_samp": 64600,
    "first_conv": 128,
    "filts": [
        70,
        [1,32],
        [32,32],
        [32,64],
        [64,64]
    ],
    "gat_dims":[64,32],
    "pool_ratios":[0.5,0.7,0.5,0.5],
    "temperatures":[2.0,2.0,100.0,100.0]
}
model = Model(CONFIG)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "aasist",
    "models",
    "weights",
    "AASIST.pth"
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location="cpu"
)

if isinstance(checkpoint, dict):
    if "state_dict" in checkpoint:
        checkpoint = checkpoint["state_dict"]
    elif "model" in checkpoint:
        checkpoint = checkpoint["model"]

model.load_state_dict(checkpoint)
model.eval()
model.eval()

device = torch.device("cpu")
model.to(device)

print("AASIST Loaded")
@torch.no_grad()
def detect_spoof(audio_file):

    waveform, sr = torchaudio.load(audio_file)

    # Convert to mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Resample to 16 kHz
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(sr, 16000)
        waveform = resampler(waveform)

    waveform = waveform.squeeze(0).numpy()

    waveform = pad(waveform, 64600)

    waveform = torch.FloatTensor(waveform).unsqueeze(0)

    _, logits = model(waveform)

    prediction = torch.argmax(logits, dim=1).item()

    print("--------------------------------")
    print("AASIST Prediction :", prediction)
    print("--------------------------------")

    return prediction == 0
