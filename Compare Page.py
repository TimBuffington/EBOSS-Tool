
def tech_specs()
from spec_data import spec_data

st.title("Tech Specs Comparison")

selected_model = st.selectbox("Select EBOSS® Model", list(spec_data.keys()))

model_data = spec_data[selected_model]

col1, col2 = st.columns(2)
for label, value in model_data.items():
    with col1:
        st.markdown(f"**{label}**")
    with col2:
        st.markdown(f"{value}")
    
