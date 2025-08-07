
import streamlit as st
from spec_data import spec_data

st.set_page_config(page_title="EBOSS Tool", layout="wide")

st.markdown("<h1 style='text-align: center;'>Welcome to the EBOSS® Tool</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?embedded=true" width="640" height="900" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    <br><br>
    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?embedded=true" width="640" height="900" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    <br><br>
    <a href="Compare Page.py"><button>🔍 Launch EBOSS Tool</button></a>
</div>
""", unsafe_allow_html=True)
    