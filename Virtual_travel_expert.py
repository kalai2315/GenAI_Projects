import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set the page configuration for Streamlit
st.set_page_config(
    page_title="Virtual Travel Expert",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS for page styling
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        color: #2e86c1;
        text-align: center;
    }
    .fade-in {
        animation: fadeIn 2s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .stApp {
        background-image: url("https://your-image-link.com/background.jpg");
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Create the model configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Initialize the Gemini AI model
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Set initial chat history
chat_history = [
    {"role": "user", "parts": ["Virtual Travel Expert with gemini ai"]},
    {"role": "model", "parts": [
        "## Virtual Travel Expert with Gemini AI: A Guide \n\n"
        "**Gemini AI** has the potential to revolutionize the travel industry, "
        "offering an unparalleled level of personalization and efficiency to the travel experience. "
        "Here's how you can leverage Gemini AI's capabilities to create a virtual travel expert..."
    ]}
]

# Start a chat session with the model
chat_session = model.start_chat(history=chat_history)

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ("Home", "Itineraries", "Bookings"))

# Sidebar contact details
st.sidebar.markdown("### Contact Us")
st.sidebar.write("📧 Email: support@virtualtravelexpert.com")
st.sidebar.write("📞 Phone: +123 456 7890")

# Display content based on navigation selection
if option == "Home":
    # Title with custom font size and animation
    st.markdown('<h1 class="big-font fade-in">Welcome to the Virtual Travel Expert 🌍</h1>', unsafe_allow_html=True)
    
    # Custom button for interaction
    if st.button("Click Here to Start Planning!"):
        st.write("Let’s explore the world!")

    # Adding an image
    #image = Image.open("F:\Openai_chatgpt\travel_image.jpg")  # Replace with the actual path to your image
    #st.image(image, caption="Explore beautiful destinations with AI.")

    # Using columns for layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("📍 Destinations")
        st.write("Discover popular travel spots.")

    with col2:
        st.header("🏨 Hotels")
        st.write("Find the best places to stay.")

    with col3:
        st.header("✈️ Flights")
        st.write("Get the best flight deals.")

elif option == "Itineraries":
    st.write("Here are your itineraries!")
    
    # Input fields for personalized travel recommendations
    destination = st.text_input("Enter your preferred destination")
    budget = st.slider("Choose your budget ($)", 100, 5000)
    
    if st.button("Generate Itinerary"):
        if destination:
            st.write(f"Generating a custom itinerary for {destination} within a ${budget} budget!")
        else:
            st.write("Please enter a destination!")

else:
    st.write("Manage your bookings here.")
    
# Streamlit UI setup for chat functionality
st.title("Ask the Travel Expert")

# User input for interaction
user_input = st.text_input("Ask the travel expert anything:")

if st.button("Get Response"):
    if user_input:
        # Add user input to the chat history
        chat_history.append({"role": "user", "parts": [user_input]})

        # Send user message to the model and receive a response
        response = chat_session.send_message(user_input)
        
        # Add model's response to the chat history
        chat_history.append({"role": "model", "parts": [response.text]})
        
        # Display the model's response on the Streamlit app
        st.write(response.text)
    else:
        st.write("Please enter a question for the AI expert!")

# Footer for branding and additional styling
st.markdown("""
    <footer style="position:fixed;bottom:0;width:100%;text-align:center;padding:10px;background-color:#4CAF50;color:white;">
    <p>Powered by Virtual Travel Expert © 2024</p>
    </footer>
""", unsafe_allow_html=True)
