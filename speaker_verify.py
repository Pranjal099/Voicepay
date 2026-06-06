from speechbrain.inference.speaker import SpeakerRecognition

print("Loading Speaker Verification Model...")

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models"
)

def verify_speaker(owner_file, test_file):
    print("Comparing Voices...")

    score, prediction = verification.verify_files(
        owner_file,
        test_file
    )

    score_value = score.item()

    print("\nSimilarity Score:")
    print(score_value)

    return score_value