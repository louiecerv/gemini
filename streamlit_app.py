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

    # Initialize the conversation
    url = f"https://dialogflow.googleapis.com/v2/projects/{project_id}/locations/global/conversations/my-conversation-id"

    # Create initial conversation (if needed, remove if already exists)
    conversation_config = {
        "audio_config": {
            "audio_encoding": "AUDIO_ENCODING_LINEAR_16"
        }
    }
    response = requests.post(url, headers=headers, json=conversation_config)
    if response.status_code == 200:
        print("Conversation created successfully")
    else:
        print(f"Error creating conversation: {response.text}")

    # Input text field
    user_input = st.text_input("Message")

    # Once the user hits enter, send the message
    if user_input:
        # Set the input text
        text_input = {"text": user_input}

        # Send the message to the API
        url = f"https://dialogflow.googleapis.com/v2/projects/{project_id}/locations/global/conversations/my-conversation-id/query"
        response = requests.post(url, headers=headers, json={"queryInput": text_input})

        if response.status_code == 200:
            response_data = response.json()
            response_type = response_data["message"]["messageType"]

            # Handle the response based on the message type
            if response_type == "TEXT":
                st.write(f"Bot: {response_data['message']['text']['text']}")
            elif response_type in ["CARD", "CAROUSEL"]:
                display_card(response_data["message"]["cards"])
            else:
                st.write("Sorry, I'm not sure how to respond to that.")
        else:
            print(f"Error sending message: {response.text}")

if __name__ == "__main__":
    app()
