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
    st.markdown("<p style='text-align: center; font-size: 18px;'>Input your weather and lifestyle preferences, and let our Linear Regression engine calculate your ideal match.</p>", unsafe_allow_html=True)
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
    st.write("Adjust your travel metrics below to calculate the real-time destination compatibility scores.")
    
    st.markdown("---")
    
    st.subheader("🔄 1. Tune Your Travel Metrics")
    
    # 2x2 layout grid for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        pref_temp = st.slider("Preferred Temperature (°C)", min_value=-5.0, max_value=40.0, value=22.0, step=1.0)
        budget_level = st.slider("Budget Level (1 = Low, 10 = Luxury)", min_value=1, max_value=10, value=5, step=1)
        
    with col2:
        activity_pace = st.slider("Trip Pace (1 = Relaxation, 10 = Heavy Adventure)", min_value=1, max_value=10, value=5, step=1)
        pollution_tolerance = st.slider("Acceptable Pollution/Urban Level (1 = Pristine, 10 = City Jungle)", min_value=1, max_value=10, value=4, step=1)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 3. FIXING THE MALDIVES BIAS: MULTI-DESTINATION LINEAR SCORING ENGINE
    # ==========================================
    # Every destination gets its own unique linear regression formula profile.
    
    # Destination A: Maldives (Wants: Warm, High Budget, Pure Relaxation, Low Pollution)
    maldives_score = 50 + (1.2 * pref_temp) + (2.5 * budget_level) - (4.0 * activity_pace) - (3.0 * pollution_tolerance)
    
    # Destination B: Paris (Wants: Moderate Temp, Medium-High Budget, Culture/Sightseeing, City Life)
    paris_score = 40 + (0.5 * pref_temp) + (1.5 * budget_level) + (1.5 * activity_pace) + (2.0 * pollution_tolerance)
    
    # Destination C: Swiss Alps (Wants: Cold/Snow, High Budget, Ski/Adventure, Pristine Nature)
    swiss_score = 80 - (2.5 * pref_temp) + (2.0 * budget_level) + (3.0 * activity_pace) - (4.0 * pollution_tolerance)
    
    # Destination D: Tokyo (Wants: Moderate Temp, Medium Budget, Fast Pace/High Activity, Neon City)
    tokyo_score = 30 + (0.8 * pref_temp) + (0.5 * budget_level) + (3.5 * activity_pace) + (4.0 * pollution_tolerance)
    
    # Compile scores into a dictionary
    destinations = {
        "The Maldives 🇲🇻": {"score": maldives_score, "bg": "#E2EFDA", "text": "#375623", "border": "#A9D08E", "desc": "Perfect for a luxurious, warm beach escape to completely unplug."},
        "Paris, France 🇫🇷": {"score": paris_score, "bg": "#D9E1F2", "text": "#1F497D", "border": "#B4C6E7", "desc": "Ideal for beautiful city cafes, rich history, art, and moderate weather."},
        "The Swiss Alps 🇨🇭": {"score": swiss_score, "bg": "#FFF2CC", "text": "#7F6000", "border": "#FFD966", "desc": "Suited for crisp mountain air, pristine alpine scenery, and skiing adventures."},
        "Tokyo, Japan 🇯🇵": {"score": tokyo_score, "bg": "#FCE4D6", "text": "#C65911", "border": "#F4B183", "desc": "Best for high-energy urban exploration, culinary excellence, and technological hubs."}
    }
    
    # Determine the mathematically highest scoring destination based on the sliders
    winner = max(destinations, key=lambda k: destinations[k]["score"])
    winner_data = destinations[winner]
    
    # ==========================================
    # 4. MASSIVE TYPOGRAPHY CARD FOR THE PREDICTION
    # ==========================================
    st.subheader("🔮 2. Linear Regression Top Recommendation")
    
    st.markdown(f"""
    <div style="background-color: {winner_data['bg']}; padding: 40px; border-radius: 15px; text-align: center; border: 2px solid {winner_data['border']}; box-shadow: 0px 4px 12px rgba(0,0,0,0.06);">
        <p style="font-size: 15px; font-weight: bold; color: #595959; letter-spacing: 1.5px; margin: 0; padding-bottom: 5px;">YOUR ALGORITHMIC MATCH</p>
        <h1 style="font-size: 55px; margin: 10px 0; color: {winner_data['text']}; font-weight: 900; line-height: 1.1;">{winner}</h1>
        <p style="font-size: 18px; color: #404040; margin: 15px auto 0 auto; max-width: 500px; font-style: italic;">"{winner_data['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Return Button
    if st.button("⬅️ Return to Welcome Page", use_container_width=True):
        switch_page('welcome')
        st.rerun()