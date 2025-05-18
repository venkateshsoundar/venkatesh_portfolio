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
st.markdown('''
<style>
body { background-color: #121212; color: #e0e0e0; }
.stApp .sidebar-content { background-color: #1e1e1e; }
.card { border-radius:12px; padding:20px; margin-bottom:20px; color:#ffffff; background:linear-gradient(135deg, #2E3B4E, #627D98); transition:transform .3s ease,box-shadow .3s ease; }
.card:hover { transform:translateY(-5px); box-shadow:0 8px 16px rgba(0,0,0,0.6); }
.section-title { font-size:1.6rem; border-bottom:3px solid #82A3C8; margin-bottom:12px; padding-bottom:4px; color:#82A3C8; }
.profile-pic { border-radius:50%; width:150px; margin:0 auto 12px; display:block; }
.chat-bubble { padding:8px 12px; border-radius:12px; margin:4px 0; animation:fade-in .4s ease; }
.user-msg { background:#627D98; text-align:right; color:#ffffff; }
.bot-msg { background:#A3BFD9; text-align:left; color:#121212; }
@keyframes fade-in { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }
</style>
''', unsafe_allow_html=True)

# --- Layout: three panes ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="large")

# --- Left pane: Profile + Chat ---
with left_col:
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
    st.markdown("### Chat with Me 📋")
    if 'history' not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        cls = 'user-msg' if role=='user' else 'bot-msg'
        st.markdown(f"<div class='chat-bubble {cls}'>{msg}</div>", unsafe_allow_html=True)
    query = st.chat_input("Ask me anything about my background or projects...")
    if query:
        st.session_state.history.append(('user', query))
        system = [{"role":"system","content":"You are Venkatesh’s portfolio assistant. Cite [Resume] or [Projects]."}]
        resume_ctx = "Resume:\n" + "\n".join(f"- {b}" for b in bullets)
        proj_ctx = "Projects:\n" + "\n".join([
            "- Canadian Quality of Life Analysis",
            "- Alberta Wildfire Analysis",
            "- Toronto Crime Drivers",
            "- Weight Change Regression Analysis",
            "- Calgary Childcare Compliance",
            "- Social Media Purchase Influence",
            "- Obesity Level Estimation",
            "- Weather Data Pipeline (AWS)",
            "- California Wildfire Data Story",
            "- Penguin Dataset Chatbot",
            "- Uber Ride Duration Predictor"
        ])
        msgs = system + [{"role":"system","content":resume_ctx},{"role":"system","content":proj_ctx},{"role":"user","content":query}]
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=msgs)
        st.session_state.history.append(('assistant', resp.choices[0].message.content))
        st.experimental_rerun()

# --- Center pane: Main Details ---
with mid_col:
    st.markdown("<div class='card column'><div class='section-title'>Welcome</div><p>Hello! I'm Venkatesh, a Data Science graduate student and analytics professional.</p></div>", unsafe_allow_html=True)
    highlights = "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
    st.markdown(f"<div class='card column'><div class='section-title'>Resume Highlights</div>{highlights}</div>", unsafe_allow_html=True)
    # Projects Showcase as grid
    st.markdown("<div class='section-title'>Projects Showcase</div>", unsafe_allow_html=True)
    num_cols = 3
    for i in range(0, len(projects), num_cols):
        cols = st.columns(num_cols, gap="medium")
        for idx, proj in enumerate(projects[i:i+num_cols]):
            with cols[idx]:
                st.markdown(
                    f"<a href='{proj['url']}' target='_blank'>"
                    f"<img src='{proj['image']}' class='card-img' />"
                    f"</a>"
                    , unsafe_allow_html=True)
                st.markdown(f"**{proj['title']}**", unsafe_allow_html=True)

# --- Right pane: Skills, Experience, Certifications ---
with right_col:
    st.markdown("<div class='card column'><div class='section-title'>Skills</div><ul><li>Python, SQL, R</li><li>AWS & SageMaker</li><li>Streamlit, Tableau</li><li>Scikit-learn, OpenCV</li><li>Git, Agile</li></ul></div>", unsafe_allow_html=True)
    st.markdown("<div class='card column'><div class='section-title'>Experience</div><ul><li>Deloitte Quality Lead (8+ yrs)</li><li>AWS Data Pipelines</li><li>Agile Team Lead</li><li>Risk Analytics</li></ul></div>", unsafe_allow_html=True)
    st.markdown("<div class='card column'><div class='section-title'>Certifications</div><ul><li>AWS Solutions Architect</li><li>Tableau Specialist</li><li>Scrum Master</li></ul></div>", unsafe_allow_html=True)
