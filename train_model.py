import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# 1. Load the dataset
dataset_path = "dataset/archive/phishing_email.csv"
print("Loading dataset...")
df = pd.read_csv(dataset_path)

# Handle potential missing values or column naming differences
text_col = df.columns[0]
label_col = df.columns[-1]

print(f"Using '{text_col}' for email text and '{label_col}' for labels.")

# Drop null values if any
df = df.dropna(subset=[text_col, label_col])

X = df[text_col]
y = df[label_col].astype(int)

# 2. Train-Test Split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Feature Extraction (TF-IDF Vectorizer)
print("Vectorizing email text with TF-IDF...")
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Train the Classifier
print("Training Multinomial Naive Bayes classifier...")
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# 5. Evaluate the Model
y_pred = model.predict(X_test_tfidf)
acc = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print(f"Model Accuracy: {acc * 100:.2f}%")
print("=" * 50)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=["Legitimate (0)", "Phishing (1)"]))

# 6. Save the trained model and vectorizer
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Saved trained model to 'models/phishing_model.pkl'")
print("Saved TF-IDF vectorizer to 'models/tfidf_vectorizer.pkl'")