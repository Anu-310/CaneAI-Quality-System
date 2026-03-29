import joblib
import pandas as pd

# Load trained model
model = joblib.load("brix_model.pkl")

def sugarcane_agent(ir, dielectric, moisture):
    
    # Create input
    data = pd.DataFrame([[ir, dielectric, moisture]],
                        columns=["IR_value", "Dielectric_value", "Moisture"])
    
    # Predict Brix
    brix = model.predict(data)[0]
    
    # Decision logic (RULES)
    if brix >= 15:
        decision = "ACCEPT"
        reason = "High quality cane (Brix >= 15)"
    
    elif 13 <= brix < 15:
        decision = "HOLD"
        reason = "Medium quality cane (13 <= Brix < 15)"
    
    else:
        decision = "REJECT"
        reason = "Low quality cane (Brix < 13)"
    
    # Output
    print("\n--- AI AGENT OUTPUT ---")
    print("Predicted Brix:", round(brix, 2))
    print("Decision:", decision)
    print("Reason:", reason)


# Test run
sugarcane_agent(0.6, 15, 70)
