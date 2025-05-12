import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2
from time import sleep

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
st.markdown("## Welcome to my Portfolio<span class='blink-dots'>...</span>", unsafe_allow_html=True)

# Load resume from GitHub raw
@st.cache_data
def load_resume_text(url):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = ""
    for p in reader.pages:
        text += p.extract_text() + "\n"
    return text

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_text = load_resume_text(resume_url)

# Fetch GitHub repos
@st.cache_data
def fetch_github_repos(user):
    r = requests.get(f"https://api.github.com/users/{user}/repos")
    return r.json() if r.status_code == 200 else []

repos_data = fetch_github_repos("venkateshsoundar")
repos = [r["name"] for r in repos_data]

# Define projects
projects = [
    "canadian-qol-analysis",
    "alberta-wildfire-analysis",
    "toronto-crime-drivers",
    "weight-change-regression-analysis",
    "calgary-childcare-compliance",
    "social-media-purchase-influence",
    "obesity-level-estimation",
    "weather-data-pipeline-aws",
    "california-wildfire-datastory",
    "penguin-dataset-chatbot",
    "uber-ride-duration-predictorapp"
]

# Fetch READMEs
@st.cache_data
def fetch_readme(user, repo):
    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/README.md"
    r = requests.get(url)
    return r.text if r.status_code == 200 else ""

readmes = {repo: fetch_readme("venkateshsoundar", repo) for repo in projects}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

# Chat input
user_input = st.chat_input("Ask me anything about my background or projects...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # Build context messages
    messages = [
        {"role": "system", "content": "You are Venkatesh's portfolio assistant. Answer concisely and cite sources: [Resume], [Repos], [Projects]."},
        {"role": "system", "content": "Resume extract: " + resume_text[:1500]}
    ]

    # Add repos list
    messages.append({"role": "system", "content": "GitHub Repositories: " + ", ".join(repos)})

    # Add project READMEs
    for repo in projects:
        readme_text = readmes.get(repo, "")
        summary = readme_text[:1000]  # include first 1000 chars
        messages.append({"role": "system", "content": f"Readme of {repo}:\n" + summary})

    # User question
    messages.append({"role": "user", "content": user_input})

    # Call API
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets.get("DEEPSEEK_API_KEY"))
    resp = client.chat.completions.create(model="deepseek/deepseek-r1:free", messages=messages)
    reply = resp.choices[0].message.content

    st.session_state.messages.append(("assistant", reply))
    st.chat_message("assistant").write(reply)
