
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
    box-sizing: border-box;
    max-width: 100%;
}
</style>

import streamlit as st

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

import pandas as pd
import numpy as np

# Initialize session state variables
if 'show_cost_analysis' not in st.session_state:
    st.session_state.show_cost_analysis = False
if 'show_cost_dialog' not in st.session_state:
    st.session_state.show_cost_dialog = False
if 'cost_standard_generator' not in st.session_state:
    st.session_state.cost_standard_generator = None
if 'pm_charge_enabled' not in st.session_state:
    st.session_state.pm_charge_enabled = False

# Page configuration
st.set_page_config(
    page_title="EBOSS® Model Selection Tool",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with the specified color palette
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for color palette */
    :root {
        --black-asphalt: #000000;
        --cool-gray-8c: #939598;
        --cool-gray-10c: #636569;
        --charcoal: #636569;
        --alpine-white: #FFFFFF;
        --energy-green: #81BD47;
    }
    
    /* Hide Streamlit branding and white bar completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {
        background-color: transparent;
        height: 0px;
    }
    .stApp {
        margin-top: -90px;
        padding-top: 0;
    }
    /* Force hide any remaining header elements */
    [data-testid="stHeader"] {
        display: none;
    }
    .stAppHeader {
        display: none;
    }
    /* Remove top padding from main block */
    .block-container {
        padding-top: 0rem;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, var(--black-asphalt) 0%, var(--charcoal) 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main-container {
        background: var(--alpine-white);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border: 1px solid var(--cool-gray-8c);
    }
    
    /* Title styling */
    .main-title {
        color: var(--black-asphalt);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .subtitle {
        color: var(--cool-gray-10c);
        font-size: 1.2rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Form container styling */
    .form-container {
        background: var(--charcoal);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .form-section-title {
        color: var(--alpine-white);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background-color: var(--cool-gray-10c) !important;
        border: 2px solid var(--energy-green) !important;
        border-radius: 8px !important;
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        font-weight: 500 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--energy-green);
        box-shadow: 0 8px 16px rgba(129, 189, 71, 0.5), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        transform: translateY(-1px);
    }
    
    .stSelectbox > div > div > div {
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stNumberInput > div > div {
        background-color: var(--cool-gray-10c) !important;
        border: 2px solid var(--energy-green) !important;
        border-radius: 8px !important;
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        font-weight: 500 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .stNumberInput > div > div:hover {
        border-color: var(--energy-green);
        box-shadow: 0 8px 16px rgba(129, 189, 71, 0.5), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        transform: translateY(-1px);
    }
    
    .stNumberInput input {
        background-color: transparent !important;
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
        border: none !important;
    }
    
    /* Enhanced Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--energy-green) 0%, #6ba534 100%);
        color: var(--alpine-white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-family: Arial, sans-serif;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 6px 12px rgba(129, 189, 71, 0.4), inset 0 1px 2px rgba(255,255,255,0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6ba534 0%, var(--energy-green) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(129, 189, 71, 0.6), inset 0 1px 2px rgba(255,255,255,0.3);
    }
    
    /* Enhanced Checkbox styling */
    .stCheckbox > label {
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stCheckbox > label > div {
        background-color: var(--cool-gray-10c) !important;
        border: 2px solid var(--energy-green) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3), inset 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Labels */
    .stSelectbox > label,
    .stNumberInput > label {
        color: var(--alpine-white) !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    /* Dialog/Modal styling */
    .stDialog {
        background-color: var(--charcoal) !important;
    }
    
    .stDialog h1, .stDialog h2, .stDialog h3, .stDialog h4, .stDialog h5, .stDialog h6 {
        color: var(--alpine-white) !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
    }
    
    .stDialog p, .stDialog div, .stDialog span, .stDialog label {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stDialog .stMarkdown {
        color: var(--alpine-white) !important;
    }
    
    .stDialog .stMarkdown h1, .stDialog .stMarkdown h2, .stDialog .stMarkdown h3, 
    .stDialog .stMarkdown h4, .stDialog .stMarkdown h5, .stDialog .stMarkdown h6 {
        color: var(--alpine-white) !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
    }
    
    .stDialog .stMarkdown p, .stDialog .stMarkdown div, .stDialog .stMarkdown span {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stDialog .stRadio > label {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stDialog .stRadio > div > label {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, var(--energy-green) 0%, #6ba534 100%);
        color: var(--alpine-white);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(129, 189, 71, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: var(--alpine-white);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 0;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .main-title {
            font-size: 1.8rem;
            margin-top: 0.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .form-container {
            padding: 1rem;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.5rem 0;
        }
        
        /* Mobile logo adjustments */
        .logo-container img {
            max-width: 150px !important;
            width: auto !important;
        }
    }
    
    /* Desktop optimization */
    @media (min-width: 1200px) {
        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
        }
    }
</style>
""", unsafe_allow_html=True)

# EBOSS® Load Calculation Reference Data
EBOSS_LOAD_REFERENCE = {
    "battery_capacities": {
        "EB25 kVA": 15,
        "EB70 kVA": 25,
        "EB125 kVA": 50,
        "EB220 kVA": 75,
        "EB400 kVA": 125
    },
    "generator_kva_hybrid": {
        "EB25 kVA": 25,
        "EB70 kVA": 45,
        "EB125 kVA": 65,
        "EB220 kVA": 125,
        "EB400 kVA": 220
    },
    "generator_sizes": {
        25: {"eboss_model": "EB25 kVA", "pm_charge_rate": 18.5, "fh_charge_rate": 19.5, "max_charge_rate": 20, "kwh": 15, "gen_kw": 20},
        45: {"eboss_model": "EB70 kVA", "pm_charge_rate": 33, "fh_charge_rate": 36, "max_charge_rate": 45, "kwh": 25, "gen_kw": 36},
        65: {"eboss_model": "EB125 kVA", "pm_charge_rate": 48, "fh_charge_rate": 52, "max_charge_rate": 65, "kwh": 50, "gen_kw": 52},
        125: {"eboss_model": "EB220 kVA", "pm_charge_rate": 96, "fh_charge_rate": 100, "max_charge_rate": 125, "kwh": 75, "gen_kw": 100},
        220: {"eboss_model": "EB400 kVA", "pm_charge_rate": 166, "fh_charge_rate": 176, "max_charge_rate": 220, "kwh": 125, "gen_kw": 176}
    },
    "gph_interpolation": {
        25: {"25%": 0.67, "50%": 0.94, "75%": 1.26, "100%": 1.62},
        45: {"25%": 1.04, "50%": 1.60, "75%": 2.20, "100%": 2.03},
        70: {"25%": 1.70, "50%": 2.60, "75%": 3.50, "100%": 4.40},
        125: {"25%": 2.60, "50%": 4.10, "75%": 5.60, "100%": 7.10},
        220: {"25%": 4.60, "50%": 6.90, "75%": 9.40, "100%": 12.00},
        400: {"25%": 7.70, "50%": 12.20, "75%": 17.30, "100%": 22.50}
    }
}

# Standard Diesel Generator Reference Data (based on authentic industry specifications)
STANDARD_GENERATOR_DATA = {
    "25 kVA / 20 kW": {
        "kva": 25, "kw": 20,
        "fuel_consumption_gph": {"50%": 0.90, "75%": 1.30, "100%": 1.60},
        "noise_level_db": 68, "dimensions": "L:48\" W:24\" H:30\"", "weight_lbs": 650,
        "fuel_tank_gal": 12, "runtime_at_50_load": 13.3, "co2_per_gal": 22.4
    },
    "45 kVA / 36 kW": {
        "kva": 45, "kw": 36,
        "fuel_consumption_gph": {"50%": 2.30, "75%": 3.20, "100%": 4.00},
        "noise_level_db": 72, "dimensions": "L:60\" W:28\" H:36\"", "weight_lbs": 1200,
        "fuel_tank_gal": 25, "runtime_at_50_load": 10.9, "co2_per_gal": 22.4
    },
    "65 kVA / 52 kW": {
        "kva": 65, "kw": 52,
        "fuel_consumption_gph": {"50%": 2.90, "75%": 3.80, "100%": 4.80},
        "noise_level_db": 75, "dimensions": "L:72\" W:32\" H:42\"", "weight_lbs": 1800,
        "fuel_tank_gal": 40, "runtime_at_50_load": 13.8, "co2_per_gal": 22.4
    },
    "125 kVA / 100 kW": {
        "kva": 125, "kw": 100,
        "fuel_consumption_gph": {"50%": 5.00, "75%": 7.10, "100%": 9.10},
        "noise_level_db": 78, "dimensions": "L:96\" W:36\" H:48\"", "weight_lbs": 3200,
        "fuel_tank_gal": 75, "runtime_at_50_load": 15.0, "co2_per_gal": 22.4
    },
    "220 kVA / 176 kW": {
        "kva": 220, "kw": 176,
        "fuel_consumption_gph": {"50%": 8.80, "75%": 12.50, "100%": 16.60},
        "noise_level_db": 82, "dimensions": "L:120\" W:48\" H:60\"", "weight_lbs": 5500,
        "fuel_tank_gal": 125, "runtime_at_50_load": 14.2, "co2_per_gal": 22.4
    },
    "400 kVA / 320 kW": {
        "kva": 400, "kw": 320,
        "fuel_consumption_gph": {"50%": 14.90, "75%": 21.30, "100%": 28.60},
        "noise_level_db": 85, "dimensions": "L:144\" W:60\" H:72\"", "weight_lbs": 8800,
        "fuel_tank_gal": 200, "runtime_at_50_load": 13.4, "co2_per_gal": 22.4
    }
}

# Standard Generator Data for Comparison
STANDARD_GENERATOR_DATA = {
    "25 kVA / 20 kW": {
        "kw": 20,
        "fuel_consumption_gph": {"50%": 1.2, "75%": 1.7, "100%": 2.3},
        "fuel_tank_gal": 38,
        "co2_per_gal": 22.4,
        "noise_level_db": 75,
        "dimensions": "60\" x 24\" x 36\"",
        "weight_lbs": 1850
    },
    "45 kVA / 36 kW": {
        "kw": 36,
        "fuel_consumption_gph": {"50%": 2.1, "75%": 3.0, "100%": 4.1},
        "fuel_tank_gal": 60,
        "co2_per_gal": 22.4,
        "noise_level_db": 78,
        "dimensions": "72\" x 30\" x 42\"",
        "weight_lbs": 2850
    },
    "65 kVA / 52 kW": {
        "kw": 52,
        "fuel_consumption_gph": {"50%": 2.8, "75%": 4.2, "100%": 5.8},
        "fuel_tank_gal": 80,
        "co2_per_gal": 22.4,
        "noise_level_db": 80,
        "dimensions": "84\" x 36\" x 48\"",
        "weight_lbs": 4200
    },
    "125 kVA / 100 kW": {
        "kw": 100,
        "fuel_consumption_gph": {"50%": 5.2, "75%": 7.8, "100%": 10.5},
        "fuel_tank_gal": 120,
        "co2_per_gal": 22.4,
        "noise_level_db": 82,
        "dimensions": "120\" x 48\" x 60\"",
        "weight_lbs": 8500
    },
    "220 kVA / 176 kW": {
        "kw": 176,
        "fuel_consumption_gph": {"50%": 9.1, "75%": 13.7, "100%": 18.2},
        "fuel_tank_gal": 200,
        "co2_per_gal": 22.4,
        "noise_level_db": 85,
        "dimensions": "144\" x 60\" x 72\"",
        "weight_lbs": 15000
    },
    "400 kVA / 320 kW": {
        "kw": 320,
        "fuel_consumption_gph": {"50%": 16.8, "75%": 25.2, "100%": 33.6},
        "fuel_tank_gal": 350,
        "co2_per_gal": 22.4,
        "noise_level_db": 88,
        "dimensions": "180\" x 72\" x 84\"",
        "weight_lbs": 28000
    }
}

def interpolate_gph(generator_kva, load_percent):
    """
    Interpolate GPH fuel consumption based on generator kVA and load percentage
    Uses authentic EBOSS® GPH interpolation data from working_Accurate_Fuel_Calc_1752711064907.xlsx
    """
    # Convert load percent to decimal if needed
    if load_percent > 1:
        load_percent = load_percent / 100
    
    # Get GPH interpolation data
    gph_data_map = EBOSS_LOAD_REFERENCE["gph_interpolation"]
    
    # Find the correct generator size data or closest match
    if generator_kva not in gph_data_map:
        # Find closest generator size
        available_sizes = list(gph_data_map.keys())
        closest_size = min(available_sizes, key=lambda x: abs(x - generator_kva))
        gph_data = gph_data_map[closest_size]
    else:
        gph_data = gph_data_map[generator_kva]
    
    # Define load percentage breakpoints and corresponding GPH values
    load_points = [0.25, 0.50, 0.75, 1.00]
    gph_values = [gph_data["25%"], gph_data["50%"], gph_data["75%"], gph_data["100%"]]
    
    # Clamp load_percent to valid range
    load_percent = max(0.25, min(1.00, load_percent))
    
    # Handle edge cases
    if load_percent <= 0.25:
        return gph_values[0]
    elif load_percent >= 1.00:
        return gph_values[3]
    
    # Find the two points to interpolate between
    for i in range(len(load_points) - 1):
        if load_points[i] <= load_percent <= load_points[i + 1]:
            # Linear interpolation formula: y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
            x1, x2 = load_points[i], load_points[i + 1]
            y1, y2 = gph_values[i], gph_values[i + 1]
            
            interpolated_gph = y1 + (load_percent - x1) * (y2 - y1) / (x2 - x1)
            return round(interpolated_gph, 4)
    
    return 0

def calculate_charge_rate(eboss_model, eboss_type, generator_kva=None, custom_rate=None):
    """Calculate charge rate using authentic formulas"""
    if custom_rate:
        return custom_rate
        
    # Get generator kW capacity
    generator_kw = 0
    if eboss_type == "Full Hybrid":
        # Use paired generator for hybrid
        hybrid_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = hybrid_kva * 0.8  # kW = kVA * 0.8
    elif eboss_type == "Power Module" and generator_kva:
        # Use selected generator for power module
        gen_kva = float(generator_kva.replace("kVA", ""))
        generator_kw = gen_kva * 0.8  # kW = kVA * 0.8
    
    # Calculate charge rate based on formulas
    if eboss_type == "Full Hybrid":
        # Full Hybrid: 98% of generator kW
        charge_rate = generator_kw * 0.98
    elif eboss_type == "Power Module":
        # Power Module: 98% of (90% of generator kW)
        charge_rate = generator_kw * 0.90 * 0.98
    else:
        charge_rate = 0
        
    return round(charge_rate, 1)

def get_max_charge_rate(eboss_model, eboss_type, generator_kva=None):
    """Get maximum allowed charge rate using model-specific limits, with 98% generator kW as fallback"""
    
    # EBOSS® model specific maximum charge rates from the table
    model_max_charge_rates = {
        "EB25 kVA": 20,
        "EB70 kVA": 45,
        "EB125 kVA": 65,
        "EB220 kVA": 125,
        "EB400 kVA": 220
    }
    
    # Get model-specific max charge rate
    model_max = model_max_charge_rates.get(eboss_model, 0)
    
    # Calculate 98% of generator kW as secondary limit
    generator_kw = 0
    if eboss_type == "Full Hybrid":
        hybrid_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = hybrid_kva * 0.8
    elif eboss_type == "Power Module" and generator_kva:
        gen_kva = float(generator_kva.replace("kVA", ""))
        generator_kw = gen_kva * 0.8
    
    generator_98_percent = generator_kw * 0.98
    
    # Use the lower of the two limits (model max or 98% generator kW)
    if model_max > 0 and generator_98_percent > 0:
        max_charge_rate = min(model_max, generator_98_percent)
    elif model_max > 0:
        max_charge_rate = model_max
    elif generator_98_percent > 0:
        max_charge_rate = generator_98_percent
    else:
        max_charge_rate = 0
    
    return round(max_charge_rate, 1)

def calculate_standard_generator_specs(standard_generator_size, continuous_load, max_peak_load):
    """Calculate specifications for standard diesel generator comparison using authentic interpolation"""
    if not standard_generator_size or standard_generator_size not in STANDARD_GENERATOR_DATA:
        return {}
    
    gen_data = STANDARD_GENERATOR_DATA[standard_generator_size]
    gen_kw = gen_data["kw"]
    
    # Calculate engine load percentage based on continuous load (since it runs 24/7)
    engine_load_percent = (continuous_load / gen_kw * 100) if gen_kw > 0 else 0
    load_percentage = continuous_load / gen_kw if gen_kw > 0 else 0
    
    # Use same interpolation method as EBOSS® for consistency
    fuel_gph_data = gen_data["fuel_consumption_gph"]
    if load_percentage <= 0.5:
        fuel_per_hour = fuel_gph_data["50%"]
    elif load_percentage <= 0.75:
        fuel_per_hour = fuel_gph_data["75%"]
    else:
        fuel_per_hour = fuel_gph_data["100%"]
    
    # Calculate daily, weekly, monthly consumption (runs 24/7)
    fuel_per_day = fuel_per_hour * 24
    fuel_per_week = fuel_per_day * 7
    fuel_per_month = fuel_per_day * 30
    
    # Calculate CO2 emissions (22.4 lbs CO2 per gallon of diesel)
    co2_per_day = fuel_per_day * gen_data["co2_per_gal"]
    
    # Runtime is continuous (24 hours) since no battery backup
    runtime_per_day = 24.0
    
    # Tank runtime calculation
    tank_runtime = gen_data["fuel_tank_gal"] / fuel_per_hour if fuel_per_hour > 0 else 0
    
    return {
        "generator_type": "Standard Diesel Generator",
        "generator_size": standard_generator_size,
        "engine_load_percent": engine_load_percent,
        "continuous_load_percent": load_percentage * 100,
        "fuel_consumption_gph": fuel_per_hour,
        "fuel_per_hour": fuel_per_hour,
        "fuel_per_day": fuel_per_day,
        "fuel_per_week": fuel_per_week,
        "fuel_per_month": fuel_per_month,
        "co2_per_day": co2_per_day,
        "runtime_per_day": runtime_per_day,
        "tank_runtime_hours": tank_runtime,
        "noise_level": gen_data["noise_level_db"],
        "dimensions": gen_data["dimensions"],
        "weight_lbs": gen_data["weight_lbs"],
        "fuel_tank_capacity": gen_data["fuel_tank_gal"]
    }

def calculate_load_specs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva=None, custom_charge_rate=None):
    """Calculate load-based specifications using authentic EBOSS® reference data"""
    
    # Get EBOSS® model capacity based on generator size and max continuous load
    generator_kw_mapping = {
        "EB25 kVA": 14.5,   # Gen Size 25 kVA
        "EB70 kVA": 24.5,   # Gen Size 45 kVA  
        "EB125 kVA": 49,    # Gen Size 65 kVA
        "EB220 kVA": 74,    # Gen Size 125 kVA
        "EB400 kVA": 125    # Gen Size 220 kVA
    }
    model_capacity = generator_kw_mapping.get(eboss_model, 0)
    
    # Find matching generator data
    generator_data = None
    if generator_kva:
        gen_size = int(generator_kva.replace("kVA", ""))
        generator_data = EBOSS_LOAD_REFERENCE["generator_sizes"].get(gen_size)
    
    # Calculate utilization
    peak_utilization = (max_peak_load / model_capacity * 100) if model_capacity > 0 else 0
    continuous_utilization = (continuous_load / model_capacity * 100) if model_capacity > 0 else 0
    
    # Calculate charge rate using new formula
    charge_rate = calculate_charge_rate(eboss_model, eboss_type, generator_kva, custom_charge_rate)
    
    # Calculate fuel consumption and engine load based on EBOSS® model's paired generator
    fuel_consumption = None
    engine_load_percent = 0
    
    # Get the appropriate generator size for this EBOSS® model
    paired_generator_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
    if paired_generator_kva > 0:
        # Get paired generator data
        paired_gen_data = EBOSS_LOAD_REFERENCE["generator_sizes"].get(paired_generator_kva)
        if paired_gen_data:
            gen_kw = paired_gen_data["gen_kw"]
            charge_rate_kw = charge_rate  # charge rate is already in kW
            engine_load_percent = (charge_rate_kw / gen_kw * 100) if gen_kw > 0 else 0
            
            # Use charge rate for GPH interpolation
            load_percentage = charge_rate_kw / gen_kw if gen_kw > 0 else 0
            
            # Interpolate GPH based on paired generator size and load percentage
            gph_data = EBOSS_LOAD_REFERENCE["gph_interpolation"].get(paired_generator_kva, {})
            
            if load_percentage <= 0.25:
                fuel_consumption = gph_data.get("25%", 0)
            elif load_percentage <= 0.5:
                fuel_consumption = gph_data.get("50%", 0)
            elif load_percentage <= 0.75:
                fuel_consumption = gph_data.get("75%", 0)
            else:
                fuel_consumption = gph_data.get("100%", 0)
    
    # Calculate battery specs - always use model-specific capacity
    battery_capacity = EBOSS_LOAD_REFERENCE["battery_capacities"].get(eboss_model, 0)
    charge_time = (battery_capacity / charge_rate) if charge_rate > 0 else 0
    
    # Calculate environmental impact
    co2_per_day = fuel_consumption * 24 * 19.6 if fuel_consumption else 0  # 19.6 lbs CO2 per gallon
    
    return {
        "model_capacity": model_capacity,
        "peak_utilization": peak_utilization,
        "continuous_utilization": continuous_utilization,
        "charge_rate": charge_rate,
        "battery_capacity": battery_capacity,
        "charge_time": charge_time,
        "fuel_consumption_gph": fuel_consumption,
        "fuel_per_day": fuel_consumption * 24 if fuel_consumption else 0,
        "co2_per_day": co2_per_day,
        "engine_load_percent": engine_load_percent,
        "generator_data": generator_data
    }

# EBOSS® Specifications Data
EBOSS_SPECS = {
    "EB25 kVA": {
        "Hybrid Energy System": "ANA EBOSS",
        "Three-phase Max Power": "30 kVA / 24 kW",
        "Single-phase Max Power": "20 kVA / 16 kW",
        "Frequency": "60 Hz",
        "Simultaneous voltage": "120/240 (1Φ) • 208/480 (3Φ)",
        "Voltage regulation": "Adjustable",
        "Max Intermittent amp-load 208V": "70 A / 13.5 kW",
        "Max Continuous amp-load 208V": "55 A / 10.5 kW",
        "Max Intermittent amp-load 240V": "61 A / 13.5 kW",
        "Max Continuous amp-load 240V": "48 A / 10.5 kW",
        "Max Intermittent amp-load 480V": "35 A / 28 kW",
        "Max Continuous amp-load 480V": "28 A / 22 kW",
        "Battery Type": "Lithium Titanate Oxide (Li4Ti5O12)",
        "Battery Capacity": "15 kWh",
        "Generator kVA": "25 kVA (Hybrid units only)",
        "Battery Voltage": "440 VDC",
        "Inverter Type": "Pure Sine Wave",
        "Operating Temperature": "-4°F to 113°F (-20°C to 45°C)",
        "Dimensions (L x W x H)": "108\" x 45\" x 62\"",
        "Weight": "8,200 lbs",
        "Warranty - EBOSS® only": "2 Years",
        "Warranty - With trailer & generator": "2 Years, 2000 Hours",
        "Battery warranty": "7 Years",
        "Service & Support": "24/7, 365 Days",
        "Training": "Henderson, NV or On Location"
    },
    "EB70 kVA": {
        "Hybrid Energy System": "ANA EBOSS",
        "Three-phase Max Power": "70 kVA / 56 kW",
        "Single-phase Max Power": "47 kVA / 37 kW",
        "Frequency": "60 Hz",
        "Simultaneous voltage": "120/240 (1Φ) • 208/480 (3Φ)",
        "Voltage regulation": "Adjustable",
        "Max Intermittent amp-load 208V": "194 A / 37.2 kW",
        "Max Continuous amp-load 208V": "155 A / 29.8 kW",
        "Max Intermittent amp-load 240V": "169 A / 37.2 kW",
        "Max Continuous amp-load 240V": "135 A / 29.8 kW",
        "Max Intermittent amp-load 480V": "84 A / 70 kW",
        "Max Continuous amp-load 480V": "67 A / 56 kW",
        "Battery Type": "Lithium Titanate Oxide (Li4Ti5O12)",
        "Battery Capacity": "25 kWh",
        "Generator kVA": "45 kVA (Hybrid units only)",
        "Battery Voltage": "440 VDC",
        "Inverter Type": "Pure Sine Wave",
        "Operating Temperature": "-4°F to 113°F (-20°C to 45°C)",
        "Dimensions (L x W x H)": "108\" x 60\" x 62\"",
        "Weight": "13,200 lbs",
        "Warranty - EBOSS® only": "2 Years",
        "Warranty - With trailer & generator": "2 Years, 2000 Hours",
        "Battery warranty": "7 Years",
        "Service & Support": "24/7, 365 Days",
        "Training": "Henderson, NV or On Location"
    },
    "EB125 kVA": {
        "Hybrid Energy System": "ANA EBOSS",
        "Three-phase Max Power": "125 kVA / 100 kW",
        "Single-phase Max Power": "N/A / N/A",
        "Frequency": "60 Hz",
        "Simultaneous voltage": "120V (1Φ) • 208/480 (3Φ)",
        "Voltage regulation": "Adjustable",
        "Max Intermittent amp-load 208V": "345 A / 66.2 kW",
        "Max Continuous amp-load 208V": "276 A / 53 kW",
        "Max Intermittent amp-load 240V": "301 A / 66.2 kW",
        "Max Continuous amp-load 240V": "241 A / 53 kW",
        "Max Intermittent amp-load 480V": "150 A / 125 kW",
        "Max Continuous amp-load 480V": "120 A / 100 kW",
        "Battery Type": "Lithium Titanate Oxide (Li4Ti5O12)",
        "Battery Capacity": "50 kWh",
        "Generator kVA": "65 kVA (Hybrid units only)",
        "Battery Voltage": "440 VDC",
        "Inverter Type": "Pure Sine Wave",
        "Operating Temperature": "-4°F to 113°F (-20°C to 45°C)",
        "Dimensions (L x W x H)": "144\" x 60\" x 62\"",
        "Weight": "18,200 lbs",
        "Warranty - EBOSS® only": "2 Years",
        "Warranty - With trailer & generator": "2 Years, 2000 Hours",
        "Battery warranty": "7 Years",
        "Service & Support": "24/7, 365 Days",
        "Training": "Henderson, NV or On Location"
    },
    "EB220 kVA": {
        "Hybrid Energy System": "ANA EBOSS",
        "Three-phase Max Power": "220 kVA / 176 kW",
        "Single-phase Max Power": "N/A / N/A",
        "Frequency": "60 Hz",
        "Simultaneous voltage": "120V (1Φ) • 208/480 (3Φ)",
        "Voltage regulation": "Adjustable",
        "Max Intermittent amp-load 208V": "700 A / 134 kW",
        "Max Continuous amp-load 208V": "560 A / 108 kW",
        "Max Intermittent amp-load 240V": "611 A / 134 kW",
        "Max Continuous amp-load 240V": "489 A / 108 kW",
        "Max Intermittent amp-load 480V": "264 A / 220 kW",
        "Max Continuous amp-load 480V": "211 A / 176 kW",
        "Battery Type": "Lithium Titanate Oxide (Li4Ti5O12)",
        "Battery Capacity": "75 kWh",
        "Generator kVA": "125 kVA (Hybrid units only)",
        "Battery Voltage": "440 VDC",
        "Inverter Type": "Pure Sine Wave",
        "Operating Temperature": "-4°F to 113°F (-20°C to 45°C)",
        "Dimensions (L x W x H)": "192\" x 60\" x 62\"",
        "Weight": "29,200 lbs",
        "Warranty - EBOSS® only": "2 Years",
        "Warranty - With trailer & generator": "2 Years, 2000 Hours",
        "Battery warranty": "7 Years",
        "Service & Support": "24/7, 365 Days",
        "Training": "Henderson, NV or On Location"
    },
    "EB400 kVA": {
        "Hybrid Energy System": "ANA EBOSS™",
        "Three-phase Max Power": "400 kVA / 320 kW",
        "Single-phase Max Power": "N/A",
        "Frequency": "60 Hz",
        "Simultaneous voltage": "120V (Courtesy Outlets) • 480 (3Φ)",
        "Voltage regulation": "Adjustable",
        "Max Intermittent amp-load 208V": "481 A / 92.5 kW",
        "Max Continuous amp-load 208V": "385 A / 74 kW",
        "Max Intermittent amp-load 240V": "419 A / 92.5 kW",
        "Max Continuous amp-load 240V": "335 A / 74 kW",
        "Max Intermittent amp-load 480V": "481 A / 400 kW",
        "Max Continuous amp-load 480V": "385 A / 320 kW",
        "Battery Type": "Lithium Titanate Oxide (Li4Ti5O12)",
        "Battery Capacity": "125 kWh",
        "Generator kVA": "220 kVA (Hybrid units only)",
        "Battery Voltage": "440 VDC",
        "Inverter Type": "Pure Sine Wave",
        "Operating Temperature": "-4°F to 113°F (-20°C to 45°C)",
        "Dimensions (L x W x H)": "240\" x 60\" x 62\"",
        "Weight": "38,200 lbs",
        "Warranty": "2 Years",
        "Warranty - With generator": "2 Years, 2000 Hours",
        "Battery warranty": "7 Years",
        "Service & Support": "24/7, 365 Days",
        "Training": "Henderson, NV or On Location"
    }
}

# Initialize session state
if 'eboss_model' not in st.session_state:
    st.session_state.eboss_model = None
if 'eboss_type' not in st.session_state:
    st.session_state.eboss_type = None
if 'generator_kva' not in st.session_state:
    st.session_state.generator_kva = None
if 'continuous_load' not in st.session_state:
    st.session_state.continuous_load = None
if 'max_peak_load' not in st.session_state:
    st.session_state.max_peak_load = None
if 'show_specs' not in st.session_state:
    st.session_state.show_specs = False
if 'show_load_specs' not in st.session_state:
    st.session_state.show_load_specs = False
if 'show_comparison' not in st.session_state:
    st.session_state.show_comparison = False
if 'standard_generator' not in st.session_state:
    st.session_state.standard_generator = None
if 'custom_charge_rate' not in st.session_state:
    st.session_state.custom_charge_rate = None
if 'use_custom_charge' not in st.session_state:
    st.session_state.use_custom_charge = False
if 'show_generator_dialog' not in st.session_state:
    st.session_state.show_generator_dialog = False
if 'paired_generator' not in st.session_state:
    st.session_state.paired_generator = None

# EBOSS® to Standard Generator Pairing (ascending order: 25, 65, 125, 220, 400 kVA)
EBOSS_STANDARD_PAIRING = {
    "EB25 kVA": "25 kVA / 20 kW",
    "EB70 kVA": "65 kVA / 52 kW", 
    "EB125 kVA": "125 kVA / 100 kW",
    "EB220 kVA": "220 kVA / 176 kW",
    "EB400 kVA": "400 kVA / 320 kW"
}

def generator_selection_dialog():
    """Dialog to confirm or change paired generator selection"""
    paired_gen = EBOSS_STANDARD_PAIRING.get(st.session_state.eboss_model, "25 kVA / 20 kW")
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">🔄 Generator Selection</h3>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
    For the <strong>{st.session_state.eboss_model}</strong> model, the recommended standard generator comparison is:<br>
    <strong>{paired_gen}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("✅ Use Recommended Generator", key="use_paired_gen"):
            st.session_state.standard_generator = paired_gen
            st.session_state.show_generator_dialog = False
            st.session_state.show_comparison = True
            st.rerun()
    
    with col2:
        if st.button("🔧 Select Different Generator", key="select_different_gen"):
            st.session_state.standard_generator = None
            st.session_state.show_generator_dialog = False
            st.session_state.show_comparison = True
            st.rerun()
    
    if st.button("❌ Cancel", key="cancel_dialog"):
        st.session_state.show_generator_dialog = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

@st.dialog("
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
 Setup")
def cost_analysis_dialog():
    """Modal dialog for cost analysis with generator selection and input fields"""
    paired_gen = EBOSS_STANDARD_PAIRING.get(st.session_state.eboss_model, "25 kVA / 20 kW")
    
    # Generator selection section
    st.markdown(f"""
    <div style="background: rgba(129, 189, 71, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #81BD47; margin-bottom: 1rem;">
    <strong>Recommended Generator:</strong><br>
    For the <strong>{st.session_state.eboss_model}</strong> model: <strong>{paired_gen}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    gen_col1, gen_col2 = st.columns([1, 1])
    
    with gen_col1:
        if st.button("✅ Use Recommended", key="use_paired_gen_cost", use_container_width=True):
            st.session_state.cost_standard_generator = paired_gen
            st.rerun()
    
    with gen_col2:
        if st.button("🔧 Select Different", key="select_different_gen_cost", use_container_width=True):
            # Show dropdown for different generator selection
            available_generators = list(STANDARD_GENERATOR_DATA.keys())
            st.session_state.cost_standard_generator = st.selectbox(
                "Choose Standard Generator:",
                options=available_generators,
                index=available_generators.index(paired_gen) if paired_gen in available_generators else 0,
                key="cost_generator_select"
            )
    
    # If a generator is selected, show the cost analysis form
    if st.session_state.cost_standard_generator:
        st.divider()
        st.subheader("
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
 Parameters")
        
        # Row 1: Fuel price and delivery fee
        st.markdown("**Fuel Information**")
        fuel_col1, fuel_col2 = st.columns([1, 1])
        
        with fuel_col1:
            local_fuel_price = st.number_input(
                "Local Fuel Price / Gal ($)",
               min_value=1,
                max_value=1000,
                value=0,
                step=1,
                key="local_fuel_price"
            )
        
        with fuel_col2:
            fuel_delivery_fee = st.number_input(
                "Fuel Delivery Fee ($)",
                min_value=1,
                max_value=1000,
                value=0,
                step=1,
                key="fuel_delivery_fee"
            )
        
        # Row 2: PM interval and PM charge
        st.markdown("**Maintenance Information**")
        pm_col1, pm_col2 = st.columns([1, 1])
        
        with pm_col1:
            pm_interval_hrs = st.number_input(
                "PM Interval Hrs",
                min_value=1,
                max_value=10000,
                value=500,
                step=1,
                key="pm_interval_hrs"
            )
        
        with pm_col2:
            pm_charge_selection = st.radio(
                "Is there a PM Charge?",
                options=["No", "Yes"],
                index=0,
                key="pm_charge_radio",
                horizontal=True
            )
            
            if pm_charge_selection == "Yes":
                cost_per_pm = st.number_input(
                    "Cost per PM ($)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=0.0,
                    step=0.1,
                    format="%.2f",
                    key="cost_per_pm"
                )
        
        # Row 3: Weekly and Monthly rates for both systems
        st.markdown("**System Rates**")
        rate_col1, rate_col2 = st.columns([1, 1])
        
        with rate_col1:
            st.markdown("**EBOSS® Hybrid System**")
            eboss_weekly_rate = st.number_input(
                "Weekly Rate ($)",
                min_value=1,
                max_value=1000,
                value=0,
                step=1,
                key="eboss_weekly_rate"
            )
            eboss_monthly_rate = st.number_input(
                "Monthly Rate ($)",
                min_value=1,
                max_value=1000,
                value=0,
                step=1,
                key="eboss_monthly_rate"
            )
        
        with rate_col2:
            st.markdown("**Standard Generator**")
            standard_weekly_rate = st.number_input(
                "Weekly Rate ($)",
                min_value=1,
                max_value=1000,
                value=0,
                step=1,
                key="standard_weekly_rate"
            )
            standard_monthly_rate = st.number_input(
                "Monthly Rate ($)",
                min_value=0.0,
                max_value=200000.0,
                value=0.0,
                step=0.1,
                format="%.2f",
                key="standard_monthly_rate"
            )
        
        # Action buttons
        st.divider()
        action_col1, action_col2, action_col3 = st.columns([1, 1, 1])
        
        with action_col1:
            if st.button("📊 Generate Analysis", key="generate_cost_analysis", use_container_width=True):
                st.session_state.show_cost_dialog = False
                st.session_state.show_cost_analysis = True
                st.rerun()
        
        with action_col2:
            if st.button("🔄 Reset Form", key="reset_cost_form", use_container_width=True):
                # Reset all form values
                for key in ['local_fuel_price', 'fuel_delivery_fee', 'pm_interval_hrs', 'cost_per_pm', 
                           'eboss_weekly_rate', 'eboss_monthly_rate', 'standard_weekly_rate', 'standard_monthly_rate']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with action_col3:
            if st.button("❌ Cancel", key="cancel_cost_dialog", use_container_width=True):
                st.session_state.show_cost_dialog = False
                st.rerun()

def calculate_mathematical_difference(eboss_value, standard_value, spec_name):
    """Calculate mathematical difference between EBOSS® and standard values"""
    import re
    
    # Skip calculation for certain rows
    if spec_name in ["Generator Size", "Frequency", "Voltage regulation", "Simultaneous voltage", "Parallelable"]:
        if spec_name == "Simultaneous voltage":
            return "EBOSS® Advantage" if "Yes" in str(eboss_value) else "N/A"
        elif spec_name == "Parallelable":
            return "EBOSS® Advantage" if eboss_value == "Yes" and standard_value == "No" else "Same"
        elif spec_name == "Frequency":
            return "Same" if eboss_value == standard_value else "Different"
        elif spec_name == "Voltage regulation":
            return "Same" if eboss_value == standard_value else "Different"
        else:
            return "EBOSS® vs Standard"
    
    # Handle N/A values
    if str(eboss_value) == "N/A" or str(standard_value) == "N/A":
        if str(eboss_value) != "N/A" and str(standard_value) == "N/A":
            return "EBOSS® Only"
        return "N/A"
    
    try:
        # Extract kVA and kW values from strings like "30 kVA / 24 kW"
        if "kVA" in str(eboss_value) and "kW" in str(eboss_value):
            eboss_kva = float(re.search(r'(\d+(?:\.\d+)?)\s*kVA', str(eboss_value)).group(1))
            eboss_kw = float(re.search(r'(\d+(?:\.\d+)?)\s*kW', str(eboss_value)).group(1))
            
            if "kVA" in str(standard_value) and "kW" in str(standard_value):
                std_kva = float(re.search(r'(\d+(?:\.\d+)?)\s*kVA', str(standard_value)).group(1))
                std_kw = float(re.search(r'(\d+(?:\.\d+)?)\s*kW', str(standard_value)).group(1))
                
                kva_diff = eboss_kva - std_kva
                kw_diff = eboss_kw - std_kw
                
                kva_sign = "+" if kva_diff >= 0 else ""
                kw_sign = "+" if kw_diff >= 0 else ""
                
                return f"{kva_sign}{kva_diff:.1f} kVA / {kw_sign}{kw_diff:.1f} kW"
        
        # Extract single kW values
        elif "kW" in str(eboss_value) and "kW" in str(standard_value):
            eboss_kw = float(re.search(r'(\d+(?:\.\d+)?)\s*kW', str(eboss_value)).group(1))
            std_kw = float(re.search(r'(\d+(?:\.\d+)?)\s*kW', str(standard_value)).group(1))
            
            kw_diff = eboss_kw - std_kw
            kw_sign = "+" if kw_diff >= 0 else ""
            
            return f"{kw_sign}{kw_diff:.1f} kW"
        
        # Extract percentage values
        elif "%" in str(eboss_value) and "%" in str(standard_value):
            eboss_pct = float(re.search(r'(\d+(?:\.\d+)?)', str(eboss_value)).group(1))
            std_pct = float(re.search(r'(\d+(?:\.\d+)?)', str(standard_value)).group(1))
            
            pct_diff = eboss_pct - std_pct
            pct_sign = "+" if pct_diff >= 0 else ""
            
            return f"{pct_sign}{pct_diff:.1f}%"
        
        # Extract GPH values
        elif "GPH" in str(eboss_value) and "GPH" in str(standard_value):
            eboss_gph = float(re.search(r'(\d+(?:\.\d+)?)', str(eboss_value)).group(1))
            std_gph = float(re.search(r'(\d+(?:\.\d+)?)', str(standard_value)).group(1))
            
            gph_diff = eboss_gph - std_gph
            gph_sign = "+" if gph_diff >= 0 else ""
            
            return f"{gph_sign}{gph_diff:.2f} GPH"
        
        # Extract gallons values
        elif "gallons" in str(eboss_value) and "gallons" in str(standard_value):
            eboss_gal = float(re.search(r'(\d+(?:\.\d+)?)', str(eboss_value)).group(1))
            std_gal = float(re.search(r'(\d+(?:\.\d+)?)', str(standard_value)).group(1))
            
            gal_diff = eboss_gal - std_gal
            gal_sign = "+" if gal_diff >= 0 else ""
            
            return f"{gal_sign}{gal_diff:.1f} gallons"
        
        # Extract lbs values (emissions)
        elif "lbs" in str(eboss_value) and "lbs" in str(standard_value):
            eboss_lbs = float(re.search(r'(\d+(?:\.\d+)?)', str(eboss_value)).group(1))
            std_lbs = float(re.search(r'(\d+(?:\.\d+)?)', str(standard_value)).group(1))
            
            lbs_diff = eboss_lbs - std_lbs
            lbs_sign = "+" if lbs_diff >= 0 else ""
            
            return f"{lbs_sign}{lbs_diff:.1f} lbs"
        
        # Extract amp values
        elif "A" in str(eboss_value) and "A" in str(standard_value):
            eboss_amps = float(re.search(r'(\d+(?:\.\d+)?)', str(eboss_value)).group(1))
            std_amps = float(re.search(r'(\d+(?:\.\d+)?)', str(standard_value)).group(1))
            
            amp_diff = eboss_amps - std_amps
            amp_sign = "+" if amp_diff >= 0 else ""
            
            return f"{amp_sign}{amp_diff:.0f} A"
        
        elif "A" in str(eboss_value) and str(standard_value) == "N/A":
            return "EBOSS® Only"
            
    except (AttributeError, ValueError, TypeError):
        pass
    
    # Default cases
    if str(eboss_value) == str(standard_value):
        return "Same"
    
    return "Different"

def format_difference_value(difference, spec_name):
    """Format difference values with consistent font color matching other columns"""
    if difference == "N/A" or not difference or str(difference).strip() == "":
        return "N/A", "var(--alpine-white)"
    
    diff_str = str(difference).strip()
    
    # Return all values with consistent white font color
    return diff_str, "var(--alpine-white)"

def create_section_header(title):
    """Create a section header that spans all 4 columns"""
    return f"""
    <div style="background: linear-gradient(135deg, var(--energy-green) 0%, #2d5a3d 100%); 
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
            {title}
        </strong>
    </div>
    """

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with logo on separate line
st.markdown('<div class="logo-container" style="text-align: center; margin-bottom: 1rem;">', unsafe_allow_html=True)
st.image("ANA-ENERGY-LOGO-PADDED.png", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# Title in styled container
st.markdown('''
<div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 1.5rem; margin: 1rem 0 2rem 0; border-radius: 12px; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.4); text-shadow: 2px 2px 4px rgba(0,0,0,0.6);">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 600; letter-spacing: 1px;">EBOSS® Spec and Comparison Tool</h1>
</div>
''', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">System Configuration</h3>', unsafe_allow_html=True)
    
    # EBOSS® Model dropdown
    eboss_models = ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"]
    st.session_state.eboss_model = st.selectbox(
        "EBOSS® Model",
        options=eboss_models,
        index=0 if st.session_state.eboss_model is None else eboss_models.index(st.session_state.eboss_model),
        key="eboss_model_select"
    )
    
    # EBOSS® Type dropdown
    eboss_types = ["Full Hybrid", "Power Module"]
    st.session_state.eboss_type = st.selectbox(
        "EBOSS® Type",
        options=eboss_types,
        index=0 if st.session_state.eboss_type is None else eboss_types.index(st.session_state.eboss_type),
        key="eboss_type_select"
    )
    
    # Conditional Generator kVA dropdown
    if st.session_state.eboss_type == "Power Module":
        generator_options = ["25kVA", "45kVA", "65kVA", "125kVA", "220kVA", "400kVA"]
        st.session_state.generator_kva = st.selectbox(
            "Generator Size",
            options=generator_options,
            index=0 if st.session_state.generator_kva is None else generator_options.index(st.session_state.generator_kva),
            key="generator_kva_select"
        )
    else:
        st.session_state.generator_kva = None
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">Load Requirements</h3>', unsafe_allow_html=True)
    
    # Show text inputs based on conditions
    show_load_inputs = False
    if st.session_state.eboss_type == "Full Hybrid":
        show_load_inputs = True
    elif st.session_state.eboss_type == "Power Module" and st.session_state.generator_kva is not None:
        show_load_inputs = True
    
    if show_load_inputs:
        # Continuous Load input
        continuous_load = st.number_input(
            "Continuous Load (kW)",
            min_value=0,
            max_value=500,
            value=0 if st.session_state.continuous_load is None else int(st.session_state.continuous_load) if st.session_state.continuous_load == int(st.session_state.continuous_load) else st.session_state.continuous_load,
            step=1,
            key="continuous_load_input"
        )
        st.session_state.continuous_load = continuous_load
        
        # Max Peak Load input
        max_peak_load = st.number_input(
            "Max Peak Load (kW)",
            min_value=0,
            max_value=500,
            value=0 if st.session_state.max_peak_load is None else int(st.session_state.max_peak_load) if st.session_state.max_peak_load == int(st.session_state.max_peak_load) else st.session_state.max_peak_load,
            step=1,
            key="max_peak_load_input"
        )
        st.session_state.max_peak_load = max_peak_load
        
        # Input validation
        if continuous_load > max_peak_load and max_peak_load > 0:
            st.markdown('<div class="warning-box">⚠️ Warning: Continuous load cannot exceed max peak load</div>', unsafe_allow_html=True)
        elif continuous_load > 0 and max_peak_load > 0:
            st.markdown('<div class="info-box">✅ Load configuration is valid</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">ℹ️ Please complete the system configuration to enter load requirements</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Button section
st.markdown('<br>', unsafe_allow_html=True)
button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns([1, 1, 1, 1, 1])

with button_col1:
    if st.button("📋 Technical Specs", key="specs_button"):
        if st.session_state.eboss_model:
            st.session_state.show_specs = True
            st.session_state.show_load_specs = False
            st.session_state.show_cost_analysis = False
            st.rerun()
        else:
            st.markdown('<div class="warning-box">⚠️ Please select an EBOSS® model first</div>', unsafe_allow_html=True)

with button_col2:
    if st.button("⚡ Load Based Specs", key="load_specs_button"):
        if st.session_state.eboss_model and st.session_state.continuous_load and st.session_state.max_peak_load:
            st.session_state.show_load_specs = True
            st.session_state.show_specs = False
            st.session_state.show_cost_analysis = False
            st.rerun()
        else:
            st.markdown('<div class="warning-box">⚠️ Please complete configuration and enter load values first</div>', unsafe_allow_html=True)

with button_col3:
    if st.button("⚖️ Compare", key="compare_button"):
        if (st.session_state.eboss_model and st.session_state.eboss_type and 
            st.session_state.continuous_load and st.session_state.max_peak_load):
            st.session_state.show_generator_dialog = True
            st.session_state.show_specs = False
            st.session_state.show_load_specs = False
            st.session_state.show_comparison = False
            st.session_state.show_cost_analysis = False
            st.rerun()
        else:
            missing_items = []
            if not st.session_state.eboss_model: missing_items.append("EBOSS® model")
            if not st.session_state.eboss_type: missing_items.append("EBOSS® type")
            if not st.session_state.continuous_load: missing_items.append("continuous load")
            if not st.session_state.max_peak_load: missing_items.append("max peak load")
            
            st.markdown(f'<div class="warning-box">⚠️ Please complete: {", ".join(missing_items)}</div>', unsafe_allow_html=True)

with button_col4:
    if st.button("💰 
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
", key="cost_analysis_button"):
        if (st.session_state.eboss_model and st.session_state.eboss_type and 
            st.session_state.continuous_load and st.session_state.max_peak_load):
            st.session_state.show_cost_dialog = True
            st.session_state.show_specs = False
            st.session_state.show_load_specs = False
            st.session_state.show_comparison = False
            st.session_state.show_cost_analysis = False
            st.rerun()
        else:
            missing_items = []
            if not st.session_state.eboss_model: missing_items.append("EBOSS® model")
            if not st.session_state.eboss_type: missing_items.append("EBOSS® type")
            if not st.session_state.continuous_load: missing_items.append("continuous load")
            if not st.session_state.max_peak_load: missing_items.append("max peak load")
            
            st.markdown(f'<div class="warning-box">⚠️ Please complete: {", ".join(missing_items)}</div>', unsafe_allow_html=True)

with button_col5:
    if st.button("🔄 Reset", key="reset_button"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key not in ['eboss_model_select', 'eboss_type_select', 'generator_kva_select', 'continuous_load_input', 'max_peak_load_input', 'standard_generator_select']:
                del st.session_state[key]
        st.session_state.show_specs = False
        st.session_state.show_load_specs = False
        st.session_state.show_comparison = False
        st.session_state.show_cost_analysis = False
        st.rerun()

# Specifications Display
if st.session_state.show_specs and st.session_state.eboss_model:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">📋 Technical Specifications</h3>', unsafe_allow_html=True)
    
    # Close button for specs
    if st.button("✕ Close Specs", key="close_specs"):
        st.session_state.show_specs = False
        st.rerun()
    
    # Get specifications for selected model
    specs = EBOSS_SPECS.get(st.session_state.eboss_model, {}).copy()
    
    # Dynamic Generator kVA based on EBOSS® type
    if st.session_state.eboss_type == "Full Hybrid":
        # Use fixed hybrid generator size
        hybrid_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(st.session_state.eboss_model)
        if hybrid_kva:
            specs["Generator kVA"] = f"{hybrid_kva} kVA (Hybrid units only)"
    elif st.session_state.eboss_type == "Power Module" and st.session_state.generator_kva:
        # Use user-selected generator size
        specs["Generator kVA"] = f"{st.session_state.generator_kva} (User selected)"
    
    if specs:
        # Create two columns - left for specs, right for values
        spec_col1, spec_col2 = st.columns([1, 1])
        
        # Define sections and their specs
        sections = {
            "Power Output": [
                "Hybrid Energy System", "Three-phase Max Power", "Single-phase Max Power", 
                "Frequency", "Simultaneous voltage", "Voltage regulation"
            ],
            "Load Specifications": [
                "Max Intermittent amp-load 208V", "Max Continuous amp-load 208V",
                "Max Intermittent amp-load 240V", "Max Continuous amp-load 240V", 
                "Max Intermittent amp-load 480V", "Max Continuous amp-load 480V"
            ],
            "Battery & Power Systems": [
                "Battery Type", "Battery Capacity", "Generator kVA", "Battery Voltage", "Inverter Type"
            ],
            "Physical Specifications": [
                "Operating Temperature", "Dimensions (L x W x H)", "Weight"
            ],
            "Warranty & Support": [
                "Warranty - EBOSS® only", "Warranty - With trailer & generator", "Battery warranty",
                "Service & Support", "Training", "Warranty", "Warranty - With generator"
            ]
        }
        
        with spec_col1:
            st.markdown('<h3 style="color: var(--alpine-white); font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.6); margin-bottom: 1rem;">Specifications</h3>')
            for section_name, section_specs in sections.items():
                # Section header
                st.markdown(f"""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                    <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">{section_name}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Section specs
                for spec_name in section_specs:
                    if spec_name in specs:
                        st.markdown(f"""
                        <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; text-align: left; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3); border: 2px solid var(--energy-green);">
                            <strong style="font-size: 0.95rem; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{spec_name}</strong>
                        </div>
                        """, unsafe_allow_html=True)
        
        with spec_col2:
            st.markdown('<h3 style="color: var(--alpine-white); font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.6); margin-bottom: 1rem;">Values</h3>')
            for section_name, section_specs in sections.items():
                # Section header (matching left column)
                st.markdown(f"""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                    <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">{section_name}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Section values
                for spec_name in section_specs:
                    if spec_name in specs:
                        spec_value = specs[spec_name]
                        st.markdown(f"""
                        <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid var(--energy-green); box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                            <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{spec_value}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        # User input override section
        if st.session_state.continuous_load and st.session_state.max_peak_load:
            st.markdown('<hr style="margin: 1.5rem 0; border-color: var(--cool-gray-8c);">', unsafe_allow_html=True)
            st.markdown("### Your Load Requirements")
            load_col1, load_col2 = st.columns([1, 1])
            
            with load_col1:
                st.markdown(f"""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Continuous Load</strong><br>
                    <span style="font-size: 1.5rem; font-weight: bold;">{st.session_state.continuous_load} kW</span>
                </div>
                """, unsafe_allow_html=True)
            
            with load_col2:
                st.markdown(f"""
                <div style="background: var(--energy-green); color: var(--alpine-white); padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Max Peak Load</strong><br>
                    <span style="font-size: 1.5rem; font-weight: bold;">{st.session_state.max_peak_load} kW</span>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Load Based Specifications Display
elif st.session_state.show_load_specs and st.session_state.eboss_model and st.session_state.continuous_load and st.session_state.max_peak_load:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">⚡ Load Based Specifications</h3>', unsafe_allow_html=True)
    
    # Close button for load specs
    if st.button("✕ Close Load Specs", key="close_load_specs"):
        st.session_state.show_load_specs = False
        st.rerun()
    
    # Get specifications for selected model
    specs = EBOSS_SPECS.get(st.session_state.eboss_model, {})
    
    if specs:
        # Calculate load-based recommendations using authentic data
        custom_charge = st.session_state.custom_charge_rate if st.session_state.use_custom_charge else None
        load_calc = calculate_load_specs(
            st.session_state.eboss_model,
            st.session_state.eboss_type,
            st.session_state.continuous_load,
            st.session_state.max_peak_load,
            st.session_state.generator_kva,
            custom_charge
        )
        

        
        # Remove the old column structure - will be replaced with section-by-section layout
        
        # Calculate default and max charge rates for inline display
        default_charge_rate = calculate_charge_rate(
            st.session_state.eboss_model,
            st.session_state.eboss_type,
            st.session_state.generator_kva
        )
        max_charge_rate = get_max_charge_rate(
            st.session_state.eboss_model,
            st.session_state.eboss_type,
            st.session_state.generator_kva
        )
        
        # Calculate enhanced load-based specifications with new formulas
        # Get proper generator size display and kW values
        if st.session_state.eboss_type == "Full Hybrid":
            # Fixed hybrid generator sizes with kVA/kW mappings
            hybrid_generator_map = {
                "EB25 kVA": {"kva": 25, "kw": 20, "display": "25 kVA / 20 kW"},
                "EB70 kVA": {"kva": 45, "kw": 36, "display": "45 kVA / 36 kW"},
                "EB125 kVA": {"kva": 65, "kw": 52, "display": "65 kVA / 52 kW"},
                "EB220 kVA": {"kva": 125, "kw": 100, "display": "125 kVA / 100 kW"},
                "EB400 kVA": {"kva": 220, "kw": 176, "display": "220 kVA / 176 kW"}
            }
            # Note: EB400 uses 220 kVA generator, add the 400 kVA option
            if st.session_state.eboss_model == "EB400 kVA":
                generator_display = "400 kVA / 320 kW"
                generator_kw = 320
            else:
                gen_info = hybrid_generator_map.get(st.session_state.eboss_model, {})
                generator_display = gen_info.get("display", "Not specified")
                generator_kw = gen_info.get("kw", 0)
        else:
            # Power Module - use user-selected value
            generator_display = f"{st.session_state.generator_kva}" if st.session_state.generator_kva else "Not specified"
            # Extract numeric value from generator_kva (remove "kVA" text)
            if st.session_state.generator_kva:
                generator_kva_numeric = st.session_state.generator_kva.replace("kVA", "").strip()
                generator_kw = float(generator_kva_numeric) * 0.8  # Convert kVA to kW (0.8 power factor)
            else:
                generator_kw = 0
            
        continuous_load_kw = float(st.session_state.continuous_load)
        battery_capacity_kwh = float(load_calc['battery_capacity']) if load_calc['battery_capacity'] > 0 else 0
        charge_rate_kw = float(load_calc['charge_rate']) if load_calc['charge_rate'] > 0 else 0
        
        # New calculations based on provided formulas
        battery_longevity = (battery_capacity_kwh / continuous_load_kw) if continuous_load_kw > 0 else 0
        charge_time = (battery_capacity_kwh / charge_rate_kw) if charge_rate_kw > 0 else 0
        charges_per_day = 24 / (charge_time + battery_longevity) if (charge_time + battery_longevity) > 0 else 0
        engine_load_percent = (charge_rate_kw / generator_kw * 100) if generator_kw > 0 else 0
        runtime_per_day = 24 / (charge_time + battery_longevity) if (charge_time + battery_longevity) > 0 else 0
        # Calculate authentic fuel consumption using GPH interpolation
        generator_kva_for_gph = generator_kw / 0.8 if generator_kw > 0 else 0  # Convert kW back to kVA for GPH lookup
        fuel_per_hour = interpolate_gph(generator_kva_for_gph, engine_load_percent) if engine_load_percent > 0 else 0
        fuel_per_day_calc = fuel_per_hour * charges_per_day if fuel_per_hour > 0 else 0
        fuel_per_week = fuel_per_day_calc * 7
        fuel_per_month = fuel_per_day_calc * 30
        co2_per_day_calc = 250 * fuel_per_hour if fuel_per_hour > 0 else 0
        
        # Load-specific sections with new structure and calculations
        load_sections = {
            "EBOSS® & Load Info": [
                ("Continuous Load", f"{st.session_state.continuous_load} kW"),
                ("Max Peak Load", f"{st.session_state.max_peak_load} kW"),
                ("EBOSS® Type", st.session_state.eboss_type or "Not specified"),
                ("EBOSS® Model", st.session_state.eboss_model or "Not specified"),
                ("Generator Size", generator_display)
            ],
            "Battery & Charging": [
                ("Battery Capacity", f"{battery_capacity_kwh:.1f} kWh" if battery_capacity_kwh > 0 else "Already Specified"),
                ("Battery Longevity", f"{battery_longevity:.2f} hours" if battery_longevity > 0 else "N/A"),
                ("Charge Rate", f"{charge_rate_kw} kW" + (" (Custom)" if st.session_state.use_custom_charge else " (Recommended)") if charge_rate_kw > 0 else "Already Specified"),
                ("Charge Time", f"{charge_time:.2f} hours" if charge_time > 0 else "N/A"),
                ("Charges / Day", f"{charges_per_day:.2f}" if charges_per_day > 0 else "N/A")
            ],
            "Engine & Environmental": [
                ("Engine Load", f"{engine_load_percent:.1f}%" if engine_load_percent > 0 else "N/A"),
                ("Runtime / Day", f"{runtime_per_day:.2f} hours" if runtime_per_day > 0 else "N/A"),
                ("Fuel / Hr", f"{fuel_per_hour:.2f} GPH" if fuel_per_hour > 0 else "N/A"),
                ("Fuel / Day", f"{fuel_per_day_calc:.1f} gallons" if fuel_per_day_calc > 0 else "N/A"),
                ("Fuel / Week", f"{fuel_per_week:.1f} gallons" if fuel_per_week > 0 else "N/A"),
                ("Fuel / Month", f"{fuel_per_month:.1f} gallons" if fuel_per_month > 0 else "N/A"),
                ("CO2 Emitted / Day", f"{co2_per_day_calc:.1f} lbs" if co2_per_day_calc > 0 else "N/A")
            ]
        }
        
        # Display each section with a single header spanning both columns
        for section_name, section_items in load_sections.items():
            # Single header spanning both columns
            st.markdown(f"""
            <div style="background: var(--energy-green); color: var(--alpine-white); padding: 0.6rem; margin: 1rem 0 0.25rem 0; border-radius: 8px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
                <strong style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; font-family: Arial, sans-serif;">{section_name}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Create two columns for this section's content
            section_col1, section_col2 = st.columns([1, 1])
            
            with section_col1:
                # Section specs
                for spec_name, spec_value in section_items:
                    st.markdown(f"""
                    <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; text-align: left; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3); border: 2px solid var(--energy-green);">
                        <strong style="font-size: 0.95rem; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{spec_name}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            with section_col2:
                # Section values with consistent styling
                for spec_name, spec_value in section_items:
                    # Consistent styling for all values
                    bg_color = "var(--cool-gray-10c)"
                    border_color = "var(--energy-green)"
                    text_color = "var(--alpine-white)"
                    
                    # Special handling for Charge Rate with Change option
                    if spec_name == "Charge Rate" and charge_rate_kw > 0:
                        change_col1, change_col2 = st.columns([3, 1])
                        
                        with change_col1:
                            st.markdown(f"""
                            <div style="background: {bg_color}; color: {text_color}; padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid {border_color}; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                                <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{spec_value}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with change_col2:
                            if st.button("Change", key="change_charge_rate"):
                                st.session_state.current_charge_rate = charge_rate_kw
                                st.session_state.max_charge_rate = max_charge_rate  
                                st.session_state.default_charge_rate = default_charge_rate
                                st.session_state.battery_capacity_kwh = battery_capacity_kwh
                                st.session_state.battery_longevity = battery_longevity
                                st.session_state.show_charge_modal = True
                                st.rerun()
                    else:
                        st.markdown(f"""
                        <div style="background: {bg_color}; color: {text_color}; padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid {border_color}; box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3);">
                            <span style="font-size: 0.95rem; font-weight: 500; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">{spec_value}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Generator selection display if applicable
        if st.session_state.generator_kva:
            st.markdown('<hr style="margin: 1.5rem 0; border-color: var(--cool-gray-8c);">', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 1rem; border-radius: 8px; text-align: center;">
                <strong>Selected Generator: {st.session_state.generator_kva}</strong><br>
                <span style="font-size: 0.9rem;">Power Module Configuration</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Charge Rate Modal Dialog
@st.dialog("⚡ Charge Rate Configuration")
def charge_rate_modal():
    # Apply custom styling for better readability
    st.markdown("""
    <style>
    .stDialog > div > div {
        background-color: #2a2a2a;
        color: #ffffff;
    }
    .stDialog .stMarkdown p {
        color: #ffffff !important;
    }
    .stDialog .stMarkdown strong {
        color: #ffffff !important;
    }
    </style>
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