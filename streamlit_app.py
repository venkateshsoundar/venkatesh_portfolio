import streamlit as st
from openai import OpenAI
from ats_tool import extract_text_from_pdf, calculate_ats_score, tailor_resume
from portfolio_carousel import render_section_carousel

# Initialize OpenAI client lazily to speed up app start
@st.cache_resource
def get_openai_client():
    api_key = st.secrets.get("DEEPSEEK_API_KEY")
    if not api_key:
        return None
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# ---- PAGE CONFIG & GLOBAL CSS ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")


# ---- FREEZED (FIXED) NAVIGATION BAR ----
st.markdown("""
<style>
:root {
    --navbar-total-height: 0px;
    --section-gap: 32px;
}
body {
    margin: 0 !important;
    padding: 0 !important;
}
header[data-testid="stHeader"],
div[data-testid="stToolbar"] {
    display: none !important;
}
[data-testid="stAppViewContainer"] .main .block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
[data-testid="stAppViewContainer"] .main .block-container > [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
[data-testid="stMainBlockContainer"],
.stMainBlockContainer,
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
.hero-card,
.card,
.skills-section {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}
div[data-testid="stElementContainer"]:has(.navbar-container) {
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar-container {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    z-index: 1000;
    background:
        linear-gradient(rgba(18, 32, 61, 0.72), rgba(31, 42, 68, 0.86)),
        url("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif") center/cover no-repeat;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    border-radius: 0 0 18px 18px;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}
.sticky-spacer {
    display: none !important;
}
.navbar {
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
    gap: 10px;
    padding: 12px 0 10px 0;
    margin: 0;
    border-radius: 0 0 18px 18px;
    background: rgba(31, 42, 68, 0.38);
    backdrop-filter: brightness(0.86);
    overflow-x: auto;
}
.navbar a {
    color: #ffd166;
    font-weight: bold;
    font-size: 1.08rem;
    text-decoration: none;
    padding: 7px 18px;
    border-radius: 8px;
    transition: color 0.18s, background 0.18s;
    white-space: nowrap;
}
.navbar a:hover {
    background: #ffd16633;
    color: #fff;
}
.mobile-nav-toggle {
    display: none;
}
@media screen and (max-width: 768px) {
    .navbar-container {
        position: relative;
        border-radius: 0;
    }
    .sticky-spacer {
        height: 0 !important;
    }
    .main .block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
    .navbar {
        display: none;
        flex-direction: column;
        align-items: stretch;
        gap: 14px;
        width: 100%;
        padding: 10px 0;
    }
    .navbar.show {
        display: flex;
    }
    .navbar a {
        width: 100%;
        text-align: center;
        padding: 10px 20px;
        font-size: 1rem;
    }
    .mobile-nav-toggle {
        display: block;
        background: rgba(31, 42, 68, 0.68);
        color: #ffd166;
        font-weight: bold;
        font-size: 1.5rem;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        border: none;
        margin-bottom: 10px;
        width: 100%;
        text-align: center;
    }
}

</style>

<!-- Sticky Nav HTML -->
<div class="navbar-container">
  <button class="mobile-nav-toggle" onclick="toggleMenu()">☰ Menu</button>
  <div class="navbar" id="navbarLinks">
    <a href="#about">About Me</a>
    <a href="#education">Education</a>
    <a href="#experience">Experience</a>
    <a href="#certifications">Certifications</a>
    <a href="#recognitions">Recognitions</a>
    <a href="#projects">Projects Gallery</a>
    <a href="#skills">Skills</a>
  </div>
</div>

<!-- Spacer so content isn't overlapped -->
<div class="sticky-spacer"></div>

<script>
const root = document.documentElement;
const navbarContainer = document.querySelector('.navbar-container');
const spacer = document.querySelector('.sticky-spacer');
const navbarLinks = document.getElementById('navbarLinks');

function updateNavbarOffset() {
  if (!navbarContainer) {
    return;
  }

  const computedStyle = window.getComputedStyle(navbarContainer);
  const position = computedStyle.position;
  let totalHeight = 0;

  if (position === 'fixed') {
    const computedTop = parseFloat(computedStyle.top) || 0;
    totalHeight = Math.max(0, navbarContainer.getBoundingClientRect().height + computedTop);
  }

  root.style.setProperty('--navbar-total-height', `${totalHeight}px`);

  if (spacer) {
    spacer.style.height = `${totalHeight}px`;
  }
}

function toggleMenu() {
  if (!navbarLinks) {
    return;
  }
  navbarLinks.classList.toggle('show');
  requestAnimationFrame(updateNavbarOffset);
}

function handleResize() {
  if (navbarLinks && window.innerWidth > 768) {
    navbarLinks.classList.remove('show');
  }
  updateNavbarOffset();
}

window.addEventListener('load', () => {
  updateNavbarOffset();
  requestAnimationFrame(updateNavbarOffset);
});
window.addEventListener('resize', handleResize);
window.addEventListener('orientationchange', () => requestAnimationFrame(updateNavbarOffset));

if (window.ResizeObserver && navbarContainer) {
  const resizeObserver = new ResizeObserver(() => updateNavbarOffset());
  resizeObserver.observe(navbarContainer);
}

if (window.MutationObserver && navbarLinks) {
  const mutationObserver = new MutationObserver(() => updateNavbarOffset());
  mutationObserver.observe(navbarLinks, { attributes: true, childList: true, subtree: true });
}
</script>
""", unsafe_allow_html=True)


