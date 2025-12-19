import streamlit as st
from openai import OpenAI

# ----------------- API KEY (Streamlit Secrets) -----------------
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Patrika AI News Desk",
    layout="wide"
)

st.title("📰 Patrika AI News Rewriter")
st.caption("AI-powered Hindi Journalism Assistant")

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
    height=280
)

# ----------------- AI REWRITE -----------------
if st.button("🚀 Rewrite with AI"):
    if not news_text.strip():
        st.warning("❗ Bhai, pehle news paste karo")
    else:
        with st.spinner("🧠 Patrika AI Desk working..."):
            try:
                prompt = f"""
Tum Rajasthan Patrika ke senior Hindi editor ho.

Rules:
- Facts same rahen
- Bilkul naya likho
- Shuddh, professional Hindi
- Style: {tone}
- Length: {length}
- Headline + Article do
- Plagiarism free

Original News:
\"\"\"{news_text}\"\"\"

Output Format:
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
                st.error(f"❌ Error: {e}")

# ----------------- API KEY TEST -----------------
if st.button("🔑 Test API Key"):
    try:
        client.models.list()
        st.success("✅ API key valid & working")
    except Exception as e:
        st.error(f"❌ API issue: {e}")
