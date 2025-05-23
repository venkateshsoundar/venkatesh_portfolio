import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# --- Page configuration ---
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
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/calgary-childcare-compliance/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/obesity-level-estimation/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/weather-data-pipeline-aws/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/gmail-sentiment-analysis/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/penguin-dataset-chatbot/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/uber-ride-duration-predictorapp/main/Uberride_Prediction.jpeg"}
]

# --- ANIMATIONS + CSS ---
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.js"></script>
<script>
    window.addEventListener('DOMContentLoaded', function() {
        if (window.AOS) {
            AOS.init({duration: 1100, once: false, mirror: true});
        }
    });
</script>
<style>
body, html { font-size: 22px !important; }
.stApp {background: #191e29;}
.hero-marquee-bg {
    background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif') center/cover no-repeat;
    border-radius: 0 0 36px 36px; min-height:340px;
    box-shadow: 0 10px 50px #1237;
    display: flex; flex-direction:column; align-items:center; justify-content:center; padding-top:55px; margin-bottom:35px;
    position:relative;
}
.marquee {
    width: 100vw; max-width:1400px; overflow: hidden; white-space: nowrap; margin-bottom:25px;
}
.marquee span {
    display: inline-block;
    padding-left: 100vw;
    font-size: 3.4rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 2px 12px #113a;
    animation: marqueeMove 14s linear infinite;
    letter-spacing:3px;
}
@keyframes marqueeMove {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-110vw, 0); }
}
.hero-desc {
    background: rgba(10,10,10,0.48);
    border-radius:22px; color: #f4e3b3; font-size:1.32rem; max-width:820px; margin:0 auto 12px auto; padding:19px 44px 12px 44px; text-align:center; box-shadow:0 2px 16px #3232;
}
.intro-card {
    background:linear-gradient(120deg, #3549a0 70%, #35cbe0 100%);
    border-radius: 22px;
    box-shadow: 0 4px 32px 0 rgba(30,40,90,.14);
    color: #fff; padding: 38px 48px;
    margin-bottom: 36px; display:flex; align-items:center; justify-content:space-between;
}
.intro-details {flex:2; text-align:left; padding-right:28px;}
.intro-details h2 {font-size:2.25rem;font-weight:700;margin-bottom:6px;}
.intro-details h4 {font-size:1.21rem;margin:8px 0;}
.intro-links a {color:#FFD700;margin-right:20px;font-size:1.25rem;}
.intro-profilepic {
    width:260px; height:260px; border-radius:50%; object-fit:cover;
    border:4px solid #fff; box-shadow:0 4px 40px #1138;
    background:#fff; margin-left:12px;
}
.section-card {
    background:linear-gradient(120deg, #252849 65%, #1976d2 100%);
    border-radius: 18px;
    margin: 40px 0 30px 0;
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
/* --- Horizontal timeline for education/experience --- */
.timeline-horiz {
    display:flex; flex-wrap:wrap; align-items:center; justify-content:center; margin:36px 0;
    width:100%; max-width:1240px; margin-left:auto; margin-right:auto;
}
.timeline-block {
    background:linear-gradient(120deg,#223363 60%,#20bde3 100%);
    border-radius:18px; min-width:260px; max-width:320px; padding:22px 16px;
    margin:0 16px; color:#fff; text-align:center; position:relative;
    box-shadow:0 2px 14px #1128;
    transition:transform .25s;
    z-index:2;
}
.timeline-block[data-aos] { opacity:0; transform:translateY(60px);}
.timeline-block.aos-animate { opacity:1; transform:translateY(0);}
.timeline-block .tl-title {font-weight:700; font-size:1.2rem; margin-bottom:6px;}
.timeline-block .tl-org {color:#ffd166; font-size:1.08rem;}
.timeline-block .tl-dates {font-size:1.01rem; color:#f1eeb7;}
.timeline-bar {
    flex:1; height:6px; background:linear-gradient(90deg,#ffd166,#1976d2); border-radius:4px; margin:0 6px; min-width:20px; z-index:1;
}
@media (max-width:900px) {
    .intro-card {flex-direction:column-reverse; text-align:center;}
    .intro-details {padding-right:0;}
    .intro-profilepic {margin-left:0;margin-bottom:20px;}
    .timeline-horiz {flex-direction:column;}
    .timeline-bar {display:none;}
    .timeline-block {margin:14px 0;}
}
.chatbot-gif-bg {
    background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif') center/cover no-repeat;
    border-radius: 20px; padding:32px 34px;
    margin-top:36px; margin-bottom:30px;
    min-height:220px;
    box-shadow:0 4px 30px #2039;
    display: flex; align-items: center;
}
</style>
""", unsafe_allow_html=True)

# --- HERO BANNER with MARQUEE and GIF background ---
st.markdown("""
<div class="hero-marquee-bg" data-aos="fade-down">
  <div class="marquee"><span>Welcome to My Portfolio! &nbsp; 🚀 Data, Analytics & Impact! &nbsp;|&nbsp; Hello, I'm Venkatesh! &nbsp;|&nbsp; Let's create together. &nbsp;</span></div>
  <div class="hero-desc">
    I'm Venkatesh, a Data Science and Analytics enthusiast.<br>
    Explore my journey, projects, and experience.
  </div>
</div>
""", unsafe_allow_html=True)

# --- INTRO CARD (profile pic right) ---
st.markdown(f"""
<div class="intro-card" data-aos="fade-left">
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

# --- HORIZONTAL TIMELINE (Education + Experience) ---
st.markdown("""
<div class="section-card" style="padding-bottom:12px;">
  <div class="section-head">Education & Experience Timeline</div>
  <div class="timeline-horiz">
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Masters in Data Science & Analytics</div>
      <div class="tl-org">University of Calgary</div>
      <div class="tl-dates">2024 – Present</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">B.E., Engineering</div>
      <div class="tl-org">Anna University</div>
      <div class="tl-dates">2009 – 2013</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Software Developer Intern</div>
      <div class="tl-org">Tech Insights</div>
      <div class="tl-dates">2025 – Present</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Senior Consultant</div>
      <div class="tl-org">Deloitte</div>
      <div class="tl-dates">2024</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Consultant</div>
      <div class="tl-org">Deloitte</div>
      <div class="tl-dates">2021 – 2024</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Consultant</div>
      <div class="tl-org">Capgemini</div>
      <div class="tl-dates">2018 – 2021</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Associate</div>
      <div class="tl-org">Cognizant</div>
      <div class="tl-dates">2016 – 2018</div>
    </div>
    <div class="timeline-bar"></div>
    <div class="timeline-block" data-aos="zoom-in">
      <div class="tl-title">Programmer Analyst</div>
      <div class="tl-org">Cognizant</div>
      <div class="tl-dates">2013 – 2018</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Certifications & Awards ---
st.markdown("""
<div class="section-card" data-aos="fade-up">
  <div class="section-head">Certifications & Awards</div>
  <b>Certifications:</b> Insurance & Guidewire Suite Analyst 10.0 | Karate DSL | Rest API Automation | Selenium WebDriver | SQL for Data Science | SDET <br><br>
  <b>Awards:</b> Spot Award • Best Contributor • QE & A Maestro • Pride of the Quarter • Pillar of the Month
</div>
""", unsafe_allow_html=True)

# --- Skills ---
st.markdown("""
<div class="section-card" data-aos="fade-up">
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

# --- Projects Gallery (Grid) ---
st.markdown('<div class="section-card" data-aos="fade-up"><div class="section-head" style="font-size:2rem;">Projects Gallery</div></div>', unsafe_allow_html=True)
grid_html = '<div class="grid-container">'
for proj in projects:
    grid_html += (
        f'<div class="project-card" data-aos="flip-right">'
        f'  <a href="{proj["url"]}" target="_blank" style="text-decoration:none;">'
        f'    <img src="{proj["image"]}" class="project-img"/>'
        f'    <div style="font-size:1.21rem;font-weight:600;margin-top:13px;">{proj["title"]}</div>'
        f'  </a>'
        f'</div>'
    )
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

# --- Chatbot with GIF Background ---
ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
st.markdown(
    f"""
    <div class="chatbot-gif-bg" data-aos="fade-up">
        <h2 style="flex:1;color:#ffd166;font-size:2.1rem;text-shadow:0 3px 15px #3338;">Ask Buddy Bot!</h2>
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
