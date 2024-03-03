import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import google.cloud.dialogflow as dialogflow
from google.cloud.dialogflow_v2beta1.services import conversations_client
from google.protobuf import field_mask_pb2

# Define the Streamlit app
def app():

    project_id = "wvsu-cloud"
    #text_input_field_name = "USER"

    st.title("Chatbot using Google Gemini API on Streamlit")
    st.subheader("Enter your message below, and I will respond!")

    # Initialize the Gemini client
    client = conversations_client.ConversationsClient()

    # Set up the initial conversation
    conversation_config = dialogflow.ConversationsConfig(
        audio_config=dialogflow.AudioConfig(
            audio_encoding=dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        )
    )
    create_request = conversations_client.CreateConversationRequest(
        parent=f"projects/{project_id}/locations/global",
        conversation_id="my-conversation-id",
        conversation=conversation_config,
    )
    conversation_name = client.create_conversation(create_request).name

    # Input text field
    user_input = st.text_input("Message")

    # Once the user hits enter, send the message to the chatbot
    if user_input:
        # Set the input text and associated metadata
        text_input = dialogflow.TextInput(text=user_input)
        message = dialogflow.Message(text_input=text_input)

        # Send the message to the Gemini API
        text_response = client.send_message(
            request={
                "conversation": conversation_name,
                "query_input": dialogflow.QueryInput(text=text_input),
            }
        )
        response_type = text_response.message.message_type
        
        # Handle the response based on the message type
        if response_type == dialogflow.Message.MessageType.TEXT:
            st.write(f"Bot: {text_response.message.text.text}")
        elif (
            response_type == dialogflow.Message.MessageType.CARD
            or response_type == dialogflow.Message.MessageType.CAROUSEL
        ):
            display_card(text_response.message.cards)
        else:
            st.write("Sorry, I'm not sure how to respond to that.")

if __name__ == "__main__":
    app()
