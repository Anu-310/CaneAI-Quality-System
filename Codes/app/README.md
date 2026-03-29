# Application Module

This module contains the main application responsible for real-time data processing, AI-based prediction, and user interface.

## Functionality

- Receives sensor data via serial communication from the hardware module
- Processes input features (IR value, dielectric value, moisture)
- Uses a trained machine learning model to predict Brix value
- Performs quality classification (Accept / Hold / Reject)
- Displays results through an interactive Streamlit dashboard

## Features

- Real-time data visualization
- Automated decision-making
- Continuous monitoring (simulated conveyor flow)
- Integration-ready with embedded sensor systems

## Execution

Run the application using:

```bash
py -m streamlit run finalapp.py
