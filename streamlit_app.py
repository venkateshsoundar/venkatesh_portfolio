import streamlit as st
from openai import OpenAI
import requests
import io
import PyPDF2

# --- Page configuration ---
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")

# --- Load resume bullets ---
@st.cache_data
def load_resume_bullets(url, max_bullets=5):
    r = requests.get(url)
    r.raise_for_status()
    reader = PyPDF2.PdfReader(io.BytesIO(r.content))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    sentences = [s.strip() for s in text.split('.') if len(s) > 50]
    return sentences[:max_bullets]

resume_url = (
    "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/"
    "Venkateshwaran_Resume.pdf"
)
bullets = load_resume_bullets(resume_url)

# --- Projects list ---
projects = [
    {"title": "Canadian Quality of Life Analysis", "url": "https://github.com/venkateshsoundar/canadian-qol-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg"},
    {"title": "Alberta Wildfire Analysis", "url": "https://github.com/venkateshsoundar/alberta-wildfire-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg"},
    {"title": "Toronto Crime Drivers", "url": "https://github.com/venkateshsoundar/toronto-crime-drivers", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg"},
    {"title": "Weight Change Regression Analysis", "url": "https://github.com/venkateshsoundar/weight-change-regression-analysis", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg"},
    {"title": "Calgary Childcare Compliance", "url": "https://github.com/venkateshsoundar/calgary-childcare-compliance", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg"},
    {"title": "Social Media Purchase Influence", "url": "https://github.com/venkateshsoundar/social-media-purchase-influence", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg"},
    {"title": "Obesity Level Estimation", "url": "https://github.com/venkateshsoundar/obesity-level-estimation", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg"},
    {"title": "Weather Data Pipeline (AWS)", "url": "https://github.com/venkateshsoundar/weather-data-pipeline-aws", "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg"}
]

# --- Global CSS & Background ---
st.markdown(
    '''
<style>
.stApp {
  background: url('https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/desk-with-objects.jpg') center/cover no-repeat;
  background-attachment: fixed;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
}
.card {
  width: 100% !important;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
  transition: transform .3s ease, box-shadow .3s ease;
  text-align: center;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.7);
}
.section-title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 6px;
}
.profile-pic {
  border-radius: 50%;
  width: 150px;
  display: block;
  margin: 0 auto 12px;
}
.contact-icon {
  width: 30px;
  height: 30px;
  filter: invert(100%);
  margin: 0 8px;
  vertical-align: middle;
}
.project-item {
  position: relative;
  aspect-ratio: 1/1;
  overflow: hidden;
  border-radius: 12px;
}
.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .3s ease;
}
.project-item:hover .card-img {
  transform: scale(1.05);
}
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity .3s ease;
  font-size: 1.2rem;
  color: #ffffff;
}
.project-item:hover .overlay {
  opacity: 1;
}
.typewriter {
  width: fit-content;
  margin: 0 auto 20px;
}
.typewriter h1 {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  border-right: .15em solid #5A84B4;
  animation: typing 3.5s steps(40,end), blink-caret .75s step-end infinite;
  color: #ffffff;
}
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { from, to { border-color: transparent; } 50% { border-color: #5A84B4; } }
.details-summary {
  background: linear-gradient(135deg, #1F2A44 0%, #324665 100%) !important;
  color: #ffffff !important;
  font-size: 1.6rem !important;
  font-weight: bold !important;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 10px;
  text-align: center;
  cursor: pointer;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
/* --- Chat Styling --- */
.chat-area {
  max-height: 340px;
  overflow-y: auto;
  margin-bottom: 14px;
  padding-right:8px;
  padding-left:2px;
  background: rgba(255,255,255,0.03);
  border-radius: 10px;
}
.bubble-user {
  background: #e8f0fe;
  color: #222;
  padding: 8px 16px;
  border-radius: 18px 18px 2px 18px;
  margin-bottom: 8px;
  text-align: left;
  display: inline-block;
  max-width: 85%;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(120,120,180,0.04);
}
.bubble-assistant {
  background: #5A84B4;
  color: #fff;
  padding: 8px 16px;
  border-radius: 18px 18px 18px 2px;
  margin-bottom: 8px;
  text-align: left;
  display: inline-block;
  max-width: 85%;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.row-user { width: 100%; display: flex; justify-content: flex-end; }
.row-assistant { width: 100%; display: flex; justify-content: flex-start; }
.send-icon-btn {
  background: #5A84B4;
  border: none;
  border-radius: 8px;
  height: 40px;
  width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-top: 2px;
}
.send-icon-btn:hover {
  background: #406496;
}
</style>
    ''', unsafe_allow_html=True
)

# --- Layout ---
left_col, mid_col, right_col = st.columns([1,2,1], gap="large")

# --- Left Pane ---
with left_col:
    st.markdown(
        '<div class="card hover-zoom"><img src="https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Venkatesh.jpg" class="profile-pic"/><h2>Venkatesh Soundararajan</h2><p><strong>M.S. Data Science & Analytics</strong><br>University of Calgary</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#2C3E50;">Contact</div>' +
        '<div style="display:flex; justify-content:center; gap:16px; margin-top:10px;">' +
        '<a href="mailto:venkatesh.balusoundar@gmail.com" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" class="contact-icon"/></a>' +
        '<a href="https://www.linkedin.com/in/venkateshbalus/" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" class="contact-icon"/></a>' +
        '<a href="https://github.com/venkateshsoundar" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" class="contact-icon"/></a>' +
        '</div></div>',
        unsafe_allow_html=True
    )

# --- Center Pane ---
with mid_col:
    # Unified Welcome + Chat Card
    st.markdown(
        '<div class="card hover-zoom">',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="typewriter"><h1>Hello!</h1></div><p>Welcome to my data science portfolio. '
        'Explore my projects below—or ask me about my experience or any project!</p>',
        unsafe_allow_html=True
    )

    # --- Chat History (inside the card, just below intro) ---
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""

    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for role, msg in st.session_state.history:
        if role == "user":
            st.markdown(f'<div class="row-user"><div class="bubble-user"><b>You:</b> {msg}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="row-assistant"><div class="bubble-assistant"><b>Assistant:</b><br>{msg}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Chatbot Prompt (input + icon + clear) ---
    with st.form("chat_form", clear_on_submit=True):
        input_col, send_col, clear_col = st.columns([6, 1, 1])
        with input_col:
            user_input = st.text_input(
                "Ask about my experience or projects...",
                key="chat_input",
                label_visibility="collapsed"
            )
        # Icon send button using HTML
        send_icon_html = """
        <button type="submit" class="send-icon-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
        """
        send_col.markdown(send_icon_html, unsafe_allow_html=True)
        clear_clicked = clear_col.form_submit_button("Clear")

        # Form submit logic: Streamlit form always submits when Enter or the send icon is clicked
        submitted = st.form_submit_button("", use_container_width=False)
        if submitted and user_input.strip():
            st.session_state.history.append(('user', user_input))
            messages = [
                {"role": "system", "content": "You are Venkatesh’s assistant."},
                {"role": "system", "content": "Resume:\n" + "\n".join(f"- {b}" for b in bullets)},
                {"role": "system", "content": "Projects:\n" + "\n".join(f"- {p['title']}" for p in projects)},
                {"role": "user", "content": user_input}
            ]
            with st.spinner("Assistant is typing..."):
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=st.secrets["DEEPSEEK_API_KEY"]
                )
                resp = client.chat.completions.create(
                    model="deepseek/deepseek-r1:free",
                    messages=messages
                )
                reply = resp.choices[0].message.content
            st.session_state.history.append(('assistant', reply))
        if clear_clicked:
            st.session_state.history = []
            st.session_state.chat_input = ""

    # End of card
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Projects Showcase remains below ---
    grid_html = '<div class="grid-container">'
    for proj in projects:
        grid_html += (
            f'<div class="project-item hover-zoom"><a href="{proj["url"]}" target="_blank">'
            f'<img src="{proj["image"]}" class="card-img"/><div class="overlay">{proj["title"]}</div></a></div>'
        )
    grid_html += '</div>'
    st.markdown(
        f"""
<details open>
  <summary class="details-summary">Projects Showcase</summary>
  {grid_html}
</details>
""",
        unsafe_allow_html=True
    )

# --- Right Pane ---
with right_col:
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#1ABC9C;">Skills</div><p style="text-align:center;">Python, SQL, R<br>AWS & SageMaker<br>Streamlit, Tableau<br>Scikit-learn, OpenCV<br>Git, Agile</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#8E44AD;">Experience</div><p style="text-align:center;">Deloitte Quality Lead (8+ yrs)<br>AWS Data Pipelines<br>Agile Team Lead<br>Risk Analytics</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card hover-zoom"><div class="section-title" style="background:#D35400;">Certifications</div><p style="text-align:center;">AWS Solutions Architect<br>Tableau Specialist<br>Scrum Master</p></div>',
        unsafe_allow_html=True
    )
