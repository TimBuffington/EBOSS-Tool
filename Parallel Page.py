
import streamlit as st

st.title("Parallel Generator Sizing Calculator")

st.markdown("## Enter Generator Configuration")
num_units = st.number_input("Number of Generators", min_value=1, value=2)
gen_kva = st.number_input("Generator Size (kVA)", min_value=1)
voltage = st.selectbox("Voltage", ["208V", "480V"])

if voltage == "208V":
    factor = 0.8
else:
    factor = 1.0

total_kva = num_units * gen_kva
total_kw = total_kva * factor

st.markdown(f"### Total kVA: `{total_kva}`")
st.markdown(f"### Estimated Total kW: `{total_kw}`")
