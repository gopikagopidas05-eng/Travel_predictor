import streamlit as st

# 1. Page Configurations
st.set_page_config(
    page_title="Smart Travel Destination Predictor",
    page_icon="✈️",
    layout="centered"
)

# 2. Manage App Navigation via Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

def switch_page(page_name):
    st.session_state.current_page = page_name

# ==========================================
# PAGE 1: WELCOME / LANDING PAGE
# ==========================================
if st.session_state.current_page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #1F497D;'>✈️ Travel Destination Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #595959; font-weight: normal;'>Discover your next perfect getaway powered by predictive analytics.</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Input your weather, group size, and lifestyle preferences to calculate your ideal match.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Clean full-width GO button
    if st.button("GO", type="primary", use_container_width=True):
        switch_page('app_interface')
        st.rerun()

# ==========================================
# PAGE 2: MAIN PREDICTOR APP INTERFACE
# ==========================================
elif st.session_state.current_page == 'app_interface':
    st.markdown("<h2 style='color: #1F497D; margin-bottom: 0;'>📊 Destination Matching Dashboard</h2>", unsafe_allow_html=True)
    st.write("Adjust your travel metrics below. The underlying Linear Regression profiles will calculate your optimal match instantly.")
    
    st.markdown("---")
    
    st.subheader("🔄 1. Tune Your Travel Metrics")
    
    # Balanced 2-column layout grid for the 5 dashboard metrics
    col1, col2 = st.columns(2)
    
    with col1:
        pref_temp = st.slider("Preferred Temperature (°C)", min_value=-5.0, max_value=40.0, value=24.0, step=1.0)
        budget_level = st.slider("Budget Level (1 = Low, 10 = Luxury)", min_value=1, max_value=10, value=5, step=1)
        num_persons = st.slider("Number of Persons", min_value=1, max_value=12, value=2, step=1)
        
    with col2:
        activity_pace = st.slider("Trip Pace (1 = Relaxation, 10 = Heavy Adventure)", min_value=1, max_value=10, value=5, step=1)
        pollution_tolerance = st.slider("Acceptable Pollution/Urban Level (1 = Pristine, 10 = City Jungle)", min_value=1, max_value=10, value=3, step=1)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 3. ADVANCED MULTI-DESTINATION SCORING ENGINE
    # ==========================================
    # Each place calculates its own score based on explicit linear coefficients.
    
    # 🏝️ The Maldives (Luxury, Warm, Intimate/Low headcount, Pure relaxation, Pristine)
    maldives_score = 55 + (1.0 * pref_temp) + (3.5 * budget_level) - (1.5 * num_persons) - (4.5 * activity_pace) - (4.0 * pollution_tolerance)
    
    # 🏰 Paris, France (High Culture, Medium-High Budget, Urban Cityscape, Good for any group size)
    paris_score = 40 + (0.4 * pref_temp) + (2.0 * budget_level) + (0.5 * num_persons) + (1.5 * activity_pace) + (2.5 * pollution_tolerance)
    
    # 🏔️ Swiss Alps (Cold/Snow, High Budget, Active/Adventure, Low Pollution, Mid-to-Large Groups)
    swiss_score = 85 - (2.5 * pref_temp) + (2.5 * budget_level) + (0.2 * num_persons) + (3.0 * activity_pace) - (4.5 * pollution_tolerance)
    
    # 🗼 Tokyo, Japan (Fast Pace, Urban Hyper-city, Moderate Temp, High Tech exploration)
    tokyo_score = 30 + (0.5 * pref_temp) + (1.2 * budget_level) + (0.6 * num_persons) + (4.0 * activity_pace) + (4.5 * pollution_tolerance)
    
    # 🏖️ Phuket, Thailand (Warm, Highly Budget-Friendly, Great for group trips/nightlife, Active mix)
    phuket_score = 45 + (1.5 * pref_temp) - (1.5 * budget_level) + (2.0 * num_persons) + (2.5 * activity_pace) - (0.5 * pollution_tolerance)
    
    # 🛕 Bangkok, Thailand (Warm, Low Budget, Vibrant Street Life/Pollution, Ultra-fast pace, Group friendly)
    bangkok_score = 35 + (1.2 * pref_temp) - (2.0 * budget_level) + (1.5 * num_persons) + (3.5 * activity_pace) + (4.0 * pollution_tolerance)
    
    # 🌊 Lakshadweep, India (Warm, Budget-to-Mid, Intimate/Low headcount, Pristine coral reef nature, Extreme relaxation)
    lakshadweep_score = 60 + (1.3 * pref_temp) - (0.5 * budget_level) - (2.5 * num_persons) - (4.0 * activity_pace) - (5.0 * pollution_tolerance)

    # Dictionary containing all customized destination properties and visual profiles
    destinations = {
        "The Maldives 🇲🇻": {
            "score": maldives_score, "bg": "#E2EFDA", "text": "#375623", "border": "#A9D08E",
            "desc": "An elite, ultra-luxurious tropical getaway optimized for intimate, peaceful relaxation."
        },
        "Paris, France 🇫🇷": {
            "score": paris_score, "bg": "#D9E1F2", "text": "#1F497D", "border": "#B4C6E7",
            "desc": "A sophisticated journey filled with world-class art, rich European heritage, and city lights."
        },
        "The Swiss Alps 🇨🇭": {
            "score": swiss_score, "bg": "#FFF2CC", "text": "#7F6000", "border": "#FFD966",
            "desc": "Perfect for stunning snowcapped peaks, alpine fresh air, and exhilarating ski slopes."
        },
        "Tokyo, Japan 🇯🇵": {
            "score": tokyo_score, "bg": "#F5E6FA", "text": "#660066", "border": "#D6A3E4",
            "desc": "An energetic metropolis combining neon lights, street exploration, and futuristic tech hubs."
        },
        "Phuket, Thailand 🇹🇭": {
            "score": phuket_score, "bg": "#E6F4F8", "text": "#006680", "border": "#99D6E6",
            "desc": "A vibrant, budget-friendly beach paradise perfectly suited for lively groups and nightlife."
        },
        "Bangkok, Thailand 🇹🇭": {
            "score": bangkok_score, "bg": "#FCE4D6", "text": "#C65911", "border": "#F4B183",
            "desc": "A high-octane city adventure filled with historic temples, incredible street food, and bustling markets."
        },
        "Lakshadweep, India 🇮🇳": {
            "score": lakshadweep_score, "bg": "#E6F9F3", "text": "#006644", "border": "#99E6CC",
            "desc": "An untouched, serene archipelago offering pristine coral reefs, quiet sands, and complete seclusion."
        }
    }
    
    # Extract the highest scoring option
    winner = max(destinations, key=lambda k: destinations[k]["score"])
    winner_data = destinations[winner]
    
    # ==========================================
    # 4. MASSIVE HIGHLIGHT CARD FOR PREDICTION
    # ==========================================
    st.subheader("🔮 2. Recommended Destination Match")
    
    st.markdown(f"""
    <div style="background-color: {winner_data['bg']}; padding: 45px; border-radius: 15px; text-align: center; border: 2px solid {winner_data['border']}; box-shadow: 0px 4px 15px rgba(0,0,0,0.06);">
        <p style="font-size: 14px; font-weight: bold; color: #595959; letter-spacing: 2px; margin: 0; padding-bottom: 5px;">YOUR ALGORITHMIC GETAWAY MATCH</p>
        <h1 style="font-size: 60px; margin: 12px 0; color: {winner_data['text']}; font-weight: 900; line-height: 1.1;">{winner}</h1>
        <hr style="border: 0; border-top: 1px solid {winner_data['border']}; width: 60%; margin: 15px auto;">
        <p style="font-size: 19px; color: #333333; margin: 10px auto 0 auto; max-width: 550px; font-style: italic; line-height: 1.4;">"{winner_data['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Return Button
    if st.button("⬅️ Return to Welcome Page", use_container_width=True):
        switch_page('welcome')
        st.rerun()