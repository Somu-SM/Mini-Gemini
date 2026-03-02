import streamlit as st
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBSDSIVc4dkBO6msUSmWdfbt3HZE0ItdOU"
client = genai.Client(api_key=GEMINI_API_KEY)

# --- CHAT STORAGE SETUP ---
# This initializes a list to store the conversation if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (Left Side Storage View) ---
with st.sidebar:
    st.title("Chat History")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Display previous questions as a list on the left
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write(f"🗨️ {msg['content'][:30]}...")

# --- MAIN INTERFACE ---
st.title("Welcome to Gemini")

# Display the "below by below" chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask me anything:"):
    # 1. Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get Response from Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash", # Or your preferred model
        contents=prompt
    )
    
    # 3. Add assistant response to state and display it
    full_response = response.text
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    with st.chat_message("assistant"):
        st.markdown(full_response)