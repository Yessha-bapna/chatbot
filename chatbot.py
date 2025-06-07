# chatbot.py

import streamlit as st
import requests

import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set page layout
st.set_page_config(page_title="My Assistant", layout="centered")
st.markdown("""
    <style>
    .stChatMessage { padding: 0.5rem 1rem; border-radius: 12px; margin: 0.5rem 0; }
    .stChatMessage.user { background-color: #e8f0fe; text-align: right; }
    .stChatMessage.assistant { background-color: #f4f4f4; text-align: left; }
    .st-emotion-cache-1kyxreq { padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🤖 Your Personal AI Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose a model to start chatting</p>", unsafe_allow_html=True)

# Step 1: Ask user to choose model
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if not st.session_state.selected_model:
    model = st.selectbox("🔧 Choose a model:", [
        "llama3-8b-8192",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ])
    if st.button("Start Chat"):
        st.session_state.selected_model = model
        st.rerun()
    st.stop()

# Step 2: Initialize chat after model is selected
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": f"Hi! You're now chatting with `{st.session_state.selected_model}`. How can I help you today?"}]

# Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": st.session_state.selected_model,
                    "messages": st.session_state.chat_history,
                    "temperature": 0.7
                }
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").markdown(reply)
            else:
                error_msg = f"⚠️ Error {response.status_code}: {response.text}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                st.chat_message("assistant").markdown(error_msg)

        except Exception as e:
            error = f"❌ An error occurred: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": error})
            st.chat_message("assistant").markdown(error)