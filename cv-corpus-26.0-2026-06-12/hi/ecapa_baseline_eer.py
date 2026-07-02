import pandas as pd
import random
import os
import torch
import numpy as np

from speechbrain.inference.speaker import EncoderClassifier
from sklearn.metrics import roc_curve

print("Loading ECAPA...")
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_ecapa"
)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(
    os.path.join(BASE_DIR, "validated.tsv"),
    sep="\t"
)

speaker_groups = df.groupby("client_id")

valid_speakers = []

for spk, group in speaker_groups:
    if len(group) >= 2:
        valid_speakers.append(spk)

print("Speakers with >=2 recordings:", len(valid_speakers))

# ==========================
# GENUINE PAIRS
# ==========================

genuine_pairs = []

for spk in valid_speakers:

    rows = speaker_groups.get_group(spk)

    files = rows["path"].tolist()

    if len(files) >= 2:

        a, b = random.sample(files, 2)

        genuine_pairs.append(
            (
                os.path.join("clips", a),
                os.path.join("clips", b),
                1
            )
        )

# ==========================
# IMPOSTOR PAIRS
# ==========================

impostor_pairs = []

for _ in range(len(genuine_pairs)):

    spk1, spk2 = random.sample(
        valid_speakers,
        2
    )

    file1 = random.choice(
        speaker_groups.get_group(spk1)["path"].tolist()
    )

    file2 = random.choice(
        speaker_groups.get_group(spk2)["path"].tolist()
    )

    impostor_pairs.append(
        (
            os.path.join(BASE_DIR, "clips", file1),
            os.path.join(BASE_DIR, "clips", file2),
            0
        )
    )

pairs = genuine_pairs + impostor_pairs

print("Total pairs:", len(pairs))

scores = []
labels = []

for idx, (f1, f2, label) in enumerate(pairs):

    sig1, sr1 = torchaudio.load(f1)
    sig2, sr2 = torchaudio.load(f2)

    emb1 = classifier.encode_batch(sig1)
    emb2 = classifier.encode_batch(sig2)

    score = torch.nn.functional.cosine_similarity(
        emb1.squeeze(),
        emb2.squeeze(),
        dim=0
    ).item()

    scores.append(score)
    labels.append(label)

    if idx % 100 == 0:
        print(idx, "/", len(pairs))

# ==========================
# EER
# ==========================

fpr, tpr, thresholds = roc_curve(
    labels,
    scores
)

fnr = 1 - tpr

eer_idx = np.nanargmin(
    np.abs(fnr - fpr)
)

eer = fpr[eer_idx]

print("\n====================")
print(f"EER: {eer*100:.2f}%")
print("====================")