st.markdown("""
<style>
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
  margin-bottom: 16px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  text-align: center;
}
.card:hover, .card.hover-zoom:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 8px 16px rgba(0,0,0,0.24);
}
.section-title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 6px;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 32px;
}
.project-item {
  position: relative;
  aspect-ratio: 1/1;
  overflow: hidden;
  border-radius: 12px;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
}
.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1);
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
.profile-pic-popout {
  width: 160px;
  height: 200px;
  object-fit: cover;
  border-radius: 0%;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.18);
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 20px;
  z-index: 10;
}
.profile-card-container {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}
.profile-card-content {
  padding-top: 200px;
}
.contact-icon {
  width: 32px;
  height: 32px;
  filter: invert(100%);
  color:#ADD8E6;
  margin: 0 8px;
  vertical-align: middle;
}
.edu-cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 20px;
  margin-bottom: 18px;
}
.edu-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 15px;
  padding: 22px 14px 16px 14px;
  box-shadow: 0 2px 10px rgba(30,50,80,0.13);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 170px;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  border: 2px solid #40649622;
}
.edu-card:hover {
  transform: translateY(-4px) scale(1.015);
  box-shadow: 0 8px 18px rgba(20,40,80,0.19);
  background: linear-gradient(135deg, #406496 0%, #34495E 100%);
}
.edu-card-logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 11px;
  background: #fff;
  margin-bottom: 10px;
  box-shadow: 0 1px 8px rgba(44,62,80,0.09);
  border: 1.5px solid #eee;
}
.edu-card-degree { font-weight: 700; font-size: 1.12rem; margin-bottom: 3px; color: #ffd166;}
.edu-card-univ { color: #ADD8E6; font-size: 1.01rem; margin-bottom: 4px;}
.edu-card-date { color: #fff; font-size: 0.98rem;}
.edu-research-row {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 72px 1fr;
  align-items: center;
  gap: 18px;
  min-height: 0;
  padding: 18px 22px;
  text-align: left;
}
.edu-research-row .edu-card-logo {
  margin: 0;
}
.edu-research-content {
  text-align: left;
}
.edu-research-summary {
  color: #fff;
  font-size: 0.95rem;
  line-height: 1.55;
  margin-top: 8px;
  opacity: 0.92;
}
@media (max-width: 700px) {
  .edu-cards-grid {
    grid-template-columns: 1fr;
  }
  .edu-research-row {
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
  }
  .edu-research-content {
    text-align: center;
  }
}
/* Awards/Certifications */
.cert-grid, .awards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 18px;
  margin-bottom: 2px;
}
.cert-card, .award-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(60,100,160,0.07);
  padding: 18px 18px 14px 18px;
  min-height: 80px;
  transition: transform .17s, box-shadow .17s;
  border: 1.5px solid #40649644;
  text-align: left;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.cert-card:hover, .award-card:hover {
  transform: translateY(-3px) scale(1.015);
  box-shadow: 0 8px 24px rgba(20,60,120,0.15);
  background: linear-gradient(135deg, #22304A 0%, #406496 88%);
}
.cert-title, .award-title { font-weight: bold; font-size: 1.07rem; color: #ffd166; margin-bottom: 2px; margin-top: 0;}
.cert-provider, .award-sub { font-size: 0.99rem; color: #ADD8E6; margin-bottom: 2px;}
.cert-year, .award-year { font-size: 0.97rem; color: #fff; opacity: 0.8;}
.award-year {margin-bottom: 2px;}
/* Experience */
.exp-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 18px;
  margin-top: 20px;
  margin-bottom: 20px;
}
.exp-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 15px;
  padding: 22px 14px 16px 14px;
  box-shadow: 0 2px 10px rgba(30,50,80,0.13);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 215px;
  transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s;
  border: 2px solid #40649622;
}
.exp-card:hover {
  transform: translateY(-4px) scale(1.015);
  box-shadow: 0 8px 18px rgba(20,40,80,0.19);
  background: linear-gradient(135deg, #406496 0%, #34495E 100%);
}
.exp-card-logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
  border-radius: 11px;
  background: #fff;
  margin-bottom: 10px;
  box-shadow: 0 1px 8px rgba(44,62,80,0.09);
  border: 1.5px solid #eee;
}
.exp-card a.toggle-link {
      display: block;
      color: #ffd166;
      margin-top: 10px;
      font-weight: 500;
      cursor: pointer;
      text-align: right;
}
.exp-card-title { font-weight: 700; font-size: 1.12rem; margin-bottom: 3px;}
.exp-card-company { color: #ADD8E6; font-size: 1.01rem; margin-bottom: 6px;}
.exp-card-date { color: #ffd166; font-size: 0.98rem;}
.current-badge {
  display: inline-flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #dff7e6;
  color: #14532d;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.exp-impact {
  width: 100%;
  margin-top: 12px;
  padding: 9px 11px;
  border-left: 3px solid #ffd166;
  border-radius: 8px;
  background: rgba(31, 42, 68, 0.48);
  color: #fff;
  font-size: 0.84rem;
  line-height: 1.45;
  text-align: left;
}
.exp-impact strong {
  color: #ffd166;
}
/* Skills */
.skills-category {
  margin-bottom: 14px;
}
.skills-header {
  font-size: 1.04rem;
  color: #ffd166;
  font-weight: 600;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.skill-icon {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  filter: brightness(0.95) invert(0.09) sepia(1) hue-rotate(165deg) saturate(6);
}
.skills-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 2px;
}
.section-anchor {
  display: block;
  height: var(--section-gap);
  scroll-margin-top: 160px; /* or 100px, depending on your navbar height */
}
.skill-chip {
  background: rgba(255,255,255,0.12);
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 0.97rem;
  color: #fff;
  font-weight: 500;
  border: 1.5px solid #40649633;
}
.profile-row {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: stretch;
  margin-bottom: 30px;
}
.profile-card, .about-card {
  flex: 1 1 0px;
  min-width: 250px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  border-radius: 16px;
  padding: 32px 18px 24px 18px;
  box-shadow: 0 3px 16px rgba(44,62,80,0.16);
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeUpCard .85s cubic-bezier(.5,1.6,.4,1) both;
}
.profile-card {
  max-width: 340px;
  justify-content: flex-start;
}
.profile-pic-square {
  width: 130px;
  height: 130px;
  object-fit: cover;
  border-radius: 24px;
  border: 2.5px solid #fff;
  margin-bottom: 18px;
  box-shadow: 0 2px 10px rgba(44,62,80,0.17);
}
.about-card {
  align-items: flex-start;
  justify-content: flex-start;
}
@media (max-width: 900px) {
  .profile-row {
    flex-direction: column;
    gap: 18px;
  }
  .about-card, .profile-card {
    min-width: 0;
    width: 100%;
  }
}
.exp-responsibilities-box {    
    padding: 12px 16px;
    border-radius: 10px;
    margin-top: 14px;    
    font-size: 13px;
    font-style: normal;
    line-height: 1.6;
    background: rgba(31, 42, 68, 0.24);
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

projects = [
    {
        "title": "Weather Data Pipeline (AWS)",
        "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg",
        "tools": ["AWS", "Python", "Streamlit"],
        "desc": "Built an automated AWS pipeline for weather-data ingestion, storage, processing, and dashboard reporting."
    },
    {
        "title": "Canadian Quality of Life Analysis",
        "url": "https://github.com/venkateshsoundar/canadian-qol-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg",
        "tools": ["Python", "Pandas", "Tableau"],
        "desc": "Compared quality-of-life indicators across Canadian provinces through reproducible analysis and visualization."
    },
    {
        "title": "Toronto Crime Drivers",
        "url": "https://github.com/venkateshsoundar/toronto-crime-drivers",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg",
        "tools": ["Python", "Pandas", "Matplotlib"],
        "desc": "Analyzed neighborhood-level crime patterns to identify key drivers and communicate actionable urban insights."
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
        "title": "Alberta Wildfire Analysis",
        "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg",
        "tools": ["Python", "GeoPandas", "Power BI"],
        "desc": "Combined geospatial analysis and dashboards to examine wildfire patterns and risk trends across Alberta."
    },
    {
        "title": "Gmail Sentiment Analysis",
        "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg",
        "tools": ["Python", "NLTK", "Gmail API"],
        "desc": "Created an NLP workflow to classify email sentiment and summarize communication patterns from Gmail data."
    },
    {
        "title": "Penguin Species Prediction Chatbot",
        "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg",
        "tools": ["Python", "Scikit-learn", "Streamlit"],
        "desc": "Developed an interactive machine-learning application that predicts penguin species from user inputs."
    },
    {
        "title": "Uber Ride Prediction",
        "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg",
        "tools": ["Python", "XGBoost", "Matplotlib"],
        "desc": "Predicted Uber ride durations using machine learning and explained predictions with visualizations."
    }
]


st.markdown('<a name="about" class="section-anchor"></a>', unsafe_allow_html=True)
st.markdown("""
<style>
.hero-card {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  gap: 0;
  background: linear-gradient(135deg, #253451 0%, #324665 100%);
  border-radius: 24px;
  box-shadow: 0 6px 26px rgba(20,30,55,0.18), 0 2px 14px rgba(44,62,80,0.08);
  margin: 16px 0;
  min-height: 330px;
  position: relative;
  overflow: hidden;
  transition: transform .33s cubic-bezier(.37,1.7,.7,1), box-shadow .33s;
}
.hero-card:hover {
  transform: translateY(-3px) scale(1.005);
  box-shadow: 0 14px 38px 0 #ffd16630, 0 2px 18px rgba(44,62,80,0.12);
}
.hero-left {
  flex: 1 1 0px;
  min-width: 320px;
  max-width: 430px;
  background: linear-gradient(135deg, #253451 70%, #ffd16610 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 38px 0 26px 0;
  box-shadow: 2px 0 18px 0 #ffd16609;
  z-index: 1;
}
.hero-pic-glow {
  display: flex !important;
  justify-content: center !important;
  margin-bottom: 20px !important;
}
.hero-pic-glow img {
  width: 230px !important;
  height: 230px !important;
  border-radius: 50% !important;
  border: none !important;
  background: none !important;
  box-shadow: 0 12px 32px rgba(0,0,0,0.28) !important;
  object-fit: cover !important;
  object-position: center !important;
}
.hero-name {
  color: #fff;
  font-size: 2.44rem;
  font-weight: 800;
  text-align: center;
  margin: 6px 0 0 0;
  line-height: 1.17;
  letter-spacing: 0.01em;
}
.hero-role {
  color: #ADD8E6;
  font-size: 1.03rem;
  margin-top: 3px;
  margin-bottom: 0px;
  text-align: center;
}
.hero-location {
  color: #FFFFE0;
  font-weight: 600;
  margin-top: 8px;
  font-size: 1.01rem;
  text-align: center;
}

.hero-right {
  flex: 2 1 0px;
  padding: 38px 38px 16px 38px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background: none;
}
.hero-about-title {
  font-size: 1.13rem;
  color: #ffd166;
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: .01em;
}
.hero-about-body {
  font-size: 1.09rem;
  color: #fff;
  line-height: 1.7;
  margin-bottom: 18px;
}
.achievement-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 18px;
}
.achievement-item {
  padding: 12px 8px;
  border: 1px solid rgba(255, 209, 102, 0.24);
  border-radius: 12px;
  background: rgba(31, 42, 68, 0.46);
  text-align: center;
}
.achievement-value {
  display: block;
  color: #ffd166;
  font-size: 1.18rem;
  font-weight: 800;
  line-height: 1.15;
}
.achievement-label {
  display: block;
  margin-top: 5px;
  color: #fff;
  font-size: 0.76rem;
  line-height: 1.3;
}
.hero-contact-bar {
  width: 100%;
  margin-top: 6px;
  background: rgba(90, 130, 160, 0.12);
  border-radius: 13px;
  padding: 12px 0 6px 0;
  text-align: center;
  box-shadow: 0 2px 14px rgba(255,209,102,0.04);
}
.hero-contact-bar-title {
  color: #fff;
  font-weight: 600;
  font-size: 1.10rem;
  margin-bottom: 5px;
  letter-spacing: 0.01em;
}
.hero-contact-icons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  margin-top: 7px;
  margin-bottom: 3px;
}
.hero-contact-icons a {
  display: inline-block;
  border-radius: 8px;
  padding: 3px;
  transition: background 0.15s, transform 0.15s;
}
.hero-contact-icons a:hover {
  background: #ffd16633;
  transform: translateY(-2px) scale(1.05);
}
.hero-contact-icons img {
  width: 30px;
  height: 30px;
  filter: invert(100%);
}
.hero-cta-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 16px;
}
.hero-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 145px;
  padding: 11px 16px;
  border: 1px solid rgba(255, 209, 102, 0.55);
  border-radius: 12px;
  background: transparent;
  color: #ffd166 !important;
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none !important;
  transition: transform 0.18s ease, background 0.18s ease, color 0.18s ease;
}
.hero-cta.primary {
  background: #ffd166;
  color: #22304A !important;
}
.hero-cta:hover {
  transform: translateY(-2px);
  background: rgba(255, 209, 102, 0.16);
  color: #fff !important;
}
.hero-cta.primary:hover {
  background: #ffe29a;
  color: #22304A !important;
}


