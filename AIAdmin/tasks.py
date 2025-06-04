import pandas as pd
import json
import time
from .utils import generate_wearable_data, detect_anomalies
from .openai_api import get_summary_from_chatgpt


def collect_wearable_data():
    # Define DataFrame columns
    columns = ["Timestamp", "Temperature (°C)", "O2 Saturation (%)",
               "Heart Rate (bpm)", "Gyroscope (x, y, z)", "Glucose Level (mg/dL)"]

    # Create an empty list to store new data
    data_list = []

    # Generate data and populate list
    for _ in range(12):  # Generate data for 12 intervals
        new_data = generate_wearable_data()

        # Check if new_data is valid (not empty or all NaN)
        if pd.DataFrame([new_data]).notna().any().any():
            data_list.append(new_data)

    # Create a DataFrame from the collected data
    wearable_data_df = pd.DataFrame(data_list, columns=columns)

    # Save DataFrame to JSON
    json_data = wearable_data_df.to_json(orient='records')

    # Detect anomalies in the entire dataset
    anomalies = detect_anomalies(wearable_data_df)

    # Pass JSON data to AI for summary
    summary = get_summary_from_chatgpt(json_data, wearable_data_df)

    return wearable_data_df, summary
