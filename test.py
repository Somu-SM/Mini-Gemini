import streamlit as st
import json
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- CONFIGURATION ---
GEMINI_API_KEY = "Enter Google API Key:"  # Replace with your actual key

# 1. Initialize the new GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Setup the Text Splitter (example settings)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

# --- APP LOGIC ---
st.title("Google Gemini Chatbot")

user_input = st.text_input("Ask me anything:")

if user_input:
    # 3. Use the new client syntax to generate a response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )

    st.write(response.text)
