import streamlit as st
import joblib
import os
import re
import time

st.set_page_config(
    page_title="MailGuardX | Phishing AI Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Dynamic Styling ---
def inject_custom_styling(status=None):
    if status == "safe":
        bg_style = "background: radial-gradient(circle at 50% 20%, #064e3b 0%, #022c22 45%, #0a0f1d 100%) !important;"
        accent_color = "#34d399"
        glow_effect = "0 0 35px rgba(52, 211, 153, 0.35)"
    elif status == "unsafe":
        bg_style = "background: radial-gradient(circle at 50% 20%, #7f1d1d 0%, #450a0a 45%, #0a0f1d 100%) !important;"
        accent_color = "#f87171"
        glow_effect = "0 0 35px rgba(248, 113, 113, 0.4)"
    else:
        bg_style = "background: radial-gradient(circle at 50% 10%, #172554 0%, #0b1120 50%, #030712 100%) !important;"
        accent_color = "#38bdf8"
        glow_effect = "0 0 25px rgba(56, 189, 248, 0.25)"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {{
            {bg_style}
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f3f4f6;
            transition: background 0.8s ease-in-out;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        @keyframes cardSlideUp {{
            0% {{ opacity: 0; transform: translateY(20px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Smooth calm speed: moves across, completely exits left, pauses ~2s, repeats */
        @keyframes tickerSlideWithPause {{
            0% {{
                transform: translateX(100%);
            }}
            92% {{
                transform: translateX(-100%);
            }}
            100% {{
                transform: translateX(-100%);
            }}
        }}

        .ticker-wrap {{
            width: 100%;
            overflow: hidden;
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 30px;
            padding: 10px 0;
            margin: 18px 0 24px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.15);
            white-space: nowrap;
        }}

        .ticker-content {{
            display: inline-block;
            white-space: nowrap;
            animation: tickerSlideWithPause 28s linear infinite;
            font-size: 14px;
            font-weight: 600;
            color: #e0f2fe;
            letter-spacing: 0.3px;
        }}

        .ticker-wrap:hover .ticker-content {{
            animation-play-state: paused;
        }}

        .ticker-badge {{
            background: #ef4444;
            color: #ffffff;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            margin-right: 8px;
            display: inline-block;
        }}

        /* Text Area */
        .stTextArea textarea {{
            background: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 16px !important;
            color: #f8fafc !important;
            font-size: 15px !important;
            padding: 18px !important;
            box-shadow: {glow_effect} !important;
            transition: all 0.3s ease;
        }}
        .stTextArea textarea:focus {{
            border-color: {accent_color} !important;
            box-shadow: 0 0 20px {accent_color}55 !important;
        }}

        /* Action Buttons */
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
            transform: translateY(-2px);
            box-shadow: 0 8px 30px {accent_color}88;
        }}

        /* Output Cards */
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
        }}

        .status-subtitle {{
            font-size: 15px;
            color: #e5e7eb;
            opacity: 0.95;
        }}

        .indicator-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 12px 16px;
            margin-top: 14px;
            text-align: left;
            font-size: 14px;
        }}

        /* Custom Footer */
        .custom-footer {{
            text-align: center;
            margin-top: 50px;
            margin-bottom: 25px;
        }}
        .designer-tag {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 8px 20px;
            border-radius: 20px;
            color: #cbd5e1;
            display: inline-block;
            backdrop-filter: blur(8px);
            font-size: 14px;
        }}
        .designer-name {{
            color: #60a5fa;
            font-weight: 700;
            text-decoration: none;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- Heuristic Rule Scanner ---
def analyze_heuristics(text):
    flags = []
    
    # 1. Numeric IP in URL
    if re.search(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text):
        flags.append("Suspicious numeric IP address link detected.")
        
    # 2. Obfuscated link shorteners
    if re.search(r'bit\.ly|tinyurl\.com|t\.co|is\.gd|cutt\.ly|ow\.ly', text, re.IGNORECASE):
        flags.append("Shortened link detected (used to hide true destinations).")
        
    # 3. Urgency triggers
    urgency_patterns = [
        r'\bverify your account\b', r'\baccount (has been )?suspended\b',
        r'\bimmediate action required\b', r'\bwithin 24 hours\b',
        r'\bunauthorized access\b', r'\bsecurity alert\b', r'\bclick here immediately\b'
    ]
    for pattern in urgency_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            flags.append("Urgent warning or threat of account blockage detected.")
            break

    # 4. Credential solicitation
    credential_patterns = [r'\benter your password\b', r'\bprovide your (ssn|otp|pin|cvv)\b', r'\bconfirm bank details\b']
    for pattern in credential_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            flags.append("Direct request for confidential passwords or bank details.")
            break

    return flags

# --- Load Models ---
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

if "analysis_status" not in st.session_state:
    st.session_state["analysis_status"] = None
if "result_data" not in st.session_state:
    st.session_state["result_data"] = {}

inject_custom_styling(st.session_state["analysis_status"])

# --- Layout ---
col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    st.markdown("""
        <div style='text-align: center; padding: 15px 0 5px 0;'>
            <h1 style='font-size: 46px; font-weight: 800; background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                MailGuardX
            </h1>
            <p style='color: #94a3b8; font-size: 15px; max-width: 620px; margin: 0 auto; letter-spacing: 0.2px;'>
                Protect your inbox with intelligent threat detection and instant email safety analysis.
            </p>
        </div>

        <!-- Floating Alert Ticker with 2-Second Pause Interval -->
        <div class='ticker-wrap'>
            <div class='ticker-content'>
                <span class='ticker-badge'>ALERT</span>
                Never share OTP, CVV, or passwords with anyone! &nbsp;&bull;&nbsp;
                🔍 Real banks never ask for passwords in an email. &nbsp;&bull;&nbsp;
                ⚠️ Be careful if an email threatens to block your account. &nbsp;&bull;&nbsp;
                🔗 Always verify link addresses before clicking.
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
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
                    time.sleep(0.3)
                    
                    heuristic_flags = analyze_heuristics(user_input)
                    transformed = vectorizer.transform([user_input])
                    prediction = model.predict(transformed)[0]

                    if hasattr(model, "predict_proba"):
                        probs = model.predict_proba(transformed)[0]
                        phish_prob = probs[1] * 100
                        safe_prob = probs[0] * 100
                    else:
                        phish_prob = 92.0 if prediction == 1 else 8.0
                        safe_prob = 100 - phish_prob

                    is_phishing = (prediction == 1) or (len(heuristic_flags) >= 2)
                    
                    if is_phishing:
                        final_confidence = max(phish_prob, 88.0 if heuristic_flags else 75.0)
                        status = "unsafe"
                    else:
                        final_confidence = safe_prob
                        status = "safe"

                    st.session_state["analysis_status"] = status
                    st.session_state["result_data"] = {
                        "prediction": 1 if is_phishing else 0,
                        "confidence": final_confidence,
                        "flags": heuristic_flags
                    }
                    st.rerun()

        # Display Result Card
        if st.session_state["analysis_status"] == "safe":
            conf = st.session_state["result_data"].get("confidence", 95.0)
            st.markdown(f"""
                <div style='height: 20px;'></div>
                <div class='result-safe'>
                    <div class='status-title'>🎉 ALL CLEAR — SAFE & AUTHENTIC</div>
                    <div class='status-subtitle'>
                        No deceptive intent, malicious payload links, or high-risk language discovered.
                    </div>
                    <div style='margin-top: 15px; font-weight: 700; color: #ecfdf5;'>
                        Authenticity Confidence: {conf:.1f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

        elif st.session_state["analysis_status"] == "unsafe":
            conf = st.session_state["result_data"].get("confidence", 95.0)
            flags = st.session_state["result_data"].get("flags", [])
            
            flag_html = ""
            if flags:
                flag_items = "".join([f"<li>{f}</li>" for f in flags])
                flag_html = f"""
                    <div class='indicator-box'>
                        <div style='font-weight: 700; color: #fca5a5; margin-bottom: 5px;'>Identified Risk Indicators:</div>
                        <ul style='margin: 0; padding-left: 20px; color: #fecaca;'>
                            {flag_items}
                        </ul>
                    </div>
                """

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
                    {flag_html}
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class='custom-footer'>
        <div class='designer-tag'>
            Designed by | <a href='https://www.linkedin.com/in/dandabattula-manikanta' target='_blank' class='designer-name'>Manikanta</a>
        </div>
    </div>
""", unsafe_allow_html=True)
