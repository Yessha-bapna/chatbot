import streamlit as st
import requests
import subprocess
import os
import platform  

# Load your Groq API Key from .streamlit/secrets.toml
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# File extension mapping
EXTENSIONS = {
    "python": "py",
    "java": "java",
    "c++": "cpp",
    "c": "c",
    "javascript": "js",
    "html": "html",
    "bash": "sh"
}

# --- UI Setup ---
st.set_page_config(page_title="AutoCode AI", layout="centered")
st.markdown("""
    <style>
    .stChatMessage { padding: 0.5rem 1rem; border-radius: 12px; margin: 0.5rem 0; }
    .stChatMessage.user { background-color: #e8f0fe; text-align: right; }
    .stChatMessage.assistant { background-color: #f4f4f4; text-align: left; }
    .st-emotion-cache-1kyxreq { padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)



# --- Model Selection ---
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if not st.session_state.selected_model:
    model = st.selectbox("🔧 Choose a model:", [
        "llama3-8b-8192",
        "llama3-70b-8192"
    ])
    if st.button("Start Chat"):
        st.session_state.selected_model = model
        st.rerun()
    st.stop()

# --- Chat Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

system_prompt = {
    "role": "system",
    "content": "You are AutoCode Bot. Generate only the required code (no explanations, no comments unless asked). Detect the language from the prompt and respond only with clean code."
}

# --- Language Detection ---
def detect_language(text):
    text = text.lower()
    if "python" in text: return "python"
    if "java" in text: return "java"
    if "c++" in text: return "c++"
    if "c " in text: return "c"
    if "javascript" in text: return "javascript"
    if "html" in text: return "html"
    if "bash" in text or "shell" in text: return "bash"
    return "txt"

# --- Save and Open File ---


def save_and_open_file(code, lang):
    ext = EXTENSIONS.get(lang, "txt")
    filename = f"autocode_output.{ext}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    os_name = platform.system().lower()

    try:
        # Try VS Code first
        subprocess.Popen(["code", filename])
    except FileNotFoundError:
        try:
            if "windows" in os_name:
                subprocess.Popen(["notepad", filename])
            elif "darwin" in os_name:  # macOS
                subprocess.Popen(["open", "-a", "TextEdit", filename])
            elif "linux" in os_name:
                subprocess.Popen(["gedit", filename])
            else:
                st.warning("⚠️ Couldn't detect a suitable editor. Please open the file manually.")
        except Exception as e:
            st.warning(f"⚠️ Failed to open editor: {e}")


# --- Show Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
user_input = st.chat_input("Enter your coding task...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Generating your code..."):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": st.session_state.selected_model,
                    "messages": [system_prompt] + st.session_state.chat_history,
                    "temperature": 0.7
                }
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").markdown(reply)

                # Detect language and save code
                lang = detect_language(user_input)
                save_and_open_file(reply, lang)

            else:
                error_msg = f"⚠️ Error {response.status_code}: {response.text}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                st.chat_message("assistant").markdown(error_msg)

        except Exception as e:
            error = f"❌ An error occurred: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": error})
            st.chat_message("assistant").markdown(error)
