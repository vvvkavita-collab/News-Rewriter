# file: app.py
import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# ----------------- LOAD API KEY -----------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API key missing. .env check karo")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------- STREAMLIT UI -----------------
st.set_page_config(
    page_title="Patrika AI News Desk",
    layout="wide"
)

st.title("📰 Patrika AI News Rewriter")
st.caption("AI-powered Hindi Journalism Assistant")

col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "✍ Writing Style",
        ["Neutral News", "Breaking News", "Investigative", "Editorial", "SEO Friendly"]
    )

with col2:
    length = st.selectbox(
        "📏 Article Length",
        ["Short", "Medium", "Detailed"]
    )

news_text = st.text_area(
    "📝 Paste original news here",
    height=250
)

# ----------------- AI REWRITE -----------------
if st.button("🚀 Rewrite with AI"):
    if not news_text.strip():
        st.warning("Text paste karo bhai 🙂")
    else:
        with st.spinner("AI Patrika Desk working..."):
            try:
                prompt = f"""
Tum Rajasthan Patrika ke senior Hindi editor ho.

Task:
- News ko bilkul naya likho
- Facts same rakho
- Language: Shuddh, professional Hindi
- Style: {tone}
- Length: {length}
- Plagiarism free
- Headline bhi do

Original News:
\"\"\"{news_text}\"\"\"

Output format:
Headline:
<Headline>

Article:
<Article>
"""

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional Hindi news editor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=900
                )

                result = response.choices[0].message.content

                st.subheader("📰 AI Rewritten News")
                st.write(result)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ----------------- API KEY TEST -----------------
if st.button("🔑 Test API Key"):
    try:
        client.models.list()
        st.success("✅ API key valid & working")
    except Exception as e:
        st.error(f"❌ API issue: {e}")
