# helpful_assistant.py
import streamlit as st
import openai
import json
import os
from utils import load_settings  # Import shared functions

# Function to setup OpenAI API
def setup_openai():
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to save the chat history to a file
def save_history_to_file(history, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Function to load the chat history from a file
def load_history_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def helpful_assistant_page():
    st.title('🤝 Helpful Assistant')

    # Load settings
    settings = load_settings()
    current_model = settings["model"]

    # File to save chat history
    history_file = 'chat_history_helpful.json'

    # Initialize chat session in Streamlit if not already present
    if "chat_history_helpful" not in st.session_state:
        st.session_state.chat_history_helpful = load_history_from_file(history_file)

    # Display chat history
    for message in st.session_state.chat_history_helpful:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user's message
    user_prompt = st.chat_input("👉 Enter your query...")

    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history_helpful.append({"role": "user", "content": user_prompt})

        # Send user's message to GPT-3.5-turbo and get a response
        setup_openai()
        response = openai.ChatCompletion.create(
            model=current_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.chat_history_helpful
            ]
        )

        assistant_response = response.choices[0].message['content']
        st.session_state.chat_history_helpful.append({"role": "assistant", "content": assistant_response})

        # Display GPT-3.5-turbo's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Save the updated chat history
        save_history_to_file(st.session_state.chat_history_helpful, history_file)

if __name__ == "__main__":
    helpful_assistant_page()
