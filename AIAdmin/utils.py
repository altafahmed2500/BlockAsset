import pandas as pd
import random


def generate_wearable_data():
    return {
        "Timestamp": pd.Timestamp.now(),
        "Temperature (°C)": round(random.uniform(36.0, 37.5), 2),
        "O2 Saturation (%)": random.randint(90, 100),
        "Heart Rate (bpm)": random.randint(60, 100),
        "Gyroscope (x, y, z)": (
            round(random.uniform(-2.0, 2.0), 2),
            round(random.uniform(-2.0, 2.0), 2),
            round(random.uniform(-2.0, 2.0), 2),
        ),
        "Glucose Level (mg/dL)": random.randint(70, 140),
    }


def detect_anomalies(data):
    """
    Detect anomalies in the entire dataset.

    Parameters:
        data (pd.DataFrame): The dataset containing wearable data.

    Returns:
        dict: A dictionary mapping row indices to detected anomalies.
    """
    anomalies = {}

    # Iterate over each row in the dataset
    for index, row in data.iterrows():
        row_anomalies = []

        if row["Temperature (°C)"] > 37.5 or row["Temperature (°C)"] < 36.0:
            row_anomalies.append("Abnormal temperature detected.")
        if row["O2 Saturation (%)"] < 90:
            row_anomalies.append("Low oxygen saturation detected.")
        if row["Heart Rate (bpm)"] > 100 or row["Heart Rate (bpm)"] < 60:
            row_anomalies.append("Abnormal heart rate detected.")
        if row["Glucose Level (mg/dL)"] > 140 or row["Glucose Level (mg/dL)"] < 70:
            row_anomalies.append("Abnormal glucose level detected.")

        # If anomalies are detected for this row, add them to the dictionary
        if row_anomalies:
            anomalies[index] = row_anomalies

    return anomalies
