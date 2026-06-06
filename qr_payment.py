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

    return details