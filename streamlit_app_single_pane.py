import streamlit as st

# ----- PAGE CONFIG -----
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# ----- ANIMATION & GLOBAL CSS -----
st.markdown("""
<style>
body, .stApp { font-family: 'Poppins', sans-serif; color: #fff; }
.stApp { background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat; background-attachment: fixed; }

/* Fade-in up animation */
.fade-in-card {
  opacity: 0;
  transform: translateY(42px);
  transition: opacity 0.72s cubic-bezier(.45,1.6,.7,1), transform 0.72s cubic-bezier(.4,1.5,.8,1);
}
.fade-in-card.visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
}
</style>
""", unsafe_allow_html=True)

# ----- NAVBAR -----
st.markdown("""
<style>
.navbar {
    display: flex; gap: 28px; justify-content: center; background: #1F2A44;
    padding: 12px 0 10px 0; border-radius: 0 0 18px 18px;
    margin-bottom: 20px; position: sticky; top: 0; z-index: 100;
}
.navbar a {
    color: #ffd166; font-weight: bold; font-size: 1.08rem;
    text-decoration: none; transition: color .18s;
    padding: 7px 22px; border-radius: 8px;
}
.navbar a:hover {
    background: #ffd16633; color: #fff;
}
</style>
<div class="navbar">
    <a href="#about">About</a>
    <a href="#education">Education</a>
    <a href="#experience">Experience</a>
    <a href="#certifications">Certifications</a>
    <a href="#recognitions">Recognitions</a>
    <a href="#projects">Projects Gallery</a>
    <a href="#skills">Skills</a>
</div>
""", unsafe_allow_html=True)

