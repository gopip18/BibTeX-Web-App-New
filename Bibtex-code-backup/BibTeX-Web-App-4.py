import streamlit as st
import openai
import json
import os
from latex_encoder import latex_encode  # Import the function

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

# Function to get BibTeX format using ChatGPT
def get_bibtex(reference, conversation, model):
    conversation = trim_conversation(conversation, max_length=1500)  # Adjust max_length as needed

    if not any(msg.get('role') == 'system' for msg in conversation):
        conversation.insert(0, {"role": "system", "content": "You are an assistant trained to convert academic references into BibTeX format."})
    conversation.append({"role": "user", "content": reference})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=0.7,
            max_tokens=4096  # Adjust max_tokens if necessary
        )
        bibtex_entry = response.choices[0].message['content'].strip()
        conversation.append({"role": "assistant", "content": bibtex_entry})
        return latex_encode(bibtex_entry)  # Encode special characters to LaTeX
    except Exception as e:
        return f"An error occurred: {e}"

# Function to save the conversation history to a file
def save_history_to_file(history):
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f)

# Function to load the conversation history from a file
def load_history_from_file():
    if os.path.exists('history.json'):
        with open('history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Function to save settings to a file
def save_settings(settings):
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f)

# Function to load settings from a file
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"model": "gpt-3.5-turbo"}

def main():
    st.title('Bibliography Management System')

    # Load settings
    settings = load_settings()
    current_model = settings["model"]

    # Sidebar for updating the model
    st.sidebar.title("Settings")
    model_input = st.sidebar.text_input("ChatGPT Model:", value=current_model)
    if st.sidebar.button("Save Model"):
        settings["model"] = model_input
        save_settings(settings)
        st.sidebar.success("Model updated successfully!")

    # Main application interface
    current_history = load_history_from_file()

    with st.form("bib_form", clear_on_submit=True):
        user_input = st.text_area("Enter your reference here", height=300, key='user_input')
        submit_button = st.form_submit_button("Convert to BibTeX")

    if submit_button and user_input:
        bibtex_output = get_bibtex(user_input, current_history, model_input)
        st.text_area("Editable BibTeX Output", bibtex_output, height=300)  # Editable text area for output
        st.text("You can copy the BibTeX output below:")
        st.code(bibtex_output, language="plaintext")  # Non-editable code block for easy copying
        save_history_to_file(current_history)

    if st.button("Clear History"):
        current_history.clear()
        save_history_to_file(current_history)

if __name__ == "__main__":
    main()
