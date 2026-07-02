import os
import torch
from speechbrain.inference.speaker import SpeakerRecognition

print("Loading Fine-tuned ECAPA Model...")

# --------------------------------------------------
# Load pretrained SpeechBrain verification pipeline
# --------------------------------------------------

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models"
)

# --------------------------------------------------
# Load fine-tuned ECAPA encoder weights
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "voicepay_best_epoch_40_eer_3.60.pth"
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location="cpu"
)

verification.mods.embedding_model.load_state_dict(
    checkpoint,
    strict=True
)

verification.eval()

print("Fine-tuned ECAPA loaded successfully.")

# --------------------------------------------------
# Speaker Verification Function
# --------------------------------------------------

def verify_speaker(owner_file, test_file):

    score, prediction = verification.verify_files(
        owner_file,
        test_file
    )

    score = score.item()

    print("--------------------------------")
    print("Speaker Verification")
    print("--------------------------------")
    print("Enrollment :", owner_file)
    print("Test Voice :", test_file)
    print("Similarity :", round(score, 4))
    print("Prediction :", prediction)
    print("--------------------------------")

    return score