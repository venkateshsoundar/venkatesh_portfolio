import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2

# Page config
st.set_page_config(page_title="Portfolio Chatbot", layout="centered")

# CSS for blinking dots
st.markdown("""
<style>
@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}
.blink-dots {
  display: inline-block;
  animation: blink 1s step-start infinite;
}
</style>
""", unsafe_allow_html=True)

# Blinking heading
st.markdown("## This is Venky.Welcome to my Portfolio<span class='blink-dots'>...</span>", unsafe_allow_html=True)

# Project list
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws"},
    {"title": "California Wildfire Data Story", "url": "https://github.com/venkateshsoundar/california-wildfire-datastory"},
    {"title": "Penguin Dataset Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot"},
    {"title": "Uber Ride Duration Predictor", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp"}
]

# Load resume from GitHub raw
@st.cache_data
def load_resume_text(url):
    resp = requests.get(url)
    resp.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(resp.content))
    text = ""
    for p in reader.pages:
        text += p.extract_text() + "\n"
    return text

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_text = load_resume_text(resume_url)

# Fetch GitHub repos
@st.cache_data
def fetch_github_repos(username):
    r = requests.get(f"https://api.github.com/users/{username}/repos")
    if r.status_code == 200:
        return [f"{repo['name']}: {repo['html_url']}" for repo in r.json()]
    return []

github_repos = fetch_github_repos("venkateshsoundar")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

# Chat input
user_input = st.chat_input("Ask me anything about my background or projects...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # Build context
    context = "Resume Text:\n" + resume_text[:2000] + "\n\n"
    context += "GitHub Repos:\n" + "\n".join(github_repos) + "\n\n"
    context += "Projects:\n" + "\n".join([f"- {p['title']}: {p['url']}" for p in projects]) + "\n\n"

    prompt = context + f"User: {user_input}\nAssistant:"

    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets.get("DEEPSEEK_API_KEY"))
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.session_state.messages.append(("assistant", reply))
    st.chat_message("assistant").write(reply)
