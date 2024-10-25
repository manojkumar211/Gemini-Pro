import streamlit as st
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")

# Set the page configuration
st.set_page_config(page_title="Requirements")
st.header("Gemini LLM Model")

# User input and file uploader
input_text = st.text_input("Input:", key="input")
upload_file = st.file_uploader("Upload a file", type=['xlsx', 'docx', 'pdf'])
submit = st.button("Submit Here")

def get_gen_response(input_text, upload_file):
    # Generate response based on input and file upload
    if input_text:
        response = model.generate_content([input_text, upload_file])
        return response.txt
    return None

def process_uploaded_file(upload_file):
    # Process the uploaded file and return JSON output
    if upload_file.name.endswith('.xlsx'):
        df = pd.read_excel(upload_file)
    elif upload_file.name.endswith('.csv'):
        df = pd.read_csv(upload_file)
    else:
        st.error("Unsupported file format!")
        return None
    
    # Convert DataFrame to JSON format
    json_output = df.to_json(orient='records')
    return json_output

# Handle submission
if submit:
    response = get_gen_response(input_text, upload_file)
    if response:
        st.subheader("The Final Answer")
        st.write(response)

# Process the uploaded file for JSON output
if upload_file is not None:
    json_data = process_uploaded_file(upload_file)
    
    if json_data:
        st.subheader("JSON Output:")
        st.json(json_data)