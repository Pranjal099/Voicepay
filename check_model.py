import torch

MODEL_PATH = "voicepay_best_epoch_40_eer_3.60.pth"

checkpoint = torch.load(
    MODEL_PATH,
    map_location="cpu"
)

print("=" * 60)
print(type(checkpoint))
print("=" * 60)

if isinstance(checkpoint, dict):
    print("Keys:")
    print(checkpoint.keys())

    print("\n")

    for k, v in checkpoint.items():
        print("KEY:", k)
        print("TYPE:", type(v))

        if isinstance(v, dict):
            print("Subkeys:", list(v.keys())[:20])

        elif hasattr(v, "keys"):
            print("Subkeys:", list(v.keys())[:20])

        print("-" * 60)