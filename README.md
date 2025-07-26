# 🎓 **CollegeBot – Smart AI-Powered Campus Assistant**  

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> _An intelligent chatbot system designed for universities and colleges, built with FastAPI and a dynamic FAQ system._

---

## 📌 **Features**

✔️ `AI Chatbot` with FastAPI  
✔️ `Live Web UI` for users to chat easily  
✔️ `Dynamic FAQ System` (editable YAML)  
✔️ `Admin Dashboard` for control  
✔️ `Chat Logging` via SQLite  
✔️ `Modular Backend` for future expansion  
✔️ `Easy Deployment` (Local or Cloud)

---

## ⚙️ Project Structure

```
college_bot/
└── backend/
    ├── app2.py               # ▶ FastAPI Server with NLP logic
    ├── admin/dashboard.py    # ▶ Streamlit Admin Panel
    ├── data/faqs.yaml        # ▶ Editable FAQ knowledge base
    ├── database/chatbot.db   # ▶ SQLite chat logs & feedback
    ├── static/               # ▶ CSS, icons
    └── templates/index.html  # ▶ Web UI for chatbot


```

## 🚀 **Getting Started**

### 🔧 Requirements

- ✅ Python `3.11+`  
- ✅ `FastAPI`, `Uvicorn`, `PyYAML`, `Jinja2`  
- ✅ SQLite3  
- ✅ (Optional) LangChain, spaCy, FAISS

---

### ⚙️ Installation

```bash
git clone https://github.com/OMI-KALIX/college_bot.git
cd 2_college_bot/with_api_bot_more_efficient/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app2:app --reload
```
## 🛡️ License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

📄 This project is licensed under the MIT License.  
✅ You are free to:
- Use
- Modify
- Share 

*(with attribution)*

## 👨‍💻 Author

**OMKAR SAWANT**  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?logo=github)](https://github.com/OMI-KALIX)

Made with 💙 by OMI-KALIX  
> For collaboration or deployment inquiries - contact via GitHub!
