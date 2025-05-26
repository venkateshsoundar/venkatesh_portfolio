import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# ---- PAGE CONFIG & GLOBAL CSS ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

st.markdown("""
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 3px solid #22304A;
}
.stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
    color: #ffd166 !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 16px 36px !important;
    font-size: 1.14rem;
    font-weight: bold;
    margin-bottom: -3px !important;
    transition: all .25s;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #fff !important;
    background: linear-gradient(135deg, #406496 0%, #22304A 100%);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #22304A 0%, #ffd166 150%) !important;
    color: #222 !important;
    border-bottom: 4px solid #ffd166 !important;
    transform: scale(1.06) translateY(-2px);
    box-shadow: 0 6px 22px rgba(44,62,80,0.13);
}
.card {
  width: 100% !important;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 32px;
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
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 32px;
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
.profile-card-container {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}
.profile-card-content {
  padding-top: 200px;
}
.contact-icon {
  width: 32px;
  height: 32px;
  filter: invert(100%);
  color:#ADD8E6;
  margin: 0 8px;
  vertical-align: middle;
}
.edu-cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 20px;
  margin-bottom: 18px;
}
.edu-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 15px;
  padding: 22px 14px 16px 14px;
  box-shadow: 0 2px 10px rgba(30,50,80,0.13);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 170px;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  border: 2px solid #40649622;
}
.edu-card:hover {
  transform: translateY(-7px) scale(1.03);
  box-shadow: 0 8px 18px rgba(20,40,80,0.19);
  background: linear-gradient(135deg, #406496 0%, #34495E 100%);
}
.edu-card-logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 11px;
  background: #fff;
  margin-bottom: 10px;
  box-shadow: 0 1px 8px rgba(44,62,80,0.09);
  border: 1.5px solid #eee;
}
.edu-card-degree { font-weight: 700; font-size: 1.12rem; margin-bottom: 3px; color: #ffd166;}
.edu-card-univ { color: #ADD8E6; font-size: 1.01rem; margin-bottom: 4px;}
.edu-card-date { color: #fff; font-size: 0.98rem;}
/* Awards/Certifications */
.cert-grid, .awards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 18px;
  margin-bottom: 2px;
}
.cert-card, .award-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(60,100,160,0.07);
  padding: 18px 18px 14px 18px;
  min-height: 80px;
  transition: transform .17s, box-shadow .17s;
  border: 1.5px solid #40649644;
  text-align: left;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.cert-card:hover, .award-card:hover {
  transform: translateY(-4px) scale(1.03);
  box-shadow: 0 8px 24px rgba(20,60,120,0.15);
  background: linear-gradient(135deg, #22304A 0%, #406496 88%);
}
.cert-title, .award-title { font-weight: bold; font-size: 1.07rem; color: #ffd166; margin-bottom: 2px; margin-top: 0;}
.cert-provider, .award-sub { font-size: 0.99rem; color: #ADD8E6; margin-bottom: 2px;}
.cert-year, .award-year { font-size: 0.97rem; color: #fff; opacity: 0.8;}
.award-year {margin-bottom: 2px;}
/* Experience */
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
/* Skills */
.skills-category {
  margin-bottom: 14px;
}
.skills-header {
  font-size: 1.04rem;
  color: #ffd166;
  font-weight: 600;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.skill-icon {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  filter: brightness(0.95) invert(0.09) sepia(1) hue-rotate(165deg) saturate(6);
}
.skills-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 2px;
}
.skill-chip {
  background: rgba(255,255,255,0.12);
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 0.97rem;
  color: #fff;
  font-weight: 500;
  border: 1.5px solid #40649633;
}
</style>
""", unsafe_allow_html=True)

# ---- DATA LOADING ----
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

# ---- WELCOME & CHATBOT ----
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
        margin-bottom:24px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="welcome-card">
      <div>
        <h1>Hello and Welcome...</h1>
        <p>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

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
        margin-bottom: 32px;
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

# ---- TABS ----
tabs = st.tabs(["About", "Projects", "Experience", "Skills", "Contact"])

