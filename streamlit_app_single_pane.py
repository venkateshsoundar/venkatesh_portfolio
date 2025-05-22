
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

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
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
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg"}
]

# --- Global CSS styles ---
st.markdown(r"""
<style>
.section { margin-bottom: 3rem; }
.project-item { position: relative; border-radius: 12px; overflow: hidden; }
.card-img { width: 100%; height: auto; transition: transform .3s ease; }
.project-item:hover .card-img { transform: scale(1.05); }
.overlay {
  position: absolute; inset: 0; background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 1.2rem; opacity: 0;
  transition: opacity .3s ease; text-align: center;
}
.project-item:hover .overlay { opacity: 1; }
</style>
""", unsafe_allow_html=True)

# --- Welcome section ---
st.markdown(r"""
<div class="section">
  <h1 style='text-align:center;'>Hello and Welcome...</h1>
  <p style='text-align:center;'>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
</div>
""", unsafe_allow_html=True)

# --- Profile info ---
st.image("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg", width=180)
st.markdown("**Venkatesh Soundararajan**")
st.markdown("Software Development Intern | Data Engineering")
st.markdown("📍 Calgary, AB, Canada")

# --- Chatbot section ---
st.markdown("### Ask Buddy Bot!")
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
user_input = st.chat_input("Ask something about Venkatesh's Professional Projects and Skills...")
if user_input:
    st.chat_message("user").write(user_input)
    prompt = (
        "You are Venkatesh's professional assistant. Here is his resume data as JSON:\n" + resume_json +
        "\n\nAnswer the question based only on this DataFrame JSON. If you can't, say you don't know.\nQuestion: " + user_input
    )
    with st.spinner("Assistant is typing..."):
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[{"role": "system", "content": prompt}]
        )
        reply = response.choices[0].message.content
    st.chat_message("assistant").write(reply)

# --- Projects Gallery ---
st.markdown("## Projects Gallery")
grid_html = '<div class="grid-container" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px;">'
for proj in projects:
    grid_html += (
        f'<div class="project-item">'
        f'  <a href="{proj["url"]}" target="_blank">'
        f'    <img src="{proj["image"]}" class="card-img"/>'
        f'    <div class="overlay">{proj["title"]}</div>'
        f'  </a>'
        f'</div>'
    )
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)
