import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import requests
from google.cloud import aiplatform

# Define the Streamlit app
def app():

    project_id = "wvsu-cloud"
    api_key = st.secrets["API_KEY"]
    st.title("Chatbot using Google Gemini API on Streamlit")
    st.subheader("Enter your message below, and I will respond!")
    
    # Set up headers with the API key
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Model ID for Gemini 1.0 Pro (replace if using a different model)
    model_id = "projects/{}/locations/global/models/gemini-1.0-pro".format(project_id)
    
    # Input text field
    user_input = st.text_input("Message")
    
    # Once the user hits enter, send the message
    if st.button('Submit'):
        st.write('Sending prompt...')
    
        # Create the request body
        request_body = {
            "contents": [
                {
                    "text": user_input
                }
            ]
        }
    
        # Send the request to the Gemini API
        url = f"https://{project_id}-us.vertexai.googleapis.com/v1/{model_id}:streamGenerateContent"
        response = requests.post(url, headers=headers, json=request_body)
    
        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data["contents"][0]["text"]
            st.write(f"Bot: {generated_text}")
        else:
            st.write(f"Error sending message: {response.text}")

if __name__ == "__main__":
    app()
