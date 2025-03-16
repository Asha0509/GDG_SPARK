import streamlit as st

st.set_page_config(page_title="Guidance Placeholder", layout="centered")

with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🚧 Guidance Coming Soon")
st.info("This section will be replaced with Aframe soon.")
