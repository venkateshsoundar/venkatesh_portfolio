import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide", initial_sidebar_state="expanded")

# --- Load resume bullets ---
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    sents = [s.strip() for s in text.split('.') if len(s) > 50]
    return sents[:max_bullets]

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
bullets = load_resume_bullets(resume_url)

# --- Global CSS ---
st.markdown("""
<style>
/* Always expand sidebar */
[aria-label="Toggle sidebar"] { visibility: hidden !important; }
/* Dark background and light text */
body { background-color: #121212; color: #e0e0e0; }
st-app .sidebar .sidebar-content { background-color: #1e1e1e; }
/* Section cards */
.card { background: #1e1e1e; border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
.card, .card * { color: #e0e0e0 !important; }
.section-title { font-size: 1.6rem; border-bottom: 3px solid #bb86fc; margin-bottom: 12px; color: #bb86fc; }
.profile-pic { border-radius: 50%; width: 150px; margin: 0 auto 12px; display: block; }
/* Chat bubbles */
.chat-bubble { padding: 8px 12px; border-radius: 12px; margin: 4px 0; animation: fade-in 0.4s ease; }
.user-msg { background: #333; text-align: right; }
.bot-msg { background: #444; text-align: left; }
@keyframes fade-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
/* Projects grid */
.grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.project-item { position: relative; overflow: hidden; border-radius: 12px; }
.project-item img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; transition: transform 0.3s ease; }
.project-item:hover img { transform: scale(1.1); }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; color: #fff; opacity: 0; transition: opacity 0.3s ease; font-size: 1.2rem; text-align: center; padding: 10px; }
.project-item:hover .overlay { opacity: 1; }
a { color: #bb86fc; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Profile and Chat ---
with st.sidebar:
    st.markdown("<img src='https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/profile.jpg' class='profile-pic'>", unsafe_allow_html=True)
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
    if 'history' not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        css_class = 'user-msg' if role == 'user' else 'bot-msg'
        st.markdown(f"<div class='chat-bubble {css_class}'>{msg}</div>", unsafe_allow_html=True)
    query = st.chat_input("Ask me anything about my background or projects...")
    if query:
        st.session_state.history.append(('user', query))
        # Send to API
        system = [{"role": "system", "content": "You are Venkatesh’s portfolio assistant. Cite [Resume] or [Projects]."}]
        resume_ctx = "Resume:\n" + "\n".join(f"- {b}" for b in bullets)
        proj_list = ["Quality of Life Analysis", "Wildfire Analysis", "Crime Drivers", "Regression Analysis"]
        proj_ctx = "Projects:\n" + "\n".join(f"- {p}" for p in proj_list)
        msgs = system + [{"role": "system", "content": resume_ctx}, {"role": "system", "content": proj_ctx}, {"role": "user", "content": query}]
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=msgs)
        reply = resp.choices[0].message.content
        st.session_state.history.append(('assistant', reply))
        st.experimental_rerun()

# --- Main content ---
container = st.container()
with container:
    # Sections
    sections = [
        ("Welcome", "<p>Hello! I'm Venkatesh, a Data Science graduate student and analytics professional.</p>"),
        ("Resume Highlights", "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"),
        ("Experience", "<ul>" + "".join(f"<li>{e}</li>" for e in ["Quality Lead at Deloitte Consulting (8+ yrs)", "AWS ETL Pipeline Architect", "Agile Team Lead", "Insurance & Healthcare Risk Analytics"]) + "</ul>"),
        ("Skills", "<ul>" + "".join(f"<li>{s}</li>" for s in ["Python, SQL, R", "AWS (S3, EC2, Lambda, SageMaker)", "Streamlit, Tableau, Power BI", "Scikit-learn, OpenCV, Flask", "Git, Jira, Agile"]) + "</ul>"),
        ("Education", "<p><strong>M.S. Data Science & Analytics</strong>, University of Calgary, 2024-present</p><p><strong>B.S. Computer Science</strong>, University of Mumbai, 2014-2018</p>"),
        ("Certifications", "<ul>" + "".join(f"<li>{c}</li>" for c in ["AWS Certified Solutions Architect – Associate", "Tableau Desktop Specialist", "Certified Scrum Master"]) + "</ul>")
    ]
    for title, html_content in sections:
        st.markdown(f"<div class='card'><div class='section-title'>{title}</div>{html_content}</div>", unsafe_allow_html=True)

    # Projects Showcase
    st.markdown("<div class='section-title'>Projects Showcase</div>", unsafe_allow_html=True)
    proj_map = {
        "Quality of Life Analysis": ("City income vs crime trends.", "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif", "https://github.com/venkateshsoundar/canadian-qol-analysis"),
        "Wildfire Analysis": ("Alberta wildfire pattern analysis.", "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif", "https://github.com/venkateshsoundar/alberta-wildfire-analysis"),
        "Crime Drivers": ("Mapping Toronto crime factors.", "https://media.giphy.com/media/26u4b45b8KlgAB7iM/giphy.gif", "https://github.com/venkateshsoundar/toronto-crime-drivers"),
        "Regression Analysis": ("Predicting weight change.", "https://media.giphy.com/media/xT0xezQGU5xCDJuCPe/giphy.gif", "https://github.com/venkateshsoundar/weight-change-regression")
    }
    st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
    for name, (desc, img, repo) in proj_map.items():
        st.markdown("<div class='project-item'>", unsafe_allow_html=True)
        st.markdown(f"<a href='{repo}' target='_blank'><img src='{img}' /><div class='overlay'>{name}</div></a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
