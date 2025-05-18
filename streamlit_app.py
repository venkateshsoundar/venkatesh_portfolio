# Streamlit Portfolio Chatbot with Digital Resume Template Enhancements
# Adapted from Sven-Bo/digital-resume-template-streamlit and customized with all sections

import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2
from time import sleep

# --- Page configuration ---
st.set_page_config(
    page_title="Venkatesh Portfolio", layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load resume bullets once ---
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    sents = [s.strip() for s in text.split('.') if len(s) > 50]
    return sents[:max_bullets]

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/"
    "venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
)
bullets = load_resume_bullets(resume_url)

# --- Global CSS ---
st.markdown(
    """
    <style>
    /* Cards and sections */
    .card { border: 1px solid #ddd; border-radius: 12px; padding: 20px; margin-bottom: 20px; background: #fff; transition: transform .2s; }
    .card:hover { transform: translateY(-5px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .section-title { font-size: 1.8em; border-bottom: 3px solid #4a90e2; padding-bottom: 4px; margin-bottom: 12px; }
    .profile-pic { border-radius: 50%; width: 150px; margin-bottom: 12px; }
    .card-img { width: 100%; border-radius: 8px; }
    .grid-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .hover-zoom:hover { transform: scale(1.05); }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar: Profile + Chat ---
with st.sidebar:
    st.markdown(
        "<img src='https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/profile.jpg' class='profile-pic' />",
        unsafe_allow_html=True
    )
    st.markdown("# Venkatesh Soundararajan")
    st.markdown("**M.S. Data Science & Analytics**")
    st.markdown("University of Calgary")
    st.markdown("---")
    st.markdown("## Contact")
    st.markdown("- 📧 youremail@example.com")
    st.markdown("- 🔗 [LinkedIn](https://www.linkedin.com/in/venkateshsoundar/)")
    st.markdown("- 💻 [GitHub](https://github.com/venkateshsoundar)")
    st.markdown("---")
    st.markdown("## Chat with Me 📋")
    if "history" not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        st.chat_message(role).write(msg)
    query = st.chat_input("Ask about my background or projects...")
    if query:
        st.session_state.history.append(("user", query))
        st.chat_message("user").write(query)
        # Build AI context
        system = [{"role":"system","content":"You are Venkatesh’s portfolio assistant. Cite [Resume] or [Projects]."}]
        resume_ctx = "Resume:\n" + "\n".join(f"- {b}" for b in bullets)
        proj_list = ["Quality of Life Analysis","Wildfire Analysis","Crime Drivers","Regression Analysis"]
        proj_ctx = "Projects:\n" + "\n".join(f"- {p}" for p in proj_list)
        msgs = system + [
            {"role":"system","content": resume_ctx},
            {"role":"system","content": proj_ctx},
            {"role":"user","content": query}
        ]
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=msgs)
        reply = resp.choices[0].message.content
        st.session_state.history.append(("assistant", reply))
        st.chat_message("assistant").write(reply)

# --- Main content ---
with st.container():
    # Welcome
    st.markdown("<div class='section-title'>Welcome</div>", unsafe_allow_html=True)
    st.markdown("Hello! I'm Venkatesh, a Data Science graduate student and analytics professional.")

    # Resume Highlights
    st.markdown("<div class='section-title'>Resume Highlights</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for b in bullets:
        st.markdown(f"- {b}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Experience
    st.markdown("<div class='section-title'>Experience</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    experiences = [
        "Quality Lead at Deloitte Consulting (8+ yrs)",
        "AWS ETL Pipeline Architect",
        "Agile Team Lead",
        "Insurance & Healthcare Risk Analytics"
    ]
    for exp in experiences:
        st.markdown(f"- {exp}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Skills
    st.markdown("<div class='section-title'>Skills</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    skills = [
        "Python, SQL, R",
        "AWS (S3, EC2, Lambda, SageMaker)",
        "Streamlit, Tableau, Power BI",
        "Scikit-learn, OpenCV, Flask",
        "Git, Jira, Agile"
    ]
    cols = st.columns(2)
    for i, skill in enumerate(skills):
        with cols[i % 2]:
            st.markdown(f"- {skill}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Education
    st.markdown("<div class='section-title'>Education</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**M.S. Data Science & Analytics**, University of Calgary, 2024-present")
    st.markdown("**B.S. Computer Science**, University of Mumbai, 2014-2018")
    st.markdown("</div>", unsafe_allow_html=True)

    # Certifications
    st.markdown("<div class='section-title'>Certifications</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    certs = [
        "AWS Certified Solutions Architect – Associate",
        "Tableau Desktop Specialist",
        "Certified Scrum Master"
    ]
    for cert in certs:
        st.markdown(f"- {cert}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Projects Showcase
    st.markdown("<div class='section-title'>Projects Showcase</div>", unsafe_allow_html=True)
    proj_map = {
        "Quality of Life Analysis": ("City income vs crime trends.", "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif", "https://github.com/venkateshsoundar/canadian-qol-analysis"),
        "Wildfire Analysis": ("Alberta wildfire pattern analysis.", "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif", "https://github.com/venkateshsoundar/alberta-wildfire-analysis"),
        "Crime Drivers": ("Mapping Toronto crime factors.", "https://media.giphy.com/media/26u4b45b8KlgAB7iM/giphy.gif", "https://github.com/venkateshsoundar/toronto-crime-drivers"),
        "Regression Analysis": ("Predicting weight change.", "https://media.giphy.com/media/xT0xezQGU5xCDJuCPe/giphy.gif", "https://github.com/venkateshsoundar/weight-change-regression")
    }
    st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
    for name, (desc, img, repo_url) in proj_map.items():
        st.markdown("<div class='card hover-zoom'>", unsafe_allow_html=True)
        st.markdown(
            f"<a href='{repo_url}' target='_blank'><img src='{img}' class='card-img' title='{desc}' /></a>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='card-title'><a href='{repo_url}' target='_blank' style='text-decoration:none;color:inherit'>{name}</a></div>"
            f"<p>{desc}</p>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
