import streamlit as st
import requests
import io
import PyPDF2
import pandas as pd

st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Global CSS for background, image animation, larger cards ---
st.markdown("""
    <style>
        .stApp {
            background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center center/cover no-repeat fixed !important;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .project-card {
            background: rgba(31,42,68,0.83);
            border-radius: 20px;
            padding: 32px 20px 20px 20px;
            margin: 22px 0 18px 0;
            color: #fff;
            box-shadow: 0 8px 24px 0 rgba(0,0,0,0.08);
            text-align: center;
        }
        .project-img-animate {
            width: 350px !important;
            height: 220px !important;
            object-fit: cover !important;
            border-radius: 16px;
            margin-bottom: 12px;
            opacity: 0;
            transform: scale(0.97);
            animation: fadeinimg 0.8s ease forwards;
        }
        @keyframes fadeinimg {
            from {opacity:0; transform:scale(0.97);}
            to {opacity:1; transform:scale(1);}
        }
        .main-head {font-size:2.7rem; font-weight:bold; color:#fff; letter-spacing:1px; text-shadow:0 2px 12px #222;}
        .section-head {font-size:2.0rem; margin-top:28px; color:#a0e3ff;}
    </style>
""", unsafe_allow_html=True)

# --- Resume loading utility ---
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

# --- Welcome Header ---
st.markdown("<div class='main-head'>Venkatesh Portfolio</div>", unsafe_allow_html=True)
st.write("Explore my portfolio to learn more about my work in data science, analytics, and technology.")

# --- Profile and Contact ---
col1, col2 = st.columns([1,3])
with col1:
    st.image("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg", width=160)
with col2:
    st.markdown("""
        <div style="font-size:1.25rem; color:#eee;">
            Results-driven data analyst and developer, passionate about analytics, cloud, and automation.<br>
            <b>Email:</b> <a href="mailto:venkatesh.balusoundar@gmail.com">venkatesh.balusoundar@gmail.com</a><br>
            <b>LinkedIn:</b> <a href="https://linkedin.com/in/venkateshbalusoundar" style="color:#96e6ff;">Profile</a> &nbsp;
            <b>GitHub:</b> <a href="https://github.com/venkateshsoundar" style="color:#96e6ff;">Repo</a>
        </div>
    """, unsafe_allow_html=True)

# --- Education, Certs, Awards, Skills ---
st.markdown("<div class='section-head'>Education</div>", unsafe_allow_html=True)
st.write("""
- **Masters in Data Science and Analytics**, University of Calgary (Sep 2024–Present)
- **Bachelor of Engineering**, Anna University (Aug 2009–May 2013)
""")

st.markdown("<div class='section-head'>Certifications & Courses</div>", unsafe_allow_html=True)
st.write("""
- Insurance & Guidewire Suite Analyst 10.0
- Karate DSL, Rest API Automation, Selenium WebDriver
- SQL for Data Science, SDET
""")

st.markdown("<div class='section-head'>Awards & Recognitions</div>", unsafe_allow_html=True)
st.write("""
- Spot Award, Best Contributor, QE & A Maestro
- Pride of the Quarter, Pillar of the Month
""")

st.markdown("<div class='section-head'>Core Skills & Tools</div>", unsafe_allow_html=True)
st.write("""
Python, R, SQL, Java, Pandas, NumPy, Power BI, Git, JIRA, Selenium, Guidewire
""")

# --- Projects Gallery (Animated Grid) ---
st.markdown("<div class='section-head'>Projects Gallery</div>", unsafe_allow_html=True)
grid_cols = st.columns(3)
for idx, proj in enumerate(projects):
    with grid_cols[idx % 3]:
        st.markdown(f"""
            <div class="project-card">
                <img src="{proj['image']}" class="project-img-animate"/>
                <div style="font-size:1.1rem; font-weight:600; margin:9px 0 7px 0;">{proj['title']}</div>
                <a href="{proj['url']}" style="color:#92edff;" target="_blank">GitHub Link</a>
            </div>
        """, unsafe_allow_html=True)

# --- Download Resume Section ---
st.markdown("<div class='section-head'>Download My Resume</div>", unsafe_allow_html=True)
resume_file_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
st.markdown(f"[Download Resume (PDF)]({resume_file_url})")

# --- ATS Match Score Section ---
st.markdown("<div class='section-head'>ATS Job Match Demo</div>", unsafe_allow_html=True)
job_desc = st.text_area("Paste Job Description Here")
if st.button("Check ATS Match"):
    required_keywords = [
        "data risk", "control self-assessment", "collibra", "BCBS239",
        "DRA", "data quality", "regulatory reporting", "metadata", "lineage"
    ]
    resume_text = " ".join(resume_df['sentence'])
    score = sum(1 for kw in required_keywords if kw.lower() in resume_text.lower())
    st.success(f"ATS Match Score: {score}/{len(required_keywords)} ({int(100*score/len(required_keywords))}%)")

# --- End of app ---
