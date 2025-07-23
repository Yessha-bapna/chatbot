
# AutoCode AI 🤖

Your personal code-writing assistant powered by LLMs, built using [Streamlit](https://streamlit.io/). This assistant helps you generate code in various programming languages like Python, C++, Java, and more using Groq's LLaMA3 model.

## 🌐 Live Demo
Check out the deployed app here: [https://autocode-bot.streamlit.app](https://autocode-bot.streamlit.app)

---

## 📁 Project Structure

```
chatbot/
├── chatbot.py          # Main Streamlit app
├── .env                # Environment file storing GROQ API Key
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (you are here)
```

---

## 🚀 Features

- Multi-language code generation (Python, Java, C++, etc.)
- Easy-to-use Streamlit UI
- Powered by LLaMA3 via Groq API
- Downloadable generated code files
- Supports interactive conversations for coding help

---

## 🛠️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Yessha-bapna/chatbot.git
cd chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root folder (`chatbot/`) and add your [Groq API key](https://console.groq.com/keys) as follows:

```
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Make sure you never share your `.env` file or commit it to public repositories.

---

## ▶️ Running the App Locally

```bash
streamlit run chatbot.py
```

Once the app launches, you can select the model (`llama3-8b-8192` or any other), click "Start Chat", and begin entering your coding queries.

---

## ✍️ Example Prompts

```
✅ Write a Python code to add two numbers.
✅ Give me a Java function for bubble sort.
✅ Provide a C++ program to reverse a string.
```

---

## 📦 Deployment

This app is currently deployed at **[https://autocode-bot.streamlit.app](https://autocode-bot.streamlit.app)** using **Streamlit Community Cloud**.

To deploy your own version:

1. Push the project to a GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in.
3. Click on "New App", connect your repo, and deploy!
4. Make sure to set `GROQ_API_KEY` in the Secrets tab.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) for blazing-fast LLM APIs.
- [Meta](https://ai.meta.com/llama/) for LLaMA3 models.
- [Streamlit](https://streamlit.io) for UI framework.

---

Enjoy building with AutoCode AI 💻✨
