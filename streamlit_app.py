import streamlit as st
import requests, io
import PyPDF2

# --- Page config ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume bullets ---
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url); r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    sents = [s.strip() for s in text.split(".") if len(s) > 50]
    return sents[:max_bullets]

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/"
    "main/Venkateshwaran_Resume.pdf"
)
bullets = load_resume_bullets(resume_url)

# --- Projects list ---
projects = [
    {
      "title": "Canadian Quality of Life Analysis",
      "url":   "https://github.com/venkateshsoundar/canadian-qol-analysis",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/QualityofLife.jpeg"
    },
    {
      "title": "Alberta Wildfire Analysis",
      "url":   "https://github.com/venkateshsoundar/alberta-wildfire-analysis",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/Alberta_forestfire.jpeg"
    },
    {
      "title": "Toronto Crime Drivers",
      "url":   "https://github.com/venkateshsoundar/toronto-crime-drivers",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/Toronto_Crimes.jpeg"
    },
    {
      "title": "Weight Change Regression Analysis",
      "url":   "https://github.com/venkateshsoundar/weight-change-regression-analysis",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/Weight_Change.jpeg"
    },
    {
      "title": "Calgary Childcare Compliance",
      "url":   "https://github.com/venkateshsoundar/calgary-childcare-compliance",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/CalgaryChildcare.jpeg"
    },
    {
      "title": "Social Media Purchase Influence",
      "url":   "https://github.com/venkateshsoundar/social-media-purchase-influence",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"
    },
    {
      "title": "Obesity Level Estimation",
      "url":   "https://github.com/venkateshsoundar/obesity-level-estimation",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/ObeseLevels.jpeg"
    },
    {
      "title": "Weather Data Pipeline (AWS)",
      "url":   "https://github.com/venkateshsoundar/weather-data-pipeline-aws",
      "image": "https://raw.githubusercontent.com/venkateshsoundar/"
               "venkatesh_portfolio/main/weatherprediction.jpeg"
    }
]

# --- Global CSS & background ---
st.markdown(
    """
<style>
/* Full-page background */
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg')
              center/cover no-repeat fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
}

/* Card styling and hover lift */
.card {
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  transition: transform .3s ease, box-shadow .3s ease;
  color: #ffffff !important;
  width: 100%;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.4);
}

/* Profile pic */
.profile-pic {
  width: 150px; height: 150px;
  border-radius: 50%;
  display: block; margin: 0 auto 12px;
  border: 2px solid #5A84B4;
}

/* Contact icons */
.contact-icon {
  width: 30px; height: 30px;
  filter: invert(100%);
  transition: transform .3s ease;
}
.contact-icon:hover {
  transform: scale(1.2);
}

/* Section titles */
.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 12px;
  text-align: center;
}

/* Typewriter */
.typewriter h1 {
  overflow: hidden;
  white-space: nowrap;
  display: inline-block;
  border-right: .15em solid #5A84B4;
  animation:
    typing 2.5s steps(30, end),
    blink-caret .75s step-end infinite;
}
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { from, to { border-color: transparent; } 50% { border-color: #5A84B4; } }

/* Projects <details> expander */
.details-container {
  margin-bottom: 20px;
  color: #ffffff;
}
.details-container summary {
  cursor: pointer;
  list-style: none;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  padding: 12px;
  border-radius: 12px;
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
  text-align: center;
}
.details-container summary::-webkit-details-marker { display: none; }

/* Grid inside details */
.proj-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 12px;
}

/* Project item */
.project-item {
  position: relative; overflow: hidden;
  border-radius: 12px;
  aspect-ratio: 1/1;
  transition: transform .3s ease;
}
.project-item:hover {
  transform: scale(1.03);
}
.project-item img {
  width: 100%; height: 100%;
  object-fit: cover;
}
.project-item .overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity .3s ease;
  color: #ffffff; text-align: center; padding: 10px;
}
.project-item:hover .overlay {
  opacity: 1;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Three-column layout ---
left_col, mid_col, right_col = st.columns([1, 2, 1], gap="large")

# --- Left pane: Profile & Contact ---
with left_col:
    st.markdown(
        '<div class="card"><img src="https://raw.githubusercontent.com/venkateshsoundar/'
        'venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic"/>'
        '<h2 style="text-align:center;">Venkatesh Soundararajan</h2>'
        '<p style="text-align:center;"><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="card"><div class="section-title">Contact</div>'
        '<div style="display:flex;justify-content:center;gap:20px;">'
        '<a href="mailto:venkatesh.balusoundar@gmail.com">'
        '<img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/>'
        '</a>'
        '<a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank">'
        '<img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/>'
        '</a>'
        '<a href="https://github.com/venkateshsoundar" target="_blank">'
        '<img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/>'
        '</a>'
        '</div></div>',
        unsafe_allow_html=True,
    )

# --- Center pane: Welcome & Projects ---
with mid_col:
    # Welcome
    st.markdown(
        '<div class="card"><div class="typewriter"><h1>Welcome to My Portfolio</h1></div>'
        '<p style="margin-top:12px; text-align:center;">Discover my work below!</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    # Projects Showcase
    grid_html = '<div class="details-container"><details open>' \
                '<summary>Projects Showcase</summary>' \
                '<div class="proj-grid">'
    for p in projects:
        grid_html += (
            f'<div class="project-item">'
            f'<a href="{p["url"]}" target="_blank">'
            f'<img src="{p["image"]}"/>'
            f'<div class="overlay">{p["title"]}</div>'
            f'</a></div>'
        )
    grid_html += '</div></details></div>'
    st.markdown(grid_html, unsafe_allow_html=True)

# --- Right pane: Skills, Experience, Certifications ---
with right_col:
    st.markdown(
        '<div class="card"><div class="section-title">Skills</div>'
        '<p style="text-align:center;">Python, SQL, R<br>AWS & SageMaker<br>'
        'Streamlit, Tableau<br>Scikit-learn, OpenCV<br>Git, Agile</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="card"><div class="section-title">Experience</div>'
        '<p style="text-align:center;">Deloitte Quality Lead (8+ yrs)<br>'
        'AWS Data Pipelines<br>Agile Team Lead<br>Risk Analytics</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="card"><div class="section-title">Certifications</div>'
        '<p style="text-align:center;">AWS Solutions Architect<br>'
        'Tableau Specialist<br>Scrum Master</p>'
        '</div>',
        unsafe_allow_html=True,
    )
