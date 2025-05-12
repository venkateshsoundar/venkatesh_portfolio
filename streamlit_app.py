
import streamlit as st
from openai import OpenAI
from time import sleep

st.set_page_config(layout="wide")

# --- Typewriter Effect ---
def typewriter(text, delay=25):
    placeholder = st.empty()
    full = ""
    for c in text:
        full += c
        placeholder.markdown(f"<h5 style='text-align:center;'>{full}</h5>", unsafe_allow_html=True)
        sleep(delay / 1000.0)

# --- Profile & Project Data ---
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

# --- Layout ---
col1, col2, col3 = st.columns([0.3, 0.4, 0.3])

# Left Column - Profile
with col1:
    st.subheader("👤 About Me")
    st.markdown(f"**{profile['name']}**")
    st.markdown(profile["bio"])
    st.markdown("### Skills")
    st.markdown(", ".join(profile["skills"]))
    st.markdown("### Achievements")
    for a in profile["achievements"]:
        st.markdown(f"- {a}")
    st.markdown(f"[📄 Resume]({profile['resume']})<br>[🔗 LinkedIn]({profile['linkedin']}) | [GitHub]({profile['github']})", unsafe_allow_html=True)

# Middle Column - Chat
with col2:
    st.subheader("🤖 Chatbot")
    typewriter("Hi, this is Venkatesh. Welcome to my Portfolio! Ask anything about my skills or projects.")
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    for role, msg in st.session_state.history:
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Bot:** {msg}")
    
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state.history.append(("user", user_input))
        context = f"Name: {profile['name']}
Bio: {profile['bio']}
Skills: {', '.join(profile['skills'])}
Projects:
" +                   "
".join([f"- {p['title']}: {p['url']}" for p in projects]) +                   f"
Achievements: {', '.join(profile['achievements'])}"
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

# Right Column - Projects
with col3:
    st.subheader("📊 Projects")
    for proj in projects:
        st.image(proj["image"], use_column_width=True)
        st.markdown(f"**[{proj['title']}]({proj['url']})**")
