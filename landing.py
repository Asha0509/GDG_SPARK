import streamlit as st

st.set_page_config(page_title="S.P.A.R.K", layout="centered")

with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-top: 5rem;'>
        <h1>WELCOME TO <span style='color: #00FFFF;'>S.P.A.R.K</span></h1>
        <h4>Strategic Predictive Analytics & Robust Knowledge Platform</h4>
    </div>
    <br><br>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/aframe_placeholder.py", label="🧠 Need guidance about finance and investing", use_container_width=True)

with col2:
    st.page_link("pages/dashboard.py", label="📚 Knows about investing and finance but need guidance", use_container_width=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>© 2025 S.P.A.R.K Platform</p>", unsafe_allow_html=True)
