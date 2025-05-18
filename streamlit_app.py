# Streamlit Portfolio Chatbot
# Source: https://github.com/venkateshsoundar/venkatesh_portfolio/blob/main/streamlit_app.py

import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2
from time import sleep

# 1) Page config
st.set_page_config(page_title="Portfolio Chatbot", layout="wide")

# 2) Sidebar profile section
with st.sidebar:
    # Profile picture (replace with your image URL or local file)
    st.image("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/profile.jpg", width=150)
    st.markdown("# Venkatesh Soundararajan")
    st.markdown("**M.S. in Data Science & Analytics**")
    st.markdown("University of Calgary")
    st.markdown("---")
    st.markdown("**Contact**")
    st.markdown("- Email: youremail@example.com")
    st.markdown("- LinkedIn: [venkateshsoundar](https://www.linkedin.com/in/venkateshsoundar/)")
    st.markdown("- GitHub: [venkateshsoundar](https://github.com/venkateshsoundar)")
    st.markdown("---")

# 3) Blinking dots CSS
st.markdown("""
<style>
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.blink-dots{display:inline-block;animation:blink 1s step-start infinite;}
</style>
""", unsafe_allow_html=True)
st.markdown("## Welcome to my Portfolio<span class='blink-dots'>...</span>", unsafe_allow_html=True)

# 4) Preload & summarize resume once
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url); r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    sentences = [s.strip() for s in text.split(".") if len(s)>50]
    return sentences[:max_bullets]

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_bullets = load_resume_bullets(resume_url)

# 5) Predefine your project list
projects = [
    "Canadian Quality of Life Analysis",
    "Alberta Wildfire Analysis",
    "Toronto Crime Drivers",
    "Weight Change Regression Analysis",
    "Calgary Childcare Compliance",
    "Social Media Purchase Influence",
    "Obesity Level Estimation",
    "Weather Data Pipeline (AWS)",
    "California Wildfire Data Story",
    "Penguin Dataset Chatbot",
    "Uber Ride Duration Predictor"
]

# 6) Build base messages once
system_messages = [
    {"role":"system","content":"You are Venkatesh’s portfolio assistant. Answer concisely and cite your source: [Resume] or [Projects]."}
]
resume_ctx = "Resume Summary:\n" + "\n".join(f"- {b}" for b in resume_bullets)
projects_ctx = "Projects:\n" + "\n".join(f"- {p}" for p in projects)
base_messages = system_messages + [
    {"role":"system","content": resume_ctx},
    {"role":"system","content": projects_ctx},
]

# 7) Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# 8) Render history
for r, m in st.session_state.history:
    st.chat_message(r).write(m)

# 9) Get input
user_q = st.chat_input("Ask me anything about my background or projects…")
if user_q:
    st.session_state.history.append(("user", user_q))
    st.chat_message("user").write(user_q)

    # 10) Call API with minimal context
    msgs = base_messages + [{"role":"user","content": user_q}]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
    resp = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=msgs
    )
    reply = resp.choices[0].message.content

    st.session_state.history.append(("assistant", reply))
    st.chat_message("assistant").write(reply)
