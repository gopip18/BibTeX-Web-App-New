# BibTeX_journal_abbr.py
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

# Function to estimate token count of a message (approximation)
def estimate_token_count(text):
    return len(text.split())

# Function to trim the conversation to avoid exceeding token limits
def trim_conversation(conversation, max_tokens=16000):
    total_tokens = sum([estimate_token_count(msg['content']) for msg in conversation])
    trimmed_conversation = conversation[:]

    # Trim older messages only if total tokens exceed max limit
    while total_tokens > max_tokens and len(trimmed_conversation) > 1:
        total_tokens -= estimate_token_count(trimmed_conversation.pop(0)['content'])
    return trimmed_conversation

def main_page_with_abbr():
    st.title('🚀 BibTeX with Journal Abbreviation')

    # Load settings
    settings = load_settings()
    current_model = settings["model"]

    # File to save chat history
    history_file = 'chat_history_abbr.json'

    # Initialize chat session in Streamlit if not already present
    if "chat_history_abbr" not in st.session_state:
        st.session_state.chat_history_abbr = load_history_from_file(history_file)

    # Display chat history
    for message in st.session_state.chat_history_abbr:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user's message
    user_prompt = st.chat_input("👉 Enter your Refs...")

    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history_abbr.append({"role": "user", "content": user_prompt})

        # Trim conversation history to stay within token limits
        st.session_state.chat_history_abbr = trim_conversation(st.session_state.chat_history_abbr)

        # Send user's message to GPT-3.5-turbo and get a response
        setup_openai()
        try:
            response = openai.ChatCompletion.create(
                model=current_model,
                messages=[
                    {"role": "system", "content": "You are an assistant trained to convert academic references into BibTeX format with journal abbreviations."},
                    *st.session_state.chat_history_abbr
                ]
            )

            assistant_response = response.choices[0].message['content']
            st.session_state.chat_history_abbr.append({"role": "assistant", "content": assistant_response})

            # Display GPT-3.5-turbo's response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

            # Save the updated chat history
            save_history_to_file(st.session_state.chat_history_abbr, history_file)

        except openai.error.InvalidRequestError as e:
            st.error(f"Invalid request error: {e}")
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main_page_with_abbr()
