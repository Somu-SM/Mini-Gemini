import streamlit as st
from google import genai
import uuid
import urllib.parse # For social media links

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gemini Sanskruti AI", page_icon="🪔", layout="wide")

# (Keep your existing CSS here)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🪔 Sanskruti AI")
    
    # Existing Chat Management Buttons...
    # [New Chat, Search, History list here]

    st.divider()
    
    # --- NEW: SHARE SECTION ---
    st.subheader("📢 Share this AI")
    app_url = "https://sanskruti-ai.streamlit.app" # You get this after Step 2
    
    # Create shareable links
    text_to_share = "Check out my Gemini Sanskruti AI Chatbot! 🪔"
    encoded_text = urllib.parse.quote(text_to_share)
    
    col_l, col_w = st.columns(2)
    with col_l:
        st.link_button("LinkedIn", f"https://www.linkedin.com/sharing/share-offsite/?url={app_url}")
    with col_w:
        st.link_button("WhatsApp", f"https://api.whatsapp.com/send?text={encoded_text}%20{app_url}")
    
    if st.button("📋 Copy App Link"):
        st.code(app_url) # Shows the link clearly for the user to copy
        st.success("Link ready to copy!")

# --- (Rest of your Main Interface code) ---