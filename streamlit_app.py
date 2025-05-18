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

# 2) Global CSS for cards, shapes, padding, and animations
st.markdown(
    """
    <style>
    .card {
        border: 2px solid #eee;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 32px;
        background: #fafafa;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    }
    .card-title {
        font-size: 1.4em;
        font-weight: bold;
        margin-bottom: 12px;
        color: #333;
    }
    .card-img {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .section-shape {
        border-left: 8px solid #4a90e2;
        padding-left: 16px;
        margin-bottom: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3) Sidebar profile section
with st.sidebar:
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

# 4) Layout: two columns (main | chat sidebar)
col_main, col_chat = st.columns([3, 1])

with col_main:
    # Welcome Section
    st.markdown("<div class='section-shape'>", unsafe_allow_html=True)
    st.markdown("<div class='card'>## Welcome to my Portfolio</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Resume Highlights Section
    st.markdown("<div class='section-shape'>", unsafe_allow_html=True)
    st.markdown("<div class='card'>")
    st.subheader("Resume Highlights")
    @st.cache_data
    def load_resume_bullets(url, max_bullets=5):
        r = requests.get(url); r.raise_for_status()
        reader = PyPDF2.PdfReader(io.BytesIO(r.content))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
        sentences = [s.strip() for s in text.split('.') if len(s) > 50]
        return sentences[:max_bullets]
    bullets = load_resume_bullets(
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
    )
    for b in bullets:
        st.markdown(f"- {b}")
    st.markdown("</div>")
    st.markdown("</div>", unsafe_allow_html=True)

    # Experience Section
    st.markdown("<div class='section-shape'>", unsafe_allow_html=True)
    st.markdown("<div class='card'>")
    st.subheader("Experience")
    exp_list = [
        "8+ years as Quality Lead at Deloitte Consulting",
        "Developed and optimized ETL pipelines in AWS",
        "Led agile teams implementing data reporting solutions",
        "Conducted risk analytics for insurance and healthcare"
    ]
    for exp in exp_list:
        st.markdown(f"- {exp}")
    st.markdown("</div>")
    st.markdown("</div>", unsafe_allow_html=True)

    # Skills Section
    st.markdown("<div class='section-shape'>", unsafe_allow_html=True)
    st.markdown("<div class='card'>")
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
    st.markdown("</div>")
    st.markdown("</div>", unsafe_allow_html=True)

    # Projects Showcase in 2x2 grid with hover popups
    st.subheader("Projects Showcase")
    project_data = {
        "Quality of Life Analysis": ("A city-level analysis of income vs crime.", "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif"),
        "Wildfire Analysis": ("Exploring wildfire trends in Alberta.", "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif"),
        "Crime Drivers": ("Mapping factors driving crime in Toronto.", "https://media.giphy.com/media/26u4b45b8KlgAB7iM/giphy.gif"),
        "Regression Analysis": ("Predicting weight changes with regression.", "https://media.giphy.com/media/xT0xezQGU5xCDJuCPe/giphy.gif")
    }
    items = list(project_data.items())
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j, (name, (desc, img_url)) in enumerate(items[i:i+2]):
            with cols[j]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(
                    f"<img src='{img_url}' class='card-img' onmouseover=\"this.style.transform='scale(1.1)'\" onmouseout=\"this.style.transform='scale(1)'\" title='{desc}'/>",
                    unsafe_allow_html=True
                )
                st.markdown(f"<div class='card-title'>{name}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

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
        system_msgs = [{"role": "system", "content": "You are Venkatesh’s portfolio assistant. Cite [Resume] or [Projects]."}]
        resume_ctx = "Resume Summary:\n" + "\n".join(f"- {b}" for b in bullets)
        projects_ctx = "Projects:\n" + "\n".join(f"- {n}" for n in dict(project_data).keys())
        msgs = system_msgs + [
            {"role": "system", "content": resume_ctx},
            {"role": "system", "content": projects_ctx},
            {"role": "user", "content": user_q}
        ]
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=msgs)
        reply = resp.choices[0].message.content
        st.session_state.history.append(("assistant", reply))
        st.chat_message("assistant").write(reply)
