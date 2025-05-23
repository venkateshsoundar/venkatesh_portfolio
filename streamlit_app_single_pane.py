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

# --- Projects ---
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

# --- Large CSS & Animation ---
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 20px !important;
    line-height: 1.65 !important;
}
.stApp {
    background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat fixed;
    font-family: 'Poppins', Arial, sans-serif;
}
.card {
    background: linear-gradient(120deg, #252849 65%, #1976d2 100%);
    border-radius: 22px;
    margin: 32px 0 32px 0;
    box-shadow: 0 4px 32px 0 rgba(30,40,90,.11);
    color: #fff;
    padding: 40px 42px 32px 42px;
    transition: box-shadow 0.2s, transform 0.22s;
    border: 2.5px solid #21587a22;
}
.card:hover {box-shadow:0 12px 38px 0 #15386b45; transform: translateY(-2px) scale(1.023);}
.section-head {font-size:2.1rem; font-weight:700; letter-spacing:.6px; color:#ffd166; margin-bottom:19px;}
.profilepic {
    width:180px; height:180px; border-radius:50%; object-fit:cover; border:3px solid #fff; margin:0 auto 18px auto; display:block; box-shadow:0 3px 20px #2223;
}
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 28px 28px;
    margin-bottom: 20px;
    margin-top: 8px;
}
.project-card {
    background:linear-gradient(120deg,#212647 60%,#1976d2 100%);
    border-radius:17px; box-shadow:0 2px 16px 0 #1233;
    padding:18px 13px 16px 13px; text-align:center;
    transition:box-shadow .18s, transform .18s;
    border: 2px solid #21587a22;
}
.project-card:hover {box-shadow:0 8px 40px #2349b933; transform:scale(1.037);}
.project-img {
    width:99%; max-width:420px; aspect-ratio:4/3;
    border-radius:15px; margin-bottom:12px; object-fit:cover;
    box-shadow:0 5px 22px #0004; opacity:0; transform:translateY(24px) scale(.95);
    animation:fadeinproj 1.1s cubic-bezier(.3,.71,.36,1.3) forwards;
}
@keyframes fadeinproj {to{opacity:1;transform:translateY(0) scale(1);}}
.skill-badge {
    display:inline-block; background:#ffd16644; color:#fff;
    border-radius:11px; padding:10px 24px; margin:3px 10px 7px 0;
    font-size:1.25rem; font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# --- Profile Card ---
st.markdown(f"""
<div class="card" style="background: linear-gradient(120deg,#364875 70%,#5ab5e6 100%); text-align:center;">
    <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profilepic"/>
    <div class="section-head">Venkatesh Soundararajan</div>
    <span style="color:#ffd166; font-size:1.4rem;">Software Development Intern, Tech Insights</span><br>
    <span style="color:#c0deff; font-size:1.1rem;">Calgary, AB, Canada</span>
</div>
""", unsafe_allow_html=True)

# --- Contact Card ---
st.markdown("""
<div class="card" style="background:linear-gradient(100deg,#246bb2 70%,#324665 100%);font-size:1.3rem;">
  <div class="section-head">Contact</div>
  <a href="mailto:venkatesh.balusoundar@gmail.com" style="color:#ffd166;">venkatesh.balusoundar@gmail.com</a>
  &nbsp;|&nbsp;
  <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank" style="color:#FFD700;">LinkedIn</a>
  &nbsp;|&nbsp;
  <a href="https://github.com/venkateshsoundar" target="_blank" style="color:#c0deff;">GitHub</a>
  &nbsp;|&nbsp;
  <a href="https://medium.com/@venkatesh.balusoundar" target="_blank" style="color:#ffd166;">Medium</a>
</div>
""", unsafe_allow_html=True)

# --- Education Card ---
st.markdown("""
<div class="card" style="background:linear-gradient(115deg,#21256e 60%,#2d769c 100%);font-size:1.18rem;">
  <div class="section-head">Education</div>
  <b>Masters in Data Science and Analytics</b> – University of Calgary (Sep 2024–Present)<br>
  <b>Bachelor of Engineering</b> – Anna University (Aug 2009–May 2013)
</div>
""", unsafe_allow_html=True)

# --- Certifications Card ---
st.markdown("""
<div class="card" style="background:linear-gradient(108deg,#26324a 68%,#4a9de0 100%);font-size:1.15rem;">
  <div class="section-head">Certifications & Courses</div>
  Insurance & Guidewire Suite Analyst 10.0 &nbsp; | &nbsp; Karate DSL &nbsp; | &nbsp; Rest API Automation<br>
  Selenium WebDriver &nbsp; | &nbsp; SQL for Data Science &nbsp; | &nbsp; SDET
</div>
""", unsafe_allow_html=True)

# --- Awards Card ---
st.markdown("""
<div class="card" style="background:linear-gradient(105deg,#2e2244 65%,#b788e6 100%);font-size:1.13rem;">
  <div class="section-head">Awards & Recognitions</div>
  Spot Award • Best Contributor • QE & A Maestro • Pride of the Quarter • Pillar of the Month
</div>
""", unsafe_allow_html=True)

# --- Skills Card ---
st.markdown("""
<div class="card" style="background:linear-gradient(111deg,#21374a 65%,#08b4ce 100%);">
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

# --- Experience Card ---
st.markdown("""
<div class="card" style="background:linear-gradient(115deg,#1e223c 68%,#7bc7e7 100%);font-size:1.19rem;">
  <div class="section-head">Professional Experience</div>
  <b>Software Developer Intern</b> (Tech Insights, 2025–Present)<br>
  <b>Senior Consultant</b> (Deloitte, 2024)<br>
  <b>Consultant</b> (Deloitte, 2021–24)<br>
  <b>Consultant</b> (Capgemini, 2018–21)<br>
  <b>Associate</b> (Cognizant, 2016–18)<br>
  <b>Programmer Analyst</b> (Cognizant, 2013–18)
</div>
""", unsafe_allow_html=True)

# --- Welcome Card with GIF ---
gif_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif"
st.markdown(
    f"""
    <div class="card" style="background:linear-gradient(110deg,#224870 68%,#e0b04a 100%); text-align:center;">
      <div class="section-head" style="font-size:2.5rem;">Hello and Welcome...</div>
      <img src="{gif_url}" width="390" style="margin:24px auto 0 auto; border-radius:18px; box-shadow:0 4px 32px #2226;">
      <p style="margin-top:15px;font-size:1.32rem;">Explore my portfolio to learn more about my work in data science, analytics, and technology.<br>
      Let’s connect and create something impactful together.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Chatbot Banner ---
ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
st.markdown(
    f"""
    <div class="card" style="background:linear-gradient(107deg,#3d2556 55%,#6495ed 100%); padding:0;">
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

# --- Projects Gallery (Grid) ---
st.markdown('<div class="card" style="background:linear-gradient(109deg,#223363 65%,#57c0e3 100%);"><div class="section-head" style="font-size:2.2rem;">Projects Gallery</div></div>', unsafe_allow_html=True)
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
