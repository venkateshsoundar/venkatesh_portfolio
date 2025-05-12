<!-- Full code with animations and responsive layout -->
import streamlit as st
from openai import OpenAI
import os

# --- CSS for animations and responsiveness ---
st.markdown("""
<style>
.scroll-section {
    max-height: 550px;
    overflow-y: auto;
}
a:hover img {
    transform: scale(1.03);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: transform 0.3s ease-in-out;
}
@media screen and (max-width: 900px) {
    .element-container {
        flex-direction: column !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Dark Mode Toggle ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode")
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp { background-color: #121212; color: white; }
        .block-container { color: white; }
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
    {"title": "Canadian Quality of Life", "url": "https://github.com/...", "image": "https://github.com/.../QualityofLife.jpeg"},
    {"title": "Wildfire Analysis", "url": "https://github.com/...", "image": "https://github.com/.../Alberta_forestfire.jpeg"},
    {"title": "Crime Drivers", "url": "https://github.com/...", "image": "https://github.com/.../Toronto_Crimes.jpeg"},
]

# --- Layout ---
col1, col2, col3 = st.columns([1, 1.2, 1.5])

# --- Profile ---
with col1:
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

# --- Chatbot ---
with col2:
    st.subheader("💬 Ask Me Anything")
    if "history" not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        st.chat_message(role).write(msg)

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

# --- Projects ---
with col3:
    st.subheader("📊 Projects")
    for i, proj in enumerate(projects):
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 10px;'>
                <a href='{proj['url']}' target='_blank'>
                    <img src='{proj['image']}' style='width:100%; height:150px; border-radius:10px;'>
                    <div style='padding-top:5px; font-weight:bold;'>{proj['title']}</div>
                </a>
            </div>
        """, unsafe_allow_html=True)
