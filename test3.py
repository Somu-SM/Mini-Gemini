import streamlit as st
from google import genai
import uuid
import pandas as pd

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Gemini Sanskruti AI", page_icon="🪔", layout="wide")

# Custom CSS for Indian Culture Theme & Layout
st.markdown("""
    <style>
    /* Background & Global Styles */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), 
                    url('https://www.transparenttextures.com/patterns/mandala.png');
        background-size: contain;
    }
    .centered-title {
        text-align: center;
        color: #e67e22; /* Saffron */
        font-family: 'Georgia', serif;
        font-size: 3.5rem;
        font-weight: bold;
        margin-top: -20px;
        text-shadow: 2px 2px #fdf2e9;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #fdf2e9;
        border-right: 3px solid #e67e22;
    }
    .upload-footer {
        font-size: 0.85rem;
        color: #666;
        text-align: center;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
GEMINI_API_KEY = "Enter Google API Key:" # Replace with your actual key
client = genai.Client(api_key=GEMINI_API_KEY)

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {} # {id: {title, messages}}
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

# --- 3. SIDEBAR: CHAT MANAGEMENT ---
with st.sidebar:
    st.title("🪔 CHAT MANAGEMENT")
    
    if st.button("➕ New Journey", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "New Chat", "messages": []}
        st.session_state.active_chat_id = new_id
        st.rerun()

    st.divider()
    search_term = st.text_input("🔍 Search History", "").lower()
    
    # List Chats with Rename and Delete
    for chat_id in list(st.session_state.chat_sessions.keys()):
        chat_data = st.session_state.chat_sessions[chat_id]
        if search_term in chat_data["title"].lower():
            col_msg, col_ren, col_del = st.columns([0.6, 0.2, 0.2])
            
            with col_msg:
                if st.button(f"💬 {chat_data['title'][:15]}", key=f"btn_{chat_id}", use_container_width=True):
                    st.session_state.active_chat_id = chat_id
                    st.rerun()
            
            with col_ren:
                if st.button("✏️", key=f"ren_{chat_id}"):
                    # Simple prompt-based rename for this version
                    st.session_state.rename_target = chat_id
            
            with col_del:
                if st.button("🗑️", key=f"del_{chat_id}"):
                    del st.session_state.chat_sessions[chat_id]
                    if st.session_state.active_chat_id == chat_id:
                        st.session_state.active_chat_id = None
                    st.rerun()

    # Rename Input (shows only when pencil is clicked)
    if "rename_target" in st.session_state:
        new_name = st.text_input("Enter new name:")
        if st.button("Confirm Rename"):
            st.session_state.chat_sessions[st.session_state.rename_target]["title"] = new_name
            del st.session_state.rename_target
            st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='centered-title'>Gemini Sanskruti AI</h1>", unsafe_allow_html=True)

if st.session_state.active_chat_id:
    active_id = st.session_state.active_chat_id
    current_chat = st.session_state.chat_sessions[active_id]

    # Display Chat History
    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- 5. BOTTOM SECTION: UPLOAD & INPUT ---
    st.write("---")
    
    # File Upload (Bottom)
    uploaded_file = st.file_uploader("Upload CSV/TXT for context", type=['csv', 'txt'], label_visibility="collapsed")
    file_content = ""
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            file_content = f"\nData from file:\n{df.head(10).to_string()}"
        else:
            file_content = f"\nFile Content:\n{uploaded_file.read().decode('utf-8')}"
        st.caption(f"✅ Loaded: {uploaded_file.name}")

    # Chat Input
    if prompt := st.chat_input("Start typing your question..."):
        # Update title if it's the first message
        if not current_chat["messages"]:
            current_chat["title"] = prompt[:20]

        # 1. Show User Message
        current_chat["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Get Gemini Response (using 2.5 Flash)
        with st.chat_message("assistant"):
            try:
                # Include file content in the hidden prompt if available
                full_prompt = f"{file_content}\n\nUser Question: {prompt}" if file_content else prompt
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                
                st.markdown(response.text)
                current_chat["messages"].append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
    st.markdown("<p class='upload-footer'>🪔 Powered by Gemini 2.5 Flash | Somasundaram Portfolio</p>", unsafe_allow_html=True)

else:

    st.info("Pranam! Click '➕ New Journey' in the sidebar to begin your conversation.")
