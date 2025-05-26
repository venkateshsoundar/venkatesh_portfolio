import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Sticky Top Navigation Bar with Animation ---
st.markdown(
    """
    <style>
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 36px;
        background: rgba(44,62,80,0.90);
        padding: 16px 0 6px 0;
        border-radius: 0 0 20px 20px;
        position: sticky;
        top: 0;
        z-index: 99;
        margin-bottom: 28px;
    }
    .nav-link {
        background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
        color: #ffd166 !important;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.13rem;
        letter-spacing: 1px;
        padding: 10px 26px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(44,62,80,0.15);
        transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s, background .22s;
        display: inline-block;
        margin-bottom: 0;
    }
    .nav-link:hover, .nav-link:focus {
        transform: translateY(-5px) scale(1.07);
        box-shadow: 0 8px 16px rgba(0,0,0,0.24);
        background: linear-gradient(135deg, #406496 0%, #22304A 100%);
        color: #fff !important;
        text-decoration: none;
    }
    </style>
    <div class="nav-bar">
        <a class="nav-link" href="#about-me">About</a>
        <a class="nav-link" href="#projects-gallery">Projects</a>
        <a class="nav-link" href="#professional-experience">Experience</a>
        <a class="nav-link" href="#core-skills-tools">Skills</a>
        <a class="nav-link" href="#contact">Contact</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Global CSS & Background for Cards and Animations ---
st.markdown(
    '''
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
}
.card {
  width: 100% !important;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  text-align: center;
}
.card:hover, .card.hover-zoom:hover {
  transform: translateY(-5px) scale(1.04);
  box-shadow: 0 8px 16px rgba(0,0,0,0.24);
}
.section-title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 6px;
}
.profile-pic-popout {
  width: 160px;
  height: 160px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.18);
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 20px;
  z-index: 10;
}
[data-testid="stChatInput"] input,
.stChatInput input,
input[data-baseweb="input"] {
  border: 2px solid #406496 !important;
  border-radius: 10px !important;
  background: #fff !important;
  color: #222 !important;
  font-size: 1.08rem !important;
  box-shadow: 0 2px 10px rgba(30,50,100,0.08);
  margin-top: 10px !important;
  margin-bottom: 10px !important;
}
.profile-card-container {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}
.profile-card-content {
  padding-top: 200px;
}
.contact-icon {
  width: 30px;
  height: 30px;
  filter: invert(100%);
  color:#ADD8E6;
  margin: 0 8px;
  vertical-align: middle;
}
.project-item {
  position: relative;
  aspect-ratio: 1/1;
  overflow: hidden;
  border-radius: 12px;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
}
.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1);
}
.project-item:hover .card-img {
  transform: scale(1.05);
}
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity .3s ease;
  font-size: 1.2rem;
  color: #ffffff;
}
.project-item:hover .overlay {
  opacity: 1;
}
.typewriter {
  width: fit-content;
  margin: 0 auto 20px;
}
.typewriter h1 {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  border-right: .15em solid #5A84B4;
  animation: typing 3.5s steps(40,end), blink-caret .75s step-end infinite;
  color: #ffffff;
}
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { from, to { border-color: transparent; } 50% { border-color: #5A84B4; } }
.details-summary {
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%) !important;
  color: #ffffff !important;
  font-size: 1.6rem !important;
  font-weight: bold !important;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 10px;
  text-align: center;
  cursor: pointer;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
/* --- Make chat_input box dark and bold --- */
[data-testid="stChatInput"] input,
.stChatInput input,
input[data-baseweb="input"] {
  background: #26334d !important;
  color: #222 !important;
  border: 2px solid #5A84B4 !important;
  border-radius: 12px !important;
  font-size: 1.08rem !important;
  box-shadow: 0 2px 10px rgba(30,50,100,0.14);
  margin-top: 10px !important;
  margin-bottom: 10px !important;
  transition: box-shadow 0.2s, border 0.2s;
}
[data-testid="stChatInput"] input:focus,
.stChatInput input:focus,
input[data-baseweb="input"]:focus {
  border: 2px solid #ffd166 !important;
  outline: none !important;
  box-shadow: 0 0 0 2px #ffd16666;
}
[data-testid="stChatInput"] {
  border: 2px solid #406496 !important;
  border-radius: 12px !important;
  background: #fff !important;
  box-shadow: 0 2px 10px rgba(30,50,100,0.09);
  padding: 0 !important;
}
[data-testid="stChatInput"] input,
.stChatInput input,
input[data-baseweb="input"] {
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  color: #222 !important;
  font-size: 1.08rem !important;
}
[data-testid="stChatInput"]:focus-within {
  border: 2px solid #FFD166 !important;
  box-shadow: 0 0 0 2px #ffd16633;
}
div[data-testid="stSpinner"] > div {
    color: #111 !important;
    font-weight: 600;
}
.project-title {
  text-align: center;
  margin-top: 8px;
  font-weight: bold;
  color: #ffffff;
}
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  opacity: 0;
  transition: opacity .3s ease;
  font-size: 1.2rem;
  color: #ffffff;
  padding: 0 8px;
}
</style>
''', unsafe_allow_html=True
)

# --- Load resume bullets ---
def load_resume_df(url):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    records = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        for sent in sentences:
            records.append({"page": i+1, "sentence": sent})
    return pd.DataFrame(records)

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
)
resume_df = load_resume_df(resume_url)
resume_json = resume_df.to_json(orient='records')

# --- Projects list ---
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)",     "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws",     "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg"}
]

# --- Layout ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="small")

# --- Left Pane (profile, contact, education, certs, awards) ---
with left_col:
    st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
    st.markdown('''
    <div class="profile-card-container">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"
           class="profile-pic-popout" />
      <div class="card profile-card-content hover-zoom">
        <h2>Venkatesh Soundararajan</h2>
        <p><span style="color:#ADD8E6;"><strong>Software Development Intern</strong><br>Data Engineering</span></p>
        <span style="color:#ffd166;"><strong>🍁 Calgary, AB, Canada</strong></span>
      </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#34495E;">Contact</div>' +
        '<div style="display:flex; justify-content:center; gap:16px; margin-top:10px;color:#ADD8E6">' +
        '<a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>' +
        '<a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>' +
        '<a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>' +
        '<a href="https://medium.com/@venkatesh.balusoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg" class="contact-icon"/></a>' +
        '</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("""
<style>
.edu-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 10px;
}
.edu-card-h {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(30,50,80,0.10);
  padding: 18px 24px;
  display: flex;
  align-items: center;
  min-height: 110px;
  border: 2px solid #40649622;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
}
.edu-card-h:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 6px 16px rgba(20,40,80,0.18);
  background: linear-gradient(135deg, #406496 0%, #34495E 100%);
}
.edu-logo-h {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 10px;
  background: #fff;
  margin-right: 20px;
  box-shadow: 0 2px 8px rgba(44,62,80,0.10);
  border: 1.5px solid #eee;
}
.edu-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.edu-degree { font-weight: bold; font-size: 1.08rem; margin-bottom: 2px;}
.edu-uni { color: #ADD8E6; font-size: 1.01rem; margin-bottom: 4px;}
.edu-dates { color: #ffd166; font-size: 0.96rem;}
</style>
<div class="card hover-zoom">
  <div class="section-title" style="background:#34495E;">Education</div>
  <div class="edu-list">
    <div class="edu-card-h">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Uoc.png" class="edu-logo-h"/>
      <div class="edu-info">
        <div class="edu-degree">Masters in Data Science and Analytics</div>
        <div class="edu-uni">University of Calgary, Alberta, Canada</div>
        <div class="edu-dates">September 2024 – Present</div>
      </div>
    </div>
    <div class="edu-card-h">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/AnnaUniversity.png" class="edu-logo-h"/>
      <div class="edu-info">
        <div class="edu-degree">Bachelor of Engineering</div>
        <div class="edu-uni">Anna University, Chennai, India</div>
        <div class="edu-dates">August 2009 – May 2013</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)




    st.markdown(
    """
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Certifications & Courses</div>
      <div style="text-align:left; margin-left:10px;">
        <p>
          <b>Insurance &amp; Guidewire Suite Analyst 10.0</b><br>
          <span style="color:#ADD8E6;">Jasper – Guidewire Education</span><br>
          <span style="color:#ffd166;">2024</span>
        </p>
        <p>
          <b>Karate DSL</b><br>
          <span style="color:#ADD8E6;">Udemy</span><br>
          <span style="color:#ffd166;">2023</span>
        </p>
        <p>
          <b>Rest API Automation</b><br>
          <span style="color:#ADD8E6;">TestLeaf Software Solutions Pvt. Ltd.</span><br>
          <span style="color:#ffd166;">2023</span>
        </p>
        <p>
          <b>Selenium WebDriver</b><br>
          <span style="color:#ADD8E6;">TestLeaf Software Solutions Pvt. Ltd.</span><br>
          <span style="color:#ffd166;">2022</span>
        </p>
        <p>
          <b>SQL for Data Science</b><br>
          <span style="color:#ADD8E6;">Coursera</span><br>
          <span style="color:#ffd166;">2020</span>
        </p>
        <p>
          <b>SDET</b><br>
          <span style="color:#ADD8E6;">Capgemini</span><br>
          <span style="color:#ffd166;">2020</span>
        </p>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    '''
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Awards & Recognitions</div>
      <div class="awards-grid">
        <div class="award-badge">
          <div class="award-year">2022 & 2023</div>
          <div class="award-title">Spot Award</div>
          <div class="award-sub">InsurCloud – Deloitte, Canada</div>
        </div>
        <div class="award-badge">
          <div class="award-year">2018</div>
          <div class="award-title">Best Contributor</div>
          <div class="award-sub">COMPASS Program – Hartford Insurance, USA</div>
        </div>
        <div class="award-badge">
          <div class="award-year">2017</div>
          <div class="award-title">QE & A Maestro</div>
          <div class="award-sub">Centene by Cognizant QE&A, USA</div>
        </div>
        <div class="award-badge">
          <div class="award-year">Q1 2017</div>
          <div class="award-title">Pride of the Quarter</div>
          <div class="award-sub">Health Net by Cognizant QE&A, USA</div>
        </div>
        <div class="award-badge">
          <div class="award-year">May 2014 & Aug 2015</div>
          <div class="award-title">Pillar of the Month</div>
          <div class="award-sub">Health Net by Cognizant QE&A, USA</div>
        </div>
      </div>
    </div>
    <style>
      .awards-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
        margin-top: 12px;
      }
      .award-badge {
        background: rgba(255,255,255,0.1);
        padding: 12px;
        border-radius: 8px;
        text-align: center;
      }
      .award-year {
        font-size: 0.85rem;
        color: #ffd166;
        margin-bottom: 4px;
      }
      .award-title {
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 4px;
      }
      .award-sub {
        font-size: 0.9rem;
        opacity: 0.8;
      }
    </style>
    ''',
    unsafe_allow_html=True
)

# --- Right Pane (Experience, Skills) ---
with right_col:
    st.markdown('<a id="professional-experience"></a>', unsafe_allow_html=True)
    st.markdown("""
<style>
.exp-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 18px;
  margin-top: 20px;
  margin-bottom: 20px;
}
.exp-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 15px;
  padding: 22px 14px 16px 14px;
  box-shadow: 0 2px 10px rgba(30,50,80,0.13);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 215px;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  border: 2px solid #40649622;
}
.exp-card:hover {
  transform: translateY(-7px) scale(1.03);
  box-shadow: 0 8px 18px rgba(20,40,80,0.19);
  background: linear-gradient(135deg, #406496 0%, #34495E 100%);
}
.exp-card-logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 11px;
  background: #fff;
  margin-bottom: 10px;
  box-shadow: 0 1px 8px rgba(44,62,80,0.09);
  border: 1.5px solid #eee;
}
.exp-card-title { font-weight: 700; font-size: 1.12rem; margin-bottom: 3px;}
.exp-card-company { color: #ADD8E6; font-size: 1.01rem; margin-bottom: 6px;}
.exp-card-date { color: #ffd166; font-size: 0.98rem;}
</style>
<div class="card hover-zoom">
  <div class="section-title" style="background:#34495E;">Professional Experience</div>
  <div class="exp-cards-grid">
    <div class="exp-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/TI.png" class="exp-card-logo"/>
      <div class="exp-card-title">Software Developer Intern</div>
      <div class="exp-card-company">Tech Insights Inc, Canada</div>
      <div class="exp-card-date">May 2025 – Present</div>
    </div>
    <div class="exp-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Deloitte.png" class="exp-card-logo"/>
      <div class="exp-card-title">Senior Consultant</div>
      <div class="exp-card-company">Deloitte Consulting India Private Limited, India</div>
      <div class="exp-card-date">October 2021 – August 2024</div>
    </div>
    <div class="exp-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Capgemini.png" class="exp-card-logo"/>
      <div class="exp-card-title">Consultant</div>
      <div class="exp-card-company">Capgemini Technology Services India Private Limited, India</div>
      <div class="exp-card-date">May 2018 – October 2021</div>
    </div>
    <div class="exp-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Cognizant.png" class="exp-card-logo"/>
      <div class="exp-card-title">Associate</div>
      <div class="exp-card-company">Cognizant Technology Solutions India Private Limited, India</div>
      <div class="exp-card-date">Sep 2013 – May 2018</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)




    st.markdown('<a id="core-skills-tools"></a>', unsafe_allow_html=True)
    st.markdown(
    '''
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Core Skills & Tools</div>
      <!-- Programming Languages -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Programming Languages</summary>
        <div class="skills-grid">
          <div class="skill-card">Python</div>
          <div class="skill-card">R</div>
          <div class="skill-card">SQL</div>
          <div class="skill-card">Java</div>
          <div class="skill-card">VBA Macro</div>
        </div>
      </details>
      <!-- Data Analysis Tools -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Data Analysis Tools</summary>
        <div class="skills-grid">
          <div class="skill-card">Pandas</div>
          <div class="skill-card">NumPy</div>
          <div class="skill-card">Matplotlib</div>
        </div>
      </details>
      <!-- Visualization Tools -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Data Visualization</summary>
        <div class="skills-grid">
          <div class="skill-card">Power BI</div>
          <div class="skill-card">Excel</div>
        </div>
      </details>
      <!-- Statistical Analysis -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Statistical Analysis</summary>
        <div class="skills-grid">
          <div class="skill-card">Hypothesis Tests</div>
          <div class="skill-card">Regression</div>
        </div>
      </details>
      <!-- Database Management Tools -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Database Management</summary>
        <div class="skills-grid">
          <div class="skill-card">MySQL</div>
          <div class="skill-card">Oracle</div>
          <div class="skill-card">NoSQL</div>
        </div>
      </details>
      <!-- Version Control -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Version Control</summary>
        <div class="skills-grid">
          <div class="skill-card">Git</div>
        </div>
      </details>
      <!-- Project Management Tools-->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Project Management Tools</summary>
        <div class="skills-grid">
          <div class="skill-card">JIRA</div>
          <div class="skill-card">ALM</div>
          <div class="skill-card">Rally</div>
        </div>
      </details>
      <!-- QA Automation & Insurance -->
      <details open>
        <summary style="font-weight:bold; cursor:pointer;">Automation & Insurance Suite</summary>
        <div class="skills-grid">
          <div class="skill-card">Selenium WebDriver</div>
          <div class="skill-card">Guidewire</div>
        </div>
      </details>
    </div>
    <style>
      .skills-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 8px;
        margin: 8px 0 12px;
      }
      .skill-card {
        background: rgba(255,255,255,0.15);
        padding: 6px;
        border-radius: 6px;
        font-size: 0.9rem;
        text-align: center;
      }
      details summary {
        list-style: none;
      }
      details summary::-webkit-details-marker {
        display: none;
      }
    </style>
    ''',
    unsafe_allow_html=True
)

# --- Center Pane (Welcome, About, Chatbot, Projects) ---
with mid_col:
    gif_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif"
    st.markdown(
        f"""
        <style>
          .welcome-card {{
            background: url("{gif_url}") center/cover no-repeat;
            border-radius: 16px;
            padding: 3rem;
            color: white;
            min-height: 180px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
          }}
          .stApp .welcome-card {{
            margin: 0 auto 1rem auto;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="welcome-card">
          <div class="typewriter">
          <div>
            <h1>Hello and Welcome...</h1>
            <p>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # About section
    st.markdown('<a id="about-me"></a>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card hover-zoom" style="background:linear-gradient(135deg, #34495E 0%, #406496 100%);margin-bottom:24px;">
          <div class="section-title" style="background:#22304A;">About Me</div>
          <div style="font-size:1.08rem; text-align:left; color:#fff;">
            I’m Venkatesh, a Data Scientist and Software Developer with 8+ years of experience in quality engineering, business intelligence, and analytics. I specialize in building scalable ETL pipelines, predictive models, and interactive dashboards using cloud platforms like AWS and Azure. I’m passionate about solving business problems and delivering impactful, data-driven solutions.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Chatbot section
    ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
    st.markdown(
        f"""
        <style>
          .welcome-card2 {{
            background: url("{ai_url}") center/cover no-repeat;
            border-radius: 16px;
            padding: 0;
            color: white;
            height: 200px;
            position: relative;
            overflow: hidden;
            margin-bottom: 24px;
          }}
          .welcome-card2 .text-container {{
            position: absolute;
            top: 70%;
            right: 2rem;
            transform: translateY(-50%);
            text-align: right;
          }}
          .welcome-card2 h2 {{
            margin: 0;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="welcome-card2">
          <div class="text-container">
            <h2>Ask Buddy Bot!</h2>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Chatbot input/output (replace with your key handling)
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    chat_container = st.container()
    with chat_container:
        user_input = st.chat_input("Ask something about Venkatesh's Professional Projects and Skills...")
        if user_input:
            st.chat_message("user").write(user_input)
            prompt = (
                "You are Venkatesh's professional assistant. Here is his resume data as JSON:\n" + resume_json +
                "\n\nAnswer the question based only on this DataFrame JSON. If you can't, say you don't know.\nQuestion: "
                + user_input
            )
            with st.spinner("Assistant is typing..."):
                response = client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324",
                    messages=[
                        {"role": "system", "content": prompt}
                    ]
                )
                reply = response.choices[0].message.content
            st.chat_message("assistant").write(reply)

    # Projects Gallery
    st.markdown('<a id="projects-gallery"></a>', unsafe_allow_html=True)
    st.markdown('<div class="card hover-zoom"><div class="section-title" style="background:#2C3E50;">Projects Gallery</div></div>', unsafe_allow_html=True)
    grid_html = '<div class="grid-container">'
    for proj in projects:
        grid_html += (
            f'<div class="project-item hover-zoom">'
            f'  <a href="{proj["url"]}" target="_blank">'
            f'    <img src="{proj["image"]}" class="card-img"/>'
            f'    <div class="overlay">{proj["title"]}</div>'
            f'  </a>'
            f'</div>'
        )
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    

