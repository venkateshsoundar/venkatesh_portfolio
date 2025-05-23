import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

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
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg"}
]

# --- Global CSS & Background ---
st.markdown('''
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
  font-size: 18px;
}
.card {
  width: 100% !important;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s ease, box-shadow .3s ease;
  text-align: center;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.7);
}
.section-title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 6px;
}
.profile-pic-popout {
  width: 170px;
  height: 170px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.18);
  position: relative;
  margin-bottom: 18px;
}
.contact-icon {
  width: 32px;
  height: 32px;
  filter: invert(100%);
  color:#ADD8E6;
  margin: 0 10px;
  vertical-align: middle;
}
.project-item {
  position: relative;
  aspect-ratio: 1/1;
  overflow: hidden;
  border-radius: 12px;
}
.card-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform .3s ease;
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
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 20px;
  margin-top: 12px;
}
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 10px;
  margin: 8px 0 12px;
}
.skill-card {
  background: rgba(255,255,255,0.13);
  padding: 9px;
  border-radius: 7px;
  font-size: 1rem;
  text-align: center;
  color: #fff;
}
.exp-timeline {
  position: relative;
  margin-top: 10px;
}
.exp-item {
  position: relative;
  margin-bottom: 30px;
}
.exp-dot {
  position: absolute;
  left: -30px;
  top: 7px;
  width: 16px;
  height: 16px;
  background: #406496;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 0 0 3px #b3c6e2;
}
.exp-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: -22px;
  top: 24px;
  width: 2px;
  height: 35px;
  background: #b3c6e2;
  z-index: 0;
}
.exp-title { font-weight: bold; font-size: 1.1rem; }
.exp-company { color: #ADD8E6; font-size: 1rem; }
.exp-date { color: #ffd166; font-size: 0.97rem; }
.welcome-card {
  background: url("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif") center/cover no-repeat;
  border-radius: 16px;
  padding: 3rem;
  color: white;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 18px;
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
  font-size: 2.2rem;
}
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { from, to { border-color: transparent; } 50% { border-color: #5A84B4; } }
.chatbot-gif-bg {
    background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif') center/cover no-repeat;
    border-radius: 20px; padding:32px 18px 28px 18px;
    min-height:220px;
    box-shadow:0 4px 30px #2039;
    display: flex; align-items: center; justify-content:center;
    margin-top:16px; margin-bottom:24px;
}
</style>
''', unsafe_allow_html=True)

# --- Layout ---
left_col, center_col, right_col = st.columns([1.1, 2, 1], gap="small")

# --- LEFT PANE ---
with left_col:
    st.markdown('''
    <div class="card profile-card-content hover-zoom">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"
           class="profile-pic-popout" />
      <h2>Venkatesh Soundararajan</h2>
      <p><span style="color:#ADD8E6;"><strong>Software Development Intern</strong><br>Data Engineering</span></p>
      <span style="color:#ffd166;"><strong>🍁 Calgary, AB, Canada</strong></span>
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

    st.markdown(
    """
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Education</div>
      <div style="text-align:left; margin-left:10px;">
        <p>
          <b>Masters in Data Science and Analytics</b><br>  
          <span style="color:#ADD8E6;">University of Calgary, Alberta, Canada</span><br> 
          <span style="color:#ffd166;">September 2024 – Present</span>
        </p>
        <p>
          <b>Bachelor of Engineering</b><br>  
          <span style="color:#ADD8E6;">Anna University, Chennai, India</span><br> 
          <span style="color:#ffd166;">August 2009 – May 2013</span>                
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True
)

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

# --- CENTER PANE ---
with center_col:
    # --- Welcome Card with GIF ---
    st.markdown("""
    <div class="welcome-card">
      <div class="typewriter">
        <h1>Hello and Welcome...</h1>
        <p>Explore my portfolio to learn more about my work in data science, analytics, and technology.<br>
        Let’s connect and create something impactful together.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Experience Timeline ---
    st.markdown("""
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Professional Experience</div>
      <div class="exp-timeline">
        <div class="exp-item">
          <div class="exp-dot"></div>
          <div class="exp-title">Software Developer Intern</div>
          <div class="exp-company">Tech Insights Inc, Canada</div>
          <div class="exp-date">May 2025 – Present</div>
        </div>
        <div class="exp-item">
          <div class="exp-dot"></div>
          <div class="exp-title">Senior Consultant</div>
          <div class="exp-company">Deloitte Consulting India Private Limited, India</div>
          <div class="exp-date">June 2024 – August 2024</div>
        </div>
        <div class="exp-item">
          <div class="exp-dot"></div>
          <div class="exp-title">Consultant</div>
          <div class="exp-company">Deloitte Consulting India Private Limited, India</div>
          <div class="exp-date">October 2021 – June 2024</div>
        </div>
        <div class="exp-item">
          <div class="exp-dot"></div>
          <div class="exp-title">Consultant</div>
          <div class="exp-company">Capgemini Technology Services India Private Limited, India</div>
          <div class="exp-date">May 2018 – October 2021</div>
        </div>
        <div class="exp-item">
          <div class="exp-dot"></div>
          <div class="exp-title">Associate</div>
          <div class="exp-company">Cognizant Technology Solutions India Private Limited, India</div>
          <div class="exp-date">May 2016 – May 2018</div>
        </div>
        <div class="exp-item">
          <div class="exp-dot"></div>
          <div class="exp-title">Programmer Analyst</div>
          <div class="exp-company">Cognizant Technology Solutions India Private Limited, India</div>
          <div class="exp-date">Sep 2013 – May 2018</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Skills ---
    st.markdown(
    '''
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Core Skills & Tools</div>
      <div class="skills-grid">
        <div class="skill-card">Python</div>
        <div class="skill-card">R</div>
        <div class="skill-card">SQL</div>
        <div class="skill-card">Java</div>
        <div class="skill-card">VBA Macro</div>
        <div class="skill-card">Pandas</div>
        <div class="skill-card">NumPy</div>
        <div class="skill-card">Matplotlib</div>
        <div class="skill-card">Power BI</div>
        <div class="skill-card">Excel</div>
        <div class="skill-card">Hypothesis Tests</div>
        <div class="skill-card">Regression</div>
        <div class="skill-card">MySQL</div>
        <div class="skill-card">Oracle</div>
        <div class="skill-card">NoSQL</div>
        <div class="skill-card">Git</div>
        <div class="skill-card">JIRA</div>
        <div class="skill-card">ALM</div>
        <div class="skill-card">Rally</div>
        <div class="skill-card">Selenium WebDriver</div>
        <div class="skill-card">Guidewire</div>
      </div>
    </div>
    ''', unsafe_allow_html=True
    )

    # --- Projects Gallery (Grid) ---
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

# --- RIGHT PANE: Chatbot with GIF BG ---
with right_col:
    st.markdown(
        f"""
        <div class="chatbot-gif-bg">
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
