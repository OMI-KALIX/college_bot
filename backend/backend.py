from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import sqlite3
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import yaml
import os
import sentry_sdk

# Initialize FastAPI
app = FastAPI()

# Set up Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, etc.)
app.mount("/backend/static", StaticFiles(directory="college_bot/backend/static"), name="static")

# Serve index.html at root endpoint
@app.get("/")
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Initialize Sentry for error tracking
sentry_sdk.init(dsn="https://9de4cb18f67c30a7f12a911188d79356@o4508977391468544.ingest.us.sentry.io/4508977455759360", traces_sample_rate=1.0)

# SQLite Database Setup
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "chatbot.db")

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query: str
    rating: int

class FAQRequest(BaseModel):
    question: str
    answer: str

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE,
            rating INTEGER
        )
    """)
    conn.commit()
    conn.close()

setup_db()

def store_feedback(query, rating):
    """Store unanswered queries with a low rating (rating = 1)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Prevent duplicate unanswered queries
    cursor.execute("SELECT * FROM feedback WHERE query = ?", (query,))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("INSERT INTO feedback (query, rating) VALUES (?, ?)", (query, rating))
        conn.commit()

    conn.close()

# Load BERT model
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAQ Data from YAML
script_dir = os.path.dirname(os.path.abspath(__file__))
faq_file = os.path.join(script_dir, "data", "faqs.yaml")

def load_faqs():
    """Loads FAQs from YAML while preserving order."""
    if not os.path.exists(faq_file):
        raise FileNotFoundError(f"Error: FAQs file not found at {faq_file}. Please ensure it exists.")
    
    with open(faq_file, 'r', encoding='utf-8') as f:
        faqs_data = yaml.safe_load(f)

    return faqs_data.get("faqs", [])

# Load FAQs initially
faqs = load_faqs()
faq_questions = [q["question"] for q in faqs]
faq_answers = [q["answer"] for q in faqs]

# Initialize BM25 and TF-IDF
bm25 = BM25Okapi([q.lower().split() for q in faq_questions])
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(faq_questions)

# Compute BERT embeddings
faq_embeddings = bert_model.encode(faq_questions, convert_to_tensor=False, normalize_embeddings=True)
faq_embeddings = np.array(faq_embeddings, dtype=np.float32)

# FAISS Index
faiss_index = faiss.IndexFlatIP(faq_embeddings.shape[1])
faiss_index.add(faq_embeddings)

def get_best_match(user_query):
    """Finds the best match for a user query using FAISS, BM25, and TF-IDF."""
    faqs = load_faqs()
    faq_questions = [q["question"] for q in faqs]
    faq_answers = [q["answer"] for q in faqs]

    # Update BM25 and TF-IDF dynamically
    bm25 = BM25Okapi([q.lower().split() for q in faq_questions])
    tfidf_matrix = tfidf_vectorizer.fit_transform(faq_questions)

    # FAISS update
    faq_embeddings = bert_model.encode(faq_questions, convert_to_tensor=False, normalize_embeddings=True)
    faiss_index = faiss.IndexFlatIP(faq_embeddings.shape[1])
    faiss_index.add(np.array(faq_embeddings, dtype=np.float32))

    # Preprocess query
    user_query = user_query.strip().lower()

    # FAISS search
    query_embedding = bert_model.encode([user_query], convert_to_tensor=False, normalize_embeddings=True).astype(np.float32)
    faiss_distances, faiss_best_idxs = faiss_index.search(query_embedding, 3)
    faiss_best_idxs = faiss_best_idxs[0]
    faiss_confidences = faiss_distances[0]

    # BM25 search
    bm25_scores = bm25.get_scores(user_query.split())
    bm25_best_idxs = np.argsort(bm25_scores)[-3:][::-1]

    # TF-IDF search
    tfidf_query_vector = tfidf_vectorizer.transform([user_query])
    tfidf_similarities = np.dot(tfidf_matrix, tfidf_query_vector.T).toarray().flatten()
    tfidf_best_idx = np.argmax(tfidf_similarities)

    # Select best match
    best_idx = faiss_best_idxs[0]
    best_confidence = faiss_confidences[0]
    best_answer = faq_answers[best_idx]

    if bm25_scores[bm25_best_idxs[0]] > best_confidence:
        best_idx = bm25_best_idxs[0]
        best_confidence = bm25_scores[best_idx]
        best_answer = faq_answers[best_idx]

    if tfidf_similarities[tfidf_best_idx] > best_confidence:
        best_idx = tfidf_best_idx
        best_confidence = tfidf_similarities[best_idx]
        best_answer = faq_answers[best_idx]

    # Generate better suggestions
    suggestions = list(set([faq_questions[i] for i in faiss_best_idxs[1:]] + [faq_questions[i] for i in bm25_best_idxs[1:]]))

    # Store unanswered queries
    if best_confidence < 0.5:
        store_feedback(user_query, 1)
        best_answer = "I'm not sure. Did you mean: " + ", ".join(suggestions)

    return best_answer, float(best_confidence), suggestions

@app.post("/chatbot")
async def chatbot_api(request: QueryRequest):
    response, confidence, suggestions = get_best_match(request.query)
    return {"response": response, "confidence": confidence, "suggestions": suggestions}

@app.get("/unanswered")
async def get_unanswered_queries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT query FROM feedback WHERE rating = 1")
    data = cursor.fetchall()
    conn.close()
    return {"unanswered_queries": [row[0] for row in data]}

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            query = await websocket.receive_text()
            response, confidence, suggestions = get_best_match(query)
            await websocket.send_json({"response": response, "suggestions": suggestions})

    except WebSocketDisconnect:
        print("WebSocket Disconnected by Client")
    except Exception as e:
        print(f"Unexpected WebSocket Error: {e}")
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            print("WebSocket already closed, skipping close()")
# Run FastAPI Server
# uvicorn app1:app --host 127.0.0.1 --port 8000 --reload
