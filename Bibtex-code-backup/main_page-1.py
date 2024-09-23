# main_page.py
import streamlit as st
import openai
import json
import os
from utils import load_settings, save_settings  # Import shared functions

# Configure Streamlit page settings
st.set_page_config(
    page_title="BiTeX",
    page_icon="🕵️",
    layout="centered"
)


# Function to setup OpenAI API
def setup_openai():
    openai.api_key = st.secrets["OPENAI_API_KEY"]


# Function to trim the conversation to avoid exceeding token limits
def trim_conversation(conversation, max_length=1024):
    current_length = sum(len(msg['content']) for msg in conversation)
    while current_length > max_length and len(conversation) > 1:
        removed_message = conversation.pop(0)
        current_length -= len(removed_message['content'])
    return conversation


# Initialize chat session in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("✍🏻 Bibliography Management System")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Enter your Refs...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Load settings and setup OpenAI API
    settings = load_settings()
    current_model = settings.get("model", "gpt-3.5-turbo")
    setup_openai()

    # Send user's message to GPT-3.5-turbo and get a response
    response = openai.ChatCompletion.create(
        model=current_model,
        messages=[
            {"role": "system",
             "content": "You are an assistant trained to convert academic references into BibTeX format."},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message['content']
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display GPT-3.5-turbo's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

if __name__ == "__main__":
    main_page()
