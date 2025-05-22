import streamlit as st
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
        for sent in [s.strip() for s in (page.extract_text() or "").split('.') if s.strip()]:
            records.append({"page": i+1, "sentence": sent})
    return pd.DataFrame(records)

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
)
resume_df = load_resume_df(resume_url)
resume_json = resume_df.to_json(orient="records")

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
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg"}
]

# --- CSS & Animations ---
st.markdown(r"""
<style>
/* Background */
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
}
/* AOS Animations */
@import url('https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.css');
[data-aos] {
  opacity: 0;
  transition-property: opacity, transform;
}
[data-aos].aos-animate {
  opacity: 1;
  transform: translateY(0);
}
[data-aos="fade-up"] {
  transform: translateY(30px);
}
</style>
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.js"></script>
<script>
  AOS.init({ duration: 800, once: false, mirror: true });
</script>
""", unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown(r"""
<nav style="position:fixed;top:0;width:100%;background:rgba(31,42,68,0.9);padding:12px 36px;z-index:100;display:flex;gap:20px;">
  <a href="#welcome" style="color:#fff;text-decoration:none;">Welcome</a>
  <a href="#profile" style="color:#fff;text-decoration:none;">Profile</a>
  <a href="#contact" style="color:#fff;text-decoration:none;">Contact</a>
  <a href="#education" style="color:#fff;text-decoration:none;">Education</a>
  <a href="#certifications" style="color:#fff;text-decoration:none;">Certifications</a>
  <a href="#awards" style="color:#fff;text-decoration:none;">Awards</a>
  <a href="#experience" style="color:#fff;text-decoration:none;">Experience</a>
  <a href="#skills-tools" style="color:#fff;text-decoration:none;">Skills</a>
  <a href="#chat" style="color:#fff;text-decoration:none;">Chat</a>
  <a href="#projects-gallery" style="color:#fff;text-decoration:none;">Projects</a>
</nav>
<div style="margin-top:60px;padding:0 24px;">
""", unsafe_allow_html=True)

# --- Sections in Cards with AOS ---
sections = [
    ("welcome", "Welcome", "Explore my portfolio to learn more about my work in data science, analytics, and technology."),
    ("profile", "Profile", None),
    ("contact", "Contact", "Email | LinkedIn | GitHub | Medium"),
    ("education", "Education", "Masters in Data Science and Analytics, University of Calgary (Sep 2024–Present); Bachelor of Engineering, Anna University (Aug 2009–May 2013)"),
    ("certifications", "Certifications & Courses", "Insurance & Guidewire Suite Analyst 10.0; Karate DSL; Rest API Automation; Selenium WebDriver; SQL for Data Science; SDET"),
    ("awards", "Awards & Recognitions", "Spot Award; Best Contributor; QE & A Maestro; Pride of the Quarter; Pillar of the Month"),
    ("experience", "Professional Experience", "Software Developer Intern (Tech Insights); Senior Consultant (Deloitte); Consultant (Capgemini); etc."),
    ("skills-tools", "Core Skills & Tools", "Python, R, SQL, Java, Pandas, NumPy, Power BI, Git, JIRA, Selenium, Guidewire"),
]
for idx, (sec_id, title, content) in enumerate(sections):
    html = f'<div id="{sec_id}" class="card" data-aos="fade-up"><h2>{title}</h2>'
    if content:
        html += f'<p>{content}</p>'
    if sec_id == "profile":
        html += '<img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" width="120" style="border-radius:50%;margin:12px 0;"/>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- Chat Section ---
chat_html = '<div id="chat" class="card" data-aos="fade-up"><h2>Chat</h2>' + \
            '<img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif" style="width:100%;border-radius:12px;margin-bottom:12px;"/>' + \
            '</div>'
st.markdown(chat_html, unsafe_allow_html=True)
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
user_input = st.chat_input("Ask something...")
if user_input:
    st.chat_message("user").write(user_input)
    prompt = (
        "You are Venkatesh's professional assistant. Here is his resume data as JSON:\n" + resume_json +
        "\n\nAnswer the question based only on this JSON. If you can't, say you don't know.\nQuestion: " + user_input
    )
    with st.spinner("Assistant is typing..."):
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[{"role":"system","content":prompt}]
        )
        st.chat_message("assistant").write(response.choices[0].message.content)

# --- Projects Gallery ---
st.markdown(f'<div id="projects-gallery" class="card" data-aos="fade-up"><h2>Projects Gallery</h2></div>', unsafe_allow_html=True)
cols = st.columns(3)
for idx, proj in enumerate(projects):
    with cols[idx % 3]:
        proj_html = f'<div class="project-item" data-aos="fade-up"><a href="{proj["url"]}" target="_blank">'
        proj_html += f'<img src="{proj["image"]}"/>'
        proj_html += f'<div class="overlay">{proj["title"]}</div></a></div>'
        st.markdown(proj_html, unsafe_allow_html=True)

# --- Close wrapper ---
st.markdown('</div>', unsafe_allow_html=True)
