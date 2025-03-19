import streamlit as st
import sqlite3
import os
import yaml
import pandas as pd
import plotly.express as px

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "chatbot.db")
FAQ_FILE = os.path.join(BASE_DIR, "..", "data", "faqs.yaml")

# Ensure Database & Tables Exist
def ensure_database():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            rating INTEGER NOT NULL
        );
    ''')

    conn.commit()
    conn.close()

# Fetch all feedback
def fetch_feedback(min_rating=0):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback WHERE rating <= ?", (min_rating,))
    data = cursor.fetchall()
    conn.close()
    return data

# Delete feedback entry
def delete_feedback(feedback_id):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
    conn.commit()
    conn.close()

# Load FAQs
def load_faqs():
    if not os.path.exists(FAQ_FILE):
        return []
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("faqs", [])

# Save FAQs
def save_faqs(faqs):
    with open(FAQ_FILE, "w", encoding="utf-8") as f:
        yaml.dump({"faqs": faqs}, f, allow_unicode=True,default_flow_style=False)

# Add new FAQ
def add_faq(question, answer):
    faqs = load_faqs()
    faqs.append({"question": question, "answer": answer})
    save_faqs(faqs)

# Streamlit UI
st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("📊 Chatbot Admin Dashboard")

# ✅ Section 1: Filter & Review Feedback
st.header("📢 User Feedback & Filtering")
feedback_data = fetch_feedback(1)

if feedback_data:
    for row in feedback_data:
        with st.expander(f"Query: {row[1]} | Rating: ⭐ {row[2]}"):
            if st.button("❌ Delete", key=f"delete_{row[0]}"):
                delete_feedback(row[0])
                st.warning("Feedback deleted!")
                st.rerun()
else:
    st.info("No low-rated feedback found.")

# ✅ Section 2: Unanswered Queries → FAQs
st.header("🔍 Unanswered Queries (Low Ratings)")
low_rated_feedback = fetch_feedback(1)

if low_rated_feedback:
    for query in low_rated_feedback:
        with st.expander(f"Unanswered: {query[1]}"):
            answer = st.text_area(f"Answer for: {query[1]}", key=f"answer_{query[0]}")
            if st.button("✅ Add to FAQs & Resolve", key=f"resolve_{query[0]}"):
                add_faq(query[1], answer)
                delete_feedback(query[0])
                st.success("FAQ Updated & Query Resolved!")
                st.rerun()
else:
    st.info("✅ No unanswered questions!")

# ✅ Section 3: View Existing FAQs
st.header("📖 Manage FAQs")
faqs = load_faqs()
if faqs:
    for i, faq in enumerate(faqs):
        with st.expander(f"🔹 {faq['question']}"):
            new_question = st.text_input("Edit Question", value=faq["question"], key=f"q_{i}")
            new_answer = st.text_area("Edit Answer", value=faq["answer"], key=f"a_{i}")
            if st.button("💾 Save Changes", key=f"save_{i}"):
                faqs[i] = {"question": new_question, "answer": new_answer}
                save_faqs(faqs)
                st.success("FAQ Updated!")
                st.rerun()
else:
    st.info("No FAQs found!")

# ✅ Section 4: Add New FAQ
st.header("➕ Add New FAQ")
new_question = st.text_input("Question")
new_answer = st.text_area("Answer")
if st.button("Add FAQ"):
    add_faq(new_question, new_answer)
    st.success("FAQ Added Successfully!")
    st.rerun()

# ✅ Section 5: User Feedback Analytics
st.header("📊 User Feedback Analytics")
feedback_data = fetch_feedback()

if feedback_data:
    df = pd.DataFrame(feedback_data, columns=["ID", "Query", "Rating"])
    
    # Rating Distribution Chart
    st.subheader("⭐ Feedback Rating Distribution")
    fig = px.histogram(df, x="Rating", nbins=5, title="Distribution of User Ratings", labels={"Rating": "User Rating"})
    st.plotly_chart(fig)

    # Most Common Queries
    st.subheader("🔎 Most Common Queries")
    common_queries = df["Query"].value_counts().reset_index()
    common_queries.columns = ["Query", "Count"]
    st.dataframe(common_queries.head(10))

else:
    st.info("No feedback data available.")
