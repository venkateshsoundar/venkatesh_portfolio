import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# ---- PAGE CONFIG & CSS ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")
st.markdown("""
<style>
/* (All your original CSS stays the same!) */
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
/* ...rest of your CSS (section-title, grid-container, project-item, etc.) ... */
.section-title { font-size: 1.6rem; font-weight: bold; margin-bottom: 12px; padding: 8px; border-radius: 6px;}
/* ...all your previous CSS here (copy it in full from your last version)... */
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

# ---- SECTION FUNCTIONS ----
def section_profile():
    st.markdown(
        """
        <div class="profile-card-container">
          <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"
               class="profile-pic-popout" />
          <div class="card profile-card-content hover-zoom">
            <h2>Venkatesh Soundararajan</h2>
            <p><span style="color:#ADD8E6;"><strong>Software Development Intern</strong><br>Data Engineering</span></p>
            <span style="color:#ffd166;"><strong>🍁 Calgary, AB, Canada</strong></span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def section_welcome():
    gif_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif"
    st.markdown(
        f"""
        <div class="welcome-card" style="background: url('{gif_url}') center/cover no-repeat;">
            <h1>Hello and Welcome...</h1>
            <p>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
        </div>
        """,
        unsafe_allow_html=True)

def section_about():
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

def section_chatbot(chat_enabled=True):
    ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
    st.markdown(
        f"""
        <div class="welcome-card2" style="background:url('{ai_url}') center/cover no-repeat;">
          <div class="text-container" style="position:absolute;top:70%;right:2rem;transform:translateY(-50%);text-align:right;">
            <h2>Ask Buddy Bot!</h2>
          </div>
        </div>
        """,
        unsafe_allow_html=True)
    if chat_enabled:
        api_key = st.secrets["DEEPSEEK_API_KEY"]
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        chat_container = st.container()
        with chat_container:
            user_input = st.chat_input("Ask something about Venkatesh's Professional Projects and Skills...", key="chatbot_input")
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
    else:
        st.info("Switch to the **Chatbot** tab to interact with Buddy Bot!")

def section_education():
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
    """, unsafe_allow_html=True)

def section_certs():
    st.markdown(
    """
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
    """, unsafe_allow_html=True)

def section_awards():
    st.markdown(
    """
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
    """, unsafe_allow_html=True)

def section_projects():
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

def section_experience():
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

def section_skills():
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

def section_contact():
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

# ---- TABS ----
tabs = st.tabs([
    "Home🏠", "Profile", "Welcome", "About", "Chatbot", "Education",
    "Certifications", "Awards", "Projects", "Experience", "Skills", "Contact"
])

with tabs[0]:
    section_profile()
    section_welcome()
    section_about()
    section_chatbot(chat_enabled=False)  # No chat input on Home!
    section_education()
    section_certs()
    section_awards()
    section_projects()
    section_experience()
    section_skills()
    section_contact()

with tabs[1]: section_profile()
with tabs[2]: section_welcome()
with tabs[3]: section_about()
with tabs[4]: section_chatbot(chat_enabled=True)   # Only here!
with tabs[5]: section_education()
with tabs[6]: section_certs()
with tabs[7]: section_awards()
with tabs[8]: section_projects()
with tabs[9]: section_experience()
with tabs[10]: section_skills()
with tabs[11]: section_contact()
