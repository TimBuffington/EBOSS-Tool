
import streamlit as st
from PIL import Image
import base64
import os

st.set_page_config(page_title="EBOSS Tool", layout="wide", initial_sidebar_state="collapsed")

# Inject background image via base64
def set_background():
    with open("bg.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        display: none;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background()

# Load logo
st.image("logo.png", width=250)

# Title
st.markdown("<h1 style='text-align: center; color: #81BD47;'>Welcome to the EBOSS® Tool</h1>", unsafe_allow_html=True)

# Buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📝 Request Training"):
        st.markdown("<script>window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform','_blank')</script>", unsafe_allow_html=True)
with col2:
    if st.button("📋 Request Demo"):
        st.markdown("<script>window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform','_blank')</script>", unsafe_allow_html=True)
with col3:
    if st.button("🎥 Learn How EBOSS Works"):
        st.markdown("<script>window.open('https://youtu.be/0Om2qO-zZfM?si=iTiPgIL2t-xDFixc','_blank')</script>", unsafe_allow_html=True)
with col4:
    st.session_state.show_tools = True

# Horizontal Navigation
st.markdown("""
<style>
.nav-buttons {
    display: flex;
    justify-content: space-evenly;
    margin-top: 2rem;
}
.nav-buttons button {
    background-color: #000;
    color: #81BD47;
    border: 1px solid #D3D3D3;
    border-radius: 8px;
    padding: 0.5rem 2rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

if 'show_tools' not in st.session_state:
    st.session_state.show_tools = False

if st.session_state.show_tools:
    nav = st.radio("Navigation", ["Compare Specs", "Cost Analysis", "Parallel Calculator", "Load Specs"], horizontal=True)

    if nav == "Compare Specs":
        st.title("Compare Specs")
        st.write("Dropdown-based model spec comparison will be rendered here.")
    elif nav == "Cost Analysis":
        st.title("Cost Analysis")
        st.write("Rental rate, fuel cost, and total weekly cost calculations.")
    elif nav == "Parallel Calculator":
        st.title("Parallel Generator Sizing Calculator")
        st.write("Parallel sizing logic will calculate total kW/kVA.")
    elif nav == "Load Specs":
        st.title("Load Spec Entry")
        st.write("Collect and analyze load-based runtime estimates.")
