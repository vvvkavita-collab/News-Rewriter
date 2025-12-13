import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Partika News Rewriter",
    page_icon="📰",
    layout="wide"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
.big-title {
    font-size: 36px;
    font-weight: 700;
}
.subtext {
    color: #6b7280;
    margin-bottom: 20px;
}
.box {
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 12px;
}
.output h2 {
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="big-title">📰 Partika News Rewriter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">AI-assisted Editorial Rewrite Tool (Desk Style)</div>', unsafe_allow_html=True)
st.divider()

# ---------------- API KEY ----------------
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.warning("⚠️ OpenAI API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### ✍️ Raw Reporter Copy")
    raw_text = st.text_area(
        "",
        height=420,
        placeholder="Paste reporter copy here (Hindi news text)..."
    )

with col2:
    st.markdown("### 🗞️ Akhbaar Output")
    output_placeholder = st.empty()

# ---------------- PROMPT FUNCTION ----------------
def rewrite_news(text):
    prompt = f"""
You are a senior Hindi newspaper sub-editor.

Rewrite the following reporter copy strictly for newspaper publication.

Rules:
- Do NOT add new facts, names, dates, numbers, or opinions
- Do NOT change the meaning
- Correct grammar and improve flow
- Remove repetition
- Keep tone neutral, factual, professional
- Use simple, clear Hindi (Akhbaari style)

Create output in EXACT format:

HEADLINE:
<One strong, crisp headline>

SUBHEADING:
<1–2 line standfirst summary>

BODY:
<Well-structured news body in paragraphs>

Reporter Copy:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# ---------------- BUTTON ----------------
st.divider()
if st.button("🔁 Rewrite for Akhbaar", use_container_width=True):
    if not raw_text.strip():
        st.warning("Please paste reporter copy.")
    else:
        with st.spinner("Rewriting in editorial style..."):
            result = rewrite_news(raw_text)

        # Parse output
        headline = ""
        subheading = ""
        body = ""

        if "HEADLINE:" in result:
            parts = result.split("SUBHEADING:")
            headline = parts[0].replace("HEADLINE:", "").strip()
            rest = parts[1].split("BODY:")
            subheading = rest[0].strip()
            body = rest[1].strip()

        with output_placeholder.container():
            st.markdown(f"## {headline}")
            st.markdown(f"**{subheading}**")
            st.markdown("---")
            st.markdown(body)
