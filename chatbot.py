import streamlit as st
import requests
import subprocess
import os
import platform  
import base64
# Set up the page configuration
st.set_page_config(page_title="AutoCode AI", layout="wide")

st.markdown("""
    <style>
    /* Fonts and Reset */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f9f9fb;
        color: #333;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(to right, #6366F1, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }

    /* Chat Messages */
    .stChatMessage {
        padding: 0.75rem 1.2rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        transition: 0.2s ease-in-out;
    }
    .stChatMessage:hover {
        transform: scale(1.01);
    }
    .stChatMessage.user {
        background-color: #e0ecff;
        text-align: right;
    }
    .stChatMessage.assistant {
        background-color: #f1f5f9;
        text-align: left;
    }

    /* Input */
    .stTextInput>div>div>input {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #ccc;
    }

    /* Buttons & Select */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: bold;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }

    /* Scroll for chat container */
    .st-emotion-cache-1kyxreq {
        max-height: 75vh;
        overflow-y: auto;
        padding-bottom: 1rem;
    }

    /* Download button */
    .stDownloadButton {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load your Groq API Key from .streamlit/secrets.toml
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# File extension mapping
EXTENSIONS = {
     "python": "py",
    "cpp": "cpp",
    "c": "c",
    "java": "java",
    "javascript": "js",
    "html": "html",
    "text": "txt"
}

st.set_page_config(page_title="My Assistant", layout="centered")
st.markdown("""
    <style>
    .stChatMessage { padding: 0.5rem 1rem; border-radius: 12px; margin: 0.5rem 0; }
    .stChatMessage.user { background-color: #e8f0fe; text-align: right; }
    .stChatMessage.assistant { background-color: #f4f4f4; text-align: left; }
    .st-emotion-cache-1kyxreq { padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🤖 AutoCode AI </h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your personal code-writing assistant powered by LLMs</p>", unsafe_allow_html=True)



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
    if "cpp" in text: return "cpp"
    if "c " in text: return "c"
    if "javascript" in text: return "javascript"
    if "html" in text: return "html"
    if "bash" in text or "shell" in text: return "bash"
    return "txt"


# --- Save and Open File ---


def save_and_open_file(code, lang):
    ext = EXTENSIONS.get(lang, "txt")
    filename = f"autocode_output.{ext}"

    # Save the code to a file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    # Provide download link
    st.success(f"✅ Code file generated: `{filename}`")
    with open(filename, "rb") as file:
        file_data = file.read()
        b64 = base64.b64encode(file_data).decode()
        href = f'<a href="data:file/{ext};base64,{b64}" download="{filename}">📥 Click here to download your file</a>'
        st.markdown(href, unsafe_allow_html=True)


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
