
st.markdown("""
<style>
.stColumn {
    flex: 1 1 0%;
    min-width: 0 !important;
    max-width: 100% !important;
    overflow-wrap: break-word;
    word-wrap: break-word;
    box-sizing: border-box;
}
.form-container div {
    padding: 0.5rem;
    box-sizing: border-box;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)

    """, unsafe_allow_html=True)
    
    # Current and max rates display
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<span style="color: #ffffff;"><strong>Current Rate:</strong> {st.session_state.get("current_charge_rate", 0)} kW</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span style="color: #ffffff;"><strong>Maximum Allowed:</strong> {st.session_state.get("max_charge_rate", 0)} kW</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Option 1: Use Recommended
    default_rate = st.session_state.get("default_charge_rate", 0)
    if st.button(f"✓ Use Recommended ({default_rate} kW)", key="dialog_recommended", use_container_width=True):
        st.session_state.use_custom_charge = False
        st.session_state.custom_charge_rate = None
        st.session_state.show_charge_modal = False
        st.rerun()
    
    st.markdown('<span style="color: #ffffff;"><strong>Or enter custom rate:</strong></span>', unsafe_allow_html=True)
    
    # Custom rate input
    current_custom = st.session_state.custom_charge_rate or default_rate
    max_rate = st.session_state.get("max_charge_rate", 100)
    
    custom_rate = st.number_input(
        "Custom Charge Rate (kW)",
        min_value=0.1,
        max_value=max_rate,
        value=float(current_custom),
        step=0.1,
        help=f"Maximum allowed: {max_rate} kW (98% of generator capacity)",
        key="dialog_custom_rate"
    )
    
    # Preview calculations
    battery_kwh = st.session_state.get("battery_capacity_kwh", 0)
    battery_life = st.session_state.get("battery_longevity", 0)
    current_rate = st.session_state.get("current_charge_rate", 0)
    
    if custom_rate != current_rate and battery_kwh > 0:
        new_charge_time = battery_kwh / custom_rate if custom_rate > 0 else 0
        new_charges_day = 24 / (new_charge_time + battery_life) if (new_charge_time + battery_life) > 0 else 0
        
        st.markdown('<span style="color: #ffffff;"><strong>Preview Changes:</strong></span>', unsafe_allow_html=True)
        prev_col1, prev_col2 = st.columns(2)
        with prev_col1:
            st.markdown(f'<span style="color: #ffffff;">New Charge Time: <strong>{new_charge_time:.2f} hours</strong></span>', unsafe_allow_html=True)
        with prev_col2:
            st.markdown(f'<span style="color: #ffffff;">New Charges/Day: <strong>{new_charges_day:.2f}</strong></span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("✓ Apply Changes", key="dialog_apply", use_container_width=True):
            if custom_rate <= max_rate:
                st.session_state.use_custom_charge = True
                st.session_state.custom_charge_rate = custom_rate
                st.session_state.show_charge_modal = False
                st.rerun()
            else:
                st.error(f"⚠️ Exceeds maximum of {max_rate} kW")
    
    with btn_col2:
        if st.button("✕ Cancel", key="dialog_cancel", use_container_width=True):
            st.session_state.show_charge_modal = False
            st.rerun()

# Show modal if requested
if st.session_state.get('show_charge_modal', False):
    charge_rate_modal()

# Show generator selection dialog
elif st.session_state.get('show_generator_dialog', False):
    generator_selection_dialog()

# Show cost analysis dialog
if st.session_state.get('show_cost_dialog', False):
    cost_analysis_dialog()

# Comparison Display
elif st.session_state.get('show_comparison', False) and st.session_state.eboss_model:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">⚖️ EBOSS® vs Standard Generator Comparison</h3>', unsafe_allow_html=True)
    
    # Close button for comparison
    if st.button("✕ Close Comparison", key="close_comparison"):
        st.session_state.show_comparison = False
        st.rerun()
    
    # Standard Generator dropdown in comparison section
    st.markdown('<br>', unsafe_allow_html=True)
    standard_generator_options = [
        "25 kVA / 20 kW", "45 kVA / 36 kW", "65 kVA / 52 kW", 
        "125 kVA / 100 kW", "220 kVA / 176 kW", "400 kVA / 320 kW"
    ]
    
    # If no standard generator is selected yet, show the paired generator as default
    if st.session_state.standard_generator is None:
        paired_gen = EBOSS_STANDARD_PAIRING.get(st.session_state.eboss_model, "25 kVA / 20 kW")
        current_index = standard_generator_options.index(paired_gen) + 1 if paired_gen in standard_generator_options else 0
    else:
        current_index = standard_generator_options.index(st.session_state.standard_generator) + 1 if st.session_state.standard_generator in standard_generator_options else 0
    
    st.session_state.standard_generator = st.selectbox(
        "Select Standard Generator for Comparison",
        options=[None] + standard_generator_options,
        index=current_index,
        key="standard_generator_select",
        help="Choose a standard diesel generator size to compare with your EBOSS® configuration"
    )
    
    # Only show comparison table if standard generator is selected
    if st.session_state.standard_generator:
        # Calculate specifications for both systems
        custom_charge = st.session_state.custom_charge_rate if st.session_state.use_custom_charge else None
        eboss_specs = calculate_load_specs(
            st.session_state.eboss_model,
            st.session_state.eboss_type,
            st.session_state.continuous_load,
            st.session_state.max_peak_load,
            st.session_state.generator_kva,
            custom_charge
        )
        
        standard_specs = calculate_standard_generator_specs(
            st.session_state.standard_generator,
            st.session_state.continuous_load,
            st.session_state.max_peak_load
        )
        
        if eboss_specs and standard_specs:
            # Create 4-column layout: Labels, EBOSS® Values, Standard Generator Values, Difference
            col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
        
            with col1:
                st.markdown("""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                    <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">SPECIFICATION</strong>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                    <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">EBOSS {st.session_state.eboss_model}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                    <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">STANDARD {st.session_state.standard_generator}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                    <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">DIFFERENCE</strong>
                </div>
                """, unsafe_allow_html=True)
        
            # Calculate EBOSS® fuel consumption values
            eboss_fuel_per_hour = eboss_specs.get('fuel_consumption_gph', 0) or 0
            battery_capacity = eboss_specs.get('battery_capacity', 0)
            charge_time = eboss_specs.get('charge_time', 0)
            battery_life = battery_capacity / st.session_state.continuous_load if st.session_state.continuous_load > 0 else 0
            
            if charge_time > 0 and battery_life > 0:
                eboss_runtime_hours = charge_time
                eboss_cycles_per_day = 24 / (charge_time + battery_life)
                eboss_fuel_per_day = eboss_fuel_per_hour * eboss_runtime_hours * eboss_cycles_per_day
            else:
                eboss_fuel_per_day = 0
                
            eboss_fuel_per_month = eboss_fuel_per_day * 30
            eboss_co2_per_day = eboss_fuel_per_day * 22.4
            
            # Calculate differences
            fuel_diff_day = eboss_fuel_per_day - standard_specs['fuel_per_day']
            fuel_diff_month = eboss_fuel_per_month - standard_specs['fuel_per_month']
            co2_diff_day = eboss_co2_per_day - standard_specs['co2_per_day']
            
            # Get EBOSS® engine load percentage from specs (based on paired generator)
            eboss_engine_load = eboss_specs.get('engine_load_percent', 0)
            standard_engine_load = 100  # Standard generators run at 100% of rated load
            engine_load_diff = eboss_engine_load - standard_engine_load
            
            # Get paired generator info for display
            paired_generator_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(st.session_state.eboss_model, 0)
            paired_gen_name = f"{paired_generator_kva} kVA" if paired_generator_kva > 0 else "N/A"
            
            # Calculate standard generator engine load based on continuous load
            standard_gen_data = STANDARD_GENERATOR_DATA.get(st.session_state.standard_generator, {})
            standard_gen_kw = standard_gen_data.get('kw', 20)
            standard_engine_load_percent = (st.session_state.continuous_load / standard_gen_kw * 100) if standard_gen_kw > 0 else 0
            
            # Get EBOSS® specs based on model
            eboss_model_specs = EBOSS_SPECS.get(st.session_state.eboss_model, {})
            
            # Get EBOSS® max continuous output kW from specifications
            eboss_max_continuous_kw = {
                "EB25 kVA": 22,    # From Max Continuous amp-load 480V: 28 A / 22 kW
                "EB70 kVA": 56,    # From Max Continuous amp-load 480V: 67 A / 56 kW  
                "EB125 kVA": 80,   # From Max Continuous amp-load 480V: 192 A / 80 kW
                "EB220 kVA": 176,  # From Max Continuous amp-load 480V: 211 A / 176 kW
                "EB400 kVA": 320   # From Max Continuous amp-load 480V: 385 A / 320 kW
            }.get(st.session_state.eboss_model, 0)
            
            # Authentic comparison data from Excel table (all values except GPH and engine load %)
            authentic_comparison_specs = {
                "EB25 kVA": {
                    "Three-phase Max Power": "30 kVA / 24 kW",
                    "Single-phase Max Power": "12 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "Yes", 
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "83 A",
                    "Max Intermittent amp-load 480V": "36 A",
                    "Motor start rating - 3 second 208V": "166 A",
                    "Motor start rating - 3 second 480V": "72 A",
                    "Three-phase Continuous": "14.5 kW",
                    "Single-phase Continuous": "12 kW", 
                    "Max Continuous amp-load 208V": "40 A",
                    "Max Continuous amp-load 480V": "17 A",
                    "Parallelable": "Yes"
                },
                "EB70 kVA": {
                    "Three-phase Max Power": "85 kVA / 68 kW",
                    "Single-phase Max Power": "30 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "Yes",
                    "Voltage regulation": "Adjustable", 
                    "Max Intermittent amp-load 208V": "236 A",
                    "Max Intermittent amp-load 480V": "102 A",
                    "Motor start rating - 3 second 208V": "472 A",
                    "Motor start rating - 3 second 480V": "204 A",
                    "Three-phase Continuous": "24.5 kW",
                    "Single-phase Continuous": "30 kW",
                    "Max Continuous amp-load 208V": "68 A", 
                    "Max Continuous amp-load 480V": "29 A",
                    "Parallelable": "Yes"
                },
                "EB125 kVA": {
                    "Three-phase Max Power": "151 kVA / 121 kW",
                    "Single-phase Max Power": "50 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "Yes",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "419 A",
                    "Max Intermittent amp-load 480V": "181 A", 
                    "Motor start rating - 3 second 208V": "838 A",
                    "Motor start rating - 3 second 480V": "362 A",
                    "Three-phase Continuous": "49 kW",
                    "Single-phase Continuous": "50 kW",
                    "Max Continuous amp-load 208V": "136 A",
                    "Max Continuous amp-load 480V": "59 A",
                    "Parallelable": "Yes"
                },
                "EB220 kVA": {
                    "Three-phase Max Power": "266 kVA / 213 kW", 
                    "Single-phase Max Power": "75 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "Yes",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "739 A",
                    "Max Intermittent amp-load 480V": "319 A",
                    "Motor start rating - 3 second 208V": "1478 A", 
                    "Motor start rating - 3 second 480V": "638 A",
                    "Three-phase Continuous": "74 kW",
                    "Single-phase Continuous": "75 kW", 
                    "Max Continuous amp-load 208V": "206 A",
                    "Max Continuous amp-load 480V": "89 A",
                    "Parallelable": "Yes"
                },
                "EB400 kVA": {
                    "Three-phase Max Power": "484 kVA / 387 kW",
                    "Single-phase Max Power": "125 kW",
                    "Frequency": "60 Hz", 
                    "Simultaneous voltage": "Yes",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "1347 A",
                    "Max Intermittent amp-load 480V": "582 A",
                    "Motor start rating - 3 second 208V": "2694 A",
                    "Motor start rating - 3 second 480V": "1164 A",
                    "Three-phase Continuous": "125 kW",
                    "Single-phase Continuous": "125 kW",
                    "Max Continuous amp-load 208V": "347 A", 
                    "Max Continuous amp-load 480V": "150 A",
                    "Parallelable": "Yes"
                }
            }
            
            # Authentic standard generator specifications from Excel table (complete data)
            authentic_standard_specs = {
                "25 kVA / 20 kW": {
                    "Three-phase Max Power": "25 kVA / 20 kW",
                    "Single-phase Max Power": "16 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "No",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "69 A",
                    "Max Intermittent amp-load 480V": "30 A",
                    "Motor start rating - 3 second 208V": "138 A",
                    "Motor start rating - 3 second 480V": "60 A",
                    "Three-phase Continuous": "20 kW",
                    "Single-phase Continuous": "16 kW",
                    "Max Continuous amp-load 208V": "56 A",
                    "Max Continuous amp-load 480V": "24 A",
                    "Parallelable": "No"
                },
                "45 kVA / 36 kW": {
                    "Three-phase Max Power": "45 kVA / 36 kW", 
                    "Single-phase Max Power": "29 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "No",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "125 A",
                    "Max Intermittent amp-load 480V": "54 A",
                    "Motor start rating - 3 second 208V": "250 A",
                    "Motor start rating - 3 second 480V": "108 A",
                    "Three-phase Continuous": "36 kW",
                    "Single-phase Continuous": "29 kW",
                    "Max Continuous amp-load 208V": "100 A",
                    "Max Continuous amp-load 480V": "43 A",
                    "Parallelable": "No"
                },
                "65 kVA / 52 kW": {
                    "Three-phase Max Power": "65 kVA / 52 kW",
                    "Single-phase Max Power": "42 kW", 
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "No",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "181 A",
                    "Max Intermittent amp-load 480V": "78 A",
                    "Motor start rating - 3 second 208V": "361 A",
                    "Motor start rating - 3 second 480V": "156 A",
                    "Three-phase Continuous": "52 kW",
                    "Single-phase Continuous": "42 kW",
                    "Max Continuous amp-load 208V": "144 A",
                    "Max Continuous amp-load 480V": "62 A",
                    "Parallelable": "No"
                },
                "125 kVA / 100 kW": {
                    "Three-phase Max Power": "125 kVA / 100 kW",
                    "Single-phase Max Power": "80 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "No", 
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "347 A",
                    "Max Intermittent amp-load 480V": "150 A",
                    "Motor start rating - 3 second 208V": "694 A",
                    "Motor start rating - 3 second 480V": "300 A",
                    "Three-phase Continuous": "100 kW",
                    "Single-phase Continuous": "80 kW",
                    "Max Continuous amp-load 208V": "278 A",
                    "Max Continuous amp-load 480V": "120 A",
                    "Parallelable": "No"
                },
                "220 kVA / 176 kW": {
                    "Three-phase Max Power": "220 kVA / 176 kW",
                    "Single-phase Max Power": "141 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "No",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "611 A",
                    "Max Intermittent amp-load 480V": "264 A", 
                    "Motor start rating - 3 second 208V": "1222 A",
                    "Motor start rating - 3 second 480V": "528 A",
                    "Three-phase Continuous": "176 kW",
                    "Single-phase Continuous": "141 kW",
                    "Max Continuous amp-load 208V": "489 A",
                    "Max Continuous amp-load 480V": "211 A",
                    "Parallelable": "No"
                },
                "400 kVA / 320 kW": {
                    "Three-phase Max Power": "400 kVA / 320 kW",
                    "Single-phase Max Power": "256 kW",
                    "Frequency": "60 Hz",
                    "Simultaneous voltage": "No",
                    "Voltage regulation": "Adjustable",
                    "Max Intermittent amp-load 208V": "1111 A",
                    "Max Intermittent amp-load 480V": "481 A",
                    "Motor start rating - 3 second 208V": "2222 A",
                    "Motor start rating - 3 second 480V": "962 A",
                    "Three-phase Continuous": "320 kW", 
                    "Single-phase Continuous": "256 kW",
                    "Max Continuous amp-load 208V": "889 A",
                    "Max Continuous amp-load 480V": "385 A",
                    "Parallelable": "No"
                }
            }
            
            # Get authentic specs for current models
            eboss_authentic_specs = authentic_comparison_specs.get(st.session_state.eboss_model, {})
            standard_authentic_specs = authentic_standard_specs.get(st.session_state.standard_generator, {})
            
            # Build comparison data with authentic values (except GPH and engine load %)
            comparison_data = [
                # Row 3: Generator Size 
                ("Generator Size", f"{st.session_state.eboss_model}", f"{st.session_state.standard_generator}"),
                
                # Row 4: Maximum Intermittent Power Output header
                ("header", "Maximum Intermittent Power Output", ""),
                
                # Rows 5-13: Intermittent power specifications (authentic values for both EBOSS® and standard)
                ("Three-phase", eboss_authentic_specs.get("Three-phase Max Power", "N/A"), standard_authentic_specs.get("Three-phase Max Power", "N/A")),
                ("Single-phase", eboss_authentic_specs.get("Single-phase Max Power", "N/A"), standard_authentic_specs.get("Single-phase Max Power", "N/A")),
                ("Frequency", eboss_authentic_specs.get("Frequency", "N/A"), standard_authentic_specs.get("Frequency", "N/A")),
                ("Simultaneous voltage", eboss_authentic_specs.get("Simultaneous voltage", "N/A"), standard_authentic_specs.get("Simultaneous voltage", "N/A")),
                ("Voltage regulation", eboss_authentic_specs.get("Voltage regulation", "N/A"), standard_authentic_specs.get("Voltage regulation", "N/A")),
                ("Max. Intermittent amp-load 208V", eboss_authentic_specs.get("Max Intermittent amp-load 208V", "N/A"), standard_authentic_specs.get("Max Intermittent amp-load 208V", "N/A")),
                ("Max. Intermittent amp-load 480V", eboss_authentic_specs.get("Max Intermittent amp-load 480V", "N/A"), standard_authentic_specs.get("Max Intermittent amp-load 480V", "N/A")),
                ("Motor start rating - 3 second 208V", eboss_authentic_specs.get("Motor start rating - 3 second 208V", "N/A"), standard_authentic_specs.get("Motor start rating - 3 second 208V", "N/A")),
                ("Motor start rating - 3 second 480V", eboss_authentic_specs.get("Motor start rating - 3 second 480V", "N/A"), standard_authentic_specs.get("Motor start rating - 3 second 480V", "N/A")),
                
                # Row 14: Maximum Continuous Power Output header
                ("header", "Maximum Continuous Power Output", ""),
                
                # Rows 15-19: Continuous power specifications (authentic values for both EBOSS® and standard)
                ("Three-phase output", eboss_authentic_specs.get("Three-phase Continuous", "N/A"), standard_authentic_specs.get("Three-phase Continuous", "N/A")),
                ("Single-phase output", eboss_authentic_specs.get("Single-phase Continuous", "N/A"), standard_authentic_specs.get("Single-phase Continuous", "N/A")),
                ("Simultaneous voltage", eboss_authentic_specs.get("Simultaneous voltage", "N/A"), standard_authentic_specs.get("Simultaneous voltage", "N/A")),
                ("Max. Continuous amp-load 208V", eboss_authentic_specs.get("Max Continuous amp-load 208V", "N/A"), standard_authentic_specs.get("Max Continuous amp-load 208V", "N/A")),
                ("Max. Continuous amp-load 480V", eboss_authentic_specs.get("Max Continuous amp-load 480V", "N/A"), standard_authentic_specs.get("Max Continuous amp-load 480V", "N/A")),
                
                # Row 21: Fuel Consumption header
                ("header", "Fuel Consumption", ""),
                
                # Rows 22-28: Fuel consumption specifications (calculated GPH and engine load %)
                ("% Engine Load", f"{eboss_engine_load:.1f}%" if eboss_engine_load > 0 else "N/A", f"{standard_engine_load_percent:.1f}%" if standard_engine_load_percent > 0 else "N/A"),
                ("Gallons per Hour", f"{eboss_fuel_per_hour:.2f} GPH" if eboss_fuel_per_hour else "N/A", f"{standard_specs.get('fuel_consumption_gph', 0):.2f} GPH" if standard_specs.get('fuel_consumption_gph') else "N/A"),
                ("Gallons per Day", f"{eboss_fuel_per_day:.1f} gallons" if eboss_fuel_per_day else "N/A", f"{standard_specs.get('fuel_per_day', 0):.1f} gallons" if standard_specs.get('fuel_per_day') else "N/A"),
                ("Gallons per Month", f"{eboss_fuel_per_month:.1f} gallons" if eboss_fuel_per_month else "N/A", f"{standard_specs.get('fuel_per_month', 0):.1f} gallons" if standard_specs.get('fuel_per_month') else "N/A"),
                ("Carbon Emissions per Day", f"{eboss_co2_per_day:.1f} lbs" if eboss_co2_per_day else "N/A", f"{standard_specs.get('co2_per_day', 0):.1f} lbs" if standard_specs.get('co2_per_day') else "N/A"),
                ("Parallelable", eboss_authentic_specs.get("Parallelable", "N/A"), standard_authentic_specs.get("Parallelable", "N/A")),
            ]
            
            # Calculate mathematical differences for each row
            comparison_rows = []
            for spec_name, eboss_value, standard_value in comparison_data:
                if spec_name == "header":
                    comparison_rows.append((spec_name, eboss_value, standard_value, ""))
                else:
                    difference = calculate_mathematical_difference(eboss_value, standard_value, spec_name)
                    comparison_rows.append((spec_name, eboss_value, standard_value, difference))
        
            # Display comparison table with proper header rendering
            for spec_name, eboss_value, standard_value, difference in comparison_rows:
                # Check if this is a header row
                if spec_name == "header":
                    # Close column layout temporarily for full-width header
                    st.markdown('</div>', unsafe_allow_html=True)  # Close the column container
                    
                    # Section header spanning full width
                    st.markdown(f"""
                    <div style="background: var(--energy-green); 
                                color: var(--alpine-white); 
                                padding: 1rem; 
                                margin: 1rem 0 0.5rem 0; 
                                border-radius: 10px; 
                                text-align: center; 
                                box-shadow: 0 8px 16px rgba(0,0,0,0.5), inset 0 2px 4px rgba(255,255,255,0.2); 
                                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                                border: 3px solid rgba(255,255,255,0.1);">
                        <strong style="font-size: 1.2rem; 
                                     text-transform: uppercase; 
                                     letter-spacing: 1px; 
                                     font-family: Arial, sans-serif; 
                                     font-weight: 700;">
                            {eboss_value}
                        </strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Restart column layout for next rows
                    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
                else:
                    # Regular data row
                    with col1:
                        st.markdown(f"""
                        <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid var(--energy-green); box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                            <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{spec_name}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        eboss_display = eboss_value if eboss_value and str(eboss_value).strip() and str(eboss_value) != "N/A" else "N/A"
                        st.markdown(f"""
                        <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid var(--energy-green); box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                            <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{eboss_display}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        standard_display = standard_value if standard_value and str(standard_value).strip() and str(standard_value) != "N/A" else "N/A"
                        st.markdown(f"""
                        <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid var(--energy-green); box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                            <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{standard_display}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        # Format difference value with proper color coding
                        formatted_diff, difference_color = format_difference_value(difference, spec_name)
                        
                        st.markdown(f"""
                        <div style="background: var(--cool-gray-10c); color: {difference_color}; padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid var(--energy-green); box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                            <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{formatted_diff}</span>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">Please select a standard generator above to view the comparison.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)



# 
<div style='text-align:right; margin-bottom: 1rem;'>
    <button onclick="window.print()" style="background-color: #636569; border: none; color: white; padding: 0.5rem 1.2rem; font-size: 0.9rem; border-radius: 6px; cursor: pointer;">
        Print Analysis
    </button>
</div>

Cost Analysis

<div style='text-align:center; margin-top:1.5rem;'>
    <a href="https://anacorp.com/contact/" target="_blank">
        <button style="background-color: #81BD47; border: none; color: white; padding: 0.75rem 1.5rem; font-size: 1rem; border-radius: 8px; cursor: pointer;">
            Contact us for more details
        </button>
    </a>
</div>
 Display
if st.session_state.show_cost_analysis and st.session_state.eboss_model:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">💰 
<div style='text-align:right; margin-bottom: 1rem;'>
    <button onclick="window.print()" style="background-color: #636569; border: none; color: white; padding: 0.5rem 1.2rem; font-size: 0.9rem; border-radius: 6px; cursor: pointer;">
        Print Analysis
    </button>
</div>

Cost Analysis

<div style='text-align:center; margin-top:1.5rem;'>
    <a href="https://anacorp.com/contact/" target="_blank">
        <button style="background-color: #81BD47; border: none; color: white; padding: 0.75rem 1.5rem; font-size: 1rem; border-radius: 8px; cursor: pointer;">
            Contact us for more details
        </button>
    </a>
</div>
 Results</h3>', unsafe_allow_html=True)
    
    # Close button for cost analysis
    if st.button("✕ Close 
<div style='text-align:right; margin-bottom: 1rem;'>
    <button onclick="window.print()" style="background-color: #636569; border: none; color: white; padding: 0.5rem 1.2rem; font-size: 0.9rem; border-radius: 6px; cursor: pointer;">
        Print Analysis
    </button>
</div>

Cost Analysis

<div style='text-align:center; margin-top:1.5rem;'>
    <a href="https://anacorp.com/contact/" target="_blank">
        <button style="background-color: #81BD47; border: none; color: white; padding: 0.75rem 1.5rem; font-size: 1rem; border-radius: 8px; cursor: pointer;">
            Contact us for more details
        </button>
    </a>
</div>
", key="close_cost_analysis"):
        st.session_state.show_cost_analysis = False
        st.rerun()
    
    # Get input values from session state with defaults
    local_fuel_price = st.session_state.get('local_fuel_price', 3.50)
    fuel_delivery_fee = st.session_state.get('fuel_delivery_fee', 0.0)
    pm_interval_hrs = st.session_state.get('pm_interval_hrs', 500)
    cost_per_pm = st.session_state.get('cost_per_pm', 0.0) if st.session_state.get('pm_charge_radio') == "Yes" else 0.0
    eboss_weekly_rate = st.session_state.get('eboss_weekly_rate', 0.0)
    eboss_monthly_rate = st.session_state.get('eboss_monthly_rate', 0.0)
    standard_weekly_rate = st.session_state.get('standard_weekly_rate', 0.0)
    standard_monthly_rate = st.session_state.get('standard_monthly_rate', 0.0)
    selected_standard_gen = st.session_state.get('cost_standard_generator', 'N/A')
    
    # Calculate fuel consumption and costs based on load data
    continuous_load = st.session_state.get('continuous_load', 0)
    
    # Get EBOSS® fuel data (from load specs calculations)
    eboss_model = st.session_state.eboss_model
    battery_capacity_kwh = EBOSS_LOAD_REFERENCE["battery_capacities"].get(eboss_model, 0)
    
    # EBOSS® calculations
    if st.session_state.eboss_type == "Full Hybrid":
        generator_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
    else:
        generator_kva = int(st.session_state.generator_kva.replace('kVA', '')) if st.session_state.generator_kva else 0
    
    generator_kw = generator_kva * 0.8
    charge_rate_kw = EBOSS_LOAD_REFERENCE["generator_sizes"].get(generator_kva, {}).get("fh_charge_rate" if st.session_state.eboss_type == "Full Hybrid" else "pm_charge_rate", 0)
    
    # Calculate EBOSS® fuel consumption
    battery_longevity = (battery_capacity_kwh / continuous_load) if continuous_load > 0 else 0
    charge_time = (battery_capacity_kwh / charge_rate_kw) if charge_rate_kw > 0 else 0
    charges_per_day = 24 / (charge_time + battery_longevity) if (charge_time + battery_longevity) > 0 else 0
    engine_load_percent = (charge_rate_kw / generator_kw * 100) if generator_kw > 0 else 0
    
    # Get authentic GPH data
    def interpolate_gph(generator_kva, load_percent):
        if generator_kva not in EBOSS_LOAD_REFERENCE["gph_interpolation"]:
            return 0
        gph_data = EBOSS_LOAD_REFERENCE["gph_interpolation"][generator_kva]
        if load_percent <= 25: return gph_data["25%"]
        elif load_percent <= 50: return gph_data["50%"]
        elif load_percent <= 75: return gph_data["75%"]
        else: return gph_data["100%"]
    
    eboss_fuel_per_hour = interpolate_gph(generator_kva, engine_load_percent) if engine_load_percent > 0 else 0
    eboss_runtime_per_day = charges_per_day * charge_time if charges_per_day > 0 and charge_time > 0 else 0
    
    # Standard generator calculations
    standard_specs = STANDARD_GENERATOR_DATA.get(selected_standard_gen, {})
    standard_fuel_gph = standard_specs.get('fuel_consumption_gph', {}).get('50%', 0)  # Use 50% load as baseline
    standard_runtime_per_day = 24  # Assume continuous operation
    
    # Cost calculations
    def calculate_costs(fuel_per_hour, runtime_per_day, rental_weekly, rental_monthly):
        # Weekly calculations
        weekly_fuel_gal = fuel_per_hour * runtime_per_day * 7
        weekly_fuel_cost = weekly_fuel_gal * local_fuel_price
        weekly_pm_cost = (runtime_per_day * 7 / pm_interval_hrs) * cost_per_pm if pm_interval_hrs > 0 else 0
        weekly_total = rental_weekly + weekly_fuel_cost + fuel_delivery_fee + weekly_pm_cost
        
        # Monthly calculations (30 days)
        monthly_fuel_gal = fuel_per_hour * runtime_per_day * 30
        monthly_fuel_cost = monthly_fuel_gal * local_fuel_price
        monthly_pm_cost = (runtime_per_day * 30 / pm_interval_hrs) * cost_per_pm if pm_interval_hrs > 0 else 0
        monthly_total = rental_monthly + monthly_fuel_cost + (fuel_delivery_fee * 4.3) + monthly_pm_cost  # 4.3 weeks per month
        
        return {
            'weekly': {
                'rental': rental_weekly,
                'runtime_hours': runtime_per_day * 7,
                'pm_services': runtime_per_day * 7 / pm_interval_hrs if pm_interval_hrs > 0 else 0,
                'pm_cost': weekly_pm_cost,
                'diesel_qty': weekly_fuel_gal,
                'diesel_cost': weekly_fuel_cost,
                'fuel_delivery': fuel_delivery_fee,
                'total': weekly_total
            },
            'monthly': {
                'rental': rental_monthly,
                'runtime_hours': runtime_per_day * 30,
                'pm_services': runtime_per_day * 30 / pm_interval_hrs if pm_interval_hrs > 0 else 0,
                'pm_cost': monthly_pm_cost,
                'diesel_qty': monthly_fuel_gal,
                'diesel_cost': monthly_fuel_cost,
                'fuel_delivery': fuel_delivery_fee * 4.3,
                'total': monthly_total
            }
        }
    
    # Debug information (temporary)
    st.write(f"Debug - EBOSS® Model: {eboss_model}")
    st.write(f"Debug - Continuous Load: {continuous_load}")
    st.write(f"Debug - Generator kVA: {generator_kva}")
    st.write(f"Debug - Battery Capacity: {battery_capacity_kwh}")
    st.write(f"Debug - Charge Rate kW: {charge_rate_kw}")
    st.write(f"Debug - Engine Load %: {engine_load_percent}")
    st.write(f"Debug - EBOSS® Fuel GPH: {eboss_fuel_per_hour}")
    st.write(f"Debug - Standard Generator: {selected_standard_gen}")
    st.write(f"Debug - Standard Fuel GPH: {standard_fuel_gph}")
    
    # Calculate costs for both systems
    eboss_costs = calculate_costs(eboss_fuel_per_hour, eboss_runtime_per_day, eboss_weekly_rate, eboss_monthly_rate)
    standard_costs = calculate_costs(standard_fuel_gph, standard_runtime_per_day, standard_weekly_rate, standard_monthly_rate)
    
    # Display the cost analysis table
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Create the table structure using HTML
    st.markdown(f"""
    <div style="background: var(--alpine-white); padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.3); border: 2px solid var(--charcoal);">
        <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 0.9rem; 
                      box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <thead>
                <tr style="background: var(--energy-green); color: var(--alpine-white); 
                          border: 2px solid var(--charcoal); box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    <th style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: left; font-weight: bold; 
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Item</th>
                    <th colspan="2" style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: center; font-weight: bold;
                                         text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Weekly</th>
                    <th colspan="2" style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: center; font-weight: bold;
                                         text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Monthly</th>
                </tr>
                <tr style="background: var(--energy-green); color: var(--alpine-white); 
                          border: 2px solid var(--charcoal); box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: left; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);"></th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">EBOSS® Hybrid</th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">Standard Generator</th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">EBOSS® Hybrid</th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">Standard Generator</th>
                </tr>
            </thead>
            <tbody style="background: var(--alpine-white); color: var(--black-asphalt);">
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Rental Rate</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['rental']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['rental']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['rental']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['rental']:,.2f}</td>
                </tr>
                <tr style="background: #f9f9f9; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Runtime Hours</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['weekly']['runtime_hours']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['weekly']['runtime_hours']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['monthly']['runtime_hours']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['monthly']['runtime_hours']:.1f}</td>
                </tr>
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">PM Services</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['weekly']['pm_services']:.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['weekly']['pm_services']:.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['monthly']['pm_services']:.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['monthly']['pm_services']:.2f}</td>
                </tr>
                <tr style="background: #f9f9f9; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">PM Service Cost</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['pm_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['pm_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['pm_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['pm_cost']:,.2f}</td>
                </tr>
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Diesel Qty (gal)</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['weekly']['diesel_qty']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['weekly']['diesel_qty']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['monthly']['diesel_qty']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['monthly']['diesel_qty']:.1f}</td>
                </tr>
                <tr style="background: #f9f9f9; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Diesel Cost</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['diesel_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['diesel_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['diesel_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['diesel_cost']:,.2f}</td>
                </tr>
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Fuel Delivery Cost</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['fuel_delivery']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['fuel_delivery']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['fuel_delivery']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['fuel_delivery']:,.2f}</td>
                </tr>
                <tr style="background: var(--energy-green); color: var(--alpine-white); font-weight: bold;
                          border: 2px solid var(--charcoal); box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Total Cost</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${eboss_costs['weekly']['total']:,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${standard_costs['weekly']['total']:,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${eboss_costs['monthly']['total']:,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${standard_costs['monthly']['total']:,.2f}</td>
                </tr>
                <tr style="background: var(--energy-green); color: var(--alpine-white); font-weight: bold;
                          border: 2px solid var(--charcoal); box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">EBOSS® Savings</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${(standard_costs['weekly']['total'] - eboss_costs['weekly']['total']):,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">-</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${(standard_costs['monthly']['total'] - eboss_costs['monthly']['total']):,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">-</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost savings summary
    weekly_savings = standard_costs['weekly']['total'] - eboss_costs['weekly']['total']
    monthly_savings = standard_costs['monthly']['total'] - eboss_costs['monthly']['total']
    yearly_savings = monthly_savings * 12  # Calculate yearly savings
    
    savings_color = "var(--energy-green)" if weekly_savings > 0 else "#FF6B6B"
    savings_text = "SAVINGS" if weekly_savings > 0 else "ADDITIONAL COST"
    
    st.markdown(f"""
    <div style="background: {savings_color}; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                text-align: center; font-weight: bold; border: 2px solid var(--charcoal); 
                box-shadow: 0 6px 12px rgba(0,0,0,0.4);">
        <h4 style="margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">EBOSS® {savings_text}</h4>
        <p style="margin: 0.5rem 0; font-size: 1.1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">
            Weekly: ${abs(weekly_savings):,.2f} | Monthly: ${abs(monthly_savings):,.2f} | Yearly: ${abs(yearly_savings):,.2f}
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<br><br>', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: var(--cool-gray-8c); font-size: 0.9rem; padding: 1rem;">
    EBOSS® Model Selection Tool | Powered by Advanced Energy Solutions
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
