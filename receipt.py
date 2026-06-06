from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


def generate_receipt(
    receiver,
    amount,
    status
):

    transaction_id = (
        f"TXN{int(datetime.now().timestamp())}"
    )

    filename = (
        f"receipt_{transaction_id}.pdf"
    )

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "VoicePay AI",
            styles["Title"]
        ),

        Spacer(1, 20),

        Paragraph(
            f"Transaction ID: {transaction_id}",
            styles["Normal"]
        ),

        Paragraph(
            f"Receiver: {receiver}",
            styles["Normal"]
        ),

        Paragraph(
            f"Amount: ₹{amount}",
            styles["Normal"]
        ),

        Paragraph(
            f"Status: {status}",
            styles["Normal"]
        ),

        Paragraph(
            f"Date: {datetime.now()}",
            styles["Normal"]
        ),

        Spacer(1, 20),

        Paragraph(
            "Thank you for using VoicePay AI",
            styles["Italic"]
        )
    ]

    doc.build(content)

    return filename