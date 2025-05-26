import streamlit as st

# -------------------- PROJECT DATA --------------------
projects = [
    {
        "title": "Canadian Quality of Life Analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/QualityofLife.jpeg",
        "description": "Analyzed quality of life metrics across Canada using open datasets, pandas, and matplotlib to uncover regional disparities and trends. Built interactive dashboards to support decision-making."
    },
    {
        "title": "Alberta Wildfire Analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Alberta_forestfire.jpeg",
        "description": "Explored and visualized wildfire patterns and environmental impacts in Alberta. Built predictive models and interactive reports for risk mitigation using Python."
    },
    {
        "title": "Toronto Crime Drivers",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Toronto_Crimes.jpeg",
        "description": "Investigated socio-economic and environmental drivers of crime in Toronto neighborhoods. Applied correlation analysis and regression for actionable insights."
    },
    {
        "title": "Weight Change Regression Analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Weight_Change.jpeg",
        "description": "Built regression models to predict weight change based on personal and lifestyle factors. Explored feature importance and visualized results with Python libraries."
    },
    {
        "title": "Calgary Childcare Compliance",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/CalgaryChildcare.jpeg",
        "description": "Analyzed and visualized compliance data from Calgary childcare providers to identify trends and inform policy recommendations."
    },
    {
        "title": "Social Media Purchase Influence",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ConsumerPurchaseDecision.jpeg",
        "description": "Studied the influence of social media marketing on consumer purchase decisions using survey data, sentiment analysis, and visualization."
    },
    {
        "title": "Obesity Level Estimation",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/ObeseLevels.jpeg",
        "description": "Developed classification models to estimate obesity levels based on eating habits, activity, and health data. Employed scikit-learn and feature engineering."
    },
    {
        "title": "Weather Data Pipeline (AWS)",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/weatherprediction.jpeg",
        "description": "Built an AWS-based ETL pipeline to ingest, process, and visualize historical and forecast weather data. Automated data quality checks and reporting."
    },
    {
        "title": "Gmail Sentiment Analysis",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/email_sentiment_Analysis.jpeg",
        "description": "Applied NLP techniques to classify sentiment of Gmail messages, visualize trends, and build a topic model using Python."
    },
    {
        "title": "Penguin Species Prediction Chatbot",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Penguin_Analysis.jpeg",
        "description": "Built a chatbot using Streamlit and ML to classify penguin species based on user input, with interactive explanations and charts."
    },
    {
        "title": "Uber Ride Prediction",
        "image": "https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Uberride_Prediction.jpeg",
        "description": "Developed a regression model to predict Uber ride durations using geospatial and temporal features. Delivered insights through a Streamlit dashboard."
    }
]

# -------------------- MODAL STATE SETUP --------------------
if "modal_open" not in st.session_state:
    st.session_state.modal_open = False
if "modal_idx" not in st.session_state:
    st.session_state.modal_idx = None

def open_modal(i):
    st.session_state.modal_open = True
    st.session_state.modal_idx = i

def close_modal():
    st.session_state.modal_open = False
    st.session_state.modal_idx = None

# -------------------- PAGE STYLE --------------------
st.set_page_config(page_title="Venkatesh Portfolio", layout="wide")
st.markdown("""
<style>
body {background: #19213a;}
h2, h3, h4 {color: #ffd166 !important;}
.project-gallery-title {font-size:2rem; font-weight:700; margin-bottom:18px;}
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px,1fr));
    gap: 28px;
}
.project-card {
    background: #1F2A44;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(44,62,80,0.16);
    text-align: center;
    transition: transform .18s, box-shadow .18s;
    cursor: pointer;
    overflow: hidden;
    position: relative;
}
.project-card:hover {
    transform: translateY(-7px) scale(1.03);
    box-shadow: 0 12px 22px rgba(44,62,80,0.28);
}
.project-card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-bottom: 3px solid #ffd166;
}
.project-title {
    font-weight: bold;
    color: #ffd166;
    padding: 12px 0 6px 0;
    font-size: 1.08rem;
}
.modal-bg {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 99;
    background: rgba(0,0,0,0.55);
    display: flex;
    align-items: center;
    justify-content: center;
}
.modal-content {
    background: linear-gradient(120deg, #22304A 60%, #324665 100%);
    border-radius: 18px;
    padding: 2.4rem 2.3rem 1.7rem 2.3rem;
    box-shadow: 0 14px 50px rgba(0,0,0,0.32);
    color: #fff;
    min-width: 340px;
    max-width: 90vw;
    position: relative;
    animation: fadeInModal .7s cubic-bezier(.17,.67,.43,1.05);
}
@keyframes fadeInModal {
    0% { opacity: 0; transform: scale(0.84) translateY(50px);}
    100% { opacity: 1; transform: none;}
}
.close-btn {
    position: absolute;
    top: 18px; right: 24px;
    background: none;
    border: none;
    font-size: 2.1rem;
    color: #ffd166;
    cursor: pointer;
    transition: color .2s;
}
.close-btn:hover { color: #ff5656; }
</style>
""", unsafe_allow_html=True)

