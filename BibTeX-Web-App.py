# BibTeX-Web-App.py
import streamlit as st
import main_page
import BibTeX_abbr
import BibTeX_journal_abbr
import helpful_assistant  # Import the new page


# Configure Streamlit page settings as the first command
st.set_page_config(
    page_title="BiTeX",
    page_icon="🤖"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.title("🚦Navigation")
page = st.sidebar.radio("Go to", ["🌏Main Page", "⚙️Settings", "💥BibTeX with Journal Abbr", "🤝Helpful Assistant"])

if page == "🌏Main Page":
    main_page.main_page()
elif page == "⚙️Settings":
    BibTeX_abbr.settings_page()
elif page == "💥BibTeX with Journal Abbr":
    BibTeX_journal_abbr.main_page_with_abbr()
elif page == "🤝Helpful Assistant":
    helpful_assistant.helpful_assistant_page()
