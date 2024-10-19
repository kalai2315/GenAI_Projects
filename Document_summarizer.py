import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from PyPDF2 import PdfReader
import re
import string

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def summarize_text(text):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "summarize the document",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Please provide me with the document you would like summarized. I need the text of the document in order to provide a summary.\n",
                ],
            },
        ]
    )

    response = chat_session.send_message(text)
    return response.text

def preprocess_text(text):
    # Basic preprocessing: remove extra spaces, newlines, and special characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading and trailing whitespace
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def process_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]
    text = ""

    if file_type == 'txt':
        text = uploaded_file.getvalue().decode("utf-8")
    elif file_type == 'csv':
        df = pd.read_csv(uploaded_file)
        text = df.to_string()  # Convert DataFrame to string
    elif file_type == 'pdf':
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + " "  # Extract text from each page
    else:
        st.error("Unsupported file type. Please upload a txt, csv, or pdf file.")
    
    return text

# Streamlit main function to deploy the app
def main():
    st.title("Document Summarizer using Gemini Pro API")
    
    uploaded_file = st.file_uploader("Upload a Document (txt, csv, pdf)", type=["txt", "csv", "pdf"])
    
    if uploaded_file is not None:
        document_text = process_file(uploaded_file)
        
        # Clean and preprocess the text
        cleaned_document_text = preprocess_text(document_text)

        st.subheader("Original Document Text")
        st.write(cleaned_document_text)

        if st.button("Summarize Document"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(cleaned_document_text)
                st.subheader("Summarized Text")
                st.write(summary)

if __name__ == "__main__":
    main()