@media (max-width: 900px) {
  .hero-card {flex-direction: column;align-items: center;}
  .hero-right, .hero-left {max-width:100%;padding:28px 8vw 12px;}
  .achievement-strip {grid-template-columns: repeat(2, minmax(0, 1fr));}
}
@media (max-width: 520px) {
  .achievement-strip {grid-template-columns: 1fr;}
  .hero-cta {width: 100%;}
}
</style>

<div class="hero-card" data-portfolio-section="about">
  <div class="hero-left">
    <div class="hero-pic-glow">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh_Profile_2026.jpg" alt="Venkatesh Soundararajan"/>
    </div>
    <div class="hero-name">Venkatesh<br>Soundararajan</div>
    <div class="hero-role">Senior Data Quality Engineer<br>RBC</div>
    <div class="hero-location">Halifax Metropolitan Area, Canada</div>
  </div>
  <div class="hero-right">
    <div class="hero-about-title">About Me</div>
    <div class="hero-about-body">
      I’m Venkatesh, a <b>Senior Data Quality Engineer at RBC</b> with 8+ years of experience in data quality, ETL validation, quality engineering, and Guidewire P&amp;C insurance.
      I use <b>SQL, Python, automation, API testing, and cloud platforms</b> to build accurate, traceable, production-ready data solutions.
      With a Master’s in Data Science and Analytics from the <b>University of Calgary</b>, I connect technical quality with dependable business outcomes.
    </div>
    <div class="achievement-strip" aria-label="Career highlights">
      <div class="achievement-item"><span class="achievement-value">8+ Years</span><span class="achievement-label">Data &amp; Quality Engineering</span></div>
      <div class="achievement-item"><span class="achievement-value">95%</span><span class="achievement-label">Defect Removal Efficiency</span></div>
      <div class="achievement-item"><span class="achievement-value">40%</span><span class="achievement-label">Fewer Post-Release Issues</span></div>
      <div class="achievement-item"><span class="achievement-value">15</span><span class="achievement-label">QA Professionals Led</span></div>
    </div>
    <div class="hero-contact-bar">
      <div class="hero-contact-bar-title">Contact</div>
      <div class="hero-contact-icons">
        <a href="mailto:venkatesh.balusoundar@gmail.com" aria-label="Email Venkatesh"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" alt="Email"/></a>
        <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank" rel="noopener noreferrer" aria-label="Venkatesh on LinkedIn"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" alt="LinkedIn"/></a>
        <a href="https://github.com/venkateshsoundar" target="_blank" rel="noopener noreferrer" aria-label="Venkatesh on GitHub"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" alt="GitHub"/></a>
        <a href="https://medium.com/@venkatesh.balusoundar" target="_blank" rel="noopener noreferrer" aria-label="Venkatesh on Medium"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg" alt="Medium"/></a>
      </div>
    </div>
    <div class="hero-cta-row">
      <a class="hero-cta primary" href="mailto:venkatesh.balusoundar@gmail.com">Contact Me</a>
      <a class="hero-cta" href="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf" target="_blank" rel="noopener noreferrer">Download Resume</a>
      <a class="hero-cta" href="https://www.linkedin.com/in/venkateshbalus/" target="_blank" rel="noopener noreferrer">View LinkedIn</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<a name="education" class="section-anchor"></a>', unsafe_allow_html=True)
