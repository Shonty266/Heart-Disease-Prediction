import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern minimal white theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    
    
    
    
    /* Main background - Pure white */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container spacing */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 680px;
    }
    
    /* Header styling */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    h1.main-title {
        color: #000000 !important;
    }
    
    .subtitle {
        text-align: center;
        color: #000000 !important;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 3rem;
        line-height: 1.5;
    }
    
    p.subtitle {
        color: #000000 !important;
    }
    
    /* Section headers */
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.875rem;
        font-weight: 600;
        color: #000000;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #d1d5db;
    }
    
    /* Input field styling */
    .stSlider {
        padding: 0.5rem 0;
    }
    
    .stSlider > div > div > div > div {
        background-color: #6b7280;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #4b5563;
    }
    
    .stSelectbox > label, .stSlider > label, .stNumberInput > label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #000000;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox > div > div, .stNumberInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        background-color: #f9fafb;
        font-size: 0.9375rem;
        color: #000000;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover, .stNumberInput > div > div > input:hover {
        border-color: #9ca3af;
        background-color: #ffffff;
    }
    
    .stSelectbox > div > div:focus-within, .stNumberInput > div > div > input:focus {
        border-color: #6b7280;
        background-color: #ffffff;
        box-shadow: 0 0 0 3px rgba(107, 114, 128, 0.1);
    }
    
    /* Button styling */
    .stButton {
        margin-top: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #000000 !important;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.9375rem;
        padding: 0.875rem 2rem;
        border-radius: 10px;
        border: none;
        transition: all 0.2s ease;
        letter-spacing: 0.01em;
    }
    
    .stButton > button:hover {
        background-color: #1f2937;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
        padding: 1rem 1.25rem;
        margin-top: 2rem;
    }
    
    /* Success message */
    div[data-baseweb="notification"] {
        border-radius: 10px;
        background-color: #f3f4f6;
        border-left: 4px solid #000000;
    }
    
    /* Error message */
    .stAlert > div {
        font-size: 0.9375rem;
        line-height: 1.6;
        color: #000000;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #d1d5db, transparent);
        margin: 2.5rem 0;
    }
    
    /* Info card */
    .info-card {
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 2rem;
        font-size: 0.875rem;
        color: #000000;
        line-height: 1.6;
    }
    
    /* Result card */
    .result-card {
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 2px solid #d1d5db;
        background-color: #f9fafb;
    }
    
    .result-card.success {
        background-color: #f9fafb;
        border-color: #6b7280;
    }
    
    .result-card.error {
        background-color: #f9fafb;
        border-color: #6b7280;
    }
    
    .result-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #000000 !important;
    }
    
    .result-title.success {
        color: #000000 !important;
    }
    
    .result-title.error {
        color: #000000 !important;
    }
    
    .result-text {
        color: #000000 !important;
        font-size: 0.9375rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Disclaimer */
    .disclaimer {
        background-color: #f3f4f6;
        border: 1px solid #d1d5db;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-top: 1.5rem;
        font-size: 0.8125rem;
        color: #000000 !important;
        line-height: 1.6;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.875rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Spacing utilities */
    .mt-1 { margin-top: 0.5rem; }
    .mt-2 { margin-top: 1rem; }
    .mt-3 { margin-top: 1.5rem; }
    .mb-1 { margin-bottom: 0.5rem; }
    .mb-2 { margin-bottom: 1rem; }
    .mb-3 { margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# Load saved model, scaler, and expected columns
@st.cache_resource
def load_models():
    model = joblib.load("KNN_heart.pkl")
    scaler = joblib.load("scaler_heart.pkl")
    expected_columns = joblib.load("columns.pkl")
    return model, scaler, expected_columns

model, scaler, expected_columns = load_models()

# Header
st.markdown("<h1 class='main-title'>Heart Disease Prediction</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# Personal Information Section
st.markdown("<div class='section-title'>Personal Information</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Age", 18, 100, 30)
with col2:
    sex = st.selectbox("Sex", ["M", "F"], format_func=lambda x: "Male" if x == "M" else "Female")

# Vital Signs Section
st.markdown("<div class='section-title'>Vital Signs</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    resting_bp = st.number_input("Resting BP (mm Hg)", 80, 200, 120)
    max_hr = st.slider("Max Heart Rate", 60, 220, 170)
with col2:
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
    oldpeak = st.slider("ST Depression", 0.0, 6.0, 0.0, 0.1)

# Clinical Parameters Section
st.markdown("<div class='section-title'>Clinical Parameters</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    chest_pain = st.selectbox(
        "Chest Pain Type", 
        ["ATA", "NAP", "ASY", "TA"],
        format_func=lambda x: {
            "ATA": "Atypical Angina",
            "NAP": "Non-Anginal Pain",
            "ASY": "Asymptomatic",
            "TA": "Typical Angina"
        }[x]
    )
    resting_ecg = st.selectbox(
        "Resting ECG", 
        ["Normal", "ST", "LVH"],
        format_func=lambda x: {
            "Normal": "Normal",
            "ST": "ST-T Abnormality",
            "LVH": "LV Hypertrophy"
        }[x]
    )
with col2:
    exercise_angina = st.selectbox(
        "Exercise Angina", 
        ["N", "Y"],
        format_func=lambda x: "Yes" if x == "Y" else "No"
    )
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

# Additional Tests Section
st.markdown("<div class='section-title'>Additional Tests</div>", unsafe_allow_html=True)

fasting_bs = st.selectbox(
    "Fasting Blood Sugar > 120 mg/dL", 
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

# Predict button
predict_button = st.button("Analyze Risk")

# Prediction logic
if predict_button:
    with st.spinner("Analyzing your data..."):
        # Create a raw input dictionary
        raw_input = {
            'Age': age,
            'RestingBP': resting_bp,
            'Cholesterol': cholesterol,
            'FastingBS': fasting_bs,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Sex_' + sex: 1,
            'ChestPainType_' + chest_pain: 1,
            'RestingECG_' + resting_ecg: 1,
            'ExerciseAngina_' + exercise_angina: 1,
            'ST_Slope_' + st_slope: 1
        }

        # Create input dataframe
        input_df = pd.DataFrame([raw_input])

        # Fill in missing columns with 0s
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Reorder columns
        input_df = input_df[expected_columns]
        
        # Scale the input
        scaled_input = scaler.transform(input_df)

        # Make prediction
        prediction = model.predict(scaled_input)[0]



        # Show result
        if prediction == 1:
            st.markdown("""
                <div class='result-card error'>
                    <div class='result-title error'>⚠️ High Risk Detected</div>
                    <p class='result-text'>
                        Based on the provided information, our model indicates an elevated risk of heart disease. 
                        We strongly recommend consulting with a healthcare professional for a comprehensive evaluation.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='result-card success'>
                    <div class='result-title success'>✓ Low Risk Detected</div>
                    <p class='result-text'>
                        Based on the provided information, our model indicates a lower risk of heart disease. 
                        Continue maintaining a healthy lifestyle and regular check-ups with your healthcare provider.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
      

# Footer
st.markdown("""
    <div class='footer'>
        Developed by Aryan
    </div>
""", unsafe_allow_html=True)