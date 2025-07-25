🎓 CollegeBot – Smart AI-Powered Campus Assistant

CollegeBot is an intelligent, modular chatbot system designed for colleges and universities. It helps students and staff access instant answers to academic questions, navigate campus resources, and streamline information flow using a beautiful, fast web interface.

📌 Features
🤖 AI Chatbot with FastAPI backend

📚 Dynamic FAQ System using YAML (easily updatable)

📊 Admin Dashboard to manage data and logs

💬 Natural Language Input processing

🗂 SQLite Database for persistent chat logging

🌐 Simple Web UI built with HTML + CSS

🧩 Easy to integrate with college websites or portals

🔄 Modular, maintainable structure with support for expansion

🗂️ Project Structure
bash
Copy
Edit
college_bot/
├── backend/
│   ├── app2.py                # Main FastAPI server
│   ├── admin/dashboard.py     # Admin tools
│   ├── data/faqs.yaml         # FAQ knowledge base
│   ├── database/chatbot.db    # SQLite DB
│   ├── static/                # CSS, images
│   └── templates/             # HTML templates
├── manual.txt                 # Setup instructions

🚀 Getting Started
🔧 Requirements
Python 3.11+

FastAPI

Uvicorn

SQLite3

YAML

Optional: Jinja2, pydantic, langchain (if using AI features)

⚙️ Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/OMI-KALIX/college_bot.git
cd college_bot/2_college_bot/with_api_bot_more_efficient/backend
Create virtual environment & install packages

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
Run the FastAPI app

bash
Copy
Edit
uvicorn app2:app --reload
Open in browser
Visit: http://localhost:8000

✨ Usage
Visit the homepage

Ask questions in natural language

The system matches against FAQs and responds

FAQs are dynamically loaded from faqs.yaml

Admin can monitor and update answers via dashboard.py

📘 FAQ Format (YAML)
You can edit backend/data/faqs.yaml like this:

yaml
Copy
Edit
- question: What is the admission process?
  answer: You need to fill out the online application on the college portal.

- question: How to access the library?
  answer: Use your student ID to log in at library.famt.ac.in.
Just restart the app to load changes—no retraining needed.

🧠 AI Integration (Optional)
Easily plug in LLMs (like Ollama, GPT, etc.) for natural conversation

Preprocess queries with tools like spaCy or NLTK

Customize response ranking using BM25, CrossEncoder, or FAISS

📸 Frontend Preview
Simple, mobile-friendly interface with input field and chat display.
Built using HTML, CSS, and Jinja2 templates.
Assets located in /static and /templates.

🧪 Testing & Debugging
Logs are printed in console (uvicorn)

Test API via: http://localhost:8000/docs (Swagger UI)

🛠️ Future Enhancements
Admin Panel UI

Real-time chat over WebSocket

Voice-to-text (Whisper) + Text-to-speech

Notification & scheduling module

WhatsApp or Telegram integration

Multi-language support

📝 License
MIT License — free to use, modify, and distribute.

🙋‍♂️ Author
Developed by OMI-KALIX
📌 GitHub: OMI-KALIX
