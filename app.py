import streamlit as st
from openai import OpenAI

# 1. Setup client (It uses the API key from Streamlit Secrets)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["GROQ_API_KEY"]
)

st.set_page_config(page_title="Koushik's ChatBot", layout="centered")
# [Insert your Custom CSS here - I left it out for brevity, keep what you had]

st.markdown("""
<div class="hero-container">
    <div class="brand-title">Koushik's ChatBot</div>
    <div class="brand-subtitle">Cloud-hosted AI Workspace <span class="mono-tag">production-ready</span></div>
</div>
""", unsafe_allow_html=True)

# 2. Logic Change: No more checking if Ollama is running!
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Message the AI...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile", # Updated model
    messages=[...],
    stream=True,
)
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})