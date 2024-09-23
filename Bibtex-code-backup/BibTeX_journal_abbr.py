# BibTeX_journal_abbr.py
import streamlit as st
import openai
import json
import os
import requests
from latex_encoder import latex_encode  # Import the function
from utils import load_settings, save_settings  # Import shared functions

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

# Function to fetch journal name abbreviation from an online source
def fetch_journal_abbreviation(journal_name):
    url = "https://www.issn.org/services/online-services/access-to-the-ltwa/#recherche"  # Replace with actual API endpoint
    params = {"journal_name": journal_name}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("abbreviation", journal_name)  # Return abbreviation or original name if not found
    except requests.RequestException as e:
        print(f"An error occurred while fetching abbreviation: {e}")
        return journal_name

# Function to get BibTeX format with journal name abbreviation using ChatGPT
def get_bibtex_with_abbr(reference, conversation, model):
    conversation = trim_conversation(conversation, max_length=1500)  # Adjust max_length as needed

    if not any(msg.get('role') == 'system' for msg in conversation):
        conversation.insert(0, {"role": "system", "content": "You are an assistant trained to convert academic references into BibTeX format with journal name abbreviation."})
    conversation.append({"role": "user", "content": reference})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=0.7,
            max_tokens=4096  # Adjust max_tokens if necessary
        )
        bibtex_entry = response.choices[0].message['content'].strip()

        # Extract journal name and fetch abbreviation
        for line in bibtex_entry.split('\n'):
            if line.lower().startswith("journal"):
                journal_name = line.split('=')[1].strip().strip('{}')
                abbr_name = fetch_journal_abbreviation(journal_name)
                bibtex_entry = bibtex_entry.replace(journal_name, abbr_name)

        conversation.append({"role": "assistant", "content": bibtex_entry})
        return latex_encode(bibtex_entry)  # Encode special characters to LaTeX
    except Exception as e:
        return f"An error occurred: {e}"

# Function to save the conversation history to a file
def save_history_to_file(history):
    with open('history_with_abbr.json', 'w', encoding='utf-8') as f:
        json.dump(history, f)

# Function to load the conversation history from a file
def load_history_from_file():
    if os.path.exists('history_with_abbr.json'):
        with open('history_with_abbr.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def main_page_with_abbr():
    st.title('BibTeX with Journal Abbreviation')

    # Load settings
    settings = load_settings()
    current_model = settings["model"]

    # Main application interface
    current_history = load_history_from_file()

    with st.form("bib_form_with_abbr", clear_on_submit=True):
        user_input = st.text_area("Enter your reference here", height=300, key='user_input_with_abbr')
        submit_button = st.form_submit_button("Convert to BibTeX with Abbreviation")

    if submit_button and user_input:
        bibtex_output = get_bibtex_with_abbr(user_input, current_history, current_model)
        st.text_area("Editable BibTeX Output with Abbreviation", bibtex_output, height=300)  # Editable text area for output
        st.text("You can copy the BibTeX output below:")
        st.code(bibtex_output, language="plaintext")  # Non-editable code block for easy copying
        save_history_to_file(current_history)

    if st.button("Clear History with Abbr"):
        current_history.clear()
        save_history_to_file(current_history)

if __name__ == "__main__":
    main_page_with_abbr()
