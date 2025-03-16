import streamlit as st

st.set_page_config(page_title="S.P.A.R.K Dashboard", layout="wide")

with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Welcome to the <span style='color:#00FFFF;'>S.P.A.R.K</span> Dashboard</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Select your next step:</p><br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💬 Chatbot")
    st.write("Chat with our AI advisor.")
    st.page_link("pages/chatbot.py", label="Open Chatbot", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Investing Companion")
    st.write("Get personalized stock recommendations.")
    st.page_link("pages/companion.py", label="Open Companion", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
