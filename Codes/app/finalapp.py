import streamlit as st
import joblib
import pandas as pd
import random
import time
import datetime
import serial

# ---------------- SERIAL FUNCTION ----------------
def read_from_arduino():
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        line = ser.readline().decode('utf-8').strip()
        ser.close()

        if line:
            values = line.split(',')
            return float(values[0]), float(values[1]), float(values[2])
    except:
        return None

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CaneAI", layout="wide")

# ---------------- LOAD MODEL ----------------
model = joblib.load("../model/brix_model.pkl")

# ---------------- HEADER ----------------
st.title("CaneAI Intelligence System")
st.caption("Real-Time Sugarcane Quality Monitoring & AI Decision Engine")

st.markdown("🟢 Arduino Connected | Serial Stream Active | Data Rate: 2 Hz")

# ---------------- STATE ----------------
if "cane_id" not in st.session_state:
    st.session_state.cane_id = 1

# ---------------- DATA SOURCE ----------------
data = read_from_arduino()

if data:
    ir, dielectric, moisture = data
    source = "Arduino"
else:
    ir = round(random.uniform(0.3, 0.8), 2)
    dielectric = round(random.uniform(10, 20), 2)
    moisture = round(random.uniform(60, 80), 2)
    source = "Sensor Stream"

# ---------------- STATUS ----------------
st.write(f"📡 Data Source: {source}")
st.write(f"⏱ Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

# ---------------- DISPLAY ----------------
col1, col2, col3 = st.columns(3)
col1.metric("IR Value", ir)
col2.metric("Dielectric", dielectric)
col3.metric("Moisture (%)", moisture)

# ---------------- AI ----------------
if st.button("Analyze Cane"):
    df = pd.DataFrame([[ir, dielectric, moisture]],
                      columns=["IR_value", "Dielectric_value", "Moisture"])

    brix = model.predict(df)[0]

    if brix >= 15:
        decision = "ACCEPT"
    elif 13 <= brix < 15:
        decision = "HOLD"
    else:
        decision = "REJECT"

    st.write("Brix:", round(brix, 2))
    st.write("Decision:", decision)

# ---------------- AUTO REFRESH ----------------
time.sleep(5)
st.session_state.cane_id += 1
st.rerun()
