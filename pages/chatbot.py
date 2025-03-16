import requests
import json
import streamlit as st
import uuid
import google.generativeai as genai
from google.generativeai import configure

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyASXv2rN1IEkpBCVwAxBH7n-JPOtuhTkDc"  # Replace with your actual API key
configure(api_key=GEMINI_API_KEY)

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return simplify_data(data)
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    except json.JSONDecodeError:
        return "Invalid JSON response from the API."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def simplify_data(data):
    if isinstance(data, dict):
        return json.dumps(data, indent=2)[:500]
    elif isinstance(data, list) and len(data) > 0:
        return "\n".join([str(item) for item in data[:5]])
    return "No relevant data found."

def query_gemini(prompt):
    structured_prompt = (
        f"""
        {prompt}

        Provide a structured answer, including:

        1️⃣ Straight Answer: - A direct and concise answer.
        2️⃣ Flowchart Representation: - A simple flowchart explaining the process or logic.
        3️⃣ Case Study: - A brief real-life case study or example.
        4️⃣ Illustration: - A short, illustrative analogy or example.
        """
    )
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(structured_prompt)
        return response.text if hasattr(response, "text") else "I couldn't find an answer. Try rephrasing!"
    except Exception as e:
        return f"Sorry, I couldn't fetch the response. Error: {e}"

def chat_ui():
    st.set_page_config(page_title="FinLit", page_icon="💬", layout="wide")

    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    if "selected_chat" not in st.session_state:
        chat_id = str(uuid.uuid4())[:8]
        st.session_state.chat_sessions[chat_id] = {"name": "New Chat", "messages": []}
        st.session_state.selected_chat = chat_id

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>FinLit</h1>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True):
            chat_id = str(uuid.uuid4())[:8]
            st.session_state.chat_sessions[chat_id] = {"name": "New Chat", "messages": []}
            st.session_state.selected_chat = chat_id

        st.markdown("### Chat History")
        for chat_id, chat_data in list(st.session_state.chat_sessions.items())[::-1]:
            if st.button(f"💬 {chat_data['name']}", use_container_width=True):
                st.session_state.selected_chat = chat_id

    messages = st.session_state.chat_sessions[st.session_state.selected_chat]["messages"]
    chat_container = st.container()
    with chat_container:
        for msg in messages:
            if msg["role"] == "user":
                st.markdown(f'<div style="display: inline-block; max-width: 60%; background-color: #0055ff22; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: right;">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="display: inline-block; max-width: 60%; background-color: #44444422; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: left;">{msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Message FinLit...")
    if user_input:
        messages.append({"role": "user", "content": user_input})
        if st.session_state.chat_sessions[st.session_state.selected_chat]["name"] == "New Chat":
            st.session_state.chat_sessions[st.session_state.selected_chat]["name"] = user_input[:30]

        if user_input.lower().startswith("api:"):
            api_url = user_input[4:].strip()
            api_response = fetch_data(api_url)
            messages.append({"role": "assistant", "content": f"API Response: {api_response}"})
        else:
            ai_response = query_gemini(user_input)
            messages.append({"role": "assistant", "content": ai_response})

        st.session_state.chat_sessions[st.session_state.selected_chat]["messages"] = messages
        st.rerun()

if __name__ == "_main_":
    chat_ui()