# ---- ABOUT TAB ----
st.markdown("""
<style>
.profile-pic-popout {
    width: 180px;
    border-radius: 50%;
    border: 4px solid #ffd166;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.4);
    margin-bottom: 12px;
}
.card {
    background: #1F2A44;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}
.hover-zoom:hover {
    transform: scale(1.02);
}
.section-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 12px;
    padding: 8px 16px;
    border-radius: 10px;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# --- Custom Styling ---
st.markdown("""
<style>
/* Square profile pic with animation */
.profile-pic-square {
    width: 180px;
    height: 180px;
    border-radius: 20px;
    object-fit: cover;
    border: 4px solid #ffd166;
    box-shadow: 0 0 12px rgba(255, 209, 102, 0.6);
    margin: 0 auto 20px auto;
    display: block;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}
.profile-pic-square:hover {
    transform: scale(1.05);
    box-shadow: 0 0 24px rgba(255, 209, 102, 0.9);
}

/* Card styling */
.card {
    background: #1F2A44;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}
.hover-zoom:hover {
    transform: scale(1.02);
}

/* Title style */
.section-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 12px;
    padding: 8px 16px;
    border-radius: 10px;
    color: #fff;
    background:#22304A;
}
</style>
""", unsafe_allow_html=True)

# --- 2-Column Layout: Left Profile / Right About ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown(
        """
        <div class="card hover-zoom" style="text-align:center;">
            <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic-square" />
            <h2 style="color:#fff; margin-bottom: 5px;">Venkatesh Soundararajan</h2>
            <p style="color:#ADD8E6; font-size: 16px;">
                <strong>Software Development Intern</strong><br>Data Engineering
            </p>
            <p style="color:#ffd166;"><strong>🍁 Calgary, AB, Canada</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card hover-zoom" style="background:linear-gradient(135deg, #34495E 0%, #406496 100%);">
            <div class="section-title">About Me</div>
            <div style="font-size:1.05rem; color:#fff; line-height:1.6;">
                I’m Venkatesh, a Data Scientist and Software Developer with 8+ years of experience in quality engineering, business intelligence, and analytics. 
                I specialize in building scalable ETL pipelines, predictive models, and interactive dashboards using cloud platforms like AWS and Azure. 
                I’m passionate about solving business problems and delivering impactful, data-driven solutions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Spacer before next section ---
st.markdown("<br><hr style='border:1px solid #666;'><br>", unsafe_allow_html=True)
    # Education Card
    st.markdown(
    """
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Education</div>
      <div class="edu-cards-grid">
        <div class="edu-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Uoc.png" class="edu-card-logo"/>
          <div class="edu-card-degree">Masters in Data Science and Analytics</div>
          <div class="edu-card-univ">University of Calgary, Alberta, Canada</div>
          <div class="edu-card-date">September 2024 – Present</div>
        </div>
        <div class="edu-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/AnnaUniversity.png" class="edu-card-logo"/>
          <div class="edu-card-degree">Bachelor of Engineering</div>
          <div class="edu-card-univ">Anna University, Chennai, India</div>
          <div class="edu-card-date">August 2009 – May 2013</div>
        </div>
      </div>
    </div>
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Certifications & Courses</div>
      <div class="cert-grid">
        <div class="cert-card">
          <div class="cert-title">Guidewire Insurance Suite Analyst 10.0</div>
          <div class="cert-provider">Jasper – Guidewire Education</div>
          <div class="cert-year">2024</div>
        </div>
        <div class="cert-card">
          <div class="cert-title">Karate DSL</div>
          <div class="cert-provider">Udemy</div>
          <div class="cert-year">2023</div>
        </div>
        <div class="cert-card">
          <div class="cert-title">Rest API Automation</div>
          <div class="cert-provider">TestLeaf Software Solutions Pvt. Ltd.</div>
          <div class="cert-year">2023</div>
        </div>
        <div class="cert-card">
          <div class="cert-title">Selenium WebDriver</div>
          <div class="cert-provider">TestLeaf Software Solutions Pvt. Ltd.</div>
          <div class="cert-year">2022</div>
        </div>
        <div class="cert-card">
          <div class="cert-title">SQL for Data Science</div>
          <div class="cert-provider">Coursera</div>
          <div class="cert-year">2020</div>
        </div>
        <div class="cert-card">
          <div class="cert-title">SDET</div>
          <div class="cert-provider">Capgemini</div>
          <div class="cert-year">2020</div>
        </div>
      </div>
    </div>
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Awards & Recognitions</div>
      <div class="awards-grid">
        <div class="award-card">
          <div class="award-title">Spot Award</div>
          <div class="award-year">2022 & 2023</div>
          <div class="award-sub">InsurCloud – Deloitte, Canada</div>
        </div>
        <div class="award-card">
          <div class="award-title">Best Contributor</div>
          <div class="award-year">2018</div>
          <div class="award-sub">COMPASS Program – Hartford Insurance, USA</div>
        </div>
        <div class="award-card">
          <div class="award-title">QE & A Maestro</div>
          <div class="award-year">2017</div>
          <div class="award-sub">Centene by Cognizant QE&A, USA</div>
        </div>
        <div class="award-card">
          <div class="award-title">Pride of the Quarter</div>
          <div class="award-year">Q1 2017</div>
          <div class="award-sub">Health Net by Cognizant QE&A, USA</div>
        </div>
        <div class="award-card">
          <div class="award-title">Pillar of the Month</div>
          <div class="award-year">May 2014 & Aug 2015</div>
          <div class="award-sub">Health Net by Cognizant QE&A, USA</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- PROJECTS TAB ----
with tabs[1]:
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

# ---- EXPERIENCE TAB ----
with tabs[2]:
    st.markdown("""
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

# ---- SKILLS TAB ----
with tabs[3]:
    st.markdown(
    '''
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Core Skills & Tools</div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/python.svg" class="skill-icon"/> Programming Languages</div>
        <div class="skills-chips">
          <span class="skill-chip">Python</span>
          <span class="skill-chip">R</span>
          <span class="skill-chip">SQL</span>
          <span class="skill-chip">Java</span>
          <span class="skill-chip">VBA Macro</span>
        </div>
      </div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/pandas.svg" class="skill-icon"/> Data Analysis</div>
        <div class="skills-chips">
          <span class="skill-chip">Pandas</span>
          <span class="skill-chip">NumPy</span>
          <span class="skill-chip">Matplotlib</span>
        </div>
      </div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/powerbi.svg" class="skill-icon"/> Data Visualization</div>
        <div class="skills-chips">
          <span class="skill-chip">Power BI</span>
          <span class="skill-chip">Excel</span>
        </div>
      </div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/mysql.svg" class="skill-icon"/> Database Management</div>
        <div class="skills-chips">
          <span class="skill-chip">MySQL</span>
          <span class="skill-chip">Oracle</span>
          <span class="skill-chip">NoSQL</span>
        </div>
      </div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/git.svg" class="skill-icon"/> Version Control</div>
        <div class="skills-chips">
          <span class="skill-chip">Git</span>
        </div>
      </div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/jira.svg" class="skill-icon"/> Project Management</div>
        <div class="skills-chips">
          <span class="skill-chip">JIRA</span>
          <span class="skill-chip">ALM</span>
          <span class="skill-chip">Rally</span>
        </div>
      </div>
      <div class="skills-category">
        <div class="skills-header"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/selenium.svg" class="skill-icon"/> Automation & Insurance Suite</div>
        <div class="skills-chips">
          <span class="skill-chip">Selenium WebDriver</span>
          <span class="skill-chip">Guidewire</span>
        </div>
      </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# ---- CONTACT TAB ----
with tabs[4]:
    st.markdown(
        '''
        <div class="card hover-zoom">
        <div class="section-title" style="background:#34495E;">Contact</div>
        <div style="display:flex; justify-content:center; gap:16px; margin-top:10px;color:#ADD8E6">
        <a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon" /></a>
        <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon" /></a>
        <a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon" /></a>
        <a href="https://medium.com/@venkatesh.balusoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg" class="contact-icon" /></a>
        </div>
        <br>
        <div style="color:#fff;font-size:1.1rem;margin-top:12px;">
        Calgary, AB, Canada<br>
        Email: <a href="mailto:venkatesh.balusoundar@gmail.com" style="color:#ffd166;">venkatesh.balusoundar@gmail.com</a>
        </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
