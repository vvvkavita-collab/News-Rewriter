import streamlit as st
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Partika News Rewriter",
    page_icon="📰",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>📰 Partika News Rewriter</h1>", unsafe_allow_html=True)
st.caption("Rule-based Heading + Subheading + Akhbaari Body | No AI")
st.divider()

REMOVE_PHRASES = [
    "दरअसल", "वास्तव में", "आपको बता दें", "गौरतलब है कि",
    "सूत्रों के अनुसार", "जानकारी के अनुसार"
]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text.strip())
    for p in REMOVE_PHRASES:
        text = text.replace(p, "")
    return text

def split_sentences(text):
    return re.split(r'(?<=[।!?])\s+', text)

def generate_headline(sentences):
    if not sentences:
        return ""
    headline = sentences[0]
    headline = re.sub(r'(है|था|थी|हुए|किया|किए)$', '', headline)
    words = headline.split()
    return " ".join(words[:10])

def generate_subheading(sentences):
    if len(sentences) > 1:
        return sentences[1]
    return ""

def build_body(sentences):
    body = []
    para = []
    for s in sentences[2:]:
        para.append(s)
        if len(para) == 2:
            body.append(" ".join(para))
            para = []
    if para:
        body.append(" ".join(para))
    return "\n\n".join(body)

def rewrite_news(raw):
    cleaned = clean_text(raw)
    sentences = split_sentences(cleaned)

    headline = generate_headline(sentences)
    subheading = generate_subheading(sentences)
    body = build_body(sentences)

    return headline, subheading, body

# ---------------- UI ----------------
left, right = st.columns(2, gap="large")

with left:
    st.subheader("✍️ Raw Reporter Copy")
    raw_news = st.text_area("", height=380, placeholder="Reporter se aayi raw news paste karein...")

with right:
    st.subheader("📰 Akhbaar Output")
    headline_box = st.empty()
    subheading_box = st.empty()
    body_box = st.empty()

if st.button("🔄 Rewrite for Akhbaar", use_container_width=True):
    if raw_news.strip() == "":
        st.warning("कृपया खबर paste करें।")
    else:
        h, sh, body = rewrite_news(raw_news)

        headline_box.markdown(f"## {h}")
        if sh:
            subheading_box.markdown(f"**{sh}**")
        body_box.markdown(body)

st.divider()
st.caption("© Editorial Desk Tool | Rule-based | No AI")
