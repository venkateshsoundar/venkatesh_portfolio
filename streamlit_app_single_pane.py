import streamlit as st

# ---- PAGE CONFIG & STYLES ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")
st.markdown("""
<style>
body {background: #19213a;}
.stApp {background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat; background-attachment: fixed;}
/* Top nav bar */
.nav-bar {
    display: flex;
    justify-content: center;
    gap: 32px;
    background: rgba(44,62,80,0.90);
    padding: 16px 0 7px 0;
    border-radius: 0 0 20px 20px;
    position: sticky;
    top: 0;
    z-index: 99;
    margin-bottom: 28px;
}
.nav-link {
    background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
    color: #ffd166 !important;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.11rem;
    letter-spacing: 1px;
    padding: 11px 25px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(44,62,80,0.17);
    transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s, background .22s;
    display: inline-block;
    margin-bottom: 0;
}
.nav-link:hover, .nav-link:focus {
    transform: translateY(-5px) scale(1.07);
    box-shadow: 0 8px 16px rgba(0,0,0,0.24);
    background: linear-gradient(135deg, #406496 0%, #22304A 100%);
    color: #fff !important;
    text-decoration: none;
}
.card {
  width: 100% !important;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 28px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  text-align: left;
}
.card:hover {
  transform: translateY(-5px) scale(1.03);
  box-shadow: 0 8px 16px rgba(0,0,0,0.24);
}
.section-title {
  font-size: 1.37rem;
  font-weight: bold;
  margin-bottom: 14px;
  padding: 8px;
  border-radius: 6px;
  background: #22304A;
  color: #ffd166;
  text-align: left;
}
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px,1fr));
    gap: 18px;
}
.project-card {
    background: #26334d;
    border-radius: 11px;
    overflow: hidden;
    box-shadow: 0 1px 5px rgba(44,62,80,0.13);
    text-align: center;
    cursor: pointer;
    transition: transform .19s, box-shadow .19s;
    border: 2px solid #34495E;
}
.project-card:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 7px 24px rgba(0,0,0,0.17);
    border: 2px solid #ffd166;
}
.project-card img {
    width: 100%;
    height: 128px;
    object-fit: cover;
    border-bottom: 2px solid #ffd166;
}
.project-title {
    color: #ffd166;
    font-weight: bold;
    padding: 12px 0 5px 0;
    font-size: 1.01rem;
}
.project-desc {
    color: #eee;
    font-size: 0.99rem;
    padding-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---- TOP MENU ----
st.markdown("""
<div class="nav-bar">
    <a class="nav-link" href="#about">About</a>
    <a class="nav-link" href="#projects">Projects</a>
    <a class="nav-link" href="#experience">Experience</a>
    <a class="nav-link" href="#skills">Skills</a>
    <a class="nav-link" href="#contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# ---- SECTIONS ----

# --- ABOUT ---
st.markdown('<a id="about"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="section-title">About Me</div>
    <div>
        <b>Venkatesh Soundararajan</b><br>
        Data Scientist & Software Developer passionate about leveraging data to drive real-world impact.<br><br>
        My expertise includes building scalable ETL pipelines, predictive models, and cloud dashboards (AWS, Azure).<br>
        I thrive at the intersection of tech and business, and enjoy solving tough data challenges.
    </div>
</div>
""", unsafe_allow_html=True)

# --- PROJECTS ---
st.markdown('<a id="projects"></a>', unsafe_allow_html=True)
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg", "desc": "Analyzed quality of life across Canada using public data, pandas, and dashboards."},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg", "desc": "Visualized wildfire patterns and built predictive models for Alberta."},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg", "desc": "Investigated socio-economic drivers of crime in Toronto with regression analysis."},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg", "desc": "Predicted weight change using health and lifestyle data."},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg", "desc": "Analyzed compliance of childcare providers for policy improvement."},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg", "desc": "Studied how social media influences consumer buying decisions."},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg", "desc": "Estimated obesity levels using classification models."},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg", "desc": "AWS pipeline for weather ETL and forecasting dashboards."},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg", "desc": "NLP classification and topic modeling of Gmail sentiment."},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg", "desc": "Interactive chatbot for penguin species classification."},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg", "desc": "Predicted Uber ride durations using ML and geospatial features."}
]
st.markdown("""
<div class="card">
    <div class="section-title">Projects Gallery</div>
    <div class="project-grid">
""", unsafe_allow_html=True)
for proj in projects:
    st.markdown(
        f"""
        <a href="{proj['url']}" target="_blank" style="text-decoration:none;">
            <div class="project-card">
                <img src="{proj['image']}" />
                <div class="project-title">{proj['title']}</div>
                <div class="project-desc">{proj['desc']}</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )
st.markdown("</div></div>", unsafe_allow_html=True)

# --- EXPERIENCE ---
st.markdown('<a id="experience"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="section-title">Professional Experience</div>
    <b>Software Developer Intern</b>, Tech Insights Inc, Canada (May 2025 – Present)<br>
    <b>Senior Consultant</b>, Deloitte Consulting India (June 2024 – August 2024)<br>
    <b>Consultant</b>, Deloitte Consulting India (Oct 2021 – June 2024)<br>
    <b>Consultant</b>, Capgemini Technology Services (May 2018 – Oct 2021)<br>
    <b>Associate / Programmer Analyst</b>, Cognizant India (Sep 2013 – May 2018)
</div>
""", unsafe_allow_html=True)

# --- SKILLS ---
st.markdown('<a id="skills"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="section-title">Core Skills & Tools</div>
    <ul>
      <li><b>Languages:</b> Python, R, SQL, Java, VBA Macro</li>
      <li><b>Analysis:</b> Pandas, NumPy, Scikit-learn, Matplotlib, Power BI, Excel</li>
      <li><b>DBMS:</b> MySQL, Oracle, NoSQL</li>
      <li><b>Automation:</b> Selenium WebDriver, Guidewire</li>
      <li><b>Version Control:</b> Git</li>
      <li><b>Project Tools:</b> JIRA, ALM, Rally</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- CONTACT ---
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="section-title">Contact</div>
    <a href="mailto:venkatesh.balusoundar@gmail.com" style="color:#ffd166;font-size:1.08rem;">Email</a> |
    <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank" style="color:#ffd166;font-size:1.08rem;">LinkedIn</a> |
    <a href="https://github.com/venkateshsoundar" target="_blank" style="color:#ffd166;font-size:1.08rem;">GitHub</a>
</div>
""", unsafe_allow_html=True)
