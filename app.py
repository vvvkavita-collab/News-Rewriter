# file: app.py
import streamlit as st
import os
from dotenv import load_dotenv
import openai

# ----------------- LOAD API KEY -----------------
# 1️⃣ Load from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 2️⃣ Alternative: direct key (testing only)
# api_key = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

if not api_key:
    st.error("API key load nahi hui. .env check karo ya direct key set karo")
    st.stop()

openai.api_key = api_key

# ----------------- STREAMLIT UI -----------------
st.set_page_config(page_title="Patrika News Rewriter", layout="wide")
st.title("📰 Patrika News Rewriter – Premium Edition")

user_input = st.text_area("Paste your news/article here:")

if st.button("Rewrite Article"):
    if not user_input.strip():
        st.warning("Please enter some text to rewrite.")
    else:
        try:
            with st.spinner("Rewriting..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional news writer."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=500
                )
                rewritten_text = response['choices'][0]['message']['content']
                st.subheader("Rewritten Article:")
                st.write(rewritten_text)
        except Exception as e:
            st.error(f"Error: {e}")

# ----------------- API KEY TEST BUTTON -----------------
if st.button("Test API Key"):
    try:
        models = openai.Model.list()
        st.success("API key valid ✅")
    except Exception as e:
        st.error(f"API key invalid ❌: {e}")
