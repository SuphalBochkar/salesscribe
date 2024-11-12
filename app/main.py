import streamlit as st
from datetime import datetime
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import time

def typingPrint(text):
    placeholder = st.empty()  # Create a placeholder to update the text
    typed_text = ""  # Empty string to hold the characters
    for character in text:
        typed_text += character
        placeholder.markdown(f"<h1 style='text-align: right font-weight: 700;'>{typed_text}</h1>", unsafe_allow_html=True)
        time.sleep(0.05)  # Simulate typing delay

def create_streamlit_app(llm, portfolio, clean_text):
    col1, col2 = st.columns([0.7, 0.4])
    with col1:
        st.title("🛒🛍️ SalesScribe AI")
    with col2:
        typingPrint("Let AI Lead the Way!")  # Use the typingPrint function

    url_input = st.text_input("Enter a URL:", placeholder="Enter a valid URL to generate a cold email")
    submit_button = st.button("Submit")

    if submit_button:
        if url_input:
            try:
                # Load data from the input URL
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                # Process each job to extract details and generate email
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')

            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()

    st.set_page_config(layout="wide", page_title="🛒🛍️ SalesScribe AI", page_icon="🛒🛍️")

    create_streamlit_app(chain, portfolio, clean_text)