# --------- ABOUT/HERO SECTION ----------
st.markdown('<a name="about"></a>', unsafe_allow_html=True)
st.markdown("""
<style>
.hero-card { display: flex; flex-direction: row; align-items: stretch; gap: 0;
  background: linear-gradient(135deg, #253451 0%, #324665 100%);
  border-radius: 24px; box-shadow: 0 6px 26px rgba(20,30,55,0.18), 0 2px 14px rgba(44,62,80,0.08);
  margin-bottom: 32px; min-height: 330px; position: relative; overflow: hidden; transition: transform .33s cubic-bezier(.37,1.7,.7,1), box-shadow .33s;
}
.hero-card:hover { transform: translateY(-7px) scale(1.016); box-shadow: 0 14px 38px 0 #ffd16630, 0 2px 18px rgba(44,62,80,0.12);}
.hero-left { flex: 1 1 0px; min-width: 260px; max-width: 340px; background: linear-gradient(135deg, #253451 70%, #ffd16610 100%);
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 38px 0 26px 0; box-shadow: 2px 0 18px 0 #ffd16609; z-index: 1;}
.hero-pic-glow { width: 130px; height: 130px; border-radius: 20%; margin-bottom: 17px;
  box-shadow: 0 0 0 4px #ffd16699, 0 0 16px 7px #ffd16644, 0 2px 14px rgba(44,62,80,0.09);
  display: flex; align-items: center; justify-content: center; background: none;}
.hero-pic-glow img { width: 116px; height: 116px; border-radius: 20%; object-fit: cover; border: 3px solid #fff; background: #fff;}
.hero-name { color: #fff; font-size: 2.44rem; font-weight: 800; text-align: center; margin: 6px 0 0 0; line-height: 1.17; letter-spacing: 0.01em;}
.hero-role { color: #ADD8E6; font-size: 1.03rem; margin-top: 3px; margin-bottom: 0px; text-align: center;}
.hero-location { color: #ffd166; font-weight: 600; margin-top: 8px; font-size: 1.01rem; text-align: center;}
.hero-right { flex: 2 1 0px; padding: 38px 38px 16px 38px; display: flex; flex-direction: column; justify-content: flex-start; background: none;}
.hero-about-title { font-size: 1.13rem; color: #ffd166; font-weight: 700; margin-bottom: 12px; letter-spacing: .01em;}
.hero-about-body { font-size: 1.09rem; color: #fff; line-height: 1.7; margin-bottom: 26px;}
.hero-contact-bar { width: 100%; margin-top: 6px; background: rgba(90, 130, 160, 0.12); border-radius: 13px; padding: 12px 0 6px 0; text-align: center; box-shadow: 0 2px 14px rgba(255,209,102,0.04);}
.hero-contact-bar-title { color: #fff; font-weight: 600; font-size: 1.10rem; margin-bottom: 5px; letter-spacing: 0.01em;}
.hero-contact-icons { display: flex; justify-content: center; align-items: center; gap: 24px; margin-top: 7px; margin-bottom: 3px;}
.hero-contact-icons a { display: inline-block; border-radius: 8px; padding: 3px; transition: background 0.15s, transform 0.15s;}
.hero-contact-icons a:hover { background: #ffd16633; transform: translateY(-2px) scale(1.11);}
.hero-contact-icons img { width: 30px; height: 30px; filter: invert(100%);}
@media (max-width: 900px) {.hero-card {flex-direction: column;align-items: center;} .hero-right, .hero-left {max-width:100%;padding:28px 8vw 12px;}}
</style>
<div class="hero-card fade-in-card" id="about">
  <div class="hero-left">
    <div class="hero-pic-glow">
      <img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg"/>
    </div>
    <div class="hero-name">Venkatesh<br>Soundararajan</div>
    <div class="hero-role">Software Development Intern<br>Data Engineering</div>
    <div class="hero-location">🍁 Calgary, AB, Canada</div>
  </div>
  <div class="hero-right">
    <div class="hero-about-title">About Me</div>
    <div class="hero-about-body">
      I’m Venkatesh, a Data Scientist and Software Developer with <b>8+ years of experience</b> in quality engineering, business intelligence, and analytics.<br><br>
      I specialize in building <b>scalable ETL pipelines</b>, predictive models, and interactive dashboards using cloud platforms like <b>AWS and Azure</b>.<br><br>
      I'm currently pursuing my Master's in Data Science and Analytics at the <b>University of Calgary</b>.<br>
      My passion lies in solving complex business problems with clean, actionable insights and AI-powered solutions.
    </div>
    <div class="hero-contact-bar">
      <div class="hero-contact-bar-title">Contact</div>
      <div class="hero-contact-icons">
        <a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg"/></a>
        <a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg"/></a>
        <a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg"/></a>
        <a href="https://medium.com/@venkatesh.balusoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg"/></a>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------- EDUCATION ----------
st.markdown('<a name="education"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom fade-in-card" id="education">
  <div class="section-title" style="background:#34495E;">Education</div>
  <div class="edu-cards-grid">
    <div class="edu-card fade-in-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Uoc.png" class="edu-card-logo"/>
      <div class="edu-card-degree">Masters in Data Science and Analytics</div>
      <div class="edu-card-univ">University of Calgary, Alberta, Canada</div>
      <div class="edu-card-date">September 2024 – Present</div>
    </div>
    <div class="edu-card fade-in-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/AnnaUniversity.png" class="edu-card-logo"/>
      <div class="edu-card-degree">Bachelor of Engineering</div>
      <div class="edu-card-univ">Anna University, Chennai, India</div>
      <div class="edu-card-date">August 2009 – May 2013</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------- EXPERIENCE ----------
st.markdown('<a name="experience"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom fade-in-card" id="experience">
  <div class="section-title" style="background:#34495E;">Professional Experience</div>
  <div class="exp-cards-grid">
    <div class="exp-card fade-in-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/TI.png" class="exp-card-logo"/>
      <div class="exp-card-title">Software Developer Intern</div>
      <div class="exp-card-company">Tech Insights Inc, Canada</div>
      <div class="exp-card-date">May 2025 – Present</div>
    </div>
    <div class="exp-card fade-in-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Deloitte.png" class="exp-card-logo"/>
      <div class="exp-card-title">Senior Consultant</div>
      <div class="exp-card-company">Deloitte Consulting India Private Limited, India</div>
      <div class="exp-card-date">October 2021 – August 2024</div>
    </div>
    <div class="exp-card fade-in-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Capgemini.png" class="exp-card-logo"/>
      <div class="exp-card-title">Consultant</div>
      <div class="exp-card-company">Capgemini Technology Services India Private Limited, India</div>
      <div class="exp-card-date">May 2018 – October 2021</div>
    </div>
    <div class="exp-card fade-in-card">
      <img src="https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Cognizant.png" class="exp-card-logo"/>
      <div class="exp-card-title">Associate</div>
      <div class="exp-card-company">Cognizant Technology Solutions India Private Limited, India</div>
      <div class="exp-card-date">Sep 2013 – May 2018</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------- CERTIFICATIONS ----------
st.markdown('<a name="certifications"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom fade-in-card" id="certifications">
  <div class="section-title" style="background:#34495E;">Certifications & Courses</div>
  <div class="cert-grid">
    <div class="cert-card fade-in-card">
      <div class="cert-title">Guidewire Insurance Suite Analyst 10.0</div>
      <div class="cert-provider">Jasper – Guidewire Education</div>
      <div class="cert-year">2024</div>
    </div>
    <div class="cert-card fade-in-card">
      <div class="cert-title">Karate DSL</div>
      <div class="cert-provider">Udemy</div>
      <div class="cert-year">2023</div>
    </div>
    <!-- Add other certs here -->
  </div>
</div>
""", unsafe_allow_html=True)

