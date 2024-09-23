import streamlit as st
import openai
import json
import os
from latex_encoder import latex_encode  # Import the function

def setup_openai():
    openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_bibtex(reference, conversation):
    if not any(msg.get('role') == 'system' for msg in conversation):
        conversation.insert(0, {"role": "system", "content": "You are an assistant trained to convert academic references into BibTeX format."})
    conversation.append({"role": "user", "content": reference})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.3,
            max_tokens=500
        )
        bibtex_entry = response.choices[0].message['content'].strip()
        conversation.append({"role": "assistant", "content": bibtex_entry})
        return latex_encode(bibtex_entry)  # Encode special characters to LaTeX
    except Exception as e:
        return f"An error occurred: {e}"

def save_history_to_file(history):
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f)

def load_history_from_file():
    if os.path.exists('history.json'):
        with open('history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def main():
    st.title('Bibliography Management System')
    current_history = load_history_from_file()

    with st.form("bib_form", clear_on_submit=True):
        user_input = st.text_area("Enter your reference here", height=300, key='user_input')
        submit_button = st.form_submit_button("Convert to BibTeX")

    if submit_button and user_input:
        bibtex_output = get_bibtex(user_input, current_history)
        st.text_area("BibTeX Output", bibtex_output, height=500)
        save_history_to_file(current_history)

    if st.button("Clear History"):
        current_history.clear()
        save_history_to_file(current_history)

if __name__ == "__main__":
    main()
