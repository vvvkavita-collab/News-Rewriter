import streamlit as st
import re

st.set_page_config(page_title="Partika News Rewriter", page_icon="📰", layout="wide")

st.markdown("<h1 style='text-align:center;'>📰 Partika News Rewriter</h1>", unsafe_allow_html=True)
st.caption("Rule-based Editorial Tool (Max Possible Without AI)")
st.divider()

GRAMMAR_FIXES = {
    "बढ़ती फूड कल्चर": "बदलता फूड कल्चर",
    "ही शहर के": "शहर के",
    "कर रहा है": "किया जा रहा है",
    "कर रही है": "की जा रही है",
}

def apply_grammar_fixes(text):
    for wrong, right in GRAMMAR_FIXES.items():
        text = text.replace(wrong, right)
    return text

def clean_lines(text):
    lines = [l.strip("–- ") for l in text.split("\n") if l.strip()]
    return list(dict.fromkeys(lines))  # remove duplicates

def generate_headline(lines):
    base = lines[0]
    base = re.sub(r"(ने|का|की|के|है|थे).*", "", base)
    words = base.split()
    return " ".join(words[:8])

def rewrite(raw):
    lines = clean_lines(raw)
    lines = [apply_grammar_fixes(l) for l in lines]

    headline = generate_headline(lines)
    subheading = lines[1] if len(lines) > 1 else ""

    body_sentences = []
    for line in lines[2:]:
        body_sentences += re.split(r'(?<=[।])\s+', line)

    body = []
    para = []
    for s in body_sentences:
        para.append(s)
        if len(para) == 2:
            body.append(" ".join(para))
            para = []
    if para:
        body.append(" ".join(para))

    return headline, subheading, "\n\n".join(body)

left, right = st.columns(2, gap="large")

with left:
    raw = st.text_area("✍️ Raw Reporter Copy", height=380)

with right:
    h_box = st.empty()
    sh_box = st.empty()
    body_box = st.empty()

if st.button("🔄 Rewrite for Akhbaar", use_container_width=True):
    if raw.strip():
        h, sh, body = rewrite(raw)
        h_box.markdown(f"## {h}")
        sh_box.markdown(f"**{sh}**")
        body_box.markdown(body)
    else:
        st.warning("कृपया खबर paste करें।")

st.divider()
st.caption("Editorial Desk Tool | No AI | Rule-based")
