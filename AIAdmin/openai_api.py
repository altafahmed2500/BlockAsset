import openai
from openai import OpenAIError

# OpenAI API key (replace with your actual key)
openai.api_key = ""


def get_summary_from_chatgpt(data, anomalies):
    prompt = f"""
    Analyze the following wearable sensor data and generate a summary:
    Data: {data}
    Detected Anomalies: {anomalies}
    include brief summary of the report in less word and concise.
    give the content in bullet points.   
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        # Handle the quota exceeded error or any other API error
        error_message = f"Error communicating with OpenAI API: {e}"
        print(error_message)
        return f"Unable to generate summary due to API error: {error_message}"
