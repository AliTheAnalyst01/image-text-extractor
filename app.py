from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load API Key from environment
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define function to get the model response
def get_gemini_response(input_prompt, image_data, user_input):
    # Use gemini-1.5-flash model instead of deprecated one
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Pass the prompt, image bytes, and user input to the model
    response = model.generate_content([input_prompt, image_data, user_input])
    
    return response.text

# Convert uploaded image file into bytes format
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()  # Get binary data from uploaded file
        image_parts = {
            'mime_type': uploaded_file.type,
            'data': image_bytes  # Get bytes data
        }
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')

# Streamlit UI setup
st.set_page_config(page_title='Gemini Image Text Extraction')
st.header("Gemini Image-Based Application")

# User text input
user_input = st.text_input('Enter text to extract from image', key="input")

# File uploader for the image
upload_file = st.file_uploader('Upload the image here', type=['jpg', 'jpeg', 'png'])

if upload_file is not None:
    # Open and display image
    image = Image.open(upload_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Button to trigger image processing
submit = st.button("Explain the image 👇")   

# The input prompt that guides the model on how to handle the process
input_prompt = """
You are a highly intelligent AI model tasked with reading and understanding text from images. Here's how you should handle the process:

Image Understanding: When an image is provided, use advanced Optical Character Recognition (OCR) techniques to accurately extract every detail of readable text from the image. This includes both printed and handwritten text, even in challenging image conditions.

Query-Based Text Extraction: After extracting the text, wait for a specific input or query from the user. This query may be a keyword, phrase, or question related to the text in the image. Your job is to search through the extracted text and find the exact or most relevant parts that match the user's input.

Precise Response: Once you identify the relevant portion of the text based on the query, return that specific information as the answer. Ensure the response is concise, accurate, and directly addresses the user’s query.

Fallback and Suggestions: If no matching text is found or if the query is unclear, provide a friendly response indicating that no relevant information was found. Suggest the user refine their query or check the image quality for better text extraction.

User-Friendly Output: Ensure that the final output is clear and easy to understand, with the option to display, download, or copy the relevant text as required by the user.
"""

# When the button is clicked, process the image and return the response
if submit and upload_file is not None:
    try:
        # Set up the image in the correct format (convert it to bytes)
        image_data = input_image_setup(upload_file)
        
        # Get the AI's response based on the image and user input
        response = get_gemini_response(input_prompt, image_data, user_input)
        
        # Display the response in the Streamlit app
        st.subheader('The response is:')
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
