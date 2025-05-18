import streamlit as st
import requests
import io
import PyPDF2

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume bullets (optional) ---
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
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"}
]

# --- Global CSS & Background ---
st.markdown(
    '''
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
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
.profile-pic {
  border-radius: 50%;
  width: 150px;
  display: block;
  margin: 0 auto 12px;
}
.contact-icon {
  width: 30px;
  height: 30px;
  filter: invert(100%);
  margin: 0 8px;
  vertical-align: middle;
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
}
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { from, to { border-color: transparent; } 50% { border-color: #5A84B4; } }
.details-summary {
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%) !important;
  color: #ffffff !important;
  font-size: 1.6rem !important;
  font-weight: bold !important;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 10px;
  text-align: center;
  cursor: pointer;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
/* ---- Flippable side card CSS ---- */
.flip-side-card {
  background: none;
  border: none;
  padding: 0;
  width: 100%;
  perspective: 1200px;
  margin-bottom: 22px;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.7s cubic-bezier(.4,2,.45,.8);
  transform-style: preserve-3d;
}
.flip-side-card.flipped .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  min-height: 220px;
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 5px 22px rgba(30,40,80,0.14);
  backface-visibility: hidden;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.flip-card-front { z-index: 2; }
.flip-card-back {
  transform: rotateY(180deg);
  background: linear-gradient(135deg, #1ABC9C 0%, #324665 100%);
  color: #fff;
  z-index: 1;
}
.flip-card-back .back-content {
  padding: 18px 10px;
  font-size: 1.07rem;
}
</style>
<script>
window.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll('.flip-side-card').forEach(card => {
    card.addEventListener('click', function(e) {
      e.currentTarget.classList.toggle('flipped');
    });
  });
});
</script>
    ''', unsafe_allow_html=True
)

# --- Layout ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="large")

# --- Left Pane (All flippable) ---
with left_col:
    # Profile Card
    st.markdown('''
<div class="flip-side-card" title="Click to flip!">
  <div class="flip-card-inner">
    <div class="flip-card-front card hover-zoom">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic"/>
      <h2>Venkatesh Soundararajan</h2>
      <p><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p>
    </div>
    <div class="flip-card-back card hover-zoom">
      <div class="back-content">👋 Hi, I’m Venkatesh!<br>I love data, building solutions, and collaborating with teams.<br>Click to flip back.</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

    # Contact Card
    st.markdown('''
<div class="flip-side-card" title="Click to flip!">
  <div class="flip-card-inner">
    <div class="flip-card-front card hover-zoom">
      <div class="section-title" style="background:#2C3E50;">Contact</div>
      <div style="display:flex; justify-content:center; gap:16px; margin-top:10px;">
        <a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>
        <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>
        <a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>
      </div>
    </div>
    <div class="flip-card-back card hover-zoom">
      <div class="back-content">Let’s connect!<br>Email or DM me on LinkedIn.<br>Click to flip back.</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

# --- Center Pane (NOT flippable) ---
with mid_col:
    # Intro card only (no chat)
    st.markdown(
        '<div class="card hover-zoom"><div class="typewriter"><h1>Hello!</h1></div>'
        '<p>Welcome to my data science portfolio. Explore my projects below.</p></div>',
        unsafe_allow_html=True
    )

    # --- Projects Showcase ---
    grid_html = '<div class="grid-container">'
    for proj in projects:
        grid_html += (
            f'<div class="project-item hover-zoom"><a href="{proj["url"]}" target="_blank">'
            f'<img src="{proj["image"]}" class="card-img"/><div class="overlay">{proj["title"]}</div></a></div>'
        )
    grid_html += '</div>'

    st.markdown(
        f"""
<details open>
  <summary class="details-summary">Projects Showcase</summary>
  {grid_html}
</details>
""",
        unsafe_allow_html=True
    )

# --- Right Pane (All flippable) ---
with right_col:
    # Skills Card
    st.markdown('''
<div class="flip-side-card" title="Click to flip!">
  <div class="flip-card-inner">
    <div class="flip-card-front card hover-zoom">
      <div class="section-title" style="background:#1ABC9C;">Skills</div>
      <p style="text-align:center;">Python, SQL, R<br>AWS & SageMaker<br>Streamlit, Tableau<br>Scikit-learn, OpenCV<br>Git, Agile</p>
    </div>
    <div class="flip-card-back card hover-zoom">
      <div class="back-content">Proficient in Data Science, ML, AWS, and BI.<br>Always eager to learn new tools.<br>Click to flip back.</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

    # Experience Card
    st.markdown('''
<div class="flip-side-card" title="Click to flip!">
  <div class="flip-card-inner">
    <div class="flip-card-front card hover-zoom">
      <div class="section-title" style="background:#8E44AD;">Experience</div>
      <p style="text-align:center;">Deloitte Quality Lead (8+ yrs)<br>AWS Data Pipelines<br>Agile Team Lead<br>Risk Analytics</p>
    </div>
    <div class="flip-card-back card hover-zoom">
      <div class="back-content">Hands-on with project management, process optimization, and risk analytics in top firms.<br>Click to flip back.</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

    # Certifications Card
    st.markdown('''
<div class="flip-side-card" title="Click to flip!">
  <div class="flip-card-inner">
    <div class="flip-card-front card hover-zoom">
      <div class="section-title" style="background:#D35400;">Certifications</div>
      <p style="text-align:center;">AWS Solutions Architect<br>Tableau Specialist<br>Scrum Master</p>
    </div>
    <div class="flip-card-back card hover-zoom">
      <div class="back-content">Certified in cloud architecture, BI, and agile.<br>Always upskilling.<br>Click to flip back.</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)
