import streamlit as st
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Partika News Rewriter",
    page_icon="📰",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>📰 Partika News Rewriter</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:gray;'>Editorial polishing tool for Hindi newspapers (No AI)</p>",
    unsafe_allow_html=True
)
st.divider()

# ---------------- RULE-BASED REWRITER ----------------
REMOVE_PHRASES = [
    "दरअसल", "वास्तव में", "बताया गया कि", "जानकारी के अनुसार",
    "सूत्रों के अनुसार", "आपको बता दें", "गौरतलब है कि"
]

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)

    for phrase in REMOVE_PHRASES:
        text = text.replace(phrase, "")

    text = text.replace("।।", "।")
    return text.strip()

def paragraphize(text):
    sentences = re.split(r'(?<=[।!?])\s+', text)

    paragraphs = []
    temp = []

    for i, s in enumerate(sentences, 1):
        temp.append(s)
        if len(temp) == 2:  # 2 sentences per paragraph (akhbaari style)
            paragraphs.append(" ".join(temp))
            temp = []

    if temp:
        paragraphs.append(" ".join(temp))

    return "\n\n".join(paragraphs)

def rewrite_news(raw):
    cleaned = clean_text(raw)
    final_news = paragraphize(cleaned)
    return final_news

# ---------------- LAYOUT ----------------
left, right = st.columns(2, gap="large")

with left:
    st.subheader("✍️ Raw News (Reporter Copy)")
    raw_news = st.text_area(
        "",
        height=380,
        placeholder="Reporter se aayi hui kच्ची खबर यहाँ paste करें..."
    )

with right:
    st.subheader("📰 Akhbaar-Ready Copy")
    output_box = st.empty()

# ---------------- ACTION ----------------
if st.button("🔄 Rewrite for Newspaper", use_container_width=True):
    if raw_news.strip() == "":
        st.warning("कृपया खबर paste करें।")
    else:
        rewritten = rewrite_news(raw_news)
        output_box.markdown(rewritten)

# ---------------- FOOTER ----------------
st.divider()
st.caption("© Internal Editorial Utility | Patrika Style | No AI Used")