# --- Spacer before next section ---
st.markdown(
    """
    <div class="card hover-zoom" data-portfolio-section="education">
      <div class="section-title" style="background:#34495E;">Education</div>
      <div class="edu-cards-grid">
        <div class="edu-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Uoc.png" class="edu-card-logo"/>
          <div class="edu-card-degree">Masters in Data Science and Analytics</div>
          <div class="edu-card-univ">University of Calgary, Alberta, Canada</div>
          <div class="edu-card-date">September 2024 – 2025</div>
        </div>
        <div class="edu-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/AnnaUniversity.png" class="edu-card-logo"/>
          <div class="edu-card-degree">Bachelor of Engineering</div>
          <div class="edu-card-univ">Anna University, Chennai, India</div>
          <div class="edu-card-date">August 2009 – May 2013</div>
        </div>
        <div class="edu-card edu-research-row">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Uoc.png" class="edu-card-logo" alt="University of Calgary logo"/>
          <div class="edu-research-content">
            <div class="edu-card-degree">Research Assistant Intern</div>
            <div class="edu-card-univ">University of Calgary, Canada</div>
            <div class="edu-card-date">April 2025 – December 2025</div>
            <div class="edu-research-summary">Researched an on-device eye-gaze and blink-based communication system for non-verbal ICU patients, evaluating computer-vision and machine-learning approaches with a focus on privacy, accessibility, and reliable real-time interaction.</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<a name="experience" class="section-anchor"></a>', unsafe_allow_html=True)
st.markdown(
    """  
    <div class="card hover-zoom" data-portfolio-section="experience">
      <div class="section-title" style="background:#34495E;">Professional Experience</div>
      <div class="exp-cards-grid">
        <div class="exp-card">
          <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/RBC.png" class="exp-card-logo" alt="RBC logo"/>
          <div class="current-badge">Current</div>
          <div class="exp-card-title">Senior Data Quality Engineer</div>
          <div class="exp-card-company">RBC, Canada</div>
          <div class="exp-card-date">April 2026 – Present</div>
          <div class="exp-responsibilities-box">
            Supporting enterprise data quality through SQL- and Python-based validation, ETL control checks, defect investigation, and cross-functional collaboration to improve data accuracy, traceability, and production reliability.
          </div>
          <div class="exp-impact"><strong>Focus:</strong> Enterprise ETL controls, traceability, and reliable production data.</div>
        </div>
        <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/TI.png" class="exp-card-logo" alt="TechInsights logo"/>
          <div class="exp-card-title">Software Development Intern – Data Engineering</div>
          <div class="exp-card-company">TechInsights Inc · Riipen / RBC Future Launch</div>
          <div class="exp-card-date">May 2025 – August 2025</div>
          <div class="exp-responsibilities-box">
            Built data-lineage and ETL-governance workflows for Salesforce-to-PostgreSQL pipelines using AWS DataZone, OpenLineage, Great Expectations, and MuleSoft. Standardized lineage events and validation checkpoints to strengthen data integrity, audit readiness, and operational visibility.
          </div>
          <div class="exp-impact"><strong>Scope:</strong> Standardized governance patterns across 7 key Salesforce data flows.</div>
        </div>
        <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Deloitte.png" class="exp-card-logo" alt="Deloitte logo"/>
          <div class="exp-card-title">Senior Consultant – Guidewire BSA &amp; Quality Engineer</div>
          <div class="exp-card-company">Deloitte Consulting India Private Limited</div>
          <div class="exp-card-date">June 2024 – August 2024</div>
          <div class="exp-responsibilities-box">
            Led business analysis and quality engineering for Guidewire PolicyCenter, BillingCenter, and ClaimCenter initiatives. Translated requirements into testable outcomes, coordinated stakeholders, and supported SQL, API, ETL, and release-quality validation.
          </div>
          <div class="exp-impact"><strong>Impact:</strong> Increased regression coverage by 40% and reduced post-release issues by 40%.</div>
        </div>
        <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Capgemini.png" class="exp-card-logo" alt="Capgemini logo"/>
          <div class="exp-card-title">Consultant – Quality Engineering</div>
          <div class="exp-card-company">Capgemini Technology Services India Private Limited</div>
          <div class="exp-card-date">May 2018 – October 2021</div>
          <div class="exp-responsibilities-box">
            Led end-to-end testing for Guidewire Workers’ Compensation workflows and developed automation for regression execution, real-time failure alerts, and issue tracking. Mentored QA team members and supported Agile delivery and CI/CD practices.
          </div>
          <div class="exp-impact"><strong>Delivery:</strong> End-to-end Guidewire QA with automation, alerts, Agile, and CI/CD support.</div>
        </div>
        <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Cognizant.png" class="exp-card-logo" alt="Cognizant logo"/>
          <div class="exp-card-title">Associate – Application &amp; Quality Engineering</div>
          <div class="exp-card-company">Cognizant Technology Solutions India Private Limited</div>
          <div class="exp-card-date">September 2013 – May 2018</div>
          <div class="exp-responsibilities-box">
            Supported enterprise healthcare applications through DB2 validation, COBOL/JCL batch testing, production-incident analysis, and test-environment coordination. Monitored critical batch workflows and led knowledge-transfer activities to strengthen operational readiness.
          </div>
          <div class="exp-impact"><strong>Technology scope:</strong> DB2, COBOL, and JCL across batch validation and production support.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<a name="certifications" class="section-anchor"></a>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="card hover-zoom" data-portfolio-section="certifications">
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
    </div>""", unsafe_allow_html=True)
st.markdown('<a name="recognitions" class="section-anchor"></a>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="card hover-zoom" data-portfolio-section="recognitions">
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
    """,
    unsafe_allow_html=True
)


