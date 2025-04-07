from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import streamlit as st

# Load the enviromental variables (API Keys) from .env file
load_dotenv()

# Get the API key from the enviroment
key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=key)

# Function to perform Scene Understanding and extract text using Google Generative Ai
def image_to_text(image):
    
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

    prompt = """You are a helpful AI assistant for visually impared persons for their navigation.
                You will be given an image and you have to tell "What is it?" it in one line.
                if an only if, the content is an obstacle in walking or hazardous object,
                you have to warn in next line without giving any sentence heading."""
    
    response = model.generate_content([image, prompt])

    return response.text

# Text to Speach Function
def text_to_speach(text):
    tts = gTTS(text, lang='en')
    file_path = 'output/output.mp3'
    tts.save(file_path)
    return file_path


# Streamlit Interface
st.title('AI Support for Visually Impaired')
st.write('Upload an image to assist in scene understanding, text extraction, and text-to-speech.')

# Image Upload
uploaded_image = st.file_uploader("Upload an Image", type=['jpg', 'png', 'jpeg'])

# Create a button by the name "Process the Image"
btn_click = st.button("Process the Image", use_container_width=True)

if btn_click:
    col1, col2 = st.columns(2)

    with col1:
        # Display the Image
        image = Image.open(uploaded_image)
        st.image(image=image, caption='Uploaded Image')

    with col2:
        # Extract text from the given image
        image_text = image_to_text(image)
        st.write(image_text)

        # Convert the extracted text to speech and autoplay it.
        audio_path = text_to_speach(image_text)
        st.audio(audio_path, format="audio/mpeg", autoplay=True)