import requests
import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Local AI Workspace",
    page_icon="🦾",
    layout="centered"
)

# -----------------------------
# Custom CSS (Utilitarian Minimalism - Ollama Style)
# -----------------------------
st.markdown("""
<style>
/* Import Inter and JetBrains Mono fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Apply Base Fonts */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Main layout constraints */
.block-container { 
    max-width: 800px; 
    padding-top: 3rem; 
    padding-bottom: 4rem;
}

/* Minimalist Hero Section */
.hero-container {
    text-align: center;
    padding-bottom: 2.5rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(128, 128, 128, 0.15);
}

.brand-title { 
    font-size: 2.75rem; 
    font-weight: 800; 
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.75rem;
    color: var(--text-color);
}

.brand-subtitle { 
    font-size: 1.05rem; 
    font-weight: 400;
    line-height: 1.6;
    color: rgba(128, 128, 128, 0.9);
    max-width: 550px;
    margin: 0 auto;
}

/* Flat, Monospace Tags/Notes */
.mono-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    background: rgba(128, 128, 128, 0.1);
    border: 1px solid rgba(128, 128, 128, 0.2);
    padding: 2px 6px;
    border-radius: 4px;
    color: var(--text-color);
}

/* Settings Expander styling */
[data-testid="stExpander"] {
    background-color: transparent !important;
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    margin-bottom: 2rem;
}
[data-testid="stExpander"] summary {
    padding: 0.75rem 1rem !important;
}
[data-testid="stExpander"] summary p {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Sleek, Flat Buttons */
.stButton button {
    font-weight: 500;
    border-radius: 6px;
    background-color: transparent;
    border: 1px solid rgba(128, 128, 128, 0.3);
    color: var(--text-color);
    transition: all 0.15s ease-in-out;
    width: 100%;
}
.stButton button:hover { 
    background-color: var(--text-color); 
    border-color: var(--text-color);
    color: var(--background-color);
}

/* Technical Notes Box */
.teaching-notes {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: rgba(128, 128, 128, 0.8);
    background: transparent;
    border-left: 2px solid rgba(128, 128, 128, 0.3);
    padding-left: 12px;
    margin-top: 8px;
    line-height: 1.6;
}

/* Minimal Chat Input */
[data-testid="stChatInput"] {
    border-radius: 8px !important;
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    background-color: transparent !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(128, 128, 128, 0.6) !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero-container">
    <div class="brand-title">Koushik's ChatBot</div>
    <div class="brand-subtitle">Build your first Generative AI app using Python, Streamlit and Ollama. <span class="mono-tag">local-env</span></div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Inline Control Panel
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"

with st.expander("Configuration", expanded=False):
    col1, col2, col3 = st.columns([1, 1, 1.2], gap="medium")
    
    with col1:
        model = st.selectbox(
            "Model",
            ["llama3.2", "llama3.1", "llama3", "mistral", "gemma2", "qwen2.5", "qwen2.5:3b"],
            index=0,
            label_visibility="collapsed"
        )
        if st.button("Clear Context"):
            st.session_state.messages = []
            st.rerun()

    with col2:
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            label_visibility="collapsed"
        )
        st.markdown("""
        <div class="teaching-notes">
            [+] Local execution<br/>
            [+] Temp: 0.0 -> 1.0<br/>
            [+] Stateless protocol
        </div>
        """, unsafe_allow_html=True)

    with col3:
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful AI assistant. Explain concepts clearly and simply. When useful, respond with examples.",
            height=110,
            label_visibility="collapsed"
        )

# -----------------------------
# Helper Function
# -----------------------------
def check_ollama_running():
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# -----------------------------
# Session State / Memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Ollama Health Check
# -----------------------------
if not check_ollama_running():
    st.error("Connection Refused: Ollama daemon is not running.")
    st.info("Run `ollama serve` in your terminal, then pull a model using `ollama pull llama3.2`.")
    st.stop()

# -----------------------------
# Show Chat History
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_prompt = st.chat_input("Message local model... (Try Telugu: 'Generative AI ante enti?')")

if user_prompt:
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Build full messages list for Ollama
    messages_for_ollama = [{"role": "system", "content": system_prompt}]
    messages_for_ollama.extend(st.session_state.messages)

    # 3. Stream assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            payload = {
                "model": model,
                "messages": messages_for_ollama,
                "stream": True,
                "options": {
                    "temperature": temperature
                }
            }

            with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        data = line.decode("utf-8")
                        import json
                        chunk = json.loads(data)

                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            full_response += content
                            response_placeholder.markdown(full_response + "▌")

                        if chunk.get("done", False):
                            break

            response_placeholder.markdown(full_response)

        except requests.exceptions.HTTPError as e:
            full_response = (
                f"**HTTP Error:** `{str(e)}`\n\n"
                f"The model `{model}` is likely not downloaded.\n\n"
                f"Execute in terminal: `ollama pull {model}`"
            )
            response_placeholder.error(full_response)

        except Exception as e:
            full_response = f"**Error:** `{str(e)}`"
            response_placeholder.error(full_response)

    # 4. Store assistant response in memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})