# ui/app.py
import streamlit as st
import os
import sys

# Add the project root to python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.rag import GhostBrain
from src.utils.encryption import decrypt_data
from config import Config

st.set_page_config(page_title="Ghost-OS", page_icon="👻", layout="wide")

# Custom CSS for that "Hacker/Cyberpunk" look
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #00FF00;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

st.title("👻 Ghost-OS // Recall")

# Initialize Brain
if 'brain' not in st.session_state:
    st.session_state.brain = GhostBrain()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Ask about your digital history..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI Response
    with st.chat_message("assistant"):
        with st.spinner("Accessing Neural Memory..."):
            response_text, sources = st.session_state.brain.ask(prompt)
            
            st.markdown(response_text)
            
            # 3. Show Evidence (with decryption)
            if sources:
                st.markdown("---")
                st.caption("🔍 Source Evidence:")
                # Limit the number of columns to avoid overcrowding
                cols = st.columns(min(len(sources), 4)) 
                for i, doc in enumerate(sources):
                    with cols[i % 4]:
                        st.caption(f"Source: {doc['source'].upper()}")
                        
                        filepath = doc.get('filepath')
                        if filepath and os.path.exists(filepath):
                            try:
                                with open(filepath, 'rb') as f:
                                    encrypted_data = f.read()
                                
                                # Decrypt data before displaying
                                decrypted_data = decrypt_data(encrypted_data)

                                if doc['source'] == 'screen':
                                    st.image(decrypted_data, use_container_width=True)
                                elif doc['source'] == 'audio':
                                    st.audio(decrypted_data)
                            except Exception as e:
                                st.error(f"Could not display evidence: {e}")
                            
            # Save response to history (simplified: not re-displaying evidence)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text,
            })