from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import spacy

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get response from Gemini
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Function for tokenization and entity extraction using spaCy
def process_input(user_input):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_input)
    tokens = [token.text for token in doc]  # Tokenization
    entities = [(ent.text, ent.label_) for ent in doc.ents]  # Entity extraction
    return tokens, entities

# Initialize Streamlit app
st.set_page_config(page_title="Chatbot")
st.header("Customer Support Chatbot")

# Initialize session state for chat history
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Input field for user query
user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    # Process the user input for tokens and entities
    tokens, entities = process_input(user_input)
    #st.write("Tokens:", tokens)
    #st.write("Entities:", entities)

    # Get response from the Gemini model
    response = get_gemini_response(user_input)

    # Add user query and response to session state chat history
    st.session_state['conversation_history'].append(("You", user_input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['conversation_history'].append(("Bot", chunk.text))

# Display conversation history
st.subheader("Conversation History:")
for role, text in st.session_state['conversation_history']:
    st.write(f"{role}: {text}")
