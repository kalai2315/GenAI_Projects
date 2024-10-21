import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from io import StringIO

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the model with desired generation settings
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

# Function to summarize text
def summarize_text(text):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "summarize the document",
                ],
            },
        ]
    )
    
    response = chat_session.send_message(text)
    return response.text

# Streamlit app
def main():
    st.title("Document Summarizer")

    # Upload a document
    uploaded_file = st.file_uploader("Upload a Document (txt, csv)", type=["txt", "csv"])
    
    if uploaded_file is not None:
        # Read the document content
        file_content = uploaded_file.read().decode("utf-8")
        
        # Display original text
        st.subheader("Original Document Text")
        st.write(file_content)

        # Summarize the text
        if st.button("Summarize Document"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(file_content)
                st.subheader("Summarized Text")
                st.write(summary)

if __name__ == "__main__":
    main()
