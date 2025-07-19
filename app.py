import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import prompt_template
import base64

# Load .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("🧠 Technical Interview Question Generator")
st.write("Generate AI-powered coding interview questions tailored to specific roles.")

# Role and category selectors
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

category = st.selectbox(
    "Choose a question category:",
    ["General", "System Design", "Behavioral", "Data Structures", "SQL"]
)

# Generate question
if st.button("Generate Question"):
    with st.spinner("Thinking... 🧠"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates technical interview questions based on job role and category."},
                {"role": "user", "content": prompt_template.format(role=role, category=category)}
            ],
            temperature=0.7
        )
        st.session_state.question = response.choices[0].message.content

# Display question if exists
if "question" in st.session_state:
    question = st.session_state.question
    st.markdown("### 🛠️ Your Interview Question:")
    st.write(question)
    st.code(question, language="markdown")

    # Download link
    def generate_download_link(text, filename):
        b64 = base64.b64encode(text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Question</a>'
        return href

    st.markdown(generate_download_link(question, "interview_question.txt"), unsafe_allow_html=True)

    # Answer submission and feedback
    st.markdown("### ✍️ Your Answer")
    user_answer = st.text_area("Write your answer here:", height=200)

    if st.button("Get AI Feedback", key="feedback_btn"):
        if not user_answer.strip():
            st.warning("⚠️ Please write an answer before submitting.")
        else:
            with st.spinner("Reviewing your answer... 🤖"):
                feedback_prompt = f"""You are an expert interviewer. Here is a question: "{question}".
The candidate answered: "{user_answer}".
Please give feedback on their technical quality, structure, and communication. Rate from 1 to 10 and suggest improvements."""
                feedback_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a technical interviewer providing constructive feedback."},
                        {"role": "user", "content": feedback_prompt}
                    ],
                    temperature=0.7
                )
                feedback = feedback_response.choices[0].message.content
                st.markdown("### 🧑‍⚖️ Interviewer Feedback:")
                st.write(feedback)

# Email capture (optional future use)
st.markdown("---")
email = st.text_input("📬 Enter your email to save this session (feature coming soon)")
if email and st.button("Save Session"):
    st.success(f"✅ Session will be sent to {email.strip()} (feature coming soon!)")
