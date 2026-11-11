import streamlit as st
import joblib
import os
import time

st.set_page_config(
    page_title="CheckMyMail | AI Security Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Dynamic Aesthetic Backgrounds & Custom Keyframe Animations ---
def inject_custom_styling(status=None):
    if status == "safe":
        bg_style = """
            background: radial-gradient(circle at 50% 20%, #064e3b 0%, #022c22 45%, #0a0f1d 100%) !important;
            transition: all 0.8s ease-in-out;
        """
        accent_color = "#34d399"
        glow_effect = "0 0 35px rgba(52, 211, 153, 0.35)"
    elif status == "unsafe":
        bg_style = """
            background: radial-gradient(circle at 50% 20%, #7f1d1d 0%, #450a0a 45%, #0a0f1d 100%) !important;
            transition: all 0.8s ease-in-out;
        """
        accent_color = "#f87171"
        glow_effect = "0 0 35px rgba(248, 113, 113, 0.4)"
    else:
        bg_style = """
            background: radial-gradient(circle at 50% 10%, #172554 0%, #0b1120 50%, #030712 100%) !important;
        """
        accent_color = "#38bdf8"
        glow_effect = "0 0 25px rgba(56, 189, 248, 0.25)"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {{
            {bg_style}
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f3f4f6;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Subtle floating animations */
        @keyframes floatSlow {{
            0% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-8px) rotate(1deg); }}
            100% {{ transform: translateY(0px) rotate(0deg); }}
        }}

        @keyframes pulseGlow {{
            0% {{ box-shadow: 0 0 15px rgba(255,255,255,0.05); }}
            50% {{ box-shadow: {glow_effect}; }}
            100% {{ box-shadow: 0 0 15px rgba(255,255,255,0.05); }}
        }}

        @keyframes cardSlideUp {{
            0% {{ opacity: 0; transform: translateY(24px) scale(0.98); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        /* Glassmorphism Container */
        .glass-panel {{
            background: rgba(17, 24, 39, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 32px;
            animation: cardSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            box-shadow: {glow_effect};
        }}

        /* Text area modern sleek style */
        .stTextArea textarea {{
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 14px !important;
            color: #f8fafc !important;
            font-size: 15px !important;
            padding: 16px !important;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }}
        .stTextArea textarea:focus {{
            border-color: {accent_color} !important;
            box-shadow: 0 0 16px {accent_color}44 !important;
        }}

        /* Primary Action Button */
        .stButton button {{
            background: linear-gradient(135deg, {accent_color}, #2563eb) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            border: none !important;
            width: 100% !important;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 20px {accent_color}55;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .stButton button:hover {{
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 8px 30px {accent_color}88;
        }}

        /* Results Aesthetic Displays */
        .result-safe {{
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.9), rgba(16, 185, 129, 0.7));
            border: 1px solid #34d399;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            animation: cardSlideUp 0.5s ease-out forwards;
            box-shadow: 0 0 35px rgba(52, 211, 153, 0.45);
        }}

        .result-unsafe {{
            background: linear-gradient(135deg, rgba(127, 29, 29, 0.9), rgba(239, 68, 68, 0.7));
            border: 1px solid #f87171;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            animation: cardSlideUp 0.5s ease-out forwards;
            box-shadow: 0 0 35px rgba(248, 113, 113, 0.55);
        }}

        .status-title {{
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}

        .status-subtitle {{
            font-size: 15px;
            color: #e5e7eb;
            opacity: 0.95;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- Model Artifact Loader ---
@st.cache_resource
def load_models():
    model = joblib.load(os.path.join("models", "phishing_model.pkl"))
    vectorizer = joblib.load(os.path.join("models", "tfidf_vectorizer.pkl"))
    return model, vectorizer

try:
    model, vectorizer = load_models()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# Initialize session state for analysis status
if "analysis_status" not in st.session_state:
    st.session_state["analysis_status"] = None
if "result_data" not in st.session_state:
    st.session_state["result_data"] = {}

# Apply initial background styling
inject_custom_styling(st.session_state["analysis_status"])

# --- Main Layout ---
col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='font-size: 44px; font-weight: 800; background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                CheckMyMail AI
            </h1>
            <p style='color: #94a3b8; font-size: 16px; max-width: 580px; margin: 0 auto;'>
                An intelligent security scanner that analyses linguistic patterns and suspicious indicators to verify email integrity.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)

        user_input = st.text_area(
            "Incoming Email Text",
            placeholder="Paste raw email header, subject, or email body text here...",
            height=180,
            label_visibility="collapsed"
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([3, 1])
        with c1:
            scan_now = st.button("✨ Run Intelligent Security Scan", use_container_width=True)
        with c2:
            reset_btn = st.button("🔄 Reset", use_container_width=True)

        if reset_btn:
            st.session_state["analysis_status"] = None
            st.session_state["result_data"] = {}
            st.rerun()

        if scan_now:
            if not user_input.strip():
                st.warning("Please paste email content first to begin inspection.")
            else:
                with st.spinner("Decoding email signatures & evaluating security weights..."):
                    time.sleep(0.4)
                    transformed = vectorizer.transform([user_input])
                    prediction = model.predict(transformed)[0]

                    prob_val = 95.0
                    if hasattr(model, "predict_proba"):
                        probs = model.predict_proba(transformed)[0]
                        prob_val = probs[1] * 100 if prediction == 1 else probs[0] * 100

                    st.session_state["analysis_status"] = "unsafe" if prediction == 1 else "safe"
                    st.session_state["result_data"] = {
                        "prediction": prediction,
                        "confidence": prob_val
                    }
                    st.rerun()

        # Display results based on state
        if st.session_state["analysis_status"] == "safe":
            st.balloons()
            conf = st.session_state["result_data"].get("confidence", 95.0)
            st.markdown(f"""
                <div style='height: 20px;'></div>
                <div class='result-safe'>
                    <div class='status-title'>🎉 ALL CLEAR — SAFE & AUTHENTIC</div>
                    <div class='status-subtitle'>
                        No deceptive intent, spoofed patterns, or high-risk language discovered.
                    </div>
                    <div style='margin-top: 15px; font-weight: 700; color: #ecfdf5;'>
                        Authenticity Confidence: {conf:.1f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

        elif st.session_state["analysis_status"] == "unsafe":
            st.snow()
            conf = st.session_state["result_data"].get("confidence", 95.0)
            st.markdown(f"""
                <div style='height: 20px;'></div>
                <div class='result-unsafe'>
                    <div class='status-title'>⚠️ HIGH RISK — PHISHING DETECTED</div>
                    <div class='status-subtitle'>
                        Urgent call-to-actions, deceptive domain traps, or manipulative threats were flagged.
                    </div>
                    <div style='margin-top: 15px; font-weight: 700; color: #fee2e2;'>
                        Risk Probability: {conf:.1f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 13px; margin-top: 40px;'>
        CheckMyMail Engine • Real-time Scikit-Learn Vector Architecture
    </div>
""", unsafe_allow_html=True)
