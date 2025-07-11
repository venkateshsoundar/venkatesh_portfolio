import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# ---- PAGE CONFIG & GLOBAL CSS ----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# ---- FREEZED (FIXED) NAVIGATION BAR ----
st.markdown("""
<style>
.block-container {
    padding-top: 5 !important;
    margin-top: 5 !important;
}
body {
    margin-top: 5 !important;
    padding-top: 5 !important;
}
/* Fix navbar at top */
.navbar-container {
    position: fixed;
    top: 3.5rem;  /* Try 2.5rem, 3rem, or 56px until it fits perfectly under the toolbar */
    left: 0;
    width: 100%;
    z-index: 1000;
    background: #1F2A44;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    padding: 0 0 0 0;
    border-radius: 0 0 18px 18px;
}

/* Flex styling for links */
.navbar {
    display: flex;
    gap: 28px;
    justify-content: center;
    background: #1F2A44;
    padding: 12px 0 10px 0;
    border-radius: 0 0 18px 18px;
    margin-bottom: 20px;
    position: sticky;
    top: 0;
    z-index: 100;
}

/* Nav link styling */
.navbar a {
    color: #ffd166;
    font-weight: bold;
    font-size: 1.08rem;
    text-decoration: none;
    padding: 7px 22px;
    border-radius: 8px;
    transition: color 0.18s, background 0.18s;
}
.navbar a:hover {
    background: #ffd16633;
    color: #fff;
}

/* Push content down to not be hidden */
.sticky-spacer {
    height: 10px;
}
</style>

<!-- Sticky Nav HTML -->
<div class="navbar-container">
  <div class="navbar">
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
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Prevent sections from being hidden behind the sticky nav */
.section-anchor {
  scroll-margin-top: 120px;  /* Adjust based on navbar + Streamlit top padding */
}
</style>
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
  transform: translateY(-5px) scale(1.04);
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
  height: 160px;
  object-fit: cover;
  border-radius: 50%;
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
  transform: translateY(-7px) scale(1.03);
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
  transform: translateY(-4px) scale(1.03);
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
  transform: translateY(-7px) scale(1.03);
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
  scroll-margin-top: 120px; /* or 100px, depending on your navbar height */
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


# --- Custom Styling ---
st.markdown("""
<style>
/* Square profile pic with animation */
.profile-pic-square {
    width: 180px;
    height: 180px;
    border-radius: 20px;
    object-fit: cover;
    border: 4px solid #ffd166;
    box-shadow: 0 0 12px rgba(255, 209, 102, 0.6);
    margin: 0 auto 20px auto;
    display: block;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}
.profile-pic-square:hover {
    transform: scale(1.05);
    box-shadow: 0 0 24px rgba(255, 209, 102, 0.9);
}

/* Card styling */

.hover-zoom:hover {
    transform: scale(1.02);
}

/* Title style */
.section-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 12px;
    padding: 8px 16px;
    border-radius: 10px;
    color: #fff;
    background:#22304A;
}
</style>
""", unsafe_allow_html=True)

# --- 2-Column Layout: Left Profile / Right About ---
st.markdown("""
<style>
.profile-pic-square {
    width: 160px;
    height: 160px;
    border-radius: 20px;
    object-fit: cover;
    border: 4px solid #ffd166;
    box-shadow: 0 0 14px rgba(255, 209, 102, 0.6);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}
