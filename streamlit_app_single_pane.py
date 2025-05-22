import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Sidebar Navigation & Actions ---
st.sidebar.title("Navigation")
st.sidebar.markdown("[Welcome](#welcome)")
st.sidebar.markdown("[Profile](#profile)")
st.sidebar.markdown("[Contact](#contact)")
st.sidebar.markdown("[Education](#education)")
st.sidebar.markdown("[Certifications](#certifications)")
st.sidebar.markdown("[Awards](#awards)")
st.sidebar.markdown("[Experience](#experience)")
st.sidebar.markdown("[Skills & Tools](#skills-tools)")
st.sidebar.markdown("[Chat](#chat)")
st.sidebar.markdown("[Projects](#projects-gallery)")

# Download Resume
resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_pdf = requests.get(resume_url).content
st.sidebar.download_button(
    "Download Resume",
    data=resume_pdf,
    file_name="Venkatesh_Resume.pdf",
    mime="application/pdf"
)

# Deploy Button (placeholder link)
st.sidebar.markdown(
    "[![Deploy to Streamlit]"
    "(https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]"
    "(https://share.streamlit.io/venkateshsoundar/venkatesh_portfolio/streamlit_app_updated.py)"
)

# --- Load resume data ---
def load_resume_df(url):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    records = []
    for i, page in enumerate(reader.pages):
        sentences = [
            s.strip()
            for s in (page.extract_text() or "").split('.')
            if s.strip()
        ]
        for sent in sentences:
            records.append({"page": i + 1, "sentence": sent})
    return pd.DataFrame(records)

resume_df = load_resume_df(resume_url)
resume_json = resume_df.to_json(orient="records")

# --- Projects list ---
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
.card-img { width: 100%; height: 200px; object-fit: cover; transition: transform .3s ease; }
.project-item { position: relative; border-radius: 12px; overflow: hidden; }
.project-item:hover .card-img { transform: scale(1.05); }
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.2rem;
  opacity: 0;
  transition: opacity .3s ease;
  text-align: center;
}
.project-item:hover .overlay { opacity: 1; }
</style>
""", unsafe_allow_html=True)

# --- Sections ---

st.markdown('<h2 id="welcome">Welcome</h2>', unsafe_allow_html=True)
st.write("Explore my portfolio to learn more about my work in data science, analytics, and technology.")

st.markdown('<h2 id="profile">Profile</h2>', unsafe_allow_html=True)
st.image("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg", width=180)
st.write("**Venkatesh Soundararajan**  \nSoftware Development Intern | Data Engineering  \n📍 Calgary, AB, Canada")

st.markdown('<h2 id="contact">Contact</h2>', unsafe_allow_html=True)
st.write(
    "[Email](mailto:venkatesh.balusoundar@gmail.com) | "
    "[LinkedIn](https://www.linkedin.com/in/venkateshbalus/) | "
    "[GitHub](https://github.com/venkateshsoundar) | "
    "[Medium](https://medium.com/@venkatesh.balusoundar)"
)

st.markdown('<h2 id="education">Education</h2>', unsafe_allow_html=True)
st.write("""
- **Masters in Data Science and Analytics**, University of Calgary (Sep 2024–Present)  
- **Bachelor of Engineering**, Anna University, Chennai, India (Aug 2009–May 2013)
""")

st.markdown('<h2 id="certifications">Certifications & Courses</h2>', unsafe_allow_html=True)
st.write("""
- Insurance & Guidewire Suite Analyst 10.0 (Jasper)  
- Karate DSL (Udemy)  
- Rest API Automation (TestLeaf)  
- Selenium WebDriver (TestLeaf)  
- SQL for Data Science (Coursera)  
- SDET (Capgemini)
""")

st.markdown('<h2 id="awards">Awards & Recognitions</h2>', unsafe_allow_html=True)
st.write("""
• Spot Award (InsurCloud – Deloitte, Canada)  
• Best Contributor (COMPASS – Hartford Insurance, USA)  
• QE & A Maestro (Centene by Cognizant, USA)  
• Pride of the Quarter (Health Net by Cognizant, USA)  
• Pillar of the Month (Health Net by Cognizant, USA)
""")

st.markdown('<h2 id="experience">Professional Experience</h2>', unsafe_allow_html=True)
st.write("""
- **Software Developer Intern**, Tech Insights Inc, Canada (May 2025–Present)  
- **Senior Consultant**, Deloitte Consulting India, India (Jun 2024–Aug 2024)  
- **Consultant**, Deloitte Consulting India, India (Oct 2021–Jun 2024)  
- **Consultant**, Capgemini, India (May 2018–Oct 2021)  
- **Associate**, Cognizant, India (May 2016–May 2018)  
- **Programmer Analyst**, Cognizant, India (Sep 2013–May 2016)
""")

st.markdown('<h2 id="skills-tools">Core Skills & Tools</h2>', unsafe_allow_html=True)
st.write("""
**Languages**: Python, R, SQL, Java, VBA  
**Analytics**: Pandas, NumPy, Matplotlib, Power BI, Excel  
**DBs**: MySQL, Oracle, NoSQL  
**Tools**: Git, JIRA, ALM, Rally, Selenium, Guidewire
""")

# --- Ask Buddy Bot Chat Section ---
st.markdown('<h2 id="chat">Chat</h2>', unsafe_allow_html=True)
st.write("Ask any question about my projects or experience:")
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
user_input = st.chat_input("Type your question here...")
if user_input:
    st.chat_message("user").write(user_input)
    prompt = (
        "You are Venkatesh's professional assistant. Here is his resume data as JSON:\n"
        + resume_json
        + "\n\nAnswer the question based only on this DataFrame JSON. If you can't, say you don't know.\nQuestion: "
        + user_input
    )
    with st.spinner("Assistant is typing..."):
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[{"role": "system", "content": prompt}]
        )
        answer = response.choices[0].message.content
    st.chat_message("assistant").write(answer)

st.markdown('<h2 id="projects-gallery">Projects Gallery</h2>', unsafe_allow_html=True)
cols = st.columns(3)
for idx, proj in enumerate(projects):
    with cols[idx % 3]:
        st.markdown(
            f"<div class='project-item'><a href='{proj['url']}' target='_blank'>"
            f"<img src='{proj['image']}' class='card-img'/>"
            f"<div class='overlay'>{proj['title']}</div></a></div>",
            unsafe_allow_html=True
        )
