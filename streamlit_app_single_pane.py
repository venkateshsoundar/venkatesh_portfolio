import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Global Background from original code ---
st.markdown(r"""
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar CSS and HTML ---
st.markdown(r"""
<style>
  nav {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(31, 42, 68, 0.9);
    padding: 8px 24px;
    z-index: 100;
    display: flex;
    gap: 16px;
    align-items: center;
  }
  nav a {
    color: #ffffff;
    text-decoration: none;
    font-weight: 500;
  }
  .content {
    margin-top: 60px;
    padding: 0 24px;
  }
  .card {
    background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    color: #ffffff;
    opacity: 0;
    transform: translateY(30px);
    animation: fadeInUp 0.8s ease forwards;
  }
  .card:nth-child(1) { animation-delay: 0.2s; }
  .card:nth-child(2) { animation-delay: 0.4s; }
  .card:nth-child(3) { animation-delay: 0.6s; }
  .card:nth-child(4) { animation-delay: 0.8s; }
  .card:nth-child(5) { animation-delay: 1s; }
  .card:nth-child(6) { animation-delay: 1.2s; }
  .card:nth-child(7) { animation-delay: 1.4s; }
  .card:nth-child(8) { animation-delay: 1.6s; }
  .card:nth-child(9) { animation-delay: 1.8s; }
  .card:nth-child(10){ animation-delay: 2s; }
  @keyframes fadeInUp {
    to { opacity: 1; transform: translateY(0); }
  }
  .project-item {
    position: relative;
    overflow: hidden;
    border-radius: 12px;
  }
  .project-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform .3s ease;
  }
  .project-item:hover img {
    transform: scale(1.05);
  }
  .project-item .overlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    opacity: 0;
    transition: opacity .3s ease;
  }
  .project-item:hover .overlay {
    opacity: 1;
  }
</style>
<nav>
  <a href="#welcome">Welcome</a>
  <a href="#profile">Profile</a>
  <a href="#contact">Contact</a>
  <a href="#education">Education</a>
  <a href="#certifications">Certifications</a>
  <a href="#awards">Awards</a>
  <a href="#experience">Experience</a>
  <a href="#skills-tools">Skills</a>
  <a href="#chat">Chat</a>
  <a href="#projects-gallery">Projects</a>
</nav>
""", unsafe_allow_html=True)

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

# --- Content Wrapper Start ---
st.markdown('<div class="content">', unsafe_allow_html=True)

# Welcome Section
st.markdown('<div id="welcome" class="card"><h2>Welcome</h2><p>Explore my portfolio to learn more about my work in data science, analytics, and technology.</p></div>', unsafe_allow_html=True)

# Profile Section
st.markdown('<div id="profile" class="card"><h2>Profile</h2><img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" width="120" style="border-radius:50%; margin-bottom:12px;"/><p><strong>Venkatesh Soundararajan</strong><br>Software Development Intern | Data Engineering<br>📍 Calgary, AB, Canada</p></div>', unsafe_allow_html=True)

# Contact Section
st.markdown('<div id="contact" class="card"><h2>Contact</h2><p><a href="mailto:venkatesh.balusoundar@gmail.com">Email</a> | <a href="https://www.linkedin.com/in/venkateshbalus/">LinkedIn</a> | <a href="https://github.com/venkateshsoundar">GitHub</a> | <a href="https://medium.com/@venkatesh.balusoundar">Medium</a></p></div>', unsafe_allow_html=True)

# Education Section
st.markdown('<div id="education" class="card"><h2>Education</h2><ul><li><strong>Masters in Data Science and Analytics</strong>, University of Calgary (Sep 2024–Present)</li><li><strong>Bachelor of Engineering</strong>, Anna University, Chennai, India (Aug 2009–May 2013)</li></ul></div>', unsafe_allow_html=True)

# Certifications Section
st.markdown('<div id="certifications" class="card"><h2>Certifications & Courses</h2><ul><li>Insurance & Guidewire Suite Analyst 10.0 (Jasper)</li><li>Karate DSL (Udemy)</li><li>Rest API Automation (TestLeaf)</li><li>Selenium WebDriver (TestLeaf)</li><li>SQL for Data Science (Coursera)</li><li>SDET (Capgemini)</li></ul></div>', unsafe_allow_html=True)

# Awards Section
st.markdown('<div id="awards" class="card"><h2>Awards & Recognitions</h2><ul><li>Spot Award (InsurCloud – Deloitte, Canada)</li><li>Best Contributor (COMPASS – Hartford Insurance, USA)</li><li>QE & A Maestro (Centene by Cognizant, USA)</li><li>Pride of the Quarter (Health Net by Cognizant, USA)</li><li>Pillar of the Month (Health Net by Cognizant, USA)</li></ul></div>', unsafe_allow_html=True)

# Experience Section
st.markdown('<div id="experience" class="card"><h2>Professional Experience</h2><ul><li><strong>Software Developer Intern</strong>, Tech Insights Inc (May 2025–Present)</li><li><strong>Senior Consultant</strong>, Deloitte Consulting India (Jun 2024–Aug 2024)</li><li><strong>Consultant</strong>, Deloitte Consulting India (Oct 2021–Jun 2024)</li><li><strong>Consultant</strong>, Capgemini (May 2018–Oct 2021)</li><li><strong>Associate</strong>, Cognizant (May 2016–May 2018)</li><li><strong>Programmer Analyst</strong>, Cognizant (Sep 2013–May 2016)</li></ul></div>', unsafe_allow_html=True)

# Skills Section
st.markdown('<div id="skills-tools" class="card"><h2>Core Skills & Tools</h2><p>**Languages**: Python, R, SQL, Java, VBA<br>**Analytics**: Pandas, NumPy, Matplotlib, Power BI, Excel<br>**DBs**: MySQL, Oracle, NoSQL<br>**Tools**: Git, JIRA, ALM, Rally, Selenium, Guidewire</p></div>', unsafe_allow_html=True)

# Chat Section
st.markdown('<div id="chat" class="card"><h2>Chat</h2><p>Ask any question about my projects or experience:</p></div>', unsafe_allow_html=True)
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
user_input = st.chat_input("Type your question here...")
if user_input:
    st.chat_message("user").write(user_input)
    prompt = (
        "You are Venkatesh's professional assistant. Here is his resume data as JSON:\n" + resume_json +
        "\n\nAnswer the question based only on this DataFrame JSON. If you can't, say you don't know.\nQuestion: " + user_input
    )
    with st.spinner("Assistant is typing..."):
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[{"role": "system", "content": prompt}]
        )
        st.chat_message("assistant").write(response.choices[0].message.content)

# Projects Gallery
st.markdown('<div id="projects-gallery" class="card"><h2>Projects Gallery</h2></div>', unsafe_allow_html=True)
cols = st.columns(3)
for idx, proj in enumerate(projects):
    with cols[idx % 3]:
        st.markdown(
            f"<div class='project-item'><a href='{proj['url']}' target='_blank'>" +
            f"<img src='{proj['image']}'/><div class='overlay'>{proj['title']}</div></a></div>",
            unsafe_allow_html=True
        )

# End content wrapper
st.markdown('</div>', unsafe_allow_html=True)
