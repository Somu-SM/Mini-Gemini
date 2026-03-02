import streamlit as st
from google import genai
import uuid
import pandas as pd

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Gemini Sanskruti AI", page_icon="🪔", layout="wide")

# Corrected CSS for Background and UI Elements
st.markdown("""
    <style>
    /* Fixed Background Image Fix */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), 
                    url('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?q=80&w=2071&auto=format&fit=crop') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }
    
    .centered-title {
        text-align: center;
        color: #d35400;
        font-family: 'Garamond', serif;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
    }

    /* Hide the "Browse files" text and make it a small icon area */
    div[data-testid="stFileUploader"] section {
        padding: 0 !important;
        min-height: 40px !important;
        border: none !important;
        background: transparent !important;
    }
    div[data-testid="stFileUploader"] label { display: none !important; }
    div[data-testid="stFileUploader"] div div { display: none !important; }

    /* Sidebar Tweaks */
    [data-testid="stSidebar"] {
        background-color: #fff9f0;
        border-right: 2px solid #e67e22;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
GEMINI_API_KEY = "AIzaSyBSDSIVc4dkBO6msUSmWdfbt3HZE0ItdOU" 
client = genai.Client(api_key=GEMINI_API_KEY)

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if "rename_id" not in st.session_state:
    st.session_state.rename_id = None

# --- 3. SIDEBAR: CHAT MANAGEMENT WITH RENAME ---
with st.sidebar:
    st.title("🪔 Sanskruti AI")
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "New Session", "messages": []}
        st.session_state.active_chat_id = new_id
        st.rerun()

    st.divider()
    
    for chat_id in list(st.session_state.chat_sessions.keys()):
        # Layout for Rename and Delete
        col_name, col_ren, col_del = st.columns([0.6, 0.2, 0.2])
        
        with col_name:
            title = st.session_state.chat_sessions[chat_id]['title'][:15]
            if st.button(f"💬 {title}", key=f"sel_{chat_id}"):
                st.session_state.active_chat_id = chat_id
                st.rerun()
        
        with col_ren:
            if st.button("✏️", key=f"ren_{chat_id}"):
                st.session_state.rename_id = chat_id
        
        with col_del:
            if st.button("🗑️", key=f"del_{chat_id}"):
                del st.session_state.chat_sessions[chat_id]
                if st.session_state.active_chat_id == chat_id:
                    st.session_state.active_chat_id = None
                st.rerun()

    # Rename Logic
    if st.session_state.rename_id:
        new_name = st.text_input("Rename Chat:", key="rename_input")
        if st.button("Save Name"):
            st.session_state.chat_sessions[st.session_state.rename_id]['title'] = new_name
            st.session_state.rename_id = None
            st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='centered-title'>Gemini Sanskruti AI</h1>", unsafe_allow_html=True)

if st.session_state.active_chat_id:
    active_id = st.session_state.active_chat_id
    current_chat = st.session_state.chat_sessions[active_id]

    # Chat Display
    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- 5. BOTTOM UI: ICON LEFT & INPUT RIGHT ---
    st.divider()
    col_icon, col_box = st.columns([0.08, 0.52])

    with col_icon:
        # Minimalist Upload Icon Placement
        uploaded_file = st.file_uploader("", type=['csv', 'txt'], label_visibility="collapsed", key="file_btn")
        st.markdown("<h3 style='text-align:center; margin-bottom:-10px;'>📎</h3>", unsafe_allow_html=True)

    with col_box:
        prompt = st.chat_input("Ask anything...")

    # Logic
    if prompt:
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

        try:
            full_query = f"Context: {file_context}\n\nQuestion: {prompt}" if file_context else prompt
            response = client.models.generate_content(model="gemini-2.5-flash", contents=full_query)
            current_chat["messages"].append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"API Error: {e}")
else:
    st.info("Vanakkam 🙏  Please create a chat to begin.")