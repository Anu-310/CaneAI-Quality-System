import joblib
import pandas as pd
from datetime import datetime

# Load model
model = joblib.load("brix_model.pkl")

def sugarcane_agent(ir, dielectric, moisture):
    
    # Input data
    data = pd.DataFrame([[ir, dielectric, moisture]],
                        columns=["IR_value", "Dielectric_value", "Moisture"])
    
    # Prediction
    brix = model.predict(data)[0]
    
    # Decision logic
    if brix >= 15:
        decision = "ACCEPT"
        reason = "High quality cane (Brix >= 15)"
    elif 13 <= brix < 15:
        decision = "HOLD"
        reason = "Medium quality cane"
    else:
        decision = "REJECT"
        reason = "Low quality cane"
    
    # Timestamp
    time = datetime.now()
    
    # Create log entry
    log = {
        "Time": time,
        "IR": ir,
        "Dielectric": dielectric,
        "Moisture": moisture,
        "Brix": round(brix, 2),
        "Decision": decision,
        "Reason": reason
    }
    
    # Convert to DataFrame
    log_df = pd.DataFrame([log])
    
    # Save to CSV (append mode)
    try:
        log_df.to_csv("audit_log.csv", mode='a', header=False, index=False)
    except:
        log_df.to_csv("audit_log.csv", index=False)
    
    # Output
    print("\n--- AI AGENT OUTPUT ---")
    print("Predicted Brix:", round(brix, 2))
    print("Decision:", decision)
    print("Reason:", reason)
    print("Logged successfully!")


# Test
sugarcane_agent(0.6, 15, 70)
