import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume bullets ---
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    sentences = [s.strip() for s in text.split('.') if len(s) > 50]
    return sentences[:max_bullets]

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/"
    "Venkateshwaran_Resume.pdf"
)
bullets = load_resume_bullets(resume_url)

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
    {"title": "California Wildfire Data Story", "url": "https://github.com/venkateshsoundar/california-wildfire-datastory", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/California_Wildfire_Data_Story.jpeg"},
    {"title": "Penguin Dataset Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Dataset_Chatbot.jpeg"},
    {"title": "Uber Ride Duration Predictor", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictor", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uber_Ride_Duration_Predictor.jpeg"}
]

# --- Global CSS & Background ---
# (CSS already injected above; now define project details)
# Projects Showcase Details
# Generate HTML grid for projects
grid_html = '<div class="grid-container">'
for proj in projects:
    grid_html += (
        f'<div class="project-item hover-zoom"><a href="{proj["url"]}" target="_blank">'
        f'<img src="{proj["image"]}" class="card-img"/><div class="overlay">{proj["title"]}</div></a></div>'
    )
grid_html += '</div>'

# Render details element
st.markdown(
    f'''
<details>
  <summary class="details-summary">Projects Showcase</summary>
  {grid_html}
</details>
''', unsafe_allow_html=True
)

# --- Right Pane ---
with right_col:
    # Skills
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#1ABC9C;">Skills</div>' +
        '<p style="text-align:center;">Python, SQL, R<br>AWS & SageMaker<br>Streamlit, Tableau<br>Scikit-learn, OpenCV<br>Git, Agile</p>' +
        '</div>',
        unsafe_allow_html=True
    )
    # Experience
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#8E44AD;">Experience</div>' +
        '<p style="text-align:center;">Deloitte Quality Lead (8+ yrs)<br>AWS Data Pipelines<br>Agile Team Lead<br>Risk Analytics</p>' +
        '</div>',
        unsafe_allow_html=True
    )
    # Certifications
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#D35400;">Certifications</div>' +
        '<p style="text-align:center;">AWS Solutions Architect<br>Tableau Specialist<br>Scrum Master</p>' +
        '</div>',
        unsafe_allow_html=True
    )