# -------------------- PAGE HEADER / WELCOME --------------------
st.markdown(
    """
    <div style="text-align:center;margin-top:20px;">
        <h1 style="color:#ffd166;font-size:2.4rem;margin-bottom:5px;">👋 Venkatesh Portfolio</h1>
        <p style="color:#fff;font-size:1.18rem;">
            Data Scientist & Software Developer passionate about analytics, cloud, and building solutions.<br>
            <span style="color:#ffd166">Click any project below to see details!</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- PROJECT GALLERY --------------------
st.markdown('<div class="project-gallery-title">Projects Gallery</div>', unsafe_allow_html=True)
st.markdown('<div class="project-grid">', unsafe_allow_html=True)
for idx, proj in enumerate(projects):
    card_html = f"""
    <div class="project-card" onclick="window.dispatchEvent(new CustomEvent('OPEN_MODAL_{idx}'));">
        <img src="{proj['image']}" />
        <div class="project-title">{proj['title']}</div>
    </div>
    """
    # Button for fallback Streamlit callback
    st.markdown(
        f"""
        <div onclick="window.dispatchEvent(new CustomEvent('OPEN_MODAL_{idx}'));" style="display:inline-block;width:100%;">
        <button style="display:none;" onClick="window.dispatchEvent(new CustomEvent('OPEN_MODAL_{idx}'));">.</button>
        {card_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- Simulate JavaScript click in Streamlit for project popup ---
for idx in range(len(projects)):
    st.components.v1.html(f"""
        <script>
        window.addEventListener('OPEN_MODAL_{idx}', function() {{
            window.parent.postMessage({{"isStreamlitMessage":true,"type":"streamlit:setComponentValue","key":"modal{idx}","value":true}}, "*");
        }});
        </script>
    """, height=0)
    if st.experimental_get_query_params().get(f"modal{idx}"):
        open_modal(idx)

# --- Streamlit-native fallback for modal on card click (so it always works) ---
for idx, proj in enumerate(projects):
    if st.button("", key=f"project_btn_{idx}", help=proj["title"], args=(idx,), on_click=open_modal, kwargs={"i": idx}):
        pass

# -------------------- MODAL POPUP --------------------
if st.session_state.modal_open and st.session_state.modal_idx is not None:
    proj = projects[st.session_state.modal_idx]
    st.markdown(
        f"""
        <div class="modal-bg">
            <div class="modal-content">
                <button class="close-btn" onclick="window.dispatchEvent(new CustomEvent('CLOSE_MODAL'));">&#10005;</button>
                <img src="{proj['image']}" style="width:100%;border-radius:10px;max-height:200px;object-fit:cover;margin-bottom:12px;"/>
                <h2 style="color:#ffd166;">{proj['title']}</h2>
                <p style="margin-top:1rem;font-size:1.08rem;">{proj['description']}</p>
            </div>
        </div>
        <script>
        window.addEventListener('CLOSE_MODAL', function() {{
            window.parent.postMessage({{"isStreamlitMessage":true,"type":"streamlit:setComponentValue","key":"close_modal","value":true}}, "*");
        }});
        </script>
        """,
        unsafe_allow_html=True
    )
    # Streamlit fallback for close
    if st.button("Close", key="modal_close_btn", on_click=close_modal):
        pass

# Fallback: Streamlit native close from JS message (always safe)
if st.experimental_get_query_params().get("close_modal"):
    close_modal()
