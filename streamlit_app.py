import streamlit as st
from openai import OpenAI
from time import sleep

# Page config
st.set_page_config(page_title="Venkatesh Chatbot", layout="centered")

# --- CSS for blinking intro ---
st.markdown("""
    <style>
    @keyframes blink {
      0% { opacity: 1; }
      50% { opacity: 0; }
      100% { opacity: 1; }
    }
    .intro {
      font-size: 48px;
      font-weight: bold;
      text-align: center;
      animation: blink 1s step-start infinite;
      margin-top: 50px;
      margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

def typewriter_effect(text, delay=50):
    placeholder = st.empty()
    full = ""
    for c in text:
        full += c
        placeholder.markdown(f"<p style='font-size:24px; text-align:center;'>{full}</p>", unsafe_allow_html=True)
        sleep(delay / 1000.0)
    placeholder.markdown(f"<p style='font-size:24px; text-align:center;'>{full}</p>", unsafe_allow_html=True)

# Render blinking intro
st.markdown("<div class='intro'>Hi This is Venkatesh</div>", unsafe_allow_html=True)

# Loop typewriter prompt
typewriter_effect("Ask me about myself...")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")

# Chat input
user_input = st.chat_input("Enter your question here...")

if user_input:
    st.session_state.history.append(("user", user_input))
    # Build context and prompt
    profile = {
        "name": "Venkateshwaran Balu Soundararajan",
        "bio": "A data-driven professional with 8+ years in analytics, QA, and data science.",
        "skills": ["Python", "SQL", "Power BI", "AWS", "Streamlit", "Machine Learning"]
    }
    context = f"Name: {profile['name']}\nBio: {profile['bio']}\nSkills: {', '.join(profile['skills'])}\n"
    prompt = f"{context}\nQ: {user_input}\nA:"
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets['DEEPSEEK_API_KEY'])
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{'role':'user','content':prompt}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {e}"
    st.session_state.history.append(("assistant", reply))
    st.experimental_rerun()
