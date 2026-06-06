import pandas as pd
from db import (
    get_balance,
    get_total_transactions,
    get_total_spent,
    get_today_spent

)
from receipt import generate_receipt
from speaker_verify import verify_speaker
from record import record_audio
from speak import speak
from qr_payment import scan_qr, parse_upi
import os
import streamlit as st
st.set_page_config(
    page_title="VoicePay AI",
    page_icon="🎤",
    layout="wide"
)

balance = get_balance()

total_txns = get_total_transactions()

total_spent = get_total_spent()

today_spent = get_today_spent()

# -------------------------
# HEADER
# -------------------------

st.markdown(f"""
<div style="
background:linear-gradient(135deg,#2563EB,#60A5FA);
padding:25px;
border-radius:25px;
margin-bottom:30px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<div>

<h1 style="
color:white;
margin-bottom:10px;
">
🎤 VoicePay AI
</h1>

<h3 style="
color:white;
margin-bottom:10px;
">
Digital payments made simple with your voice
</h3>

<p style="
color:white;
font-size:18px;
">
Secure Voice Authentication + QR Payments
</p>

</div>

<div style="
background:white;
padding:25px;
border-radius:20px;
min-width:260px;
box-shadow:0px 4px 12px rgba(0,0,0,0.1);
">



</div>

</div>
""", unsafe_allow_html=True)


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


# -------------------------
# LOAD DATA
# -------------------------

balance = get_balance()
transactions = get_transactions()

# -------------------------
# HEADER
# -------------------------

# -------------------------
# TOP CARDS
# -------------------------

col1, col2 = st.columns(2)


metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(f"""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    ">

    <div style="
    font-size:32px;
    margin-bottom:10px;
    ">
    💰
    </div>

    <p style="
    color:#6B7280;
    margin:0;
    ">
    Balance
    </p>

    <h2 style="
    color:#111827;
    margin-top:10px;
    ">
    ₹{balance}
    </h2>

    </div>
    """, unsafe_allow_html=True)

with metric2:
    st.markdown(f"""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    ">

    <div style="
    font-size:32px;
    margin-bottom:10px;
    ">
    📈
    </div>

    <p style="
    color:#6B7280;
    margin:0;
    ">
    Transactions
    </p>

    <h2 style="
    color:#111827;
    margin-top:10px;
    ">
    {total_txns}
    </h2>

    </div>
    """, unsafe_allow_html=True)

with metric3:
    st.markdown(f"""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    ">

    <div style="
    font-size:32px;
    margin-bottom:10px;
    ">
    💸
    </div>

    <p style="
    color:#6B7280;
    margin:0;
    ">
    Total Spent
    </p>

    <h2 style="
    color:#111827;
    margin-top:10px;
    ">
    ₹{total_spent}
    </h2>

    </div>
    """, unsafe_allow_html=True)

with metric4:
    st.markdown(f"""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    ">

    <div style="
    font-size:32px;
    margin-bottom:10px;
    ">
    📅
    </div>

    <p style="
    color:#6B7280;
    margin:0;
    ">
    Today
    </p>

    <h2 style="
    color:#111827;
    margin-top:10px;
    ">
    ₹{today_spent}
    </h2>

    </div>
    """, unsafe_allow_html=True)

