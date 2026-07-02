import cv2


def scan_qr(image_path):

    detector = cv2.QRCodeDetector()

    img = cv2.imread(image_path)

    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        return data

    return None


def parse_upi(qr_data):

    details = {}

    if "?" not in qr_data:
        return details

    params = qr_data.split("?")[1]

    for item in params.split("&"):

        if "=" in item:

            key, value = item.split("=", 1)

            details[key] = value

    merchant = details.get("pn", "Unknown Merchant")
    upi = details.get("pa", "")
    amount = details.get("am")

    # -----------------------------
    # Dynamic QR
    # -----------------------------
    if amount:

        return {
            "merchant_name": merchant,
            "upi_id": upi,
            "amount": amount,
            "need_amount": False,
            "need_confirmation": True,
            "speech": f"You are about to pay {amount} rupees to {merchant}. Please say Confirm."
        }

    # -----------------------------
    # Static QR
    # -----------------------------
    return {
        "merchant_name": merchant,
        "upi_id": upi,
        "amount": None,
        "need_amount": True,
        "need_confirmation": False,
        "speech": f"I found {merchant}. How much would you like to pay?"
    }