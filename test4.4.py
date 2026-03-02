import streamlit as st
from google import genai
import uuid
import pandas as pd

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Gemini Sanskruti AI", page_icon="🪔", layout="wide")

# --- 2. THEME & CSS ---
# Initializing theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Dynamic CSS based on Light/Dark Toggle
bg_opacity = "0.75" if st.session_state.theme == "light" else "0.2"
text_color = "#d35400" if st.session_state.theme == "light" else "#ffcc00"
sidebar_bg = "#fff9f0" if st.session_state.theme == "light" else "#262730"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, {bg_opacity}), rgba(255, 255, 255, {bg_opacity})), 
                    url('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?q=80&w=2071&auto=format&fit=crop') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    .centered-title {{
        text-align: center;
        color: {text_color};
        font-family: 'Garamond', serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: -10px;
    }}

    /* Minimalist Small Uploader */
    div[data-testid="stFileUploader"] section {{
        padding: 0 !important;
        min-height: 30px !important;
        width: 40px !important; /* Resized to be small */
        border: none !important;
        background: transparent !important;
    }}
    div[data-testid="stFileUploader"] label {{ display: none !important; }}
    div[data-testid="stFileUploader"] div div {{ display: none !important; }}

    .portfolio-footer {{
        position: fixed;
        bottom: 10px;
        right: 30px;
        font-size: 0.85rem;
        font-weight: bold;
        background: rgba(255, 255, 255, 0.4);
        padding: 5px 12px;
        border-radius: 15px;
    }}

    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 2px solid #e67e22;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIALIZATION ---
GEMINI_API_KEY = "AIzaSyBSDSIVc4dkBO6msUSmWdfbt3HZE0ItdOU" 
client = genai.Client(api_key=GEMINI_API_KEY)

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

# --- 4. SIDEBAR: CHAT & TOGGLE ---
with st.sidebar:
    st.title("🪔 Sanskruti AI")
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "New Session", "messages": []}
        st.session_state.active_chat_id = new_id
        st.rerun()

    st.divider()
    
    # Scrollable Chat List
    for chat_id in list(st.session_state.chat_sessions.keys()):
        col_name, col_del = st.columns([0.8, 0.2])
        with col_name:
            if st.button(f"💬 {st.session_state.chat_sessions[chat_id]['title'][:15]}", key=f"sel_{chat_id}"):
                st.session_state.active_chat_id = chat_id
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"del_{chat_id}"):
                del st.session_state.chat_sessions[chat_id]
                st.rerun()

    # Sticky Bottom Toggle for Light/Dark Mode
    st.sidebar.markdown("---")
    mode = st.sidebar.toggle("🌙 Dark Mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if mode else "light"

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='centered-title'> Welcome to Gemini </h1>", unsafe_allow_html=True)

if st.session_state.active_chat_id:
    active_id = st.session_state.active_chat_id
    current_chat = st.session_state.chat_sessions[active_id]

    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- 6. BOTTOM UI: RESIZED ICON & INPUT ---
    st.write("---")
    col_icon, col_box = st.columns([0.05, 0.95]) # Tighter column for smaller icon

    with col_icon:
        uploaded_file = st.file_uploader("", type=['csv', 'txt'], label_visibility="collapsed", key="file_btn")
        st.markdown("<h4 style='text-align:center; margin-bottom:-5px;'>📎</h4>", unsafe_allow_html=True)

    with col_box:
        prompt = st.chat_input("Ask anything...")

    if prompt:
        if not current_chat["messages"]:
            current_chat["title"] = prompt[:20]

        current_chat["messages"].append({"role": "user", "content": prompt})
        
        file_context = ""
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                file_context = f"Data Sample: {df.head(5).to_string()}"
            else:
                file_context = uploaded_file.read().decode("utf-8")

        try:
            response = client.models.generate_content(model="gemini-2.5-flash", contents=f"{file_context}\n\n{prompt}")
            current_chat["messages"].append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("<div class='portfolio-footer'>Powered by Gemini 2.5 Flash | Somasundaram Portfolio</div>", unsafe_allow_html=True)
else:
    st.info("Namaste! Please select a chat to begin.")