# --- Your projects list goes here (use the same list as above) ---
st.markdown('<a name="projects" class="section-anchor"></a>', unsafe_allow_html=True)
st.markdown("""
<style>
.card.projects-gallery-pane {
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  border-radius: 18px;
  box-shadow: 0 4px 28px rgba(44,62,80,0.14);
  padding: 22px 18px 28px 18px;
  margin-bottom: 22px;
  /* Remove max-width and margin auto for full width like other sections */
}
.section-title {
  font-size: 1.35rem;
  font-weight: bold;
  margin-bottom: 22px;
  color: #ffd166;
  background:#2C3E50;
  padding: 12px 0 12px 0;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 1px 8px #22304A22;
}
.projects-4col-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 12px 32px #ffd1661c, 0 2px 8px #22304A19;
  z-index: 2;
}
.project-img-holder {
  width: 100%;
  background: #222E40;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  padding-bottom: 10px;
}
.project-img-inner {
  width: 90px;
  height: 90px;
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
  transform: scale(1.07);
}
.project-card-info {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 8px 16px 16px 16px;
}
.project-title {
  font-size: 1.07rem;
  font-weight: bold;
  color: #ffd166;
  margin-bottom: 6px;
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
.project-card-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}
.project-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 12px;
  border: 1px solid rgba(255, 209, 102, 0.55);
  border-radius: 9px;
  color: #ffd166 !important;
  font-size: 0.9rem;
  text-decoration: none !important;
  font-weight: 700;
  transition: background 0.15s ease, transform 0.15s ease;
}
.project-action.primary {
  background: #ffd166;
  color: #22304A !important;
}
.project-action:hover {
  transform: translateY(-2px);
  background: rgba(255, 209, 102, 0.16);
}
.project-action.primary:hover {
  background: #ffe29a;
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

projects_html = '''
<div class="card projects-gallery-pane hover-zoom" data-portfolio-section="projects">
  <div class="section-title">Featured Projects</div>
  <div class="projects-4col-grid">
'''

for proj in projects:
    tools_html = ''.join(f'<span class="project-tool-badge">{tool}</span>' for tool in proj["tools"])
    actions_html = (
        f'<a class="project-action primary" href="{proj["url"]}" target="_blank" '
        f'rel="noopener noreferrer">GitHub</a>'
    )
    if proj.get("demo_url"):
        actions_html = (
            f'<a class="project-action" href="{proj["demo_url"]}" target="_blank" '
            f'rel="noopener noreferrer">Live Demo</a>'
            + actions_html
        )
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
        f'<div class="project-card-actions">{actions_html}</div>'
        f'</div></div>'
    )

projects_html += '</div></div>'

st.markdown(projects_html, unsafe_allow_html=True)


st.markdown('<a name="skills" class="section-anchor"></a>', unsafe_allow_html=True)

st.markdown("""
<style>
.skills-section {
  background: linear-gradient(120deg, #22304A 0%, #324665 100%);
  border-radius: 28px;
  padding: 36px 18px 32px 18px;
  margin-bottom: 22px;
  box-shadow: 0 8px 34px rgba(20,30,55,0.11), 0 2px 14px rgba(44,62,80,0.09);
}
.skills-header-title {
  font-size: 1.35rem;
  font-weight: bold;
  color: #ffd166;
  background: #2C3E50;
  border-radius: 10px;
  padding: 12px 0;
  margin-bottom: 22px;
  text-align: center;
  box-shadow: 0 1px 8px #22304A22;
}
.skill-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px;
}
.skill-card {
  background: #1F2A44;
  color: white;
  width: 250px;
  padding: 20px 16px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  transition: transform 0.25s ease, box-shadow 0.25s;
}
.skill-card:hover {
  transform: translateY(-3px) scale(1.015);
  box-shadow: 0 12px 28px rgba(255,209,102,0.15), 0 6px 16px rgba(44,62,80,0.12);
}
.skill-title {
  font-size: 1.1rem;
  color: #ffd166;
  margin-bottom: 12px;
  font-weight: bold;
}
.skill-list {
  font-size: 0.9rem;
  line-height: 1.6;
  margin-top: 8px;
}
.skill-list p {
  margin: 0;
  padding: 2px 0;
}
.hover-zoom {
  transition: transform 0.25s ease, box-shadow 0.25s;
}
.hover-zoom:hover {
  transform: translateY(-2px) scale(1.008);
  box-shadow: 0 14px 32px rgba(255,209,102,0.12), 0 8px 22px rgba(44,62,80,0.1);
}
</style>


<div class="skills-section hover-zoom" data-portfolio-section="skills">
  <div class="skills-header-title">Core Skills and Tools</div>
  <div class="skill-grid">
<div class="skill-card">
  <div class="skill-title">Programming Languages</div>
  <div class="skill-list">
    <p>Python</p>
    <p>R</p>
    <p>Java</p>
    <p>Excel VBA</p>
  </div>
</div>
<div class="skill-card">
  <div class="skill-title">Cloud & Data</div>
  <div class="skill-list">
    <p>AWS</p>
    <p>MySQL</p>
    <p>Oracle</p>
  </div>
</div>
<div class="skill-card">
  <div class="skill-title">Data Viz & BI</div>
  <div class="skill-list">
    <p>Power BI</p>
    <p>Tableau</p>
    <p>Excel Dashboards</p>
  </div>
</div>
<div class="skill-card">
  <div class="skill-title">Dev Tools</div>
  <div class="skill-list">
    <p>Git</p>
  </div>
</div>
<div class="skill-card">
  <div class="skill-title">Project Management</div>
  <div class="skill-list">
    <p>JIRA</p>
    <p>HP ALM</p>
    <p>Rally</p>
  </div>
</div>
<div class="skill-card">
  <div class="skill-title">Insurance & QA</div>
  <div class="skill-list">
    <p>Guidewire Insurance Suite</p>
    <p>Functional Testing</p>
    <p>Selenium Automation</p>
  </div>
</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<span class="portfolio-carousel-end-marker" aria-hidden="true"></span>',
    unsafe_allow_html=True,
)
render_section_carousel()

ats_container = st.container()
with ats_container:
    st.markdown('<div class="card hover-zoom"><div class="section-title" style="background:#2C3E50;">ATS Resume Checker</div></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="ats_resume")
    job_desc = st.text_area("Job Description", key="ats_job_desc")
    if uploaded_file and job_desc:
        resume_text = extract_text_from_pdf(uploaded_file)
        score, matched, missing = calculate_ats_score(resume_text, job_desc)
        st.metric("ATS Score", f"{score}%")
        st.write("**Matched Keywords:**", ", ".join(matched) if matched else "None")
        st.write("**Missing Keywords:**", ", ".join(missing) if missing else "None")
        if missing and st.button("Tailor Resume", key="tailor_resume"):
            client = get_openai_client()
            if client is None:
                st.warning("API key not configured in Streamlit secrets.")
            else:
                tailored = tailor_resume(resume_text, job_desc, missing, client)
                st.text_area("Tailored Resume", value=tailored, height=400)