# -------------------------
# BUTTONS
# -------------------------
st.markdown("""
<style>

.quick-card{
    background:white;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);

    height:180px;

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;

    text-align:center;
    padding:20px;
}

.stButton > button{
    width:100% !important;
    height:52px !important;

    background:#2563EB !important;
    color:white !important;

    border:none !important;
    border-radius:12px !important;

    font-size:18px !important;
    font-weight:600 !important;
}

/* Upload QR styling */

[data-testid="stFileUploaderDropzone"]{
    border:2px dashed #2563EB !important;
    background:#EFF6FF !important;
}

[data-testid="stFileUploaderDropzone"] button{
    background:#2563EB !important;
    color:white !important;
    border:none !important;
    border-radius:12px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style="
margin-top:20px;
margin-bottom:20px;
">
⚡ Quick Actions
</h2>
""", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,1,1])
# -------------------------
# QR
# -------------------------
with c1:

    st.markdown("""
    <div class="quick-card">

    <h3>📷 Upload QR</h3>

    <p>
    Scan merchant QR and pay securely.
    </p>

    </div>
    """, unsafe_allow_html=True)

    uploaded_qr = st.file_uploader(
    "",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

    if uploaded_qr is not None:

        with open("temp_qr.png", "wb") as f:
            f.write(uploaded_qr.read())

        qr_data = scan_qr("temp_qr.png")

        if qr_data:

            upi_details = parse_upi(qr_data)

            st.success("QR Detected")

            st.write(
                "👤 Merchant:",
                upi_details.get("pn", "Unknown")
            )

            st.write(
                "🏦 UPI ID:",
                upi_details.get("pa", "Unknown")
            )

            amount = st.number_input(
                "💰 Enter Amount",
                min_value=1,
                step=1,
                key="qr_amount"
            )

            st.code(qr_data)

            if st.button("💳 Pay via QR"):

                status = st.empty()

                status.info(
                    "🎤 Verifying Speaker..."
                )

                record_audio(
                    "qr_verify.wav",
                    duration=4
                )

                score = verify_speaker(
                    "owner.wav",
                    "qr_verify.wav"
                )

                print(
                    "QR VERIFY SCORE =",
                    score
                )

                if score < 0.50:

                    status.error(
                        f"❌ Voice Verification Failed | Score = {score:.3f}"
                    )

                    speak(
                        "Voice verification failed"
                    )

                    st.stop()

                st.success(
                    "✅ Voice Verification Successful"
                )

                speak(
                    "Voice verification successful"
                )

                current_balance = get_balance()

                if amount > current_balance:

                    st.error(
                        f"❌ Payment Declined\n\nInsufficient Balance\n\nAvailable Balance: ₹{current_balance}"
                    )

                    speak(
                        "Payment declined due to insufficient balance"
                    )

                else:

                    update_balance(amount)

                    add_transaction(
                        upi_details.get("pn", "Unknown"),
                        amount,
                        "Success"
                    )

                    receipt_file = generate_receipt(
                        upi_details.get("pn", "Unknown"),
                        amount,
                        "Success"
                    )

                    new_balance = get_balance()

                    st.success(
                        f"💰 Remaining Balance: ₹{new_balance}"
                    )

                    with open(
                        receipt_file,
                        "rb"
                    ) as pdf:

                        st.download_button(
                            label="📄 Download Receipt",
                            data=pdf,
                            file_name=receipt_file,
                            mime="application/pdf"
                        )

                    speak(
                        "Payment successful"
                    )

                    #st.rerun()

        else:

            st.error("Invalid QR")

# -------------------------
# VOICE PAYMENT
# -------------------------

with c2:

    st.markdown("""
    <div class="quick-card">

    <h3>🎤 Voice Payment</h3>

    <p>
    Send money using voice commands
    </p>

    </div>
    """, unsafe_allow_html=True)
    if st.button(
        "🎙️ Start Voice Payment",
        use_container_width=True
    ):

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
    st.markdown("""
    <div class="quick-card">

    <h3>📜 History</h3>

    <p>
    View transaction records
    </p>

    </div>
""", unsafe_allow_html=True)
    if st.button(
        "📜 Open History",
        use_container_width=True
    ):

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


st.markdown("---")

st.subheader(
    "📊 Spending Analytics"
)

search = st.text_input(
    "🔍 Search Receiver"
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

if search:

    history_df = history_df[
        history_df["Receiver"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if not history_df.empty:

    history_df["Timestamp"] = pd.to_datetime(
        history_df["Timestamp"]
    )

    history_df["Date"] = (
        history_df["Timestamp"]
        .dt.date
    )

    st.subheader(
        "📈 Daily Spending"
    )

    daily_spending = (
    history_df
    .groupby("Date", as_index=False)["Amount"]
    .sum()
    )

    st.bar_chart(
        daily_spending.set_index("Date")
    )

    st.subheader(
        "👤 Spending by Receiver"
    )

    receiver_spending = (
        history_df
        .groupby("Receiver")["Amount"]
        .sum()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🏆 Top Receiver",
            receiver_spending.idxmax()
        )

    with col2:
        st.metric(
            "💸 Highest Transaction",
            f"₹{history_df['Amount'].max()}"
        )


    st.bar_chart(
        receiver_spending
    )

st.markdown("---")

st.subheader(
    "Recent Transactions"
)

csv = history_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Export History CSV",
    data=csv,
    file_name="transactions.csv",
    mime="text/csv"
)

st.dataframe(
    history_df,
    width="stretch",
    hide_index=True
)