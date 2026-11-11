import streamlit as st
import joblib
import os

# Page Configuration
st.set_page_config(
    page_title="CheckMyMail",
    page_icon="🛡️",
    layout="centered"
)

# Load Model & Vectorizer
@st.cache_resource
def load_assets():
    model_path = os.path.join("models", "phishing_model.pkl")
    vectorizer_path = os.path.join("models", "tfidf_vectorizer.pkl")
    
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

try:
    model, vectorizer = load_assets()
except Exception as e:
    st.error(f"Error loading models: {e}. Please ensure train_model.py was run.")
    st.stop()

# Header Section
st.title("🛡️ CheckMyMail")
st.markdown("Enter the content of an email below to analyze whether it is **SAFE** or **UNSAFE**.")

# Input Field
email_input = st.text_area(
    "Email Content:",
    height=200,
    placeholder="Paste the email subject and body text here..."
)

# Prediction Logic
if st.button("Analyze Email", type="primary"):
    if not email_input.strip():
        st.warning("Please enter some email text before analyzing.")
    else:
        # Vectorize text
        input_vector = vectorizer.transform([email_input])
        
        # Predict
        prediction = model.predict(input_vector)[0]
        prediction_prob = model.predict_proba(input_vector)[0]

        st.divider()

        # Display Result
        if prediction == 1:
            st.error(f"⚠️ **Result: UNSAFE Email Detected!**")
            st.write(f"Confidence: **{prediction_prob[1] * 100:.2f}%**")
            st.info("Recommendation: Do not click any links or download attachments from this email.")
        else:
            st.success(f"✅ **Result: SAFE Email**")
            st.write(f"Confidence: **{prediction_prob[0] * 100:.2f}%**")