# --------- AWARDS ----------
st.markdown('<a name="recognitions"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card hover-zoom fade-in-card" id="recognitions">
  <div class="section-title" style="background:#34495E;">Awards & Recognitions</div>
  <div class="awards-grid">
    <div class="award-card fade-in-card">
      <div class="award-title">Spot Award</div>
      <div class="award-year">2022 & 2023</div>
      <div class="award-sub">InsurCloud – Deloitte, Canada</div>
    </div>
    <!-- Add others as needed -->
  </div>
</div>
""", unsafe_allow_html=True)

# --------- PROJECTS (use your own full list here) ---------
st.markdown('<a name="projects"></a>', unsafe_allow_html=True)
projects = [
    {
        "title": "Canadian Quality of Life Analysis",
        "url": "https://github.com/venkateshsoundar/canadian-qol-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg",
        "tools": ["Python", "Pandas", "Seaborn", "Tableau"],
        "desc": "Analyzed Canadian provinces' quality of life using demographic data and advanced data visualization."
    },
    {
        "title": "Alberta Wildfire Analysis",
        "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg",
        "tools": ["Python", "GeoPandas", "Power BI"],
        "desc": "Mapped and predicted wildfire trends in Alberta with geospatial analysis and interactive dashboards."
    },
    # ...Add the rest...
]
projects_html = '''
<div class="card projects-gallery-pane hover-zoom fade-in-card" id="projects">
  <div class="section-title">Projects Gallery</div>
  <div class="projects-4col-grid">
'''
for proj in projects:
    tools_html = ''.join(f'<span class="project-tool-badge">{tool}</span>' for tool in proj["tools"])
    projects_html += (
        f'<div class="project-main-card hover-zoom fade-in-card">'
        f'<div class="project-img-holder">'
        f'<div class="project-img-inner">'
        f'<img src="{proj["image"]}" alt="{proj["title"]}"/>'
        f'</div></div>'
        f'<div class="project-card-info">'
        f'<div class="project-title">{proj["title"]}</div>'
        f'<div class="project-desc">{proj["desc"]}</div>'
        f'<div class="project-tools-list">{tools_html}</div>'
        f'<div class="project-card-link"><a href="{proj["url"]}" target="_blank">View on GitHub &rarr;</a></div>'
        f'</div></div>'
    )
projects_html += '</div></div>'
st.markdown(projects_html, unsafe_allow_html=True)

# --------- SKILLS ----------
st.markdown('<a name="skills"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="card skills-pane-main hover-zoom fade-in-card" id="skills">
  <div class="skills-header-title hover-zoom">Core Skills and Tools</div>
  <div class="skills-categories-grid">
    <div class="skill-category-card fade-in-card">
      <div class="skill-category-title">Programming Languages</div>
      <div class="skill-list">
        <div class="skill-row-item"><img class="skill-icon-card-hz" src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/python.svg"/>Python</div>
        <!-- Add more -->
      </div>
    </div>
    <!-- Add more skill categories as needed -->
  </div>
</div>
""", unsafe_allow_html=True)

# --------- FADE-IN ANIMATION SCRIPT ---------
st.markdown("""
<script>
window.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.fade-in-card');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  cards.forEach(card => observer.observe(card));
});
</script>
""", unsafe_allow_html=True)
