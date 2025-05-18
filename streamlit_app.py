import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume bullets ---
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    sentences = [s.strip() for s in text.split('.') if len(s) > 50]
    return sentences[:max_bullets]

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/"
    "Venkateshwaran_Resume.pdf"
)
bullets = load_resume_bullets(resume_url)

# --- Projects list ---
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
    # ... other projects ...
]

# --- Global CSS & Background ---
st.markdown(
    '''
<style>
body { background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DS.jpg') center/cover no-repeat; color: #ffffff; }
.card { width:100%; border-radius:12px; padding:20px; margin-bottom:20px; background:linear-gradient(135deg,#1F2A44 0%,#324665 100%); color:#ffffff; box-sizing:border-box; }
.section-title { font-size:1.6rem; font-weight:bold; margin-bottom:12px; color:#ffffff; }
.profile-pic { border-radius:50%; width:150px; display:block; margin:0 auto 12px; }
.project-item { position:relative; aspect-ratio:1/1; overflow:hidden; border-radius:12px; }
.card-img { width:100%; height:100%; object-fit:cover; transition:transform .3s ease; }
.project-item:hover .card-img { transform:scale(1.05); }
.overlay { position:absolute; inset:0; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; opacity:0; transition:opacity .3s ease; color:#ffffff; }
.project-item:hover .overlay { opacity:1; }
.chat-frame { width:100%; }
</style>
    ''', unsafe_allow_html=True
)

# --- Layout ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="large")

# --- Left Pane ---
with left_col:
    st.markdown(
        f'<div class="card hover-zoom"><img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic"/><h2>Venkatesh Soundararajan</h2><p><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title">Contact</div>' +
        '<div style="display:flex; justify-content:center; gap:16px; margin-top:10px;">' +
        '<a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>' +
        '<a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>' +
        '<a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>' +
        '</div></div>',
        unsafe_allow_html=True
    )

# --- Center Pane ---
with mid_col:
    st.markdown(
        '<div class="card"><div class="section-title">Projects Showcase</div></div>',
        unsafe_allow_html=True
    )
    cols = st.columns(2, gap="medium")
    for idx, proj in enumerate(projects):
        with cols[idx % 2]:
            st.markdown(
                f'<div class="project-item"><a href="{proj["url"]}" target="_blank"><img src="{proj["image"]}" class="card-img"/><div class="overlay">{proj["title"]}</div></a></div>',
                unsafe_allow_html=True
            )
        if idx % 2 == 1:
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # Chat Frame
    chat_frame = st.container()
    with chat_frame:
        st.markdown('<div class="card"><div class="section-title">Chat with Me</div></div>', unsafe_allow_html=True)
        if 'history' not in st.session_state:
            st.session_state.history = []
        for role, msg in st.session_state.history:
            st.chat_message(role).write(msg)
    query = st.chat_input("Ask me anything...")
    if query:
        st.session_state.history.append(('user', query))
        messages = [
            {"role": "system", "content": "You are Venkatesh’s assistant."},
            {"role": "system", "content": "Resume:
" + "
".join(f"- {b}" for b in bullets)},
            {"role": "system", "content": "Projects:
" + "
".join(f"- {p['title']}" for p in projects)},
            {"role": "user", "content": query}
        ]}" for p in projects)},
            {"role":"user","content":query}
        ]
        client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=messages)
        st.session_state.history.append(('assistant', resp.choices[0].message.content))
        with chat_frame:
            st.chat_message('assistant').write(resp.choices[0].message.content)

# --- Right Pane ---
with right_col:
    st.markdown(
        '<div class="card"><div class="section-title">Skills</div><ul><li>Python, SQL, R</li><li>AWS & SageMaker</li><li>Streamlit, Tableau</li><li>Scikit-learn, OpenCV</li><li>Git, Agile</li></ul></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card"><div class="section-title">Experience</div><ul><li>Deloitte Quality Lead (8+ yrs)</li><li>AWS Data Pipelines</li><li>Agile Team Lead</li><li>Risk Analytics</li></ul></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card"><div class="section-title">Certifications</div><ul><li>AWS Solutions Architect</li><li>Tableau Specialist</li><li>Scrum Master</li></ul></div>',
        unsafe_allow_html=True
    )
