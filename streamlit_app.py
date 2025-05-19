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

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
)
resume_df = load_resume_df(resume_url)
# Serialize DataFrame to JSON for direct prompt
resume_json = resume_df.to_json(orient='records')

# --- Projects list ---
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
.profile-pic-popout {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 75%;
  border: 4px solid #fff;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.18);
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: -90px;
  z-index: 10;
}
.profile-pic-blend {
  width: 100%;
  height: 140px; /* Or any preferred height */
  object-fit: cover;
  border-radius: 12px 12px 0 0; /* Rounded top corners only */
  display: block;
  position: static;
  margin: 0;
  box-shadow: none;
  border: none;
}
.profile-card-container {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}
.profile-card-content {
  padding-top: 120px;
}
.contact-icon {
  width: 30px;
  height: 30px;
  filter: invert(100%);
  margin: 0 8px;
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
  height: 100%;
  object-fit: cover;
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

/* --- Make chat_input box dark and bold --- */
[data-testid="stChatInput"] input,
.stChatInput input,
input[data-baseweb="input"] {
  background: #26334d !important;        /* deep blue-gray */
  color: #222 !important;                /* white text */
  border: 2px solid #5A84B4 !important;  /* blue border */
  border-radius: 12px !important;
  font-size: 1.08rem !important;
  box-shadow: 0 2px 10px rgba(30,50,100,0.14);
  margin-top: 10px !important;
  margin-bottom: 10px !important;
  transition: box-shadow 0.2s, border 0.2s;
}
[data-testid="stChatInput"] input:focus,
.stChatInput input:focus,
input[data-baseweb="input"]:focus {
  border: 2px solid #ffd166 !important;  /* gold highlight on focus */
  outline: none !important;
  box-shadow: 0 0 0 2px #ffd16666;
}

</style>
    ''', unsafe_allow_html=True
)

# --- Layout ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="large")

# --- Left Pane (profile pic pops out of card) ---
with left_col:
    st.markdown('''
    <div class="profile-card-container">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"
           class="profile-pic-blend" />
      <div class="card profile-card-content hover-zoom">
        <h2>Venkatesh Soundararajan</h2>
        <p><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#34495E;">Contact</div>' +
        '<div style="display:flex; justify-content:center; gap:16px; margin-top:10px;">' +
        '<a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>' +
        '<a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>' +
        '<a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>' +
        '</div></div>',
        unsafe_allow_html=True
    )

# --- Center Pane ---
with mid_col:
    st.markdown(
        '<div class="card hover-zoom"><div class="typewriter"><h1>Hello! Welcome to my Portfolio</h1></div>',
        unsafe_allow_html=True
    )

    # --- AI Chatbot Section ---
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#5A84B4;">Chat with My Bot!</div>'
        '<p style="color:#e0e6ed;margin-top:0;">Ask anything about my professional projects and skills!</p>',
        unsafe_allow_html=True
    )
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Stateless chat - no history
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
                model="deepseek/deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
        st.chat_message("assistant").write(reply)

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
<details >
  <summary class="details-summary">Click here to view the projects</summary>
  {grid_html}
</details>
""",
        unsafe_allow_html=True
    )
    

# --- Right Pane ---
with right_col:
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#1ABC9C;">Skills</div><p style="text-align:center;">Python, SQL, R<br>AWS & SageMaker<br>Streamlit, Tableau<br>Scikit-learn, OpenCV<br>Git, Agile</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#8E44AD;">Experience</div><p style="text-align:center;">Deloitte Quality Lead (8+ yrs)<br>AWS Data Pipelines<br>Agile Team Lead<br>Risk Analytics</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#D35400;">Certifications</div><p style="text-align:center;">AWS Solutions Architect<br>Tableau Specialist<br>Scrum Master</p></div>',
        unsafe_allow_html=True
    )
