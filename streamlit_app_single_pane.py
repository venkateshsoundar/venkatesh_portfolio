import streamlit as st
import streamlit.components.v1 as components
import requests
import io
import PyPDF2
import openai
import pandas as pd

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume data ---
def load_resume_df(url):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    records = []
    for i, page in enumerate(reader.pages):
        sentences = [s.strip() for s in (page.extract_text() or "").split('.') if s.strip()]
        for sent in sentences:
            records.append({"page": i+1, "sentence": sent})
    return pd.DataFrame(records)

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_df = load_resume_df(resume_url)
resume_json = resume_df.to_json(orient="records")

# --- Projects list ---
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/toronto-crime-drivers/main/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/weight-change-regression-analysis/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/calgary-childcare-compliance/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/social-media-purchase-influence/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/obesity-level-estimation/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/weather-data-pipeline-aws/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/gmail-sentiment-analysis/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/penguin-dataset-chatbot/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/uber-ride-duration-predictorapp/main/Uberride_Prediction.jpeg"}
]

# --- Embed AOS via components ---
aos_html = """
<link href='https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.css' rel='stylesheet'>
<script src='https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.js'></script>
<script>AOS.init({ duration: 800, once: false, mirror: true });</script>
"""
components.html(aos_html, height=0)

# --- Global CSS ---
st.markdown("""
<style>
.stApp { background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat; background-attachment: fixed; }
.card { background: rgba(31,42,68,0.7); border-radius:12px; padding:20px; margin:24px 0; color:#fff; }
.project-item { position:relative; border-radius:12px; overflow:hidden; }
.project-item img { width:100%; height:200px; object-fit:cover; transition:transform .3s ease; }
.project-item:hover img { transform:scale(1.05); }
.overlay { position:absolute; inset:0; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; color:#fff; opacity:0; transition:opacity .3s; }
.project-item:hover .overlay { opacity:1; }
nav { position:fixed; top:0; width:100%; background:rgba(31,42,68,0.9); padding:12px 36px; z-index:100; display:flex; gap:20px; }
nav a { color:#fff; text-decoration:none; }
.content { margin-top:60px; padding:0 24px; }
</style>
""", unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown("""
<nav>
  <a href='#welcome'>Welcome</a>
  <a href='#profile'>Profile</a>
  <a href='#contact'>Contact</a>
  <a href='#education'>Education</a>
  <a href='#certifications'>Certifications</a>
  <a href='#awards'>Awards</a>
  <a href='#experience'>Experience</a>
  <a href='#skills'>Skills</a>
  <a href='#chat'>Chat</a>
  <a href='#projects'>Projects</a>
</nav>
<div class='content'>
""", unsafe_allow_html=True)

# --- Render Sections with AOS ---
def render_card(idx, sec_id, title, content='', img_url=None):
    html = f"<div id='{sec_id}' class='card' data-aos='fade-up'>"
    html += f"<h2>{title}</h2>"
    if img_url:
        html += f"<img src='{img_url}' width='120' style='border-radius:50%;margin:12px 0;'/>"
    if content:
        html += f"<p>{content}</p>"
    html += "</div>"
    components.html(html, height=0)

# Section data
sections = [
    ('welcome','Welcome','Explore my portfolio to learn more about my work in data science, analytics, and technology.'),
    ('profile','Profile','',"https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"),
    ('contact','Contact','Email: venkatesh.balusoundar@gmail.com | LinkedIn | GitHub | Medium'),
    ('education','Education','Masters in Data Science and Analytics, University of Calgary (Sep 2024–Present); Bachelor of Engineering, Anna University (Aug 2009–May 2013)'),
    ('certifications','Certifications & Courses','Insurance & Guidewire Suite Analyst 10.0; Karate DSL; Rest API Automation; Selenium WebDriver; SQL for Data Science; SDET'),
    ('awards','Awards & Recognitions','Spot Award; Best Contributor; QE & A Maestro; Pride of the Quarter; Pillar of the Month'),
    ('experience','Professional Experience','Software Developer Intern (Tech Insights); Senior Consultant (Deloitte); Consultant (Capgemini); etc.'),
    ('skills','Core Skills & Tools','Python, R, SQL, Java, Pandas, NumPy, Power BI, Git, JIRA, Selenium, Guidewire'),
]
for idx, sec in enumerate(sections):
    render_card(idx, *sec)

# Chat card
chat_card = f"<div id='chat' class='card' data-aos='fade-up'><h2>Chat</h2><img src='https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif' style='width:100%;border-radius:12px;margin-bottom:12px;'/></div>"
components.html(chat_card, height=0)

api_key = st.secrets['DEEPSEEK_API_KEY']
client = openai.OpenAI(base_url='https://openrouter.ai/api/v1', api_key=api_key)
user_input = st.chat_input('Ask something...')
if user_input:
    st.chat_message('user').write(user_input)
    prompt = f"You are Venkatesh's assistant. Resume JSON: {resume_json}\nQuestion: {user_input}"
    with st.spinner('Assistant is typing...'):
        response = client.chat.completions.create(model='deepseek/deepseek-chat-v3-0324', messages=[{'role':'system','content':prompt}])
    st.chat_message('assistant').write(response.choices[0].message.content)

# Projects Gallery
projects_card = f"<div id='projects' class='card' data-aos='fade-up'><h2>Projects Gallery</h2></div>"
components.html(projects_card, height=0)
cols = st.columns(3)
for idx, proj in enumerate(projects):
    with cols[idx%3]:
        proj_html = f"<div class='project-item' data-aos='fade-up'><a href='{proj['url']}' target='_blank'><img src='{proj['image']}'/><div class='overlay'>{proj['title']}</div></a></div>"
        components.html(proj_html, height=0)

# Close content wrapper
st.markdown("</div>", unsafe_allow_html=True)
