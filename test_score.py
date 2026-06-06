from speechbrain.inference.speaker import SpeakerRecognition

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models"
)

score, prediction = verification.verify_files(
    "owner.wav",
    "input.wav"
)

score = score.item()

print("\nSimilarity Score:")
print(score)