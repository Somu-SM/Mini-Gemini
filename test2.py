import streamlit as st
from google import genai
import uuid

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gemini Sanskruti AI", layout="wide")

# --- CUSTOM CSS (Indian Culture Theme) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #fdfaf6;
        background-image: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                          url('https://www.transparenttextures.com/patterns/mandala.png');
    }
    section[data-testid="stSidebar"] {
        background-color: #f8f1e5;
        border-right: 2px solid #d4a373;
    }
    .stChatInput { border-color: #d4a373; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION & CLIENT ---
GEMINI_API_KEY = "Enter Google API Key:"
client = genai.Client(api_key=GEMINI_API_KEY)

# --- SESSION STATE ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {"Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

# --- SIDEBAR: NEW CHAT & SEARCH ---
with st.sidebar:
    st.title("🪷 Sanskruti AI")
    if st.button("➕ New Chat"):
        new_id = f"Chat {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[new_id] = []
        st.session_state.current_chat = new_id
    
    st.divider()
    st.write("### Your Conversations")
    for chat_name in st.session_state.sessions.keys():
        if st.button(chat_name, key=chat_name):
            st.session_state.current_chat = chat_name

# --- MAIN INTERFACE ---
st.title(f"✨ {st.session_state.current_chat}")

# File Uploader
uploaded_file = st.file_uploader("Upload a document for analysis", type=['pdf', 'csv', 'txt'])

# Display current chat history
for msg in st.session_state.sessions[st.session_state.current_chat]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask about Indian culture or analyze your file..."):
    # Append User Message
    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini Response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):

        st.markdown(response.text)
