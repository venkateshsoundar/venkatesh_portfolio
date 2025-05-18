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
    # Intro message
    st.markdown(
        '<div class="card"><div class="typewriter"><h1>Hello!</h1></div><p>Welcome to my data science portfolio. Explore my projects below.</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card"><div class="section-title">Projects Showcase</div></div>',
        unsafe_allow_html=True
    )
    # Projects grid in 2 columns per row
    num_cols = 2
    for i in range(0, len(projects), num_cols):
        row = projects[i:i+num_cols]
        cols = st.columns(num_cols, gap="medium")
        for j, proj in enumerate(row):
            with cols[j]:
                st.markdown(
                    f'<div class="project-item"><a href="{proj["url"]}" target="_blank">'
                    f'<img src="{proj["image"]}" class="card-img"/><div class="overlay">{proj["title"]}</div></a></div>',
                    unsafe_allow_html=True
                )
        # vertical spacer after each row
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # No chat section (removed per request) (removed per request)

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
