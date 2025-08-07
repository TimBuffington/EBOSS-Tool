
import streamlit as st

st.title("Cost Analysis")

st.markdown("## Enter Rental and Fuel Info")

rental_rate = st.number_input("Generator Rental Cost per Week ($)", min_value=0)
fuel_cost = st.number_input("Fuel Cost per Gallon ($)", min_value=0.0)
fuel_consumption = st.number_input("Fuel Consumption (gal/hr)", min_value=0.0)
run_hours_per_day = st.number_input("Runtime per Day (hours)", min_value=0.0)

weekly_fuel_usage = fuel_consumption * run_hours_per_day * 7
weekly_fuel_cost = weekly_fuel_usage * fuel_cost
total_weekly_cost = rental_rate + weekly_fuel_cost

st.markdown(f"### Weekly Fuel Usage: `{weekly_fuel_usage:.2f}` gallons")
st.markdown(f"### Weekly Fuel Cost: `${weekly_fuel_cost:.2f}`")
st.markdown(f"### Total Weekly Operating Cost: `${total_weekly_cost:.2f}`")
