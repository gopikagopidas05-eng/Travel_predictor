import streamlit as st
import pickle
import numpy as np

# 1. PAGE SETUP & CONFIGURATION
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="centered")

# Initialize session state to track which page/phase the user is on
if 'phase' not in st.session_state:
    st.session_state.phase = "welcome"

# 2. LOAD TRAINED MODEL SAFELY (Logistic Regression Only)
@st.cache_resource
def load_logistic_model():
    with open('logistic_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

try:
    logistic_model = load_logistic_model()
except FileNotFoundError:
    st.error("❌ Error: 'logistic_model.pkl' not found. Please ensure it is uploaded to your GitHub repository.")
    st.stop()


# ==========================================
# PHASE 1: THE WELCOME FRONT PHASE
# ==========================================
if st.session_state.phase == "welcome":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 42px;'>🌍 AI-Powered Travel Planner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5D6D7E; font-size: 18px;'>Discover your next dream destination tailored perfectly to your budget, style, and preferences using intelligent predictive modeling.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Beautiful centered image placeholder or graphic styling
    st.markdown("""
    <div style='background-color: #EBF5FB; padding: 30px; border-radius: 15px; border: 1px solid #AED6F1; text-align: center;'>
        <span style='font-size: 60px;'>✈️🧳🏝️⛰️</span>
        <h3 style='color: #2E4053; margin-top: 15px;'>Ready to find your perfect getaway?</h3>
        <p style='color: #7F8C8D;'>Our system analyzes hundreds of travel data parameters to match you instantly.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Large interactive transition button
    if st.button("🚀 Let's Go!", use_container_width=True):
        st.session_state.phase = "questionnaire"
        st.parent_component = None
        st.rerun()


# ==========================================
# PHASE 2: THE MAIN QUESTIONNAIRE & RESULTS
# ==========================================
elif st.session_state.phase == "questionnaire":
    
    # Header with a small back navigation option
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Back"):
            st.session_state.phase = "welcome"
            st.rerun()
            
    st.markdown("<h2 style='color: #1A5276;'>🧳 Tell Us About Your Dream Trip</h2>", unsafe_allow_html=True)
    st.markdown("Fill out your trip specifications using the dropdown selections below.")
    st.markdown("---")

    # SECTION 1: FINANCIAL & TIME PROFILES
    st.markdown("### 💰 Financial & Duration Settings")
    # Using simple number box input instead of a slider
    budget = st.number_input("Trip Budget (in INR)", min_value=5000.0, max_value=800000.0, value=45000.0, step=1000.0)
    
    col1, col2 = st.columns(2)
    with col1:
        # Replaced slider with Selection Dropdown list
        duration = st.selectbox("Trip Duration (Days)", options=[2, 3, 4, 5, 6, 7, 8], index=3)
    with col2:
        # Replaced slider with Selection Dropdown list
        rating = st.selectbox("Desired Destination Rating", options=[3.5, 3.8, 4.0, 4.2, 4.5, 4.7, 4.8, 5.0], index=4)

    # SECTION 2: CONTEXT & PREFERENCES
    st.markdown("### 🌴 Social & Seasonal Selection Context")
    col3, col4 = st.columns(2)
    with col3:
        travel_type = st.selectbox("Who are you traveling with?", options=["Solo", "Couple", "Friends", "Family"])
        transport = st.selectbox("Preferred Mode of Transport", options=["Car", "Bus", "Train", "Flight"])
    with col4:
        season = st.selectbox("Preferred Travel Season", options=["Summer", "Winter", "Monsoon"])
        hotel_type = st.selectbox("Hotel Luxury Preference", options=["Budget", "Standard", "Luxury"])

    # 3. EXACT ALPHABETICAL LABEL ENCODING MAPS (Matching Dataset Behaviors)
    travel_map = {"Couple": 0, "Family": 1, "Friends": 2, "Solo": 3}
    season_map = {"Monsoon": 0, "Summer": 1, "Winter": 2}
    transport_map = {"Bus": 0, "Car": 1, "Flight": 2, "Train": 3}
    hotel_map = {"Budget": 0, "Luxury": 1, "Standard": 2}

    # Reverse target mapper to decode the prediction output indices
    destination_target_map = {
        0: "Dubai", 1: "Goa", 2: "Jaipur", 3: "Kerala", 
        4: "Maldives", 5: "Manali", 6: "Munnar", 7: "Ooty"
    }

    # Apply category value encodings safely
    travel_encoded = travel_map[travel_type]
    season_encoded = season_map[season]
    transport_encoded = transport_map[transport]
    hotel_encoded = hotel_map[hotel_type]

    st.markdown("<br>", unsafe_allow_html=True)

    # Recreate the precise feature array order required by the model
    raw_features = np.array([[
        budget, duration, rating, 
        travel_encoded, season_encoded, transport_encoded, hotel_encoded
    ]])

    # TRIGGER ENGINE BUTTON
    if st.button("🔮 Match My Best Destination", use_container_width=True):
        try:
            # Generate calculation index output
            prediction_index = logistic_model.predict(raw_features)[0]
            
            # Safely transform numeric index back to text name
            if isinstance(prediction_index, (int, np.integer)):
                final_destination = destination_target_map.get(prediction_index, str(prediction_index))
            else:
                final_destination = str(prediction_index)

            # RENDER THE MAGICAL RECOMMENDATION OUTPUT
            st.markdown("---")
            st.markdown(f"""
            <div style='background-color: #EBF5FB; padding: 25px; border-radius: 12px; border-left: 8px solid #2980B9; text-align: center;'>
                <h3 style='color: #2C3E50; margin-top: 0; font-weight: normal;'>🗺️ Your AI Recommended Match:</h3>
                <h1 style='color: #2980B9; font-size: 45px; margin: 10px 0; font-family: sans-serif;'>✨ {final_destination} ✨</h1>
                <p style='color: #7F8C8D; margin-bottom: 0;'>Calculated with high precision via <b>Logistic Regression</b> Engine.</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"🚨 Live Inference Engine Alert: {e}")