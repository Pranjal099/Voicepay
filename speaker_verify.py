from speechbrain.inference.speaker import SpeakerRecognition

print("Loading Speaker Verification Model...")

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models"
)

print("Comparing Voices...")

score, prediction = verification.verify_files(
    "owner.wav",
    "test.wav"
)

score_value = score.item()

print("\nSimilarity Score:")
print(score_value)

print("\nPrediction:")
print(prediction)

# Threshold logic
threshold = 0.75

if score_value > threshold:
    print("\n✅ ACCESS GRANTED")
else:
    print("\n❌ ACCESS DENIED")