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
    # Profile picture
    st.image(
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/profile.jpg",
        width=150
    )
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
st.markdown(
    """
    <style>
    @keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
    .blink-dots{display:inline-block;animation:blink 1s step-start infinite;}
    </style>
    """,
    unsafe_allow_html=True
)

# Layout: two columns (main content | chat sidebar)
col_main, col_chat = st.columns([3, 1])

# --- Main Column ---
with col_main:
    st.markdown("## Welcome to my Portfolio<span class='blink-dots'>...</span>", unsafe_allow_html=True)

    # Preload & summarize resume once
    @st.cache_data
    def load_resume_bullets(url, max_bullets=5):
        r = requests.get(url); r.raise_for_status()
        reader = PyPDF2.PdfReader(io.BytesIO(r.content))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
        sentences = [s.strip() for s in text.split('.') if len(s) > 50]
        return sentences[:max_bullets]

    resume_url = (
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/"
        "main/Venkateshwaran_Resume.pdf"
    )
    resume_bullets = load_resume_bullets(resume_url)

    # Resume Highlights
    st.subheader("Resume Highlights")
    for b in resume_bullets:
        st.markdown(f"- {b}")

    # Experience
    st.subheader("Experience")
    experience = [
        "8+ years as Quality Lead at Deloitte Consulting",
        "Developed and optimized ETL pipelines in AWS",
        "Led agile teams implementing data reporting solutions",
        "Conducted risk analytics for insurance and healthcare"
    ]
    for exp in experience:
        st.markdown(f"- {exp}")

    # Skills
    st.subheader("Skills")
    skills = [
        "Python, SQL, R", "AWS (S3, Lambda, EC2, SageMaker)",
        "Streamlit, Tableau, Power BI", "Scikit-learn, Prophet, OpenCV",
        "Git, Jira, Agile methodologies"
    ]
    cols_skills = st.columns(2)
    for idx, skill in enumerate(skills):
        with cols_skills[idx % 2]:
            st.markdown(f"- {skill}")

    # Projects Showcase
    st.subheader("Projects Showcase")
    project_data = {
        "Canadian Quality of Life Analysis": "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
        "Alberta Wildfire Analysis": "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif",
        "Toronto Crime Drivers": "https://media.giphy.com/media/26u4b45b8KlgAB7iM/giphy.gif",
        "Weight Change Regression Analysis": "https://media.giphy.com/media/xT0xezQGU5xCDJuCPe/giphy.gif",
        "Calgary Childcare Compliance": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "Social Media Purchase Influence": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
        "Obesity Level Estimation": "https://media.giphy.com/media/l0HlPjezlmQXJ5oXe/giphy.gif",
        "Weather Data Pipeline (AWS)": "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "California Wildfire Data Story": "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif",
        "Penguin Dataset Chatbot": "https://media.giphy.com/media/l0MYB8Ory7Hqefo9a/giphy.gif",
        "Uber Ride Duration Predictor": "https://media.giphy.com/media/3oEjHP8ELRNNlnlLGM/giphy.gif"
    }
    for name, img_url in project_data.items():
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(img_url, use_column_width=True)
        with cols[1]:
            st.markdown(f"**{name}**")
            st.markdown("A concise description of the project goes here. Add details to engage viewers.")
        st.markdown("---")

# --- Chat Sidebar Column ---
with col_chat:
    st.markdown("### Chat with Me")
    if "history" not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        st.chat_message(role).write(msg)
    user_q = st.chat_input("Ask me anything…")
    if user_q:
        st.session_state.history.append(("user", user_q))
        st.chat_message("user").write(user_q)
        system_msgs = [
            {"role": "system", "content":
             "You are Venkatesh’s portfolio assistant. Cite [Resume] or [Projects]."}
        ]
        resume_ctx = "Resume Summary:\n" + "\n".join(f"- {b}" for b in resume_bullets)
        projects_ctx = "Projects:\n" + "\n".join(f"- {p}" for p in project_data.keys())
        msgs = system_msgs + [
            {"role": "system", "content": resume_ctx},
            {"role": "system", "content": projects_ctx},
            {"role": "user", "content": user_q}
        ]
        client = OpenAI(base_url="https://openrouter.ai/api/v1",
                        api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=msgs
        )
        reply = resp.choices[0].message.content
        st.session_state.history.append(("assistant", reply))
        st.chat_message("assistant").write(reply)