.profile-pic-square:hover {
    transform: scale(1.05);
    box-shadow: 0 0 24px rgba(255, 209, 102, 0.9);
}
.profile-card-wrapper {
    display: flex;
    flex-direction: row;
    gap: 30px;
    align-items: flex-start;
    justify-content: flex-start;
    flex-wrap: wrap;
}
.profile-left {
    flex: 0 0 180px;
    text-align: center;
}
.profile-right {
    flex: 1;
}
</style>
""", unsafe_allow_html=True)

gif_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif"
st.markdown(
    f"""
    <style>
      .welcome-card {{
        background: url("{gif_url}") center/cover no-repeat;
        border-radius: 16px;
        padding: 3rem;
        color: white;
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom:24px;
        box-shadow: 0 6px 30px 0 rgba(60,100,180,0.11), 0 1.5px 8px 0 rgba(60,60,90,0.08);
        transition: transform .35s cubic-bezier(.33,1.6,.66,1), box-shadow .33s;
        position: relative;
        cursor: pointer;
      }}
      .welcome-card:hover {{
        transform: scale(1.035) translateY(-7px);
        box-shadow: 0 14px 44px 0 #ffd16638, 0 2px 18px rgba(44,62,80,0.17);
        z-index: 4;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="welcome-card">
      <div>
        <h1>Hello and Welcome...</h1>
        <p>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

  
ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
st.markdown(
    f"""
    <style>
      .welcome-card2 {{
        background: url("{ai_url}") center/cover no-repeat;
        border-radius: 16px;
        padding: 0;
        color: white;
        height: 200px;
        position: relative;
        overflow: hidden;
        margin-bottom: 32px;
        box-shadow: 0 6px 24px 0 rgba(60,100,180,0.09), 0 1.5px 8px 0 rgba(60,60,90,0.08);
        transition: transform .35s cubic-bezier(.33,1.6,.66,1), box-shadow .33s;
        cursor: pointer;
      }}
      .welcome-card2:hover {{
        transform: scale(1.035) translateY(-7px);
        box-shadow: 0 14px 44px 0 #ffd16638, 0 2px 18px rgba(44,62,80,0.16);
        z-index: 4;
      }}
      .welcome-card2 .text-container {{
        position: absolute;
        top: 70%;
        right: 2rem;
        transform: translateY(-50%);
        text-align: right;
      }}
      .welcome-card2 h2 {{
        margin: 0;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="welcome-card2">
      <div class="text-container">
        <h2>Ask Buddy Bot!</h2>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

  
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = openai.OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=api_key,
  )

st.markdown("""
<style>
/* Force assistant message text to black */
div[data-testid="stChatMessageContent"] {
  background-color: #fff8dc !important;
  color: #000000 !important;
  border-radius: 16px;
  padding: 14px 18px;
  margin: 10px 0;
  font-size: 1rem;
  line-height: 1.6;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  border-left: 6px solid #ffd166;
  font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)


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
  margin-bottom: 32px;
  min-height: 330px;
  position: relative;
  overflow: hidden;
  transition: transform .33s cubic-bezier(.37,1.7,.7,1), box-shadow .33s;
}
.hero-card:hover {
  transform: translateY(-7px) scale(1.02);
  box-shadow: 0 14px 38px 0 #ffd16630, 0 2px 18px rgba(44,62,80,0.12);
}
.hero-left {
  flex: 1 1 0px;
  min-width: 260px;
  max-width: 340px;
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
  width: 130px;
  height: 130px;
  border-radius: 20%;
  margin-bottom: 17px;
  box-shadow: 0 0 0 4px #ffd16699, 0 0 16px 7px #ffd16644, 0 2px 14px rgba(44,62,80,0.09);
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
}
.hero-pic-glow img {
  width: 116px;
  height: 116px;
  border-radius: 20%;
  object-fit: cover;
  border: 3px solid #fff;
  background: #fff;
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
  color: #ffd166;
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
  margin-bottom: 26px;
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
  transform: translateY(-2px) scale(1.11);
}
.hero-contact-icons img {
  width: 30px;
  height: 30px;
  filter: invert(100%);
}


@media (max-width: 900px) {
  .hero-card {flex-direction: column;align-items: center;}
  .hero-right, .hero-left {max-width:100%;padding:28px 8vw 12px;}
}
</style>

<div class="hero-card">
  <div class="hero-left">
    <div class="hero-pic-glow">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"/>
    </div>
    <div class="hero-name">Venkatesh<br>Soundararajan</div>
    <div class="hero-role">Software Development Intern<br>Data Engineering</div>
    <div class="hero-location">🍁 Calgary, AB, Canada</div>
  </div>
  <div class="hero-right">
    <div class="hero-about-title">About Me</div>
    <div class="hero-about-body">
      I’m Venkatesh, a Data Scientist and Software Developer with <b>8+ years of experience</b> in quality engineering, business intelligence, and analytics.
      I specialize in building <b>scalable ETL pipelines</b>, predictive models, and interactive dashboards using cloud platforms like <b>AWS and Azure</b>.
      I'm currently pursuing my Master's in Data Science and Analytics at the <b>University of Calgary</b>.
      My passion lies in solving complex business problems with clean, actionable insights and AI-powered solutions.
    </div>
    <div class="hero-contact-bar">
      <div class="hero-contact-bar-title">Contact</div>
      <div class="hero-contact-icons">
        <a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg"/></a>
        <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg"/></a>
        <a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg"/></a>
        <a href="https://medium.com/@venkatesh.balusoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg"/></a>
      </div>
    </div>
    <div style="text-align: center; margin-top: 20px;">
  <button style="
      background: #ffd166; 
      color: #22304A; 
      font-weight: 700; 
      border-radius: 14px; 
      padding: 14px 36px; 
      font-size: 1.1rem; 
      border: none; 
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(255, 209, 102, 0.8);
      transition: background 0.25s ease;">
    <a href="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf" download style="color: #22304A; text-decoration: none;">⬇️ Download Resume</a>
  </button>
</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<a name="education" class="section-anchor"></a>', unsafe_allow_html=True)
# --- Spacer before next section ---
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

st.markdown('<a name="experience" class="section-anchor"></a>', unsafe_allow_html=True)
st.markdown(
    """  
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Professional Experience</div>
      <div class="exp-cards-grid">
        <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/TI.png" class="exp-card-logo"/>
          <div class="exp-card-title">Software Developer Intern - Data Engineering</div>
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




st.markdown('<a name="experience" class="section-anchor"></a>', unsafe_allow_html=True)

st.markdown(
    """  
    <div class="card hover-zoom">
      <div class="section-title" style="background:#34495E;">Professional Experience</div>
      <div class="exp-cards-grid">
        <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/TI.png" class="exp-card-logo"/>
          <div class="exp-card-title">Software Developer Intern - Data Engineering</div>
          <div class="exp-card-company">Tech Insights Inc, Canada</div>
          <div class="exp-card-date">May 2025 – Present</div> 
          <ul class="exp-responsibilities">
            <li>Developing scalable Data Lineage framework using AWS services (Glue, Lambda, S3, Athena)</li>
            <li>Automated ETL workflows supporting compliance and audit readiness</li>
            <li>Interactive dashboards using Power BI and AWS QuickSight</li>
            <li>Implemented validation checkpoints for enhanced data integrity</li>
          </ul>         
        </div>
      <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Deloitte.png" class="exp-card-logo"/>
          <div class="exp-card-title">Senior Consultant</div>
          <div class="exp-card-company">Deloitte Consulting India Private Limited, India</div>
          <div class="exp-card-date">October 2021 – August 2024</div>
          <ul class="exp-responsibilities">
            <li>Worked as Functional Analyst for Personal Lines insurance projects</li>
            <li>Participated in 3 Amigos sessions for requirement clarification</li>
            <li>Developed automated dashboard to improve delivery efficiency</li>
            <li>Used AWS EC2, DynamoDB, and S3 for cloud integration</li>
          </ul>
      </div>
      <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Capgemini.png" class="exp-card-logo"/>
          <div class="exp-card-title">Consultant</div>
          <div class="exp-card-company">Capgemini Technology Services India Private Limited, India</div>
          <div class="exp-card-date">May 2018 – October 2021</div>
          <ul class="exp-responsibilities">
            <li>End-to-end testing of Guidewire-based Worker Compensation policies</li>
            <li>Created automation tools for real-time failure alerts</li>
            <li>Mentored QA team and led agile initiatives</li>
          </ul>
      </div>
      <div class="exp-card">
          <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Cognizant.png" class="exp-card-logo"/>
          <div class="exp-card-title">Associate</div>
          <div class="exp-card-company">Cognizant Technology Solutions India Private Limited, India</div>
          <div class="exp-card-date">Sep 2013 – May 2018</div>
          <ul class="exp-responsibilities">
            <li>Specialized in DB2 database and batch processing testing</li>
            <li>Managed key metrics for $2M healthcare IT projects</li>
            <li>Led test environment setup and delivered KT sessions</li>
          </ul>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)



st.markdown('<a name="certifications" class="section-anchor"></a>', unsafe_allow_html=True)
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
    </div>""", unsafe_allow_html=True)
st.markdown('<a name="recognitions" class="section-anchor"></a>', unsafe_allow_html=True)
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
  margin-bottom: 32px;
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
  transform: translateY(-4px) scale(1.024);
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

st.markdown('<a name="skills" class="skills-section hover-zoom"></a>', unsafe_allow_html=True)

st.markdown("""
<style>
.skills-section {
  background: linear-gradient(120deg, #22304A 0%, #324665 100%);
  border-radius: 28px;
  padding: 36px 18px 32px 18px;
  margin-bottom: 36px;
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
  width: 220px;
  padding: 20px 16px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  transition: transform 0.25s ease, box-shadow 0.25s;
}
.skill-card:hover {
  transform: translateY(-6px) scale(1.04);
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
  transform: scale(1.02);
  box-shadow: 0 14px 32px rgba(255,209,102,0.12), 0 8px 22px rgba(44,62,80,0.1);
}
</style>

<div class="skills-section hover-zoom">
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
