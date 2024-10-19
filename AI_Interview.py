import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Create the model
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

# Function to start the interview simulation
def start_interview():
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "AI Job Interview Simulation with evaluation\n",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "## AI Job Interview Simulation: Data Scientist\n\n"
                    "**Role:** Data Scientist \n**Company:** InnovateTech (Fictional company specializing in AI-driven solutions for healthcare)\n"
                    "..."
                ],
            },
        ]
    )
    return chat_session

# Function to display possible interview questions
def add_interview_questions():
    """
    This function adds possible interview questions to the sidebar.
    It helps the user to get an idea of potential questions during a job interview simulation.
    """
    st.sidebar.title("Possible Interview Questions")
    
    interview_questions = [
        "1. Can you tell me about yourself?",
        "2. What interests you about working at this company?",
        "3. Describe a project where you used machine learning. What challenges did you face?",
        "4. How do you approach feature engineering?",
        "5. What metrics would you use to evaluate a model's performance?",
        "6. How would you handle missing or corrupted data?",
        "7. Explain the difference between supervised and unsupervised learning.",
        "8. What ethical considerations are important in AI?",
        "9. How do you stay updated on trends in AI?",
        "10. Do you have any questions for us?"
    ]
    
    for question in interview_questions:
        st.sidebar.write(question)

# Streamlit main function
def main():
    st.title("AI Job Interview Simulation")

    st.write("Prepare for your upcoming interviews by simulating a data science job interview with our AI assistant.")
    
    # Add interview questions to the sidebar
    add_interview_questions()

    # Start the interview session
    chat_session = start_interview()

    # User input for responses
    user_input = st.text_area("Your Response:", placeholder="Type your answer here...")
    
    if st.button("Send Response"):
        if user_input:
            with st.spinner("Processing..."):
                response = chat_session.send_message(user_input)
                st.subheader("AI Feedback:")
                st.write(response.text)
        else:
            st.warning("Please enter a response before submitting.")

if __name__ == "__main__":
    main()
