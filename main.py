
import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="EBOSS Tool", layout="wide")

def set_background():
    with open("bg.png", "rb") as f:
        base64_img = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_img}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background()

logo = Image.open("logo.png")
st.image(logo, use_column_width=False, width=300)

st.markdown("<h1 style='text-align: center; color: #81BD47;'>Welcome to the EBOSS® Tool</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<a href='https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform' target='_blank'><button style='width:100%; height:100px'>📝 Request Training</button></a>", unsafe_allow_html=True)
with col2:
    st.markdown("<a href='https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform' target='_blank'><button style='width:100%; height:100px'>📋 Request Demo</button></a>", unsafe_allow_html=True)
with col3:
    st.markdown("<a href='https://youtu.be/0Om2qO-zZfM?si=iTiPgIL2t-xDFixc' target='_blank'><button style='width:100%; height:100px'>🎥 Learn How EBOSS Works</button></a>", unsafe_allow_html=True)
with col4:
    st.markdown("<a href='Compare Page.py'><button style='width:100%; height:100px'>🚀 Launch EBOSS Tool</button></a>", unsafe_allow_html=True)
