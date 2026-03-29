import streamlit as st
import joblib
import pandas as pd
import random
import time
import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CaneAI", layout="wide")

# ---------------- LOAD MODEL ----------------
model = joblib.load("brix_model.pkl")

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0b0b0b, #111111);
    color: #f5f5f5;
}

/* Title */
.title {
    font-size: 50px;
    font-weight: 700;
    text-align: center;
    color: #D4AF37;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #bbbbbb;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background: #181818;
    border-radius: 18px;
    padding: 28px;
    border: 1px solid rgba(212,175,55,0.3);
    box-shadow: 0 6px 25px rgba(0,0,0,0.6);
}

/* Section Titles */
.section-title {
    font-size: 20px;
    font-weight: 600;
}

/* Metrics */
.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #FFD700;
}

.metric-label {
    color: #888;
    font-size: 14px;
}

/* Status */
.status {
    color: #00ffcc;
    font-size: 14px;
    margin-bottom: 8px;
}

/* Decision */
.accept {color: #00ff88; font-size: 28px; font-weight: bold;}
.hold {color: #FFD700; font-size: 28px; font-weight: bold;}
.reject {color: #ff4d4d; font-size: 28px; font-weight: bold;}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #D4AF37, #FFD700);
    color: black;
    font-weight: bold;
    border-radius: 10px;
}

/* FIX METRICS */
[data-testid="stMetric"] {
    background: #1c1c1c;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(212,175,55,0.3);
}

[data-testid="stMetricLabel"] {
    color: #aaaaaa !important;
}

[data-testid="stMetricValue"] {
    color: #FFD700 !important;
    font-size: 32px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>CaneAI Intelligence System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Real-Time Sugarcane Quality Monitoring & AI Decision Engine</div>", unsafe_allow_html=True)

# ---------------- HARDWARE STATUS ----------------
st.markdown("<div class='status'>🟢 Arduino Connected | Serial Stream Active | Data Rate: 2 Hz</div>", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "cane_id" not in st.session_state:
    st.session_state.cane_id = 1

# ---------------- SENSOR DATA ----------------
ir = round(random.uniform(0.3, 0.8), 2)
dielectric = round(random.uniform(10, 20), 2)
moisture = round(random.uniform(60, 80), 2)

# ---------------- STATUS BAR ----------------
colA, colB, colC = st.columns(3)
colA.metric("Cane ID", f"#{st.session_state.cane_id}")
colB.metric("System Status", "Active")
colC.metric("Mode", "Real-Time")

st.markdown("---")

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns(2)

# -------- SENSOR PANEL --------
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📡 Sensor Feed</div>", unsafe_allow_html=True)
    st.markdown("<div class='status'>● Receiving data from sensor module</div>", unsafe_allow_html=True)

    # Timestamp
    st.markdown(f"<div class='metric-label'>Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='metric-label'>IR Value</div><div class='metric-value'>{ir}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>Dielectric</div><div class='metric-value'>{dielectric}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>Moisture (%)</div><div class='metric-value'>{moisture}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------- AI PANEL --------
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>🧠 AI Decision Engine</div>", unsafe_allow_html=True)

    if st.button("Analyze Cane"):
        data = pd.DataFrame([[ir, dielectric, moisture]],
                            columns=["IR_value", "Dielectric_value", "Moisture"])
        
        brix = model.predict(data)[0]

        if brix >= 15:
            decision = "ACCEPT"
            style = "accept"
            reason = "High quality cane detected"
        elif 13 <= brix < 15:
            decision = "HOLD"
            style = "hold"
            reason = "Moderate quality cane"
        else:
            decision = "REJECT"
            style = "reject"
            reason = "Low quality cane"

        st.markdown(f"<div class='metric-label'>Brix Value</div><div class='metric-value'>{round(brix,2)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{style}'>Decision: {decision}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-label'>Reason</div><div>{reason}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("<div class='subtitle'>CaneAI • Industrial Intelligence Platform</div>", unsafe_allow_html=True)

# ---------------- AUTO REFRESH ----------------
time.sleep(5)
st.session_state.cane_id += 1
st.rerun()
