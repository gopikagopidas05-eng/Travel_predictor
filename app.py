import streamlit as st
import pickle
import numpy as np

# 1. PAGE SETUP & STYLING
st.set_page_config(page_title="Travel Destination Predictor", page_icon="✈️", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2E4053;'>✈️ Smart Travel Destination Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7F8C8D;'>Enter your trip preferences to see where your AI models recommend traveling next!</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. LOAD ASSETS SAFELY
@st.cache_resource
def load_travel_assets():
    with open('logistic_model.pkl', 'rb') as f:
        lr = pickle.load(f)
    with open('knn_classifier_model.pkl', 'rb') as f:
        knn = pickle.load(f)
    return lr, knn

try:
    logistic_model, knn_model = load_travel_assets()
    st.sidebar.success("⚡ AI Travel Models Loaded Successfully!")
except FileNotFoundError:
    st.error("❌ Error: Missing machine learning model files in this repository.")
    st.stop()

# 3. SIDEBAR ARCHITECTURE CONFIGURATION
st.sidebar.header("⚙️ Model Engine")
selected_model_type = st.sidebar.radio("Choose Prediction Model", ["Logistic Regression", "KNN Classifier"])

# 4. USER PREFERENCE INPUTS
st.subheader("💰 Step 1: Main Financial Profile")
budget = st.number_input("Enter your total Trip Budget (INR)", min_value=10000.0, max_value=200000.0, value=45000.0, step=1000.0)

st.subheader("🧳 Step 2: Core Vacation Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    duration = st.slider("Duration (Days)", min_value=2, max_value=15, value=5)
with col2:
    rating = st.slider("Desired Destination Rating", min_value=1.0, max_value=5.0, value=4.5, step=0.1)
with col3:
    hotel_type = st.selectbox("Hotel Luxury Preference", ["Budget", "Standard", "Luxury"])

st.subheader("🌴 Step 3: Social & Seasonal Context")
col4, col5, col6 = st.columns(3)
with col4:
    travel_type = st.selectbox("Travel Companion Mode", ["Solo", "Couple", "Friends", "Family"])
with col5:
    season = st.selectbox("Preferred Travel Season", ["Summer", "Winter", "Monsoon"])
with col6:
    transport = st.selectbox("Preferred Mode of Transport", ["Car", "Bus", "Train", "Flight"])

# 5. EXACT ALPHABETICAL LABEL ENCODING MAPS (Matching dataset profiles)
travel_map = {"Couple": 0, "Family": 1, "Friends": 2, "Solo": 3}
season_map = {"Monsoon": 0, "Summer": 1, "Winter": 2}
transport_map = {"Bus": 0, "Car": 1, "Flight": 2, "Train": 3}
hotel_map = {"Budget": 0, "Luxury": 1, "Standard": 2}

# Target Destination reverse decoder map array
destination_target_map = {0: "Dubai", 1: "Goa", 2: "Jaipur", 3: "Kerala", 4: "Maldives", 5: "Manali", 6: "Munnar", 7: "Ooty"}

# Encode inputs
travel_encoded = travel_map[travel_type]
season_encoded = season_map[season]
transport_encoded = transport_map[transport]
hotel_encoded = hotel_map[hotel_type]

# 6. INFERENCE CALCULATION ENGINE
st.markdown("---")

# Recreate raw features array matching original columns pattern
raw_features = np.array([[
    budget, duration, rating, 
    travel_encoded, season_encoded, transport_encoded, hotel_encoded
]])

# Select execution core
active_model = logistic_model if selected_model_type == "Logistic Regression" else knn_model

if st.button("🚀 Match My Best Destination", use_container_width=True):
    try:
        # Run classification calculation
        prediction_index = active_model.predict(raw_features)[0]
        
        # Decode the numeric class index back to text destination label
        if isinstance(prediction_index, (int, np.integer)):
            final_destination = destination_target_map.get(prediction_index, str(prediction_index))
        else:
            final_destination = str(prediction_index) # fallback if target labels were raw strings
            
        # RENDER DELUXE RESULTS CARD
        st.markdown(f"""
        <div style='background-color: #EBF5FB; padding: 25px; border-radius: 12px; border-left: 8px solid #2980B9; text-align: center;'>
            <h2 style='color: #2C3E50; margin-top: 0;'>🏝️ Your AI Recommended Destination:</h2>
            <h1 style='color: #2980B9; font-size: 42px; margin: 15px 0;'>✨ {final_destination} ✨</h1>
            <p style='color: #7F8C8D; font-size: 16px;'>Prediction processed smoothly via <b>{selected_model_type}</b> engine.</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"🚨 Live Inference Engine Alert: {e}")