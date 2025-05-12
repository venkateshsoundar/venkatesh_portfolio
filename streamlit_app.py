import streamlit as st
from openai import OpenAI
import os
from streamlit_extras.stylable_container import stylable_container

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
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/canadian_qol.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/alberta_wildfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/toronto_crime.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/weight_change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/calgary_childcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/social_media_influence.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/obesity_estimation.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/weather_pipeline.jpeg"},
    {"title": "California Wildfire Data Story", "url": "https://github.com/venkateshsoundar/california-wildfire-datastory", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/california_wildfire.jpeg"},
    {"title": "Penguin Dataset Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/penguin_chatbot.jpeg"},
    {"title": "Uber Ride Duration Predictor", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/images/uber_duration.jpeg"}
]

# --- Set up OpenRouter API ---
api_key = st.secrets["DEEPSEEK_API_KEY"]
st.set_page_config(layout="wide")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

st.title("🤖 Venkatesh’s Portfolio Chatbot")

# Layout: left (bio), center (chat), right (projects)
col_bio, col_chat, col_proj = st.columns([1.1, 1.3, 1.6])

# --- Bio Section ---
with col_bio:
    st.subheader("👨‍💼 About Me")
    st.markdown(f"**Name:** {profile['name']}")
    st.markdown(f"**Bio:** {profile['bio']}")
    st.markdown("**Skills:**")
    st.markdown(", ".join(profile['skills']))
    st.markdown("**Achievements:**")
    for ach in profile["achievements"]:
        st.markdown(f"- {ach}")
    st.markdown(f"📄 [Resume]({profile['resume']})")
    st.markdown(f"🔗 [LinkedIn]({profile['linkedin']}) | [GitHub]({profile['github']})")

# --- Chat Section ---
with col_chat:
    st.subheader("💬 Chat with Me")
    if "history" not in st.session_state:
        st.session_state.history = []
    for role, msg in st.session_state.history:
        st.chat_message(role).write(msg)
    user_input = st.chat_input("Ask something like 'What is your experience with AWS?'...")
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
            context += f"- {proj['title']}: {proj['url']}\n"
        context += f"\nAchievements: {', '.join(profile['achievements'])}\n"
        context += f"LinkedIn: {profile['linkedin']} | GitHub: {profile['github']} | Resume: {profile['resume']}\n"

        prompt = f"""{context}\nNow, answer the following user question naturally:\nQ: {user_input}\nA:\n"""

        try:
            completion = client.chat.completions.create(
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

# --- Project Gallery ---
with col_proj:
    st.subheader("📊 Featured Projects")
    for project in projects:
        st.markdown(
            f"""<div style='text-align: center; padding-bottom: 20px'><a href='{project['url']}' target='_blank'><img src='{project['image']}' style='width:100%; height:180px; border-radius:10px; object-fit:cover;'/><br><strong>{project['title']}</strong></a></div>""",
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + OpenRouter")
