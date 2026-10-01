
import streamlit as st
from google import genai

# -----------------------------
# Gemini API Configuration
# -----------------------------

API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Career Guidance Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Career Guidance Chatbot")
st.write(
    "Ask questions about programming, AI, cybersecurity, "
    "software development, careers, interviews, and learning roadmaps."
)

# -----------------------------
# System Prompt
# -----------------------------

SYSTEM_PROMPT = """
You are an AI Career Guidance Assistant.

Your purpose is to help university students and fresh graduates
with technology careers and learning.

You can help with:
- Career guidance
- Programming
- Artificial Intelligence
- Machine Learning
- Data Science
- Cybersecurity
- Software Development
- Technical interviews
- Resume and CV improvement
- Learning roadmaps
- Student project ideas

Give clear, practical and beginner-friendly answers.

If the user asks something unrelated to career, education,
technology or learning, politely explain that you are mainly
designed for career and technology guidance.

Do not make up facts.
"""

# -----------------------------
# Conversation History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------

user_message = st.chat_input(
    "Ask me about your technology career..."
)

if user_message:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Build conversation history
    history_text = ""

    for message in st.session_state.messages:
        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
{SYSTEM_PROMPT}

Previous conversation:

{history_text}

Assistant:
"""

    # Generate response
    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        assistant_response = response.text

    except Exception as e:

        assistant_response = (
            "Sorry, the AI service is temporarily unavailable. "
            "Please try again in a moment."
        )

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_response
    })

# -----------------------------
# Clear Chat
# -----------------------------

if st.button("🗑️ New Chat"):

    st.session_state.messages = []

    st.rerun()
