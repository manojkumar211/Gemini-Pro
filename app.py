import streamlit as st
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

genai.configure(api_key=os.getenv("GOOGLE_API_KRY"))


# Function to load Gemini Pro model and get responses

model=genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="requirements")
st.header("Gemini LLM model")
input=st.text_input("Input:",key="input")
upload_file = st.file_uploader("Upload a CSV file", type=['xlsx','docs','pdf'])
submit=st.button("submit here")

def get_gen(input,upload_file):
    if input!="":
        response=model.generate_content([input,upload_file])
    else:
        response=model.generate_content([input,upload_file])

    return response.txt

# Initiaize our streamlit app



if submit:
    response=get_gen([input,upload_file])
    st.subheader("The Final Answer")
    st.write(response)


def get_gen(upload_file):
    # Process the uploaded file (example: read a CSV)
    if upload_file.name.endswith(['.xlsx','.docs','.pdf']):
        df = pd.read_excel(upload_file)
    else:
        st.error("Unsupported file format!")
        return None
    
    # Example processing (returning as JSON)
    json_output = df.to_json(orient='records')
    return json_output

# Set the page configuration

# Title of the app
st.title("Upload a CSV File")

# File uploader


if upload_file is not None:
    # Call the function with the uploaded file
    json_data = get_gen(upload_file)
    
    if json_data:
        st.subheader("JSON Output:")
        st.json(json_data)