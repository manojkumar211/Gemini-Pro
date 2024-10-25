import streamlit as st
import os
import pandas as pd
import openpyxl as op
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

# Set the page configuration
st.set_page_config(page_title="Requirements")
st.header("Gemini LLM Model")

# User input and file uploader
input_text = st.text_input("Input:", key="input")
upload_file = st.file_uploader("Upload a file", type=['xlsx', 'docx', 'pdf'])
submit = st.button("Submit Here")

def get_gen_response(input_text, file_content):
    # Generate response based on input and file content
    if input_text:
        response = model.generate_content([input_text, file_content])
        return response.txt
    return None

def process_uploaded_file(upload_file):
    # Read the uploaded file and return its content as a string
    if upload_file.name.endswith('.xlsx'):
        df = op.load_workbook(upload_file)
        sheet = df.active
        data = []
        headers = [cell.value for cell in sheet[1]]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {headers[i]: row[i] for i in range(len(headers))}
            data.append(row_data)
        with open("C:/Projects/astria/xlsx_json", 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return df.to_json(orient='records')  # Return JSON string
    elif upload_file.name.endswith('.csv'):
        df = pd.read_csv(upload_file)
        return df.to_json(orient='records')  # Return JSON string
    elif upload_file.name.endswith('.docx'):
        from docx import Document
        doc = Document(upload_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    elif upload_file.name.endswith('.pdf'):
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(upload_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        st.error("Unsupported file format!")
        return None

# Handle submission
if submit:
    file_content = process_uploaded_file(upload_file)
    if file_content:
        response = get_gen_response(input_text, file_content)
        if response:
            st.subheader("The Final Answer")
            st.write(response)