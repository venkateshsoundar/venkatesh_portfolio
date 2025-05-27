import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# ---- PAGE CONFIG & GLOBAL CSS ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# ---- ANIMATION CSS ----
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
}
.nav-bar {
    display: flex;
    justify-content: center;
    gap: 32px;
    background: rgba(44,62,80,0.96);
    padding: 14px 0 10px 0;
    border-radius: 0 0 20px 20px;
    position: sticky;
    top: 0;
    z-index: 999;
    margin-bottom: 35px;
}
.nav-link {
    background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
    color: #ffd166 !important;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.11rem;
    letter-spacing: 1px;
    padding: 11px 30px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(44,62,80,0.12);
    transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s, background .18s;
    display: inline-block;
    margin-bottom: 0;
    scroll-behavior: smooth;
}
.nav-link:hover, .nav-link:focus {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 8px 16px rgba(0,0,0,0.22);
    background: linear-gradient(135deg, #406496 0%, #22304A 100%);
    color: #fff !important;
    text-decoration: none;
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
/* Add all .edu-card, .exp-card, .cert-card, .skills-chips, etc., CSS from previous file here... */
/* --- Education Cards --- */
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
.contact-icon {
  width: 32px;
  height: 32px;
  filter: invert(100%);
  color:#ADD8E6;
  margin: 0 8px;
  vertical-align: middle;
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
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg"}
]

# ---- NAVIGATION BAR ----
st.markdown("""
<div class="nav-bar">
    <a class="nav-link" href="#welcome">Home</a>
    <a class="nav-link" href="#about">About</a>
    <a class="nav-link" href="#education">Education</a>
    <a class="nav-link" href="#certifications">Certifications</a>
    <a class="nav-link" href="#awards">Awards</a>
    <a class="nav-link" href="#projects">Projects</a>
    <a class="nav-link" href="#experience">Experience</a>
    <a class="nav-link" href="#skills">Skills</a>
    <a class="nav-link" href="#contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# ---- SECTIONS ----

# -- Welcome --
st.markdown('<a id="welcome"></a>', unsafe_allow_html=True)
gif_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif"
st.markdown(
    f"""
    <div class="welcome-card animate__animated animate__fadeInUp" style="background: url('{gif_url}') center/cover no-repeat;">
      <div>
        <h1>Hello and Welcome...</h1>
        <p>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -- Chatbot (animated) --
ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
st.markdown('<a id="chatbot"></a>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="welcome-card2 animate__animated animate__fadeInUp" style="background: url('{ai_url}') center/cover no-repeat;">
      <div class="text-container" style="position: absolute; top: 70%; right: 2rem; transform: translateY(-50%); text-align: right;">
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

# -- About Me --
st.markdown('<a id="about"></a>', unsafe_allow_html=True)
st.markdown("""
<style>
.profile-row {
  display: flex;
  gap: 38px;
  justify-content: center;
  align-items: stretch;
  margin-bottom: 32px;
  margin-top: 14px;
}
.profile-card-fancy, .about-card-fancy {
  flex: 1 1 0px;
  min-width: 260px;
  background: linear-gradient(135deg, #253451 0%, #334869 100%);
  border-radius: 26px;
  padding: 38px 28px 28px 28px;
  box-shadow: 0 7px 28px rgba(20,30,55,0.20), 0 2px 14px rgba(44,62,80,0.09);
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  animation: fadeUpCard .9s cubic-bezier(.5,1.6,.4,1) both;
}
.profile-card-fancy {
  max-width: 400px;
  justify-content: flex-start;
  text-align: center;
  align-items: center;
}
.profile-glow {
  width: 145px;
  height: 145px;
  border-radius: 24px;
  margin-bottom: 18px;
  box-shadow: 0 0 0 6px #ffd16688, 0 0 22px 8px #ffd16655, 0 2px 14px rgba(44,62,80,0.09);
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
}
.profile-pic-square {
  width: 135px;
  height: 135px;
  object-fit: cover;
  border-radius: 20px;
  border: 2.5px solid #fff;
  background: #fff;
}
.profile-card-fancy h2 {
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  margin: 14px 0 8px 0;
}
.profile-title {
  color: #ADD8E6;
  font-size: 1.07rem;
  margin-bottom: 2px;
}
.profile-role {
  color: #c6e6ff;
  font-size: 1rem;
  font-weight: 500;
}
.profile-location {
  color: #ffd166;
  font-weight: 600;
  margin-top: 11px;
  font-size: 1.11rem;
  letter-spacing: 0.04em;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}
.about-card-fancy {
  align-items: flex-start;
  justify-content: flex-start;
  text-align: left;
  padding-left: 44px;
  padding-right: 36px;
}
.about-title {
  font-weight: 700;
  font-size: 1.22rem;
  color: #ffd166;
  margin-bottom: 16px;
  margin-top: 0;
  letter-spacing: .01em;
}
.about-body {
  font-size: 1.11rem;
  color: #f9f9f9;
  line-height: 1.85;
  letter-spacing: 0.01em;
}
@media (max-width: 1100px) {
  .about-card-fancy {padding-left:24px;padding-right:16px;}
  .profile-card-fancy {padding:28px 14px 18px;}
}
@media (max-width: 900px) {
  .profile-row {flex-direction: column;gap: 18px;}
  .about-card-fancy, .profile-card-fancy {width: 100%;min-width: 0;}
  .about-card-fancy {padding-left:18px;padding-right:14px;}
}
</style>
<div class="profile-row">
  <div class="profile-card-fancy" style="animation-delay:0.08s;">
    <div class="profile-glow">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic-square" />
    </div>
    <h2>Venkatesh<br>Soundararajan</h2>
    <div class="profile-title">Software Development Intern</div>
    <div class="profile-role">Data Engineering</div>
    <div class="profile-location">
      <span style="font-size:1.23rem;">&#127799;</span>
      Calgary, AB, Canada
    </div>
  </div>
  <div class="about-card-fancy" style="animation-delay:0.16s;">
    <div class="about-title">About Me</div>
    <div class="about-body">
      I’m Venkatesh, a Data Scientist and Software Developer with <b>8+ years of experience</b> in quality engineering, business intelligence, and analytics.<br><br>
      I specialize in building <b>scalable ETL pipelines</b>, predictive models, and interactive dashboards using cloud platforms like <b>AWS and Azure</b>.<br><br>
      I'm currently pursuing my Master's in Data Science and Analytics at the <b>University of Calgary</b>.<br>
      My passion lies in solving complex business problems with clean, actionable insights and AI-powered solutions.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# -- Education --
st.markdown('<a id="education"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom animate__animated animate__fadeInUp">
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
""", unsafe_allow_html=True)

# -- Certifications --
st.markdown('<a id="certifications"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom animate__animated animate__fadeInUp">
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
""", unsafe_allow_html=True)

# -- Awards & Recognitions --
st.markdown('<a id="awards"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom animate__animated animate__fadeInUp">
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
>>>>>>> b2b15f39c91e321f8c81eeaf895f924908c3be40
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
""", unsafe_allow_html=True)

# -- Projects Gallery --
st.markdown('<a id="projects"></a>', unsafe_allow_html=True)
st.markdown('<div class="card hover-zoom animate__animated animate__fadeInUp"><div class="section-title" style="background:#2C3E50;">Projects Gallery</div></div>', unsafe_allow_html=True)
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

# -- Experience --
st.markdown('<a id="experience"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom animate__animated animate__fadeInUp">
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

# -- Skills --
st.markdown('<a id="skills"></a>', unsafe_allow_html=True)
st.markdown(
'''
<div class="card hover-zoom animate__animated animate__fadeInUp">
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

# -- Contact --
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="card hover-zoom animate__animated animate__fadeInUp">
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