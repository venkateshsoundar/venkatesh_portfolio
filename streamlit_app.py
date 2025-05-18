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
[aria-label=\"Toggle sidebar\"] { visibility: hidden !important; }
/* Dark background and light text */
body { background-color: #121212; color: #e0e0e0; }
.stApp .sidebar-content { background-color: #1e1e1e; }
/* Section cards with colorful gradients */
.card {
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  color: #e0e0e0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: linear-gradient(135deg, #FF6B6B, #FFD93D);
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.6);
}
.card * { color: #121212 !important; }
.section-title {
  font-size: 1.6rem;
  margin-bottom: 12px;
  padding-bottom: 4px;
  border-bottom: 3px solid #4ECDC4;
  color: #4ECDC4;
}
.profile-pic {
  border-radius: 50%;
  width: 150px;
  margin: 0 auto 12px;
  display: block;
}
/* Chat bubbles */
.chat-bubble { padding: 8px 12px; border-radius: 12px; margin: 4px 0; animation: fade-in 0.4s ease; }
.user-msg { background: #4ECDC4; text-align: right; color:#121212; }
.bot-msg { background: #FFD93D; text-align: left; color:#121212; }
@keyframes fade-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
/* Projects grid */
.grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.project-item { position: relative; overflow: hidden; border-radius: 12px; }
.project-item img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; transition: transform 0.3s ease; }
.project-item:hover img { transform: scale(1.05); filter: brightness(1.1); }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(78, 205, 196, 0.7); display: flex; align-items: center; justify-content: center; color: #121212; opacity: 0; transition: opacity 0.3s ease; font-size: 1.2rem; text-align: center; padding: 10px; }
.project-item:hover .overlay { opacity: 1; }
a { color: #FF6B6B; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)

# --- Sidebar: Profile Only ---
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
    # sidebar fixed, no chat here

# --- Main content with Right Chat Column ---
col_main, col_chat = st.columns([3,1])
with col_main:
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
        st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
        for name, (desc, img, repo) in proj_map.items():
            st.markdown("<div class='project-item'>", unsafe_allow_html=True)
            st.markdown(f"<a href='{repo}' target='_blank'><img src='{img}' /><div class='overlay'>{name}</div></a>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with col_chat:
    st.markdown("### Chat with Me 📋")
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
        resume_ctx = "Resume:
" + "
".join(f"- {b}" for b in bullets)
        proj_list = list(proj_map.keys())
        proj_ctx = "Projects:
" + "
".join(f"- {p}" for p in proj_list)
        msgs = system + [{"role": "system", "content": resume_ctx}, {"role": "system", "content": proj_ctx}, {"role": "user", "content": query}]
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=msgs)
        reply = resp.choices[0].message.content
        st.session_state.history.append(('assistant', reply))
        st.experimental_rerun()

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
    "Quality of Life Analysis": (
        "City income vs crime trends.",
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/qol_analysis.png",
        "https://github.com/venkateshsoundar/canadian-qol-analysis"
    ),
    "Alberta Wildfire Analysis": (
        "Alberta wildfire pattern analysis.",
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/wildfire_analysis.png",
        "https://github.com/venkateshsoundar/alberta-wildfire-analysis"
    ),
    "Toronto Crime Drivers": (
        "Mapping Toronto crime factors.",
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/crime_drivers.png",
        "https://github.com/venkateshsoundar/toronto-crime-drivers"
    ),
    "Uber Ride Duration Predictor": (
        "Machine learning model to predict ride durations.",
        "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/assets/uber_predictor.png",
        "https://github.com/venkateshsoundar/uber-ride-duration-predictor"
    )
}
    st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
    for name, (desc, img, repo) in proj_map.items():
        st.markdown("<div class='project-item'>", unsafe_allow_html=True)
        st.markdown(f"<a href='{repo}' target='_blank'><img src='{img}' /><div class='overlay'>{name}</div></a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
