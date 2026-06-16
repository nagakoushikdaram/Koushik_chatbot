import streamlit as st
from openai import OpenAI

# 1. Setup client 
# Ensure GROQ_API_KEY is saved in your Streamlit Cloud Settings > Secrets
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["GROQ_API_KEY"]
)

st.set_page_config(page_title="Koushik's ChatBot", layout="centered")

st.markdown("""
<style>
    .brand-title { font-size: 2em; font-weight: bold; color: #1E3A8A; }
    .mono-tag { font-family: monospace; background: #eee; padding: 2px 5px; }
</style>
<div class="hero-container">
    <div class="brand-title">Koushik's ChatBot</div>
    <div class="brand-subtitle">Cloud-hosted AI Workspace <span class="mono-tag">production-ready</span></div>
</div>
""", unsafe_allow_html=True)

# 2. Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle user input
user_prompt = st.chat_input("Message the AI...")

if user_prompt:
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 4. Generate assistant response
    with st.chat_message("assistant"):
        # Corrected list comprehension to fix JSON serialization error
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})