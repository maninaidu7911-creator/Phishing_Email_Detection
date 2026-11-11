import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score

# 1. Load Dataset
# Ensure your dataset CSV path is correctly pointed here
DATA_PATH = "phishing_email.csv"  # or your dataset filename
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Place your dataset in this directory.")

df = pd.read_csv(DATA_PATH)

# Auto-detect text and label column names
text_col = None
label_col = None

for col in df.columns:
    col_lower = col.lower().strip()
    if col_lower in ["text", "email", "body", "email_text", "message"]:
        text_col = col
    elif col_lower in ["label", "class", "target", "phishing"]:
        label_col = col

if not text_col or not label_col:
    text_col = df.columns[0]
    label_col = df.columns[1]

# Drop missing rows
df = df.dropna(subset=[text_col, label_col])
X = df[text_col].astype(str)
y = df[label_col].astype(int)

# 2. Train-Test Split (80/20 with stratification)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples...")

# 3. High-Accuracy TF-IDF Pipeline
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),        # Captures single words and two-word combinations
    max_features=15000,        # Increased vocabulary limit
    sublinear_tf=True,         # Dampens repetitive noise
    stop_words="english",
    strip_accents="unicode"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Calibrated Linear Support Vector Machine
base_svc = LinearSVC(C=1.0, random_state=42, max_iter=2000)
model = CalibratedClassifierCV(estimator=base_svc, cv=5)
model.fit(X_train_vec, y_train)

# 5. Evaluate
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f"\n==========================================")
print(f"Model Training Complete! Accuracy: {acc * 100:.2f}%")
print(f"==========================================\n")
print(classification_report(y_test, y_pred))

# 6. Save Artifacts
os.makedirs("models", exist_ok=True)
joblib.dump(model, os.path.join("models", "phishing_model.pkl"))
joblib.dump(vectorizer, os.path.join("models", "tfidf_vectorizer.pkl"))
print("Saved upgraded models to models/ directory successfully!")
