import streamlit as st
import requests
import io
import PyPDF2
import openai
import pandas as pd

st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# ---- FULL CSS for sidebar, tabs, cards ----
st.markdown("""
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #fff;
  font-family: 'Poppins', sans-serif;
}
.main-flex {
  display: flex;
  flex-direction: row;
  gap: 38px;
  align-items: flex-start;
}
.sidebar-fixed {
  min-width: 330px;
  max-width: 370px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 26px;
  margin-top: 12px;
}
@media (max-width: 900px) {
  .main-flex { flex-direction: column; }
  .sidebar-fixed { max-width: none; width: 100%; }
}
.tabs-wrap {
  width: 100%;
  margin: 0 auto 32px auto;
  display: flex;
  justify-content: center;
  z-index: 10;
}
.tab-link {
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  color: #ffd166;
  font-weight: bold;
  font-size: 1.14rem;
  padding: 15px 36px 11px 36px;
  margin: 0 5px;
  border: none;
  border-radius: 17px 17px 0 0;
  box-shadow: 0 2px 8px rgba(44,62,80,0.12);
  transition: transform .24s cubic-bezier(.4,1.6,.6,1), box-shadow .16s, background .17s;
  cursor: pointer;
  outline: none;
  position: relative;
  z-index: 2;
}
.tab-link.selected, .tab-link:focus {
  background: linear-gradient(135deg, #22304A 0%, #ffd166 130%);
  color: #222 !important;
  border-bottom: 5px solid #ffd166 !important;
  transform: scale(1.08) translateY(-4px);
  box-shadow: 0 7px 19px rgba(44,62,80,0.16);
}
.tab-link:hover {
  background: linear-gradient(135deg, #406496 0%, #22304A 100%);
  color: #fff !important;
}
.card { border-radius: 12px; padding: 22px; margin-bottom: 17px; background: linear-gradient(135deg, #1F2A44 0%, #324665 100%); }
.profile-pic-popout { width: 150px; height: 150px; object-fit: cover; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 2px 9px rgba(44, 62, 80, 0.14); margin: 0 auto 14px auto; display: block;}
.section-title { font-size: 1.3rem; font-weight: bold; margin-bottom: 9px; padding: 8px; border-radius: 7px;}
.contact-icon { width: 30px; height: 30px; filter: invert(100%); color:#ADD8E6; margin: 0 7px; vertical-align: middle;}
/* Add grid and chip CSS for your content */
.edu-cards-grid, .cert-grid, .awards-grid { display: flex; flex-wrap: wrap; gap: 16px; }
.edu-card, .cert-card, .award-card {
  background: linear-gradient(135deg, #34495E 0%, #406496 100%);
  border-radius: 12px;
  padding: 16px;
  min-width: 175px;
  flex: 1 1 200px;
  box-shadow: 0 2px 10px rgba(30,50,80,0.09);
  margin-bottom: 0;
}
.edu-card-logo { width: 56px; height: 56px; object-fit: contain; border-radius: 8px; background: #fff; margin-bottom: 10px; }
.edu-card-degree, .cert-title, .award-title { font-weight: bold; color: #ffd166; margin-bottom: 3px; }
.edu-card-univ, .cert-provider, .award-sub { color: #ADD8E6; font-size: 1.01rem; }
.edu-card-date, .cert-year, .award-year { color: #fff; font-size: 0.99rem; opacity: 0.85;}
.welcome-card { border-radius: 16px; padding: 3rem; color: white; min-height: 180px; display: flex; align-items: center; justify-content: center; text-align: center; margin-bottom:24px;}
.welcome-card2 { border-radius: 16px; padding: 0; color: white; height: 200px; position: relative; overflow: hidden; margin-bottom: 32px;}
</style>
""", unsafe_allow_html=True)

# ---- Tabs, now with Chat ----
tabs = ["Home", "Chat", "Projects", "Experience", "Skills", "Contact"]
if "tab" not in st.session_state:
    st.session_state.tab = "Home"

