import streamlit as st
import requests
import json
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AssistAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar collapsible from arrow
)

WEBHOOK_URL = "https://assistai-n8n-djqj.onrender.com/webhook/840ac786-78df-43ba-803b-9f8a1cdfa04d"

# ---------------- GLOBAL FUTURISTIC STYLE ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: radial-gradient(circle at 30% 20%, #0f172a, #020617 70%);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #0b1120);
    border-right: 1px solid #1e293b;
}

/* Sidebar Title */
.ai-title {
    font-size: 30px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Online Indicator */
.online-dot {
    height: 10px;
    width: 10px;
    background-color: #22c55e;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    box-shadow: 0 0 10px #22c55e;
}

/* Capability Cards */
.cap-card {
    background: #111827;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    margin-bottom: 10px;
    transition: all 0.3s ease-in-out;
    font-size: 14px;
}

.cap-card:hover {
    transform: translateY(-4px);
    border: 1px solid #9333ea;
    box-shadow: 0px 0px 20px rgba(147,51,234,0.25);
}

/* Welcome Box */
.welcome-box {
    background: #0f172a;
    padding: 60px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #1e293b;
    box-shadow: 0px 0px 40px rgba(168,85,247,0.1);
}

.welcome-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.welcome-sub {
    color: #94a3b8;
    font-size: 16px;
    margin-top: 12px;
}

/* Chat Bubbles */
[data-testid="stChatMessage"] {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0px 0px 18px rgba(168,85,247,0.08);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #9333ea);
    color: white;
    border-radius: 14px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 500;
    transition: 0.3s;
}

.stButton > button:hover {
    opacity: 0.85;
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<div class='ai-title'>🤖 AssistAI</div>", unsafe_allow_html=True)
    st.markdown("<span class='online-dot'></span>AI Engine Online", unsafe_allow_html=True)
    st.markdown("### Autonomous Productivity System")
    st.markdown("---")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### ⚙️ Capabilities")

    st.markdown("""
    <div class="cap-card">📅 Smart Calendar Scheduling</div>
    <div class="cap-card">📧 Intelligent Email Automation</div>
    <div class="cap-card">✅ Task Management</div>
    <div class="cap-card">📝 Knowledge Management</div>
    <div class="cap-card">💰 Expense Intelligence System</div>
    """, unsafe_allow_html=True)

# ---------------- WELCOME ----------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-title">AI Executive Assistant</div>
        <div class="welcome-sub">
            Real-time workflow orchestration. Designed to automate your digital operations.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Ask your AI assistant anything...")

# ---------------- SEND MESSAGE ----------------
if user_input:

    current_time = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.spinner("⚡ AI Engine Processing..."):

            response = requests.post(
                WEBHOOK_URL,
                json={
                    "message": user_input,
                    "userId": "demo_user_1"
                },
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list) and "output" in data[0]:
                    raw_output = data[0]["output"]
                elif isinstance(data, dict) and "output" in data:
                    raw_output = data["output"]
                else:
                    raw_output = str(data)

                try:
                    parsed = json.loads(raw_output)
                    ai_reply = parsed.get("message", raw_output)
                except:
                    ai_reply = raw_output
            else:
                ai_reply = "❌ Assistant encountered an error."

    except:
        ai_reply = "⚠️ Unable to connect to AI engine."

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply,
    })

    with st.chat_message("assistant"):
        st.markdown(ai_reply)

