import os
import streamlit as st
import pandas as pd

from voice_payment import process_voice_payment

from db import (
    get_balance,
    update_balance,
    add_transaction,
    get_transactions
)

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="VoicePay AI",
    page_icon="🎤",
    layout="wide"
)

# -------------------------
# LOAD DATA
# -------------------------

balance = get_balance()
transactions = get_transactions()

# -------------------------
# HEADER
# -------------------------

st.title("🎤 VoicePay AI")
st.caption("Built using Whisper + SpeechBrain + SQLite")

st.markdown("---")

# -------------------------
# TOP CARDS
# -------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💰 Wallet Balance",
        f"₹{balance}"
    )

with col2:
    st.metric(
        "🔒 Security",
        "Voice Verified"
    )

st.markdown("---")

# -------------------------
# BUTTONS
# -------------------------

c1, c2, c3 = st.columns(3)

# -------------------------
# QR
# -------------------------

with c1:

    if st.button("📷 Scan QR"):
        st.info("QR Scanner Coming Soon")

# -------------------------
# VOICE PAYMENT
# -------------------------

with c2:

    if st.button("🎙️ Voice Payment"):

        status = st.empty()

        try:

            status.info(
                "🎤 Starting Voice Payment..."
            )

            result = process_voice_payment()

            print("APP GOT RESULT =", result)

            if result is None:

                status.error(
                    "❌ No response returned"
                )

            elif result.get("status") == "success":

                receiver = result["receiver"]
                amount = int(result["amount"])

                current_balance = get_balance()

                print(
                    "CURRENT BALANCE =",
                    current_balance
                )

                print(
                    "PAYMENT AMOUNT =",
                    amount
                )

                # -------------------------
                # INSUFFICIENT BALANCE
                # -------------------------

                if amount > current_balance:

                    os.system(
                        f'say "Payment declined due to insufficient balance. Available balance is {current_balance} rupees"'
                    )

                    status.error(
                        f"❌ Payment Declined\n\nInsufficient Balance\n\nAvailable Balance: ₹{current_balance}"
                    )

                    st.stop()

                # -------------------------
                # UPDATE DATABASE
                # -------------------------

                print(
                    "BEFORE UPDATE =",
                    get_balance()
                )

                update_balance(amount)

                print(
                    "AFTER UPDATE =",
                    get_balance()
                )

                add_transaction(
                    receiver.title(),
                    amount,
                    "Success"
                )

                print(
                    "TRANSACTION SAVED"
                )

                new_balance = get_balance()

                os.system(
                    f'say "Payment successful. {amount} rupees sent to {receiver}"'
                )

                st.success(
                    f"✅ Payment Successful"
                )

                st.success(
                    f"₹{amount} sent to {receiver.title()}"
                )

                st.success(
                    f"💰 New Balance = ₹{new_balance}"
                )

                st.stop()

            elif result.get("status") == "declined":

                status.error(
                    "❌ Payment Declined"
                )

            elif result.get("status") == "failed":

                status.error(
                    f"❌ Voice Verification Failed | Score = {result.get('score', 0):.3f}"
                )

            else:

                status.error(
                    f"❌ Unknown Response: {result}"
                )

        except Exception as e:

            st.exception(e)

# -------------------------
# HISTORY
# -------------------------

with c3:

    if st.button("📜 History"):

        history_df = pd.DataFrame(
            transactions,
            columns=[
                "Receiver",
                "Amount",
                "Status",
                "Timestamp"
            ]
        )

        st.dataframe(
            history_df,
            width="stretch",
            hide_index=True
        )

# -------------------------
# RECENT TRANSACTIONS
# -------------------------

st.markdown("---")

st.subheader(
    "Recent Transactions"
)

history_df = pd.DataFrame(
    transactions,
    columns=[
        "Receiver",
        "Amount",
        "Status",
        "Timestamp"
    ]
)

st.dataframe(
    history_df,
    width="stretch",
    hide_index=True
)