with st.form("tab_form", clear_on_submit=True):
    tab_html = '<div class="tabs-wrap">'
    for t in tabs:
        selected = "selected" if st.session_state.tab == t else ""
        tab_html += (
            f'<button class="tab-link {selected}" type="submit" name="tab_choice" value="{t}">{t}</button>'
        )
    tab_html += '</div>'
    st.markdown(tab_html, unsafe_allow_html=True)
    submitted = st.form_submit_button("", help="tab switcher")
    if submitted and st.session_state.get("tab_choice"):
        st.session_state.tab = st.session_state.tab_choice

# ---- Data functions (as before) ----
def load_resume_df(url):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    records = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        for sent in sentences:
            records.append({"page": i+1, "sentence": sent})
    return pd.DataFrame(records)

resume_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkateshwaran_Resume.pdf"
resume_df = load_resume_df(resume_url)
resume_json = resume_df.to_json(orient='records')

projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    # ...Add all your other projects here...
]

# ---- Main flex layout ----
st.markdown('<div class="main-flex">', unsafe_allow_html=True)

# ---- Sidebar left ----
st.markdown('<div class="sidebar-fixed">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="card profile-card-content hover-zoom">
        <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"
             class="profile-pic-popout" />
        <h2 style="margin-bottom:0;">Venkatesh Soundararajan</h2>
        <div style="color:#ADD8E6;"><strong>Software Development Intern</strong><br>Data Engineering</div>
        <div style="color:#ffd166; margin-top:5px;"><strong>🍁 Calgary, AB, Canada</strong></div>
    </div>
    <div class="card hover-zoom">
      <div class="section-title" style="background:#22304A;">About Me</div>
      <div style="font-size:1.02rem; text-align:left;">
        I’m Venkatesh, a Data Scientist and Software Developer with 8+ years in quality engineering, business intelligence, and analytics. I specialize in building scalable ETL pipelines, predictive models, and dashboards using AWS/Azure. I’m passionate about solving business problems with data-driven solutions.
      </div>
    </div>
    <div class="card hover-zoom">
        <div class="section-title" style="background:#34495E;">Contact</div>
        <div style="display:flex; justify-content:center; gap:16px; margin-top:7px;">
            <a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>
            <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>
            <a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>
            <a href="https://medium.com/@venkatesh.balusoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg" class="contact-icon"/></a>
        </div>
        <div style="color:#fff;font-size:1.05rem;margin-top:11px;text-align:center;">
            Calgary, AB, Canada<br>
            <span style="color:#ffd166;">venkatesh.balusoundar@gmail.com</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # End sidebar

# ---- Main content right (tab changes this) ----
st.markdown('<div style="flex:1;min-width:0;">', unsafe_allow_html=True)

def show_home():
    gif_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif"
    st.markdown(
        f"""
        <div class="welcome-card" style="background: url('{gif_url}') center/cover no-repeat;">
            <h1>Hello and Welcome...</h1>
            <p>Explore my portfolio to learn more about my work in data science, analytics, and technology. Let’s connect and create something impactful together.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card hover-zoom">
          <div class="section-title" style="background:#34495E;">Education</div>
          <div class="edu-cards-grid">
            <div class="edu-card">
              <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Uoc.png" class="edu-card-logo"/>
              <div class="edu-card-degree">Masters in Data Science and Analytics</div>
              <div class="edu-card-univ">University of Calgary, Alberta, Canada</div>
              <div class="edu-card-date">September 2024 – Present</div>
            </div>
            <div class="edu-card">
              <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/AnnaUniversity.png" class="edu-card-logo"/>
              <div class="edu-card-degree">Bachelor of Engineering</div>
              <div class="edu-card-univ">Anna University, Chennai, India</div>
              <div class="edu-card-date">August 2009 – May 2013</div>
            </div>
          </div>
        </div>
        <div class="card hover-zoom">
          <div class="section-title" style="background:#34495E;">Certifications & Courses</div>
          <div class="cert-grid">
            <div class="cert-card">
              <div class="cert-title">Guidewire Insurance Suite Analyst 10.0</div>
              <div class="cert-provider">Jasper – Guidewire Education</div>
              <div class="cert-year">2024</div>
            </div>
            <div class="cert-card">
              <div class="cert-title">Karate DSL</div>
              <div class="cert-provider">Udemy</div>
              <div class="cert-year">2023</div>
            </div>
            <div class="cert-card">
              <div class="cert-title">Rest API Automation</div>
              <div class="cert-provider">TestLeaf Software Solutions Pvt. Ltd.</div>
              <div class="cert-year">2023</div>
            </div>
            <div class="cert-card">
              <div class="cert-title">Selenium WebDriver</div>
              <div class="cert-provider">TestLeaf Software Solutions Pvt. Ltd.</div>
              <div class="cert-year">2022</div>
            </div>
            <div class="cert-card">
              <div class="cert-title">SQL for Data Science</div>
              <div class="cert-provider">Coursera</div>
              <div class="cert-year">2020</div>
            </div>
            <div class="cert-card">
              <div class="cert-title">SDET</div>
              <div class="cert-provider">Capgemini</div>
              <div class="cert-year">2020</div>
            </div>
          </div>
        </div>
        <div class="card hover-zoom">
          <div class="section-title" style="background:#34495E;">Awards & Recognitions</div>
          <div class="awards-grid">
            <div class="award-card">
              <div class="award-title">Spot Award</div>
              <div class="award-year">2022 & 2023</div>
              <div class="award-sub">InsurCloud – Deloitte, Canada</div>
            </div>
            <div class="award-card">
              <div class="award-title">Best Contributor</div>
              <div class="award-year">2018</div>
              <div class="award-sub">COMPASS Program – Hartford Insurance, USA</div>
            </div>
            <div class="award-card">
              <div class="award-title">QE & A Maestro</div>
              <div class="award-year">2017</div>
              <div class="award-sub">Centene by Cognizant QE&A, USA</div>
            </div>
            <div class="award-card">
              <div class="award-title">Pride of the Quarter</div>
              <div class="award-year">Q1 2017</div>
              <div class="award-sub">Health Net by Cognizant QE&A, USA</div>
            </div>
            <div class="award-card">
              <div class="award-title">Pillar of the Month</div>
              <div class="award-year">May 2014 & Aug 2015</div>
              <div class="award-sub">Health Net by Cognizant QE&A, USA</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

def show_chat():
    ai_url = "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/DeepSeekAI.gif"
    st.markdown(
        f"""
        <div class="welcome-card2" style="background:url('{ai_url}') center/cover no-repeat;">
            <div style="position:absolute;top:70%;right:2rem;transform:translateY(-50%);text-align:right;">
                <h2>Ask Buddy Bot!</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    chat_container = st.container()
    with chat_container:
        user_input = st.chat_input("Ask something about Venkatesh's Professional Projects and Skills...")
        if user_input:
            st.chat_message("user").write(user_input)
            prompt = (
                "You are Venkatesh's professional assistant. Here is his resume data as JSON:\n" + resume_json +
                "\n\nAnswer the question based only on this DataFrame JSON. If you can't, say you don't know.\nQuestion: "
                + user_input
            )
            with st.spinner("Assistant is typing..."):
                response = client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324",
                    messages=[
                        {"role": "system", "content": prompt}
                    ]
                )
                reply = response.choices[0].message.content
            st.chat_message("assistant").write(reply)

def show_projects():
    st.markdown(
        """
        <div class="card hover-zoom">
            <div class="section-title" style="background:#2C3E50;">Projects Gallery</div>
            <div style="display:flex;flex-wrap:wrap;gap:20px;">
        """, unsafe_allow_html=True)
    for proj in projects:
        st.markdown(
            f"""
            <div style="flex:1 1 210px;max-width:270px;" class="project-item hover-zoom">
                <a href="{proj["url"]}" target="_blank">
                    <img src="{proj["image"]}" style="width:100%;height:170px;object-fit:cover;border-radius:11px;">
                    <div style="font-weight:bold;color:#ffd166;text-align:center;padding-top:10px;">{proj["title"]}</div>
                </a>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_experience():
    st.markdown(
        """
        <div class="card hover-zoom">
          <div class="section-title" style="background:#34495E;">Professional Experience</div>
          <div class="edu-cards-grid">
            <div class="edu-card">
              <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/TI.png" class="edu-card-logo"/>
              <div class="edu-card-degree">Software Developer Intern</div>
              <div class="edu-card-univ">Tech Insights Inc, Canada</div>
              <div class="edu-card-date">May 2025 – Present</div>
            </div>
            <div class="edu-card">
              <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Deloitte.png" class="edu-card-logo"/>
              <div class="edu-card-degree">Senior Consultant</div>
              <div class="edu-card-univ">Deloitte Consulting India Private Limited</div>
              <div class="edu-card-date">Oct 2021 – Aug 2024</div>
            </div>
            <div class="edu-card">
              <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Capgemini.png" class="edu-card-logo"/>
              <div class="edu-card-degree">Consultant</div>
              <div class="edu-card-univ">Capgemini Technology Services India Private Limited</div>
              <div class="edu-card-date">May 2018 – Oct 2021</div>
            </div>
            <div class="edu-card">
              <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Cognizant.png" class="edu-card-logo"/>
              <div class="edu-card-degree">Associate</div>
              <div class="edu-card-univ">Cognizant Technology Solutions India Private Limited</div>
              <div class="edu-card-date">Sep 2013 – May 2018</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

def show_skills():
    st.markdown(
        '''
        <div class="card hover-zoom">
          <div class="section-title" style="background:#34495E;">Core Skills & Tools</div>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Programming Languages</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">Python</div>
              <div class="cert-card">R</div>
              <div class="cert-card">SQL</div>
              <div class="cert-card">Java</div>
              <div class="cert-card">VBA Macro</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Data Analysis Tools</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">Pandas</div>
              <div class="cert-card">NumPy</div>
              <div class="cert-card">Matplotlib</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Data Visualization</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">Power BI</div>
              <div class="cert-card">Excel</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Statistical Analysis</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">Hypothesis Tests</div>
              <div class="cert-card">Regression</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Database Management</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">MySQL</div>
              <div class="cert-card">Oracle</div>
              <div class="cert-card">NoSQL</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Version Control</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">Git</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Project Management Tools</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">JIRA</div>
              <div class="cert-card">ALM</div>
              <div class="cert-card">Rally</div>
            </div>
          </details>
          <details open>
            <summary style="font-weight:bold; cursor:pointer;">Automation & Insurance Suite</summary>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="cert-card">Selenium WebDriver</div>
              <div class="cert-card">Guidewire</div>
            </div>
          </details>
        </div>
        ''', unsafe_allow_html=True)

def show_contact():
    st.markdown(
        """
        <div class="card hover-zoom">
          <div class="section-title" style="background:#34495E;">Get in Touch</div>
          <div style="font-size:1.1rem;">
            Email: <a href="mailto:venkatesh.balusoundar@gmail.com" style="color:#ffd166;">venkatesh.balusoundar@gmail.com</a><br>
            LinkedIn: <a href="https://www.linkedin.com/in/venkateshbalus/" style="color:#ffd166;" target="_blank">venkateshbalus</a><br>
            GitHub: <a href="https://github.com/venkateshsoundar" style="color:#ffd166;" target="_blank">venkateshsoundar</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

section_map = {
    "Home": show_home,
    "Chat": show_chat,
    "Projects": show_projects,
    "Experience": show_experience,
    "Skills": show_skills,
    "Contact": show_contact
}
section_map.get(st.session_state.tab, show_home)()

st.markdown('</div>', unsafe_allow_html=True)  # End main content
st.markdown('</div>', unsafe_allow_html=True)  # End .main-flex
