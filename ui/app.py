# ui/app.py
import streamlit as st
import os
import sys

# Add the project root to python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.rag import GhostBrain

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
        # If there are images associated with this message, show them
        if "images" in message and message["images"]:
            cols = st.columns(len(message["images"]))
            for i, img_path in enumerate(message["images"]):
                with cols[i]:
                    st.image(img_path, caption=f"Evidence {i+1}", width=300)

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
            
            # 3. Show Evidence
            evidence_images = []
            if sources:
                st.markdown("---")
                st.caption("🔍 Source Evidence:")
                cols = st.columns(len(sources))
                for i, doc in enumerate(sources):
                    with cols[i]:
                        # Show some metadata
                        st.caption(f"Source: {doc['source'].upper()}")
                        
                        # If it's a screenshot, show it
                        if doc['source'] == 'screen' and os.path.exists(doc['filepath']):
                            st.image(doc['filepath'], use_container_width=True)
                            evidence_images.append(doc['filepath'])
                        elif doc['source'] == 'audio':
                            st.audio(doc['filepath'])
                            
            # Save to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text,
                "images": evidence_images
            })