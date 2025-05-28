import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# ---- PAGE CONFIG & GLOBAL CSS ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

st.markdown("""
<style>
/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #1F2A44;
    border-radius: 0 28px 28px 0;
    padding-top: 30px;
}
.sidebar-title {
    color: #ffd166;
    font-size: 1.24rem;
    font-weight: bold;
    margin-bottom: 26px;
    text-align: center;
    letter-spacing: .02em;
}
.sidebar-radio label {
    color: #ffd166 !important;
    font-weight: bold;
    font-size: 1.10rem;
    border-radius: 8px;
    padding: 7px 18px;
    transition: background 0.19s, color 0.19s;
}
.sidebar-radio label[data-selected="true"] {
    background: #ffd166;
    color: #22304A !important;
}
/* ---- CARD/GRID ---- */
.card {
  width: 100% !important;
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 32px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  box-shadow: 0 3px 24px #22304A11;
  text-align: left;
}
.card:hover, .hover-zoom:hover {
  transform: translateY(-6px) scale(1.025);
  box-shadow: 0 12px 36px #ffd16634, 0 2px 12px #22304A22;
  z-index: 11;
}
.section-title {
  font-size: 1.35rem;
  font-weight: bold;
  margin-bottom: 20px;
  padding: 8px 18px;
  border-radius: 10px;
  color: #fff;
  background:#22304A;
  text-align: left;
  box-shadow: 0 1px 8px #22304A18;
}
/* ---- Projects Grid ---- */
.projects-4col-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin: 0 auto;
  justify-content: center;
  align-items: stretch;
}
.project-main-card {
  background: linear-gradient(135deg, #202C41 0%, #324665 100%);
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(44,62,80,0.10);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  transition: transform 0.18s, box-shadow 0.18s;
  border: 1.5px solid #22304A2A;
  height: 100%;
  overflow: hidden;
}
.project-main-card:hover {
  transform: translateY(-4px) scale(1.021);
  box-shadow: 0 14px 40px #ffd16618, 0 2px 12px #22304A19;
  z-index: 2;
}
.project-img-holder {
  width: 100%;
  background: #222E40;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 18px;
  padding-bottom: 10px;
}
.project-img-inner {
  width: 88px;
  height: 88px;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px #22304A11;
  display: flex;
  align-items: center;
  justify-content: center;
}
.project-img-inner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .18s cubic-bezier(.4,1.6,.6,1);
  border-radius: 12px;
}
.project-main-card:hover .project-img-inner img {
  transform: scale(1.08);
}
.project-card-info {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 8px 14px 16px 14px;
}
.project-title {
  font-size: 1.08rem;
  font-weight: bold;
  color: #ffd166;
  margin-bottom: 5px;
  margin-top: 2px;
  text-align: center;
  min-height: 38px;
}
.project-desc {
  color: #fff;
  font-size: 0.98rem;
  margin-bottom: 10px;
  text-align: center;
  flex: 1 1 0;
}
.project-tools-list {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 7px;
  justify-content: center;
}
.project-tool-badge {
  background: linear-gradient(135deg,#e2e2e2 0%,#ffd166 88%);
  color: #22304A;
  font-size: 0.88rem;
  border-radius: 9px;
  padding: 2px 9px 1.5px 9px;
  font-weight: 500;
  margin-bottom: 2px;
  box-shadow: 0 1px 3px #22304A13;
}
.project-card-link {
  text-align: center;
  margin-top: 6px;
}
.project-card-link a {
  color: #ADD8E6;
  font-size: 0.97rem;
  text-decoration: underline;
  font-weight: 600;
  transition: color 0.13s;
}
.project-card-link a:hover {
  color: #ffd166;
}
@media (max-width: 1200px) {
  .projects-4col-grid {grid-template-columns: repeat(3, 1fr);}
}
@media (max-width: 900px) {
  .projects-4col-grid {grid-template-columns: repeat(2, 1fr);}
}
@media (max-width: 600px) {
  .projects-4col-grid {grid-template-columns: 1fr;}
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
    {
        "title": "Canadian Quality of Life Analysis",
        "url": "https://github.com/venkateshsoundar/canadian-qol-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg",
        "tools": ["Python", "Pandas", "Seaborn", "Tableau"],
        "desc": "Analyzed Canadian provinces' quality of life using demographic data and advanced data visualization."
    },
    {
        "title": "Alberta Wildfire Analysis",
        "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg",
        "tools": ["Python", "GeoPandas", "Power BI"],
        "desc": "Mapped and predicted wildfire trends in Alberta with geospatial analysis and interactive dashboards."
    },
    {
        "title": "Toronto Crime Drivers",
        "url": "https://github.com/venkateshsoundar/toronto-crime-drivers",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg",
        "tools": ["Python", "Pandas", "Matplotlib"],
        "desc": "Investigated drivers of crime across Toronto neighborhoods to reveal actionable urban insights."
    },
    {
        "title": "Weight Change Regression Analysis",
        "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg",
        "tools": ["Python", "Scikit-learn", "Seaborn"],
        "desc": "Built regression models to predict weight changes based on lifestyle and demographic data."
    },
    {
        "title": "Calgary Childcare Compliance",
        "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg",
        "tools": ["Python", "Pandas", "Plotly"],
        "desc": "Assessed childcare center compliance in Calgary through data-driven dashboards."
    },
    {
        "title": "Social Media Purchase Influence",
        "url": "https://github.com/venkateshsoundar/social-media-purchase-influence",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg",
        "tools": ["Python", "Scikit-learn", "Power BI"],
        "desc": "Modeled and visualized the impact of social media on consumer purchase behavior."
    },
    {
        "title": "Obesity Level Estimation",
        "url": "https://github.com/venkateshsoundar/obesity-level-estimation",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg",
        "tools": ["Python", "Logistic Regression", "Pandas"],
        "desc": "Predicted obesity levels from health and lifestyle features using classification algorithms."
    },
    {
        "title": "Weather Data Pipeline (AWS)",
        "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg",
        "tools": ["AWS", "Python", "Streamlit"],
        "desc": "Automated weather data ingestion, storage, and visualization on AWS cloud with Streamlit dashboard."
    },
    {
        "title": "Gmail Sentimental Analysis",
        "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg",
        "tools": ["Python", "NLTK", "Gmail API"],
        "desc": "Classified and visualized sentiment of Gmail emails using NLP techniques."
    },
    {
        "title": "Penguin Species Prediction Chatbot",
        "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg",
        "tools": ["Python", "Scikit-learn", "Streamlit"],
        "desc": "Developed an interactive chatbot to predict penguin species from morphological features."
    },
    {
        "title": "Uber Ride Prediction",
        "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg",
        "tools": ["Python", "XGBoost", "Matplotlib"],
        "desc": "Predicted Uber ride durations using machine learning and explained predictions with visualizations."
    }
]

# ---- SIDEBAR ----
st.sidebar.markdown('<div class="sidebar-title">Navigate</div>', unsafe_allow_html=True)
section = st.sidebar.radio(
    "",
    [
        "About",
        "Education",
        "Experience",
        "Certifications",
        "Recognitions",
        "Projects Gallery",
        "Skills"
    ],
    key="sidebar_radio"
)

# ---- MAIN PANE: Show each section ----
if section == "About":
    st.markdown(
        """
        <div class="card hover-zoom">
            <div class="section-title">About Me</div>
            <div style="display: flex; align-items: flex-start; gap: 38px;">
              <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" style="width:150px; border-radius:18px; box-shadow:0 4px 18px #ffd16618; border:3px solid #ffd166;"/>
              <div>
                <p style="font-size: 1.1rem; color: #fff; line-height:1.7;">
                  I’m <b>Venkatesh</b>, a Data Scientist and Software Developer with <b>8+ years of experience</b> in quality engineering, business intelligence, and analytics.<br><br>
                  I specialize in building <b>scalable ETL pipelines</b>, predictive models, and interactive dashboards using cloud platforms like <b>AWS</b> and <b>Azure</b>.<br><br>
                  I'm currently pursuing my Master's in Data Science and Analytics at the <b>University of Calgary</b>.<br>
                  My passion lies in solving complex business problems with clean, actionable insights and AI-powered solutions.
                </p>
                <div style="margin-top:20px;">
                  <a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" style="width:30px;margin-right:10px;filter:invert(90%);"/></a>
                  <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" style="width:30px;margin-right:10px;filter:invert(90%);"/></a>
                  <a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" style="width:30px;margin-right:10px;filter:invert(90%);"/></a>
                  <a href="https://medium.com/@venkatesh.balusoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg" style="width:30px;filter:invert(90%);"/></a>
                </div>
              </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

elif section == "Education":
    st.markdown(
        """
        <div class="card hover-zoom">
            <div class="section-title">Education</div>
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
        """, unsafe_allow_html=True
    )

elif section == "Experience":
    st.markdown(
        """
        <div class="card hover-zoom">
            <div class="section-title">Professional Experience</div>
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
        """, unsafe_allow_html=True
    )

elif section == "Certifications":
    st.markdown(
        """
        <div class="card hover-zoom">
            <div class="section-title">Certifications & Courses</div>
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
        """, unsafe_allow_html=True
    )

elif section == "Recognitions":
    st.markdown(
        """
        <div class="card hover-zoom">
            <div class="section-title">Awards & Recognitions</div>
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
        """, unsafe_allow_html=True
    )

elif section == "Projects Gallery":
    # Build project cards grid
    projects_html = '''
    <div class="card projects-gallery-pane hover-zoom">
      <div class="section-title">Projects Gallery</div>
      <div class="projects-4col-grid">
    '''
    for proj in projects:
        tools_html = ''.join(f'<span class="project-tool-badge">{tool}</span>' for tool in proj["tools"])
        projects_html += (
            f'<div class="project-main-card hover-zoom">'
            f'<div class="project-img-holder">'
            f'<div class="project-img-inner">'
            f'<img src="{proj["image"]}" alt="{proj["title"]}"/>'
            f'</div></div>'
            f'<div class="project-card-info">'
            f'<div class="project-title">{proj["title"]}</div>'
            f'<div class="project-desc">{proj["desc"]}</div>'
            f'<div class="project-tools-list">{tools_html}</div>'
            f'<div class="project-card-link"><a href="{proj["url"]}" target="_blank">View on GitHub &rarr;</a></div>'
            f'</div></div>'
        )
    projects_html += '</div></div>'
    st.markdown(projects_html, unsafe_allow_html=True)

elif section == "Skills":
    st.markdown("""
    <div class="card skills-pane-main hover-zoom">
      <div class="section-title">Core Skills and Tools</div>
      <div class="skills-categories-grid">
        <div class="skill-category-card">
          <div class="skill-category-title">Programming Languages</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/python.svg"/>Python</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/r.svg"/>R</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/sqlite.svg"/>SQL</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/java.svg"/>Java</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/vba.svg"/>VBA Macro</div>
          </div>
        </div>
        <div class="skill-category-card">
          <div class="skill-category-title">Data Analysis & Scientific</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/pandas.svg"/>Pandas</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/numpy.svg"/>NumPy</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/matplotlib.svg"/>Matplotlib</div>
          </div>
        </div>
        <div class="skill-category-card">
          <div class="skill-category-title">Data Visualization</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/powerbi.svg"/>Power BI</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/microsoftexcel.svg"/>Excel</div>
          </div>
        </div>
        <div class="skill-category-card">
          <div class="skill-category-title">Database Management</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/mysql.svg"/>MySQL</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/oracle.svg"/>Oracle</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/mongodb.svg"/>NoSQL</div>
          </div>
        </div>
        <div class="skill-category-card">
          <div class="skill-category-title">Version Control</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/git.svg"/>Git</div>
          </div>
        </div>
        <div class="skill-category-card">
          <div class="skill-category-title">Project Management</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/jira.svg"/>JIRA</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/alm.svg"/>ALM</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/rally.svg"/>Rally</div>
          </div>
        </div>
        <div class="skill-category-card">
          <div class="skill-category-title">QA Automation & Insurance</div>
          <div class="skill-list">
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/selenium.svg"/>Selenium</div>
            <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/guidewire.svg"/>Guidewire</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
