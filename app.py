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
    ["Backend Engineer", "Frontend Engineer", "Data Scientist", "Machine Learning Engineer"]
)

# Generate button
if st.button("Generate Question"):
    with st.spinner("Thinking... 🤖"):
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": prompt_template.format(role=role)},
                {"role": "user", "content": f"Generate one technical coding interview question for a {role}."}
            ]
        )
        question = response.choices[0].message.content
        st.markdown("### 📌 Your Interview Question:")
        st.write(question)

