import streamlit as st
from openai import OpenAI
from time import sleep

# --- CSS Layout for 3-column full-width fixed layout ---
st.markdown("""
<style>
body {
    margin: 0;
    padding: 0;
}
.layout {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}
.left, .middle, .right {
    height: 100vh;
    overflow-y: auto;
    padding: 10px;
}
.left {
    flex: 0.3;
    background-color: #f7f7f7;
    border-right: 1px solid #ddd;
}
.middle {
    flex: 0.4;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #ddd;
    border-right: 1px solid #ddd;
}
.right {
    flex: 0.3;
    background-color: #f7f7f7;
}
.chat-box {
    flex-grow: 1;
    overflow-y: auto;
    padding-bottom: 60px;
}
.chat-msg {
    background-color: #e1e1e1;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 8px;
    max-width: 90%;
}
.user { align-self: flex-end; background: #cce4ff; }
.assistant { align-self: flex-start; background: #f0f0f0; }
.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 600px;
}
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 10px;
}
.project-card {
    background: #fff;
    border-radius: 8px;
    padding: 8px;
    text-align: center;
    box-shadow: 0 0 5px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}
.project-card:hover {
    transform: scale(1.05);
}
.project-card img {
    width: 100%;
    height: 100px;
    object-fit: cover;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# Typewriter intro
def typewriter(text, delay=25):
    placeholder = st.empty()
    full = ""
    for c in text:
        full += c
        placeholder.markdown(f"<h5 style='text-align:center;'>{full}</h5>", unsafe_allow_html=True)
        sleep(delay / 1000.0)

# Profile
profile = {
    "name": "Venkateshwaran Balu Soundararajan",
    "bio": "A data-driven professional with 8+ years in analytics, QA, and data science.",
    "skills": ["Python", "SQL", "Power BI", "AWS", "Streamlit", "Machine Learning"],
    "achievements": [
        "Led QA at Deloitte for agile insurance projects",
        "Built full ML pipeline with AWS and Streamlit dashboard",
        "Published interactive data story on wildfire trends"
    ],
    "linkedin": "https://linkedin.com/in/venkateshbalus",
    "github": "https://github.com/venkateshsoundar",
    "resume": "https://github.com/venkateshsoundar/venkatesh-portfolio-chatbot/blob/main/assets/Venkateshwaran_Resume.pdf"
}

projects = [
    {"title": "Canadian QOL", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
]

# Layout structure
st.markdown("<div class='layout'>", unsafe_allow_html=True)

# LEFT PANEL
st.markdown("<div class='left'>", unsafe_allow_html=True)
st.subheader("👤 About Me")
st.markdown(f"**{profile['name']}**")
st.markdown(profile["bio"])
st.markdown("### Skills")
st.markdown(", ".join(profile["skills"]))
st.markdown("### Achievements")
for a in profile["achievements"]:
    st.markdown(f"- {a}")
st.markdown(f"[📄 Resume]({profile['resume']})<br>[🔗 LinkedIn]({profile['linkedin']}) | [GitHub]({profile['github']})", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# MIDDLE CHAT PANEL
st.markdown("<div class='middle'>", unsafe_allow_html=True)
st.subheader("🤖 Chatbot")
typewriter("Hi, this is Venkatesh. Welcome to my Portfolio! Ask anything about my skills or projects.")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
for role, msg in st.session_state.history:
    role_class = "user" if role == "user" else "assistant"
    st.markdown(f"<div class='chat-msg {role_class}'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input("Type your question here...")
if user_input:
    st.session_state.history.append(("user", user_input))
context = f"""Name: {profile['name']}
Bio: {profile['bio']}
Skills: {', '.join(profile['skills'])}
Projects:
""" + "\n".join([f"- {p['title']}: {p['url']}" for p in projects]) + f"""
Achievements: {', '.join(profile['achievements'])}
"""
    prompt = f"{context}
Q: {user_input}
A:"

    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["DEEPSEEK_API_KEY"])
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.session_state.history.append(("assistant", reply))
    st.experimental_rerun()
st.markdown("</div>", unsafe_allow_html=True)

# RIGHT PROJECTS PANEL
st.markdown("<div class='right'>", unsafe_allow_html=True)
st.subheader("📊 Projects")
st.markdown("<div class='project-grid'>", unsafe_allow_html=True)
for proj in projects:
    st.markdown(f"""
    <div class='project-card'>
        <a href="{proj['url']}" target="_blank">
            <img src="{proj['image']}" />
            <div><strong>{proj['title']}</strong></div>
        </a>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
