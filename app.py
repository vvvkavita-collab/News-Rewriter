import streamlit as st
from openai import OpenAI

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Patrika AI News Desk",
    layout="wide"
)

st.title("📰 Patrika AI News Rewriter")
st.caption("AI-powered Hindi Journalism Assistant")

# ----------------- API KEY CHECK -----------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY Streamlit Secrets me set nahi hai")
    st.stop()

# IMPORTANT:
# sk-proj keys ke liye ye HI correct method hai
client = OpenAI()   # auto-reads OPENAI_API_KEY from secrets

# ----------------- CONTROLS -----------------
col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "✍ Writing Style",
        [
            "Neutral News",
            "Breaking News",
            "Investigative",
            "Editorial",
            "SEO Friendly"
        ]
    )

with col2:
    length = st.selectbox(
        "📏 Article Length",
        ["Short", "Medium", "Detailed"]
    )

news_text = st.text_area(
    "📝 Paste original news here",
    height=300
)

# ----------------- AI REWRITE -----------------
if st.button("🚀 Rewrite with AI"):
    if not news_text.strip():
        st.warning("❗ Bhai pehle news paste karo")
    else:
        with st.spinner("🧠 Patrika AI Desk kaam kar raha hai..."):
            try:
                prompt = f"""
Tum Rajasthan Patrika ke senior Hindi editor ho.

Rules:
- Facts bilkul same rahen
- Language: shuddh, professional Hindi
- Style: {tone}
- Length: {length}
- Headline + Article do
- Plagiarism free
- News publishing ready ho

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
                        {
                            "role": "system",
                            "content": "You are a professional Hindi news editor."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=900
                )

                st.subheader("📰 AI Rewritten News")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"❌ OpenAI Error: {e}")

# ----------------- API KEY TEST -----------------
st.divider()
if st.button("🔑 Test API Key"):
    try:
        client.models.list()
        st.success("✅ API key valid & working")
    except Exception as e:
        st.error(f"❌ API key issue: {e}")
