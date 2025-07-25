# 🎓 **CollegeBot – Smart AI-Powered Campus Assistant**  

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

## 🗂️ **Project Structure**

college_bot/
└── backend/
├── app2.py 👉 FastAPI server
├── admin/dashboard.py 👉 Admin dashboard logic
├── data/faqs.yaml 👉 FAQ knowledge base
├── database/chatbot.db 👉 SQLite database
├── static/ 👉 CSS & images
└── templates/ 👉 HTML pages

yaml
Copy
Edit

---

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
📂 Open your browser → http://localhost:8000

🧪 API Docs → http://localhost:8000/docs

💬 How It Works
User types a question

System searches the faqs.yaml

Best matching answer is returned

If no match found, fallback message is shown

Admin can update FAQs live with no restart

📘 Editing FAQs (YAML)
🗂️ backend/data/faqs.yaml

yaml
Copy
Edit
- question: What is the admission process?
  answer: Fill the form on the official site and submit required documents.

- question: How do I access the college Wi-Fi?
  answer: Contact the IT cell with your student ID.
✅ Just save the file — no need to restart the server.

🧠 AI & NLP Integration (Optional)
You can plug in advanced NLP tools for enhanced chatbot responses:

🧩 spaCy / NLTK for preprocessing

🔍 BM25 / FAISS / Transformers for semantic search

🤖 Ollama / GPT / LLaMA for natural dialogue

🧠 LangChain for chaining responses and context

🧪 Testing & Debugging
Use the Swagger UI for API testing:

bash
Copy
Edit
http://localhost:8000/docs
You can interact with all endpoints, view errors, and see request/response formats.

🌐 Frontend
index.html is the main chat UI

styles.css styles the chatbot

Use /static for images or theme changes

Easy to embed into your college website/portal

🎯 Future Plans
📌 Voice input (speech-to-text via Whisper)
📌 TTS output for accessibility
📌 Telegram/WhatsApp Bot support
📌 WebSocket chat (real-time)
📌 Student login & authentication
📌 College-specific API integration (attendance, timetable)

🛡️ License
📄 This project is licensed under the MIT License.
✅ You are free to use, modify, and share with attribution.

👨‍💻 Author
Made with 💙 by OMI-KALIX

⭐ Like this project?
Star the repo 🌟
Fork it 🔁
Improve it 💡
