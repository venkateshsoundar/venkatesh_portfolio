import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Resume Data ---
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

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_df = load_resume_df(resume_url)
resume_json = resume_df.to_json(orient='records')

projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/obesity-level-estimation/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/gmail-sentiment-analysis/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/penguin-dataset-chatbot/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/uber-ride-duration-predictorapp/main/Uberride_Prediction.jpeg"}
]

# --- STYLES ---
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 22px !important;
}
.stApp {background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat fixed;}
.hero-banner {
    background:linear-gradient(105deg,#224870 60%,#e0b04a 100%);
    padding:48px 0 40px 0;
    text-align:center;
    margin-bottom:18px;
    border-radius:0 0 32px 32px;
    box-shadow:0 7px 34px #2232;
}
.hero-banner h1 {color:#fff;font-size:3.1rem;font-weight:800;letter-spacing:1.5px;margin-bottom:18px;}
.hero-banner p {color:#f8f9fb;font-size:1.37rem;}
.intro-card {
    background:linear-gradient(120deg, #3549a0 70%, #35cbe0 100%);
    border-radius: 22px;
    box-shadow: 0 4px 32px 0 rgba(30,40,90,.14);
    color: #fff;
    padding: 34px 36px 34px 36px;
    margin-bottom: 34px;
    display:flex; align-items:center; justify-content:space-between;
}
.intro-details {flex:2; text-align:left; padding-right:18px;}
.intro-details h2 {font-size:2.25rem;font-weight:700;margin-bottom:6px;}
.intro-details h4 {font-size:1.21rem;margin:8px 0;}
.intro-links a {color:#FFD700;margin-right:20px;font-size:1.25rem;}
.intro-profilepic {
    width:200px; height:200px; border-radius:50%; object-fit:cover;
    border:4px solid #fff; box-shadow:0 4px 32px #1126;
    background:#fff;
}
.section-card {
    background:linear-gradient(120deg, #252849 65%, #1976d2 100%);
    border-radius: 18px;
    margin: 30px 0 26px 0;
    box-shadow: 0 2px 18px 0 rgba(30,40,90,.13);
    color: #fff;
    padding: 28px 34px 22px 34px;
}
.section-head {font-size:1.5rem; font-weight:700; color:#ffd166; margin-bottom:19px;}
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 28px 28px;
    margin-bottom: 10px;
    margin-top: 8px;
}
.project-card {
    background:linear-gradient(120deg,#212647 60%,#1976d2 100%);
    border-radius:15px; box-shadow:0 2px 16px 0 #1233;
    padding:16px 13px 16px 13px; text-align:center;
    transition:box-shadow .18s, transform .18s;
    border: 2px solid #21587a22;
}
.project-card:hover {box-shadow:0 8px 40px #2349b933; transform:scale(1.037);}
.project-img {
    width:99%; max-width:420px; aspect-ratio:4/3;
    border-radius:12px; margin-bottom:10px; object-fit:cover;
    box-shadow:0 5px 22px #0004; opacity:0; transform:translateY(24px) scale(.97);
    animation:fadeinproj 1.1s cubic-bezier(.3,.71,.36,1.3) forwards;
}
@keyframes fadeinproj {to{opacity:1;transform:translateY(0) scale(1);}}
.skill-badge {
    display:inline-block; background:#ffd16644; color:#fff;
    border-radius:11px; padding:10px 24px; margin:3px 10px 7px 0;
    font-size:1.25rem; font-weight:600;
}
.timeline {
    position:relative;
    margin-left:0;
    padding-left:24px;
    border-left:4px solid #ffd166;
}
.timeline-entry {
    margin-bottom:32px;
    position:relative;
}
.timeline-dot {
    position:absolute; left:-35px; top:5px;
    width:20px;height:20px; background:#FFD166; border-radius:50%; border:3.5px solid #223363;
    box-shadow:0 2px 8px #1234;
}
.timeline-title {font-weight:700; font-size:1.25rem;}
.timeline-sub {color:#ffd166;font-size:1.08rem;}
.timeline-dates {color:#c0deff;font-size:1.02rem;}
</style>
""", unsafe_allow_html=True)

# --- HERO BANNER ---
st.markdown(f"""
<div class="hero-banner">
  <h1>Welcome to My Portfolio!</h1>
  <p>I'm Venkatesh, a Data Science and Analytics enthusiast.<br>
  Explore my journey, projects, and experience.</p>
</div>
""", unsafe_allow_html=True)

# --- INTRO CARD (profile pic right) ---
st.markdown(f"""
<div class="intro-card">
  <div class="intro-details">
    <h2>Venkatesh Soundararajan</h2>
    <h4>Software Development Intern, Tech Insights<br>
    <span style="color:#FFD166;">Calgary, AB, Canada</span></h4>
    <p style="font-size:1.13rem; color:#f9f9f9; margin:20px 0 14px 0;">
      Passionate about leveraging data to solve real-world problems. Skilled in analytics, automation, and building end-to-end data solutions.<br>
      Let's connect and create meaningful impact together!
    </p>
    <div class="intro-links">
      <a href="mailto:venkatesh.balusoundar@gmail.com">Email</a>
      <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank">LinkedIn</a>
      <a href="https://github.com/venkateshsoundar" target="_blank">GitHub</a>
      <a href="https://medium.com/@venkatesh.balusoundar" target="_blank">Medium</a>
    </div>
  </div>
  <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="intro-profilepic"/>
</div>
""", unsafe_allow_html=True)

# --- Education Card ---
st.markdown("""
<div class="section-card">
  <div class="section-head">Education</div>
  <b>Masters in Data Science and Analytics</b> – University of Calgary (Sep 2024–Present)<br>
  <b>Bachelor of Engineering</b> – Anna University (Aug 2009–May 2013)
</div>
""", unsafe_allow_html=True)

# --- Certifications Card ---
st.markdown("""
<div class="section-card">
  <div class="section-head">Certifications & Courses</div>
  Insurance & Guidewire Suite Analyst 10.0 &nbsp; | &nbsp; Karate DSL &nbsp; | &nbsp; Rest API Automation<br>
  Selenium WebDriver &nbsp; | &nbsp; SQL for Data Science &nbsp; | &nbsp; SDET
</div>
""", unsafe_allow_html=True)

# --- Awards Card ---
st.markdown("""
<div class="section-card">
  <div class="section-head">Awards & Recognitions</div>
  Spot Award • Best Contributor • QE & A Maestro • Pride of the Quarter • Pillar of the Month
</div>
""", unsafe_allow_html=True)

# --- Skills Card ---
st.markdown("""
<div class="section-card">
  <div class="section-head">Skills & Tools</div>
  <span class="skill-badge">Python</span>
  <span class="skill-badge">R</span>
  <span class="skill-badge">SQL</span>
  <span class="skill-badge">Java</span>
  <span class="skill-badge">Pandas</span>
  <span class="skill-badge">NumPy</span>
  <span class="skill-badge">Power BI</span>
  <span class="skill-badge">Git</span>
  <span class="skill-badge">JIRA</span>
  <span class="skill-badge">Selenium</span>
  <span class="skill-badge">Guidewire</span>
</div>
""", unsafe_allow_html=True)

# --- Timeline/Experience Card ---
st.markdown("""
<div class="section-card">
  <div class="section-head">Professional Experience</div>
  <div class="timeline">
    <div class="timeline-entry">
      <div class="timeline-dot"></div>
      <div class="timeline-title">Software Developer Intern</div>
      <div class="timeline-sub">Tech Insights</div>
      <div class="timeline-dates">2025–Present</div>
    </div>
    <div class="timeline-entry">
      <div class="timeline-dot"></div>
      <div class="timeline-title">Senior Consultant</div>
      <div class="timeline-sub">Deloitte</div>
      <div class="timeline-dates">2024</div>
    </div>
    <div class="timeline-entry">
      <div class="timeline-dot"></div>
      <div class="timeline-title">Consultant</div>
      <div class="timeline-sub">Deloitte</div>
      <div class="timeline-dates">2021–24</div>
    </div>
    <div class="timeline-entry">
      <div class="timeline-dot"></div>
      <div class="timeline-title">Consultant</div>
      <div class="timeline-sub">Capgemini</div>
      <div class="timeline-dates">2018–21</div>
    </div>
    <div class="timeline-entry">
      <div class="timeline-dot"></div>
      <div class="timeline-title">Associate</div>
      <div class="timeline-sub">Cognizant</div>
      <div class="timeline-dates">2016–18</div>
    </div>
    <div class="timeline-entry">
      <div class="timeline-dot"></div>
      <div class="timeline-title">Programmer Analyst</div>
      <div class="timeline-sub">Cognizant</div>
      <div class="timeline-dates">2013–18</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Add a sample visualization (replace with your actual data!) ---
import numpy as np
import matplotlib.pyplot as plt

st.markdown("""
<div class="section-card">
  <div class="section-head">Sample Visualization</div>
""", unsafe_allow_html=True)
x = np.linspace(0, 10, 100)
y = np.sin(x)
fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(x, y, linewidth=3)
ax.set_title("Sine Wave Example", fontsize=18)
ax.grid(True, alpha=0.3)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# --- Projects Gallery (Grid) ---
st.markdown('<div class="section-card"><div class="section-head" style="font-size:2rem;">Projects Gallery</div></div>', unsafe_allow_html=True)
grid_html = '<div class="grid-container">'
for proj in projects:
    grid_html += (
        f'<div class="project-card">'
        f'  <a href="{proj["url"]}" target="_blank" style="text-decoration:none;">'
        f'    <img src="{proj["image"]}" class="project-img"/>'
        f'    <div style="font-size:1.21rem;font-weight:600;margin-top:13px;">{proj["title"]}</div>'
        f'  </a>'
        f'</div>'
    )
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

# --- Chatbot Banner ---
ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
st.markdown(
    f"""
    <div class="section-card" style="background:linear-gradient(107deg,#3d2556 55%,#6495ed 100%); padding:0;">
      <div style="display:flex;align-items:center;">
        <img src="{ai_url}" width="160" style="margin:18px 40px 18px 18px; border-radius:12px;">
        <h2 style="flex:1;color:#ffd166;font-size:2.1rem;">Ask Buddy Bot!</h2>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Chatbot (stateless, no history) ---
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
