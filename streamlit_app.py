import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Portfolio Chatbot", layout="centered")

# CSS for blinking dots
st.markdown("""
<style>
@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}
.blink-dots {
  display: inline-block;
  animation: blink 1s step-start infinite;
}
</style>
""", unsafe_allow_html=True)

# Heading with blinking dots
st.markdown("## Welcome to my Portfolio<span class='blink-dots'>...</span>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for role, content in st.session_state.messages:
    st.chat_message(role).write(content)

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append user message
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").write(user_input)
    
    # Build prompt with a simple context
    prompt = f"You are a helpful assistant. Answer the user's question.\nUser: {user_input}\nAssistant:"
    
    # Call OpenAI
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets.get("DEEPSEEK_API_KEY"))
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    
    # Append assistant response
    st.session_state.messages.append(("assistant", reply))
    st.chat_message("assistant").write(reply)
