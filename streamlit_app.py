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
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "California Wildfire Data Story", "url": "https://github.com/venkateshsoundar/california-wildfire-datastory", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/California_Wildfire_Data_Story.jpeg"},
    {"title": "Penguin Dataset Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Dataset_Chatbot.jpeg"},
    {"title": "Uber Ride Duration Predictor", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictor", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uber_Ride_Duration_Predictor.jpeg"}
]

# --- CSS & Background ---
st.markdown(
    '''
<style>
body { background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DS.jpg') center/cover no-repeat; color: #ffffff; }
.stApp .sidebar-content { background-color: rgba(31,42,68,0.9); }
.card {
  display: block !important;
  width: 100% !important;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s ease, box-shadow .3s ease;
  color: #ffffff;
  box-sizing: border-box;
}
.card * { color:#ffffff!important; }
.card-left { min-height: 260px; }
.card-mid { min-height: 180px; }
.card-right { min-height: 200px; }
.card:hover { transform:translateY(-5px); box-shadow:0 8px 16px rgba(0,0,0,0.7); }
.hover-zoom { display:inline-block; animation:zoom-in .3s ease forwards; }
.hover-zoom:hover { animation:zoom-out .3s ease forwards; }
@keyframes zoom-in { from{transform:scale(0.95);} to{transform:scale(1);} }
@keyframes zoom-out { from{transform:scale(1);} to{transform:scale(1.05);} }
.section-title { font-size:1.6rem; border-bottom:2px solid #5A84B4; margin-bottom:12px; padding-bottom:4px; }
.profile-pic { border-radius:50%; width:150px; margin:0 auto 12px; display:block; border:2px solid #5A84B4; }
.contact-icon { width:30px; height:30px; filter:invert(100%); transition:transform .3s ease; }
.contact-icon:hover { transform:scale(1.2); }
.chat-bubble { padding:8px 12px; border-radius:12px; margin:4px 0; }
.user-msg { background:#324665; text-align:right; color:#ffffff; }
.bot-msg { background:#5A84B4; text-align:left; color:#000000; }
.project-item { position:relative; overflow:hidden; border-radius:12px; aspect-ratio:1/1; }
.card-img { width:100%; height:100%; object-fit:cover; transition:transform .3s ease,filter .3s ease; }
.project-item:hover .card-img { transform:scale(1.05); filter:brightness(1.1); }
.overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; opacity:0; transition:opacity .3s ease; font-size:1.2rem; padding:10px; }
.project-item:hover .overlay { opacity:1; }
.typewriter h1 { border-right:.15em solid #5A84B4; animation:typing 3.5s steps(40,end),blink-caret .75s step-end infinite; }
@keyframes typing { from{width:0;} to{width:100%;} }
@keyframes blink-caret { from,to{border-color:transparent;} 50%{border-color:#5A84B4;} }
</style>
    ''', unsafe_allow_html=True
)

# --- Three-column layout ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="large")

# --- Left pane ---
with left_col:
    st.markdown(
        '<div class="card hover-zoom" style="min-height:250px;">'
        '<img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic"/>'
        '<h2>Venkatesh Soundararajan</h2><p><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom" style="min-height:250px;"><div class="section-title">Contact</div>'
        '<div style="display:flex;justify-content:center;gap:20px;margin-top:10px;">'
        '<a href="mailto:venkatesh.balusoundar@gmail.com"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>'
        '<a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>'
        '<a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>'
        '</div></div>',
        unsafe_allow_html=True
    )

# --- Center pane--- ---
with mid_col:
    st.markdown(
        '<div class="card"><div class="typewriter"><h1>Welcome to my Profile</h1></div><p style="margin-top:20px;">Explore projects and chat below!</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title">Projects Showcase</div></div>',
        unsafe_allow_html=True
    )
    num_cols=2
    for i in range(0,len(projects),num_cols):
        cols=st.columns(num_cols,gap="medium")
        for idx,proj in enumerate(projects[i:i+num_cols]):
            with cols[idx]:
                st.markdown(
                    f'<div class="project-item hover-zoom"><a href="{proj["url"]}" target="_blank"><img src="{proj["image"]}" class="card-img"/><div class="overlay">{proj["title"]}</div></a></div>',
                    unsafe_allow_html=True
                )
        st.markdown('<div style="height:20px;"></div>',unsafe_allow_html=True)
    # Chat
    st.markdown('<div class="card hover-zoom"><div class="section-title">Chat with Me 📋</div></div>',unsafe_allow_html=True)
    if 'history' not in st.session_state: st.session_state.history=[]
    for role, msg in st.session_state.history:
        cls='user-msg' if role=='user' else 'bot-msg'
        st.markdown(f'<div class="chat-bubble {cls}">{msg}</div>',unsafe_allow_html=True)
    query=st.chat_input("Ask me anything...")
    if query:
        st.session_state.history.append(('user',query))
        system=[{"role":"system","content":"You are Venkatesh’s assistant."}]
        resume_ctx="Resume:\n"+"\n".join(f"- {b}"for b in bullets)
        proj_ctx="Projects:\n"+"\n".join(f"- {p['title']}"for p in projects)
        msgs=system+[
            {"role":"system","content":resume_ctx},
            {"role":"system","content":proj_ctx},
            {"role":"user","content":query}
        ]
        client=OpenAI(base_url="https://openrouter.ai/api/v1",api_key=st.secrets["DEEPSEEK_API_KEY"])
        resp=client.chat.completions.create(model="deepseek/deepseek-r1:free",messages=msgs)
        st.session_state.history.append(('assistant',resp.choices[0].message.content))

# --- Right pane ---
with right_col:
    # Skills as text
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title">Skills</div>' +
        '<ul><li>Python, SQL, R</li><li>AWS & SageMaker</li><li>Streamlit, Tableau</li><li>Scikit-learn, OpenCV</li><li>Git, Agile</li></ul>' +
        '</div>',
        unsafe_allow_html=True
    )
    # Experience card
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title">Experience</div>' +
        '<ul><li>Deloitte Quality Lead (8+ yrs)</li><li>AWS Data Pipelines</li><li>Agile Team Lead</li><li>Risk Analytics</li></ul>' +
        '</div>', unsafe_allow_html=True
    )
    # Certifications card
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title">Certifications</div>' +
        '<ul><li>AWS Solutions Architect</li><li>Tableau Specialist</li><li>Scrum Master</li></ul>' +
        '</div>', unsafe_allow_html=True
    )
