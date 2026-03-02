import streamlit as st
from google import genai
import uuid
import pandas as pd

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Gemini Sanskruti AI", page_icon="🪔", layout="wide")

# Custom CSS for Background and UI refinements
st.markdown("""
    <style>
    /* Full Page Background */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?q=80&w=2071&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .centered-title {
        text-align: center;
        color: #d35400;
        font-family: 'Garamond', serif;
        font-size: 3.8rem;
        font-weight: 800;
        margin-bottom: 30px;
    }

    /* Remove "Browse File" text and clean up uploader */
    div[data-testid="stFileUploader"] section {
        padding: 0;
        min-height: 0;
    }
    div[data-testid="stFileUploader"] label {
        display: none;
    }
    div[data-testid="stFileUploader"] div div {
        display: none;
    }

    /* Sidebar Tweaks */
    [data-testid="stSidebar"] {
        background-color: #fff9f0;
        border-right: 2px solid #e67e22;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
GEMINI_API_KEY = "Enter Google API Key:" 
client = genai.Client(api_key=GEMINI_API_KEY)

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

# --- 3. SIDEBAR: CHAT MANAGEMENT ---
with st.sidebar:
    st.title("🪔 Sanskruti AI")
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "New Session", "messages": []}
        st.session_state.active_chat_id = new_id
        st.rerun()

    st.divider()
    
    for chat_id in list(st.session_state.chat_sessions.keys()):
        col_name, col_del = st.columns([0.8, 0.2])
        with col_name:
            if st.button(f"💬 {st.session_state.chat_sessions[chat_id]['title'][:18]}", key=chat_id):
                st.session_state.active_chat_id = chat_id
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"del_{chat_id}"):
                del st.session_state.chat_sessions[chat_id]
                st.session_state.active_chat_id = None
                st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='centered-title'>Gemini Sanskruti AI</h1>", unsafe_allow_html=True)

if st.session_state.active_chat_id:
    active_id = st.session_state.active_chat_id
    current_chat = st.session_state.chat_sessions[active_id]

    # Chat Container for auto-scroll
    chat_container = st.container()

    with chat_container:
        for message in current_chat["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # --- 5. BOTTOM UI ---
    # Invisible File Uploader (Shortcut)
    uploaded_file = st.file_uploader("", type=['csv', 'txt'], label_visibility="collapsed", key="file_btn")
    
    # Main Prompt
    if prompt := st.chat_input("Ask anything..."):
        # Auto-scroll logic: add message to state
        if not current_chat["messages"]:
            current_chat["title"] = prompt[:20]

        current_chat["messages"].append({"role": "user", "content": prompt})
        
        file_context = ""
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                file_context = f"Data: {df.head(5).to_string()}"
            else:
                file_context = uploaded_file.read().decode("utf-8")

        # Get Gemini Response
        try:
            full_query = f"Context: {file_context}\n\nQuestion: {prompt}" if file_context else prompt
            response = client.models.generate_content(model="gemini-2.5-flash", contents=full_query)
            current_chat["messages"].append({"role": "assistant", "content": response.text})
            st.rerun() # Refresh to show new message and scroll down
        except Exception as e:
            st.error(f"API Error: {e}")
else:

    st.info("Namaste! Please select or create a chat to begin.")
