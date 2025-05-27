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
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)",     "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws",     "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg"}
]



# ---- TABS ----
tabs = st.tabs(["Home", "Projects", "Experience", "Skills", "Contact"])

# ---- ABOUT TAB ----
st.markdown("""
<style>
.profile-pic-popout {
    width: 180px;
    border-radius: 50%;
    border: 4px solid #ffd166;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.4);
    margin-bottom: 12px;
}
.card {
    background: #1F2A44;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}
.hover-zoom:hover {
    transform: scale(1.02);
}
.section-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 12px;
    padding: 8px 16px;
    border-radius: 10px;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

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
.card {
    background: #1F2A44;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}
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
  transform: translateY(-7px) scale(1.016);
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
      I’m Venkatesh, a Data Scientist and Software Developer with <b>8+ years of experience</b> in quality engineering, business intelligence, and analytics.<br><br>
      I specialize in building <b>scalable ETL pipelines</b>, predictive models, and interactive dashboards using cloud platforms like <b>AWS and Azure</b>.<br><br>
      I'm currently pursuing my Master's in Data Science and Analytics at the <b>University of Calgary</b>.<br>
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
  </div>
</div>
""", unsafe_allow_html=True)


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

# --- Projects List (reuse your projects variable) ---
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

project_container = st.container()
    # --- Projects Showcase ---
with project_container:
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

st.markdown("""
<style>
.skills-main-vert-section {
  background: linear-gradient(120deg, #22304A 0%, #324665 100%);
  border-radius: 22px;
  box-shadow: 0 8px 38px rgba(30,50,90,0.12);
  padding: 28px 18px 24px 18px;
  margin-bottom: 34px;
}
.skills-category-title {
  font-size: 1.11rem;
  color: #ffd166;
  font-weight: 600;
  margin: 16px 0 8px 5px;
  letter-spacing: 0.01em;
}
.skills-scroll-container {
  display: flex;
  flex-direction: row;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 10px;
  margin-bottom: 10px;
  scrollbar-width: thin;
}
.skill-card-hz {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 13px;
  box-shadow: 0 4px 16px rgba(44,62,80,0.11);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 114px;
  max-width: 122px;
  padding: 16px 6px 12px 6px;
  text-align: center;
  transition: transform .18s, box-shadow .18s, background .18s;
  border: 2px solid #40649633;
  cursor: pointer;
  flex-shrink: 0;
}
.skill-card-hz:hover {
  transform: translateY(-5px) scale(1.07);
  box-shadow: 0 10px 20px #ffd16622;
  background: linear-gradient(135deg, #406496 0%, #ffd166 100%);
  color: #22304A !important;
}
.skill-icon-card-hz {
  width: 30px;
  height: 30px;
  margin-bottom: 8px;
  filter: drop-shadow(0 1px 4px #ffd16633);
}
.skill-label-card-hz {
  font-size: 1.01rem;
  font-weight: 600;
  color: #ffd166;
  letter-spacing: 0.01em;
}
@media (max-width: 700px) {
  .skills-main-vert-section {padding: 12px 1px;}
  .skills-scroll-container {gap: 9px;}
  .skill-card-hz {min-width: 82px;max-width:100px;padding:10px 2px 8px 2px;}
}
</style>

<div class="skills-main-vert-section">

  <div class="skills-category-title">Programming Languages</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/python.svg"/><span class="skill-label-card-hz">Python</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/r.svg"/><span class="skill-label-card-hz">R</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/sqlite.svg"/><span class="skill-label-card-hz">SQL</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/java.svg"/><span class="skill-label-card-hz">Java</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/vba.svg"/><span class="skill-label-card-hz">VBA Macro</span></div>
  </div>

  <div class="skills-category-title">Data Analysis & Scientific Computing</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/pandas.svg"/><span class="skill-label-card-hz">Pandas</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/numpy.svg"/><span class="skill-label-card-hz">NumPy</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/matplotlib.svg"/><span class="skill-label-card-hz">Matplotlib</span></div>
  </div>

  <div class="skills-category-title">Data Visualization</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/powerbi.svg"/><span class="skill-label-card-hz">Power BI</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/microsoftexcel.svg"/><span class="skill-label-card-hz">Excel</span></div>
  </div>

  <div class="skills-category-title">Database Management</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/mysql.svg"/><span class="skill-label-card-hz">MySQL</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/oracle.svg"/><span class="skill-label-card-hz">Oracle</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/mongodb.svg"/><span class="skill-label-card-hz">NoSQL</span></div>
  </div>

  <div class="skills-category-title">Version Control</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/git.svg"/><span class="skill-label-card-hz">Git</span></div>
  </div>

  <div class="skills-category-title">Project Management</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/jira.svg"/><span class="skill-label-card-hz">JIRA</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/alm.svg"/><span class="skill-label-card-hz">ALM</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/rally.svg"/><span class="skill-label-card-hz">Rally</span></div>
  </div>

  <div class="skills-category-title">QA Automation & Insurance Suite</div>
  <div class="skills-scroll-container">
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/selenium.svg"/><span class="skill-label-card-hz">Selenium</span></div>
    <div class="skill-card-hz"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/guidewire.svg"/><span class="skill-label-card-hz">Guidewire</span></div>
  </div>

</div>
""", unsafe_allow_html=True)






