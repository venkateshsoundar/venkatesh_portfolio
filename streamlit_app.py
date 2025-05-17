import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2
import re
from time import sleep

# --- Page config ---
st.set_page_config(page_title="Portfolio Chatbot", layout="centered")

# --- Blinking dots CSS (only inject once) ---
if 'css_loaded' not in st.session_state:
    st.markdown("""
    <style>
    @keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
    .blink-dots{display:inline-block;animation:blink 1s step-start infinite;}
    </style>
    """, unsafe_allow_html=True)
    st.session_state.css_loaded = True

# --- Sidebar Info ---
st.sidebar.title("Controls & Info")
# Reset chat
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.history = []
    st.experimental_rerun()

# Display resume bullets
st.sidebar.subheader("Resume Highlights")
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return [f"Error loading resume: {e}"]
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    sentences = [s.strip() for s in text.split('.') if len(s) > 50]
    return sentences[:max_bullets]

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_bullets = load_resume_bullets(resume_url)
for b in resume_bullets:
    st.sidebar.markdown(f"- {b}")

# Display project list
st.sidebar.subheader("Projects List")
projects = [
    "Canadian Quality of Life Analysis",
    "Alberta Wildfire Analysis",
    "Toronto Crime Drivers",
    # ... other projects
]
for p in projects:
    st.sidebar.markdown(f"- {p}")

# --- Build base messages ---
system_messages = [
    {"role":"system","content":"You are Venkatesh’s portfolio assistant. Answer concisely and cite your source: [Resume] or [Projects]."}
]
resume_ctx = "Resume Summary:\n" + "\n".join(f"- {b}" for b in resume_bullets)
projects_ctx = "Projects:\n" + "\n".join(f"- {p}" for p in projects)
base_messages = system_messages + [
    {"role":"system","content": resume_ctx},
    {"role":"system","content": projects_ctx},
]

# --- Initialize chat history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Header with blink effect ---
st.markdown(f"## Welcome to my Portfolio<span class='blink-dots'>...</span>", unsafe_allow_html=True)

# --- Render history ---
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

# --- User input ---
user_q = st.chat_input("Ask me anything about my background or projects…")
if user_q:
    st.session_state.history.append(("user", user_q))
    st.chat_message("user").write(user_q)

    # Call API within spinner and streaming
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
    msgs = base_messages + [{"role":"user","content": user_q}]
    reply_text = ""
    try:
        with st.spinner("Thinking..."):
            # streaming response
            stream = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=msgs,
                stream=True
            )
            assistant_msg = st.chat_message("assistant")
            for chunk in stream:
                token = chunk.choices[0].delta.get('content', '')
                assistant_msg.write(token, end="")
                reply_text += token
                sleep(0.02)
    except Exception as e:
        st.error(f"⚠️ API Error: {e}")
        reply_text = f"Error: {e}"

    # Post-process citations
    reply_text = re.sub(r"\[Resume\]", f"**[Resume]({resume_url})**", reply_text)
    project_link = "https://github.com/venkateshsoundar"
    reply_text = re.sub(r"\[Projects\]", f"**[Projects]({project_link})**", reply_text)

    # Save history
    st.session_state.history.append(("assistant", reply_text))
