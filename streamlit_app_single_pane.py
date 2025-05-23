import streamlit as st
import requests
import io
import PyPDF2
import pandas as pd

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume data ---
def load_resume_df(url):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    records = []
    for i, page in enumerate(reader.pages):
        sentences = [s.strip() for s in (page.extract_text() or "").split('.') if s.strip()]
        for sent in sentences:
            records.append({"page": i+1, "sentence": sent})
    return pd.DataFrame(records)

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_df = load_resume_df(resume_url)

# --- Projects list ---
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/toronto-crime-drivers/main/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/weight-change-regression-analysis/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/calgary-childcare-compliance/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/social-media-purchase-influence/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/obesity-level-estimation/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/weather-data-pipeline-aws/main/weatherprediction.jpeg"},
    {"title": "Gmail Sentimental Analysis", "url": "https://github.com/venkateshsoundar/gmail-sentiment-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/gmail-sentiment-analysis/main/email_sentiment_Analysis.jpeg"},
    {"title": "Penguin Species Prediction Chatbot", "url": "https://github.com/venkateshsoundar/penguin-dataset-chatbot", "image": "https://raw.githubusercontent.com/venkateshsoundar/penguin-dataset-chatbot/main/Penguin_Analysis.jpeg"},
    {"title": "Uber Ride Prediction", "url": "https://github.com/venkateshsoundar/uber-ride-duration-predictorapp", "image": "https://raw.githubusercontent.com/venkateshsoundar/uber-ride-duration-predictorapp/main/Uberride_Prediction.jpeg"}
]

# --- App Main Layout ---
st.title("Venkatesh Portfolio")

# --- Welcome Section ---
st.header("Welcome")
st.write("Explore my portfolio to learn more about my work in data science, analytics, and technology.")

# --- Profile Section ---
st.header("Profile")
st.image("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg", width=160)
st.write("Results-driven data analyst and developer, passionate about analytics, cloud, and automation.")

# --- Contact Section ---
st.header("Contact")
st.markdown("""
- Email: [venkatesh.balusoundar@gmail.com](mailto:venkatesh.balusoundar@gmail.com)
- [LinkedIn](https://linkedin.com/in/venkateshbalusoundar)
- [GitHub](https://github.com/venkateshsoundar)
- [Medium](https://medium.com/@venkatesh.balusoundar)
""")

# --- Education Section ---
st.header("Education")
st.write("""
- **Masters in Data Science and Analytics**, University of Calgary (Sep 2024–Present)
- **Bachelor of Engineering**, Anna University (Aug 2009–May 2013)
""")

# --- Certifications Section ---
st.header("Certifications & Courses")
st.write("""
- Insurance & Guidewire Suite Analyst 10.0
- Karate DSL, Rest API Automation, Selenium WebDriver
- SQL for Data Science, SDET
""")

# --- Awards Section ---
st.header("Awards & Recognitions")
st.write("""
- Spot Award, Best Contributor, QE & A Maestro
- Pride of the Quarter, Pillar of the Month
""")

# --- Experience Section ---
st.header("Professional Experience")
st.write("""
- **Software Developer Intern** (Tech Insights)
- **Senior Consultant** (Deloitte)
- **Consultant** (Capgemini)
- ...see full résumé for details!
""")

# --- Skills Section ---
st.header("Core Skills & Tools")
st.write("""
Python, R, SQL, Java, Pandas, NumPy, Power BI, Git, JIRA, Selenium, Guidewire
""")

# --- Chat Section (Optional: Uncomment if you have OpenAI API key in your secrets) ---
# st.header("AI Chatbot (Ask about my résumé)")
# import openai
# api_key = st.secrets["DEEPSEEK_API_KEY"]
# client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
# user_input = st.chat_input("Ask something about my experience or projects...")
# if user_input:
#     st.chat_message("user").write(user_input)
#     resume_json = resume_df.to_json(orient="records")
#     prompt = f"You are Venkatesh's assistant. Resume JSON: {resume_json}\nQuestion: {user_input}"
#     with st.spinner('Assistant is typing...'):
#         response = client.chat.completions.create(
#             model='deepseek/deepseek-chat-v3-0324',
#             messages=[{'role':'system','content':prompt}]
#         )
#     st.chat_message("assistant").write(response.choices[0].message.content)

# --- Projects Gallery (Grid) ---
st.header("Projects Gallery")
proj_cols = st.columns(3)
for idx, proj in enumerate(projects):
    with proj_cols[idx % 3]:
        st.image(proj["image"], caption=proj["title"], use_column_width=True)
        st.markdown(f"[GitHub Link]({proj['url']})", unsafe_allow_html=True)

# --- ATS Match Score Section ---
st.header("ATS Job Match Demo")
job_desc = st.text_area("Paste Job Description Here")
if st.button("Check ATS Match"):
    # Simple keyword list for demo, adjust as needed
    required_keywords = [
        "data risk", "control self-assessment", "collibra", "BCBS239",
        "DRA", "data quality", "regulatory reporting", "metadata", "lineage"
    ]
    resume_text = " ".join(resume_df['sentence'])
    score = sum(1 for kw in required_keywords if kw.lower() in resume_text.lower())
    st.success(f"ATS Match Score: {score}/{len(required_keywords)} ({int(100*score/len(required_keywords))}%)")

# --- Download Resume Section ---
st.header("Download My Resume")
resume_file_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
st.markdown(f"[Download Resume (PDF)]({resume_file_url})")

# End of app
