# Full code with animations and responsive layout
import streamlit as st
from openai import OpenAI
import os

# --- CSS for improved layout ---
st.markdown("""
<style>
body {
    margin: 0;
    padding: 0;
}
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    padding: 0;
}
.project-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px;
    background-color: #f4f4f4;
    border-radius: 10px;
    transition: 0.3s;
}
.project-card:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.project-card img {
    width: 100%;
    height: 140px;
    border-radius: 10px;
    object-fit: cover;
}
.columns-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}
.column {
    flex: 1;
    padding: 10px;
}
.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 500px;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 10px;
    background-color: #fafafa;
}
.chat-history {
    flex-grow: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}
</style>
""", unsafe_allow_html=True)

# --- Chatbot Typewriter Effect ---
def typewriter_effect(text, delay=30):
    from time import sleep
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f"`{full_text}`")
        sleep(delay / 1000.0)
    placeholder.markdown(full_text)

# --- Portfolio Content ---
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
    {"title": "Canadian Quality of Life", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
]

# --- Layout ---
st.markdown("<div class='columns-container'>", unsafe_allow_html=True)

# --- Profile ---
st.markdown("<div class='column'>", unsafe_allow_html=True)
st.subheader("👤 Profile")
st.markdown(f"**Name:** {profile['name']}")
st.markdown(profile['bio'])
st.markdown("**Skills:**")
st.markdown(", ".join(profile['skills']))
st.markdown("**Achievements:**")
for ach in profile["achievements"]:
    st.markdown(f"- {ach}")
st.markdown(f"📄 [Resume]({profile['resume']})")
st.markdown(f"🔗 [LinkedIn]({profile['linkedin']}) | [GitHub]({profile['github']})")
st.markdown("</div>", unsafe_allow_html=True)

# --- Chatbot ---
st.markdown("<div class='column'>", unsafe_allow_html=True)
st.subheader("💬 Ask Me Anything")
typewriter_effect("Hi, this is Venkatesh. Welcome to my Portfolio! Feel free to ask anything about me.")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
st.markdown("<div class='chat-history'>", unsafe_allow_html=True)
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)
st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input("Ask about skills, tools, or projects...")
if user_input:
    st.session_state.history.append(("user", user_input))
    st.chat_message("user").write(user_input)

    context = f"""
Name: {profile['name']}
Bio: {profile['bio']}
Skills: {', '.join(profile['skills'])}
Projects:
"""
    for proj in projects:
        context += f"- {proj['title']}: {proj['url']}\n"
    context += f"Achievements: {', '.join(profile['achievements'])}\n"

    prompt = f"{context}\nQ: {user_input}\nA:"

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
    st.chat_message("assistant").write(reply)
st.markdown("</div>", unsafe_allow_html=True)

# --- Projects ---
st.markdown("<div class='column'>", unsafe_allow_html=True)
st.subheader("📊 Projects")
st.markdown("<div class='project-grid'>", unsafe_allow_html=True)
for proj in projects:
    st.markdown(f"""
        <div class='project-card'>
            <a href='{proj['url']}' target='_blank'>
                <img src='{proj['image']}' alt='{proj['title']}'/>
                <div style='font-weight:bold'>{proj['title']}</div>
            </a>
        </div>
    """, unsafe_allow_html=True)
st.markdown("</div></div></div>", unsafe_allow_html=True)
