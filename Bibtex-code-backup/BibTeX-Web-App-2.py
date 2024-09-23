import streamlit as st
import openai
import json
import os

# Function to setup OpenAI API
def setup_openai():
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to get BibTeX format using ChatGPT
def get_bibtex(reference):
    prompt_text = f"Convert the following reference into a BibTeX entry:\n{reference}\n\n###\n\nBibTeX Entry:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant trained to convert academic references into BibTeX format."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3,
            max_tokens=250
        )
        bibtex_entry = response.choices[0].message['content'].strip()
        return bibtex_entry
    except Exception as e:
        return f"An error occurred: {e}"

# Save and load history functions
def save_history_to_file(history):
    with open('history.json', 'w') as f:
        json.dump(history, f)

def load_history_from_file():
    if os.path.exists('history.json'):
        with open('history.json', 'r') as f:
            return json.load(f)
    return []

# Main app function
def main():
    st.title('Bibliography Management System using ChatGPT')

    # Load history from file or initialize if not found
    current_history = load_history_from_file()

    # Use a form to submit new references
    with st.form("bib_form", clear_on_submit=True):
        # Text area for user to input reference, automatically cleared on submit
        user_input = st.text_area("Enter your reference here", height=300, key='user_input')
        submit_button = st.form_submit_button("Convert to BibTeX")

    if submit_button and user_input:
        bibtex_output = get_bibtex(user_input)
        # Display the output to history
        st.text_area("BibTeX Output", bibtex_output, height=300)
        # Append to history and save
        current_history.append({"input": user_input, "output": bibtex_output})
        save_history_to_file(current_history)

    # Button to clear the history
    if st.button("Clear History"):
        save_history_to_file([])  # Clear the history by resetting the file

if __name__ == "__main__":
    main()
