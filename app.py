# app.py

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import prompt_template

# Load .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit UI
st.title("🧠 Technical Interview Question Generator")
st.write("Generate AI-powered coding interview questions tailored to specific roles.")

# Role selector
role = st.selectbox(
    "Choose a job role:",
    [
        "Frontend Engineer (React)",
        "Backend Engineer (Node.js)",
        "ML Engineer (NLP)",
        "Data Scientist (Python)",
        "Data Analyst (SQL-heavy)"
    ]
)

# Category selector
category = st.selectbox(
    "Choose a question category:",
    ["General", "System Design", "Behavioral", "Data Structures", "SQL"]
)
import io
import base64

# Generate button
if st.button("Generate Question"):
    with st.spinner("Thinking... 🧠"):
        response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that creates technical interview questions based on job role and category."
        },
        {
            "role": "user",
            "content": prompt_template.format(role=role, category=category)
        }
    ],
    temperature=0.7
)


    question = response.choices[0].message.content
    st.markdown("### 🛠️ Your Interview Question:")
    st.write(question)
    st.code(question, language="markdown")
    st.button("📋 Copy to Clipboard", key="copy_btn")
    # ✅ CORRECT: only used after 'question' is created
def generate_download_link(text, filename):
    buffer = io.StringIO()
    buffer.write(text)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read().encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download as .txt</a>'
    return href

    st.markdown(generate_download_link(question, "interview_question.txt"), unsafe_allow_html=True)





# Answer input
user_answer = st.text_area("✍️ Your Answer", placeholder="Write your answer here...")

# Feedback button
if st.button("Get AI Feedback", key="feedback_btn"):
    if not question:
        st.warning("⚠️ Please generate a question before requesting feedback.")
    else:
        with st.spinner("Thinking... 🧠"):
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "Score and critique answers to interview questions."},
                    {"role": "user", "content": f"Candidate's answer: {user_answer}\n\nScore from 1 to 10 and give feedback."}
                ]
            )
            feedback = response.choices[0].message.content
            st.markdown("### 💬 Feedback on Your Answer:")
            st.write(feedback)

            session_log = f"""Interview Question:
{question}

Your Answer:
{user_answer}

AI Feedback:
{feedback}
"""
            st.markdown(generate_download_link(session_log, "interview_session.txt"), unsafe_allow_html=True)
import re

email = st.text_input("📧 Enter your email to receive this session (optional)")

if st.button("📨 Send to My Email"):
    if not email:
        st.warning("⚠️ Please enter an email address.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
        st.error("❌ Please enter a valid email address.")
    else:
        st.success(f"✅ Session will be sent to {email.strip()} (feature coming soon!)")
        file_name = f"{role}_{category}_session.txt".replace(" ", "_")
        import base64

# 1. Define the function first
def generate_download_link(content, filename):
    import base64
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📄 Download Question as .txt</a>'
    return href

# 2. Then use it later in the code
st.markdown(generate_download_link(question, "interview_question.txt"), unsafe_allow_html=True)





