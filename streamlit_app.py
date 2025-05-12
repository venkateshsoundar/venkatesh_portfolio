import streamlit as st
from openai import OpenAI

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
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://tse3.mm.bing.net/th?id=OIP.1VVIyku0-dGjfj4INdUxUwHaEy&pid=Api"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://tse1.mm.bing.net/th?id=OIP.jfttUG5hUH1Wb02tEHJvagHaJl&pid=Api"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://www.gettyimages.com/detail/photo/toronto-police-car-royalty-free-image/157482029"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://www.sciencedirect.com/science/article/pii/S2590048X23001644"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://newsroom.calgary.ca/keeping-future-generations-safe-city-of-calgary-introducing-new-home-based-child-care-business-licence-starting-jan-1-2023/"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://helplama.com/how-does-social-media-impact-consumer-purchase-decisions-survey/"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://www.mdpi.com/2075-4418/13/18/2949"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://miro.medium.com/v2/resize:fit:720/format:webp/1*nU4c3zqM1_m4JZniIDtCEg.png"},
    {"title": "California Wildfire Data Story", "url": "https://github.com/venkateshsoundar/california-wildfire-datastory", "image": "https://tse4.mm.bing.net/th/id/OIP.1lCJWVaJ2ZpDrTc4sMmoIQHaGL?pid=Api"},
    {"title": "Penguin Dataset Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://tse4.mm.bing.net/th?id=OIP.KU-V8tWWQU3nDtw12-bQ_gHaEa&pid=Api"},
    {"title": "Uber Ride Duration Predictor", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://i.ytimg.com/vi/6farmuPM0uw/maxresdefault.jpg"}
]

# --- Set up OpenRouter API ---
api_key = st.secrets.get("DEEPSEEK_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

st.set_page_config(page_title="Venkatesh Portfolio Chatbot", page_icon="🤖")
st.title("🤖 Venkatesh’s Portfolio Chatbot")
st.write("Ask me about my projects, skills, or experience!")

# --- Chat History ---
if "history" not in st.session_state:
    st.session_state.history = []

for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

# --- Chat Input ---
user_input = st.chat_input("Ask something like 'What is your experience with AWS?'...")

if user_input:
    st.session_state.history.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # --- Build Prompt ---
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
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.session_state.history.append(("assistant", reply))
    st.chat_message("assistant").write(reply)

# --- Project Gallery ---
st.markdown("---")
st.subheader("📊 Featured Projects")
cols = st.columns(3)
for idx, project in enumerate(projects):
    with cols[idx % 3]:
        st.markdown(
            f"""<div style='text-align: center'><a href='{project['url']}' target='_blank'><img src='{project['image']}' style='width:100%; border-radius:10px;'/><br><strong>{project['title']}</strong></a></div>""",
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + OpenRouter")
