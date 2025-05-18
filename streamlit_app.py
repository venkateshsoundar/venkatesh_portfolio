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
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
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
body {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DS.jpg') center/cover no-repeat;
  color: #f0f0f0;
}
.stApp .sidebar-content { background-color: rgba(31, 42, 68, 0.9); }
.card {
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s ease, box-shadow .3s ease;
  color: #f0f0f0;
}
.card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.7); }
.hover-zoom { transition: transform .3s ease; }
.hover-zoom:hover { transform: translateY(-5px); }
.section-title { font-size: 1.6rem; border-bottom: 2px solid #5A84B4; margin-bottom: 12px; padding-bottom: 4px; color: #AFCBE3; }
.profile-pic { border-radius: 50%; width: 150px; margin: 0 auto 12px; display: block; border: 2px solid #5A84B4; }
.contact-icon { width: 30px; height: 30px; filter: invert(100%); transition: transform .3s ease; }
.contact-icon:hover { transform: scale(1.2); }
.chat-bubble { padding: 8px 12px; border-radius: 12px; margin: 4px 0; animation: fade-in .4s ease; }
.user-msg { background: #324665; text-align: right; color: #f0f0f0; }
.bot-msg { background: #5A84B4; text-align: left; color: #1F2A44; }
@keyframes fade-in { from { opacity:0; transform:translateY(10px);} to { opacity:1; transform:translateY(0);} }
.project-item { position: relative; overflow: hidden; border-radius: 12px; height: 200px; }
.card-img { width: 100%; height: 100%; object-fit: cover; transition: transform .3s ease, filter .3s ease; }
.project-item:hover .card-img { transform: scale(1.05); filter: brightness(1.1); }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center; color: #f0f0f0; opacity: 0; transition: opacity .3s ease; font-size: 1.2rem; text-align: center; padding: 10px; }
.project-item:hover .overlay { opacity: 1; }
.typewriter h1 { white-space: normal; overflow: hidden; border-right: .15em solid #5A84B4; letter-spacing: .1em; animation: typing 3.5s steps(40,end), blink-caret .75s step-end infinite; color: #AFCBE3; }
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { from,to { border-color: transparent; } 50% { border-color: #5A84B4; } }
</style>
    ''',
    unsafe_allow_html=True
)

# --- Layout: three panes ---
left_col, mid_col, right_col = st.columns([1, 2, 1], gap="large")

# --- Left pane: Profile only ---
with left_col:
    # Profile card
    st.markdown(
        "<div class='card hover-zoom'><img src='https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg' class='profile-pic'><h2>Venkatesh Soundararajan</h2><p><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p></div>",
        unsafe_allow_html=True
    )
    # Contact card with icons
    st.markdown(
        "<div class='card hover-zoom'><div class='section
