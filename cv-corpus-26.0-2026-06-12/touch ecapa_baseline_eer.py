import pandas as pd
import random
import os
import torch
import torchaudio
import numpy as np

from speechbrain.inference.speaker import EncoderClassifier
from sklearn.metrics import roc_curve

BASE_DIR = "/Users/pranjalgautam/Desktop/Voicepay/cv-corpus-26.0-2026-06-12/hi"

print("Loading ECAPA...")

classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb"
)

df = pd.read_csv(
    os.path.join(BASE_DIR, "validated.tsv"),
    sep="\t"
)

speaker_groups = df.groupby("client_id")

valid_speakers = [
    spk
    for spk, group in speaker_groups
    if len(group) >= 2
]

print("Speakers:", len(valid_speakers))

scores = []
labels = []

for i in range(300):

    spk = random.choice(valid_speakers)

    files = speaker_groups.get_group(spk)["path"].tolist()

    a, b = random.sample(files, 2)

    f1 = os.path.join(BASE_DIR, "clips", a)
    f2 = os.path.join(BASE_DIR, "clips", b)

    sig1, _ = torchaudio.load(f1)
    sig2, _ = torchaudio.load(f2)

    emb1 = classifier.encode_batch(sig1)
    emb2 = classifier.encode_batch(sig2)

    score = torch.nn.functional.cosine_similarity(
        emb1.squeeze(),
        emb2.squeeze(),
        dim=0
    ).item()

    scores.append(score)
    labels.append(1)

for i in range(300):

    spk1, spk2 = random.sample(valid_speakers, 2)

    f1 = os.path.join(
        BASE_DIR,
        "clips",
        random.choice(
            speaker_groups.get_group(spk1)["path"].tolist()
        )
    )

    f2 = os.path.join(
        BASE_DIR,
        "clips",
        random.choice(
            speaker_groups.get_group(spk2)["path"].tolist()
        )
    )

    sig1, _ = torchaudio.load(f1)
    sig2, _ = torchaudio.load(f2)

    emb1 = classifier.encode_batch(sig1)
    emb2 = classifier.encode_batch(sig2)

    score = torch.nn.functional.cosine_similarity(
        emb1.squeeze(),
        emb2.squeeze(),
        dim=0
    ).item()

    scores.append(score)
    labels.append(0)

fpr, tpr, _ = roc_curve(labels, scores)

fnr = 1 - tpr

eer = fpr[np.nanargmin(np.abs(fnr - fpr))]

print(f"\nEER = {eer * 100:.2f}%")