# 🛡️ MailGuardX | Phishing Email Detection AI

An end-to-end Machine Learning web application designed to detect fraudulent, deceptive, and phishing emails in real time using Natural Language Processing (NLP) and Scikit-Learn.

🔗 **Live Demo:** [Check out MailGuardX Live](https://share.streamlit.io)

---

## 🚀 Key Features
- **Real-Time Text Classification:** Accurately evaluates raw email headers, subjects, and message bodies.
- **Dynamic Aesthetic UI:** Adaptive visual feedback that shifts dynamically based on email security status (Safe vs. High-Risk Phishing).
- **Lightweight & Fast:** Built on TF-IDF vectorization and a trained Scikit-Learn classification model for instant predictions.
- **Production Deployed:** Hosted and maintained live on Streamlit Community Cloud.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Machine Learning & NLP:** Scikit-Learn (`TF-IDF Vectorizer`), Pandas, Joblib
- **Frontend & Deployment:** Streamlit, Streamlit Community Cloud
- **Version Control:** Git, GitHub

---

## 📂 Project Structure
```text
Phishing_Email_Detection/
├── models/
│   ├── phishing_model.pkl       # Trained ML classification model
│   └── tfidf_vectorizer.pkl     # Pre-fitted TF-IDF feature extractor
├── app.py                       # Streamlit web application & UI logic
├── train_model.py               # Model training and artifact export script
├── inspect_phishing.py          # Dataset inspection and testing script
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
