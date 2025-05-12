import streamlit as st
from openai import OpenAI
import os
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

# Enable dark mode toggle
st.markdown("""
    <style>
    body {
        transition: background-color 0.5s ease;
    }
    </style>
""", unsafe_allow_html=True)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode")

if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #121212;
                color: white;
            }
            .block-container {
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Animate Chatbot Responses ---
def typewriter_effect(text, delay=30):
    from time import sleep
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f"`{full_text}`")
        sleep(delay / 1000.0)
    placeholder.markdown(full_text)

# The rest of the code remains as in the canvas document
# All previous imports, profile, projects, layout, and rendering logic will stay the same

# --- Sectional Navigation ---
section = st.sidebar.radio("🔍 Navigate", ["👤 Profile", "💬 Chatbot", "📊 Projects"])

# --- Profile Context ---
profile = {
    "name": "Venkateshwaran Balu Soundararajan",
    "bio": "A data-driven professional with 8+ years in analytics, QA, and data science. Passionate about transforming data into insights and impact.",
    "skills": ["Python", "SQL", "Power BI", "AWS", "Streamlit", "Machine Learning", "Guidewire", "ETL", "Git"],
    "achievements": [
        "Led QA at Deloitte for agile insurance projects",
        "Built full ML pipeline with AWS and Streamlit dashboard",
        "Published interactive data story on wildfire trends"
    ],
    "linkedin": "https://linkedin.com/in/venkateshbalus",
    "github": "https://github.com/venkateshsoundar",
    "resume": "https://github.com/venkateshsoundar/venkatesh-portfolio-chatbot/blob/main/assets/Venkateshwaran_Resume.pdf"
}

# --- Project Showcase ---
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/weatherprediction.jpeg"},
    {"title": "California Wildfire Data Story", "url": "https://github.com/venkateshsoundar/california-wildfire-datastory", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/Alberta_forestfire.jpeg"},
    {"title": "Penguin Dataset Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/penguin_chatbot.jpeg"},
    {"title": "Uber Ride Duration Predictor", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/uber_duration.jpeg"}
]

if section == "👤 Profile":
    st.header("👤 Profile")
    st.markdown(f"**Name:** {profile['name']}")
    st.markdown(f"**Bio:** {profile['bio']}")
    st.markdown("**Skills:**")
    st.markdown(", ".join(profile['skills']))
    st.markdown("**Achievements:**")
    for ach in profile["achievements"]:
        st.markdown(f"- {ach}")
    st.markdown(f"📄 [Resume]({profile['resume']})")
    st.markdown(f"🔗 [LinkedIn]({profile['linkedin']}) | [GitHub]({profile['github']})")

elif section == "💬 Chatbot":
    st.header("💬 Ask Me Anything")
    if "history" not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        st.chat_message(role).write(msg)
    user_input = st.chat_input("Ask about skills, tools, projects, or work experience...")
    if user_input:
        st.session_state.history.append(("user", user_input))
        st.chat_message("user").write(user_input)

        context = f"""
You are a helpful AI assistant chatbot trained on Venkateshwaran Balu Soundararajan's portfolio.
Here is the context:
Name: {profile['name']}
Bio: {profile['bio']}
Skills: {', '.join(profile['skills'])}
Projects:
"""
        for proj in projects:
            context += f"- {proj['title']}: {proj['url']}
"
        context += f"Achievements: {', '.join(profile['achievements'])}
"
        context += f"LinkedIn: {profile['linkedin']} | GitHub: {profile['github']} | Resume: {profile['resume']}
"

        prompt = f"""{context}
Now, answer the following user question naturally:
Q: {user_input}
A:
"""

        try:
            completion = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=st.secrets["DEEPSEEK_API_KEY"]
            ).chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "https://venkateshbs.streamlit.app",
                    "X-Title": "venkatesh-portfolio-chatbot"
                }
            )
            reply = completion.choices[0].message.content
        except Exception as e:
            reply = f"❌ Error: {e}"

        st.session_state.history.append(("assistant", reply))
        st.chat_message("assistant").write(reply)

elif section == "📊 Projects":
    st.header("📊 Project Showcase")
    rows = (len(projects) + 2) // 3
    for row in range(rows):
        cols = st.columns(3)
        for col, proj_idx in zip(cols, range(row*3, min((row+1)*3, len(projects)))):
            project = projects[proj_idx]
            col.markdown(
                f"""
                <div style='text-align:center; transition: transform 0.2s ease-in-out;'>
                    <a href='{project['url']}' target='_blank' style='text-decoration:none;'>
                        <img src='{project['image']}' style='width:100%; height:150px; border-radius:10px; object-fit:cover; transition: transform 0.3s;'>
                        <div style='padding-top:5px; font-weight:bold;'>{project['title']}</div>
                    </a>
                </div>
                <style>
                    a:hover img {{ transform: scale(1.03); box-shadow: 0 4px 20px rgba(0,0,0,0.2); }}
                </style>
                """,
                unsafe_allow_html=True
            )

# NOTE: Since the remaining app is already long and unchanged, no need to duplicate it here.
# Just remember that only the dark mode toggle and styles are appended to your current script.
