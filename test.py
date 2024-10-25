import json
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API key
genai.configure(api_key="AIzaSyDQfOqzMq5syEPdjvuAbP2ffN7V0SNBIOA")  # Use env variable for safety

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="Requirements")
st.header("Gemini LLM Model")

# User input and file uploader
input_text = st.text_input("Input:", key="input")
upload_file = st.file_uploader("Upload a file", type='pdf')
submit = st.button("Submit Here")

def get_gen_response(input_text, headers, contents):
    # Generate response based on input and content
    if input_text:
        combined_input = f"{input_text}\nHeaders: {headers}\nContents: {contents}"
        response = model.generate_content([combined_input])
        return response.content  # Access the correct attribute for generated content
    return None

def process_uploaded_file(upload_file):
    if upload_file.name.endswith('.pdf'):
        pdf_reader = PdfReader(upload_file)
        structured_data = []

        # Extract text from each page
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                lines = text.splitlines()
                current_header = None

                for line in lines:
                    # Assuming headers are lines that start with a capital letter and are not empty
                    if line.strip() and line[0].isupper():  
                        # If we encounter a header, save the previous content
                        if current_header is not None:
                            structured_data.append({"header": current_header, "content": current_content})

                        current_header = line.strip()
                        current_content = ""  # Reset current content
                    else:
                        if current_header is not None:
                            current_content += line.strip() + " "  # Append to current content

                # Add the last header-content pair
                if current_header is not None:
                    structured_data.append({"header": current_header, "content": current_content})

        # Write the structured data to a JSON file
        json_file_path = "C:/Projects/astria/files/pdf_new_json.json"  # Specify the correct JSON file path
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(structured_data, json_file, indent=4)

        return structured_data  # Return structured data for further processing
    else:
        st.error("The uploaded file is not a PDF.")
        return None

if submit:
    structured_data = process_uploaded_file(upload_file)
    if structured_data:
        headers = [item['header'] for item in structured_data]
        contents = [item['content'] for item in structured_data]
        response = get_gen_response(input_text, headers, contents)
        if response:
            st.subheader("The Final Answer")
            st.write(response)
