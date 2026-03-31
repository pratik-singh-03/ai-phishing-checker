import pandas as pd
import joblib
import os
import time
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from colorama import Fore

# =========================
# PATHS
# =========================
DATASET_PATH = "dataset/Phishing_Email.csv"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "phishing-model.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.joblib")

# =========================
# CLEAR SCREEN
# =========================
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()

print(Fore.YELLOW + "System is starting...")

# =========================
# TEXT CLEANING FUNCTION
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', ' url ', text)   # replace links
    text = re.sub(r'\d+', ' number ', text)    # replace numbers
    text = re.sub(r'[^\w\s]', '', text)        # remove punctuation
    return text

# =========================
# LOAD OR TRAIN MODEL
# =========================

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print(Fore.GREEN + "Model loaded successfully!")

else:
    print(Fore.GREEN + "Training model...")
    time.sleep(1)

    # =========================
    # LOAD DATASET (SAFE)
    # =========================
    data = pd.read_csv(DATASET_PATH, low_memory=False)

    # Remove unwanted index column
    if 'Unnamed: 0' in data.columns:
        data = data.drop(columns=['Unnamed: 0'])

    # Keep only required columns
    data = data[['Email Text', 'Email Type']]

    # Drop completely empty rows
    data = data.dropna()

    # Clean text
    data['Email Text'] = data['Email Text'].apply(clean_text)

    # =========================
    # LABEL ENCODING (SAFE)
    # =========================
    data['Email Type'] = data['Email Type'].map({
        'Safe Email': 0,
        'Phishing Email': 1
    })

    # 🔥 Remove rows where mapping failed
    data = data.dropna(subset=['Email Type'])

    # Convert to int
    data['Email Type'] = data['Email Type'].astype(int)

    # =========================
    # FEATURES & LABELS
    # =========================
    X = data['Email Text']
    Y = data['Email Type']

    # =========================
    # TRAIN TEST SPLIT
    # =========================
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=3
    )

    # =========================
    # VECTORIZER (IMPROVED)
    # =========================
    vectorizer = TfidfVectorizer(
        stop_words='english',
        lowercase=True,
        ngram_range=(1,2),   # bigrams
        max_features=5000
    )

    X_train_features = vectorizer.fit_transform(X_train)
    X_test_features = vectorizer.transform(X_test)

    # =========================
    # MODEL
    # =========================
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_features, Y_train)

    # =========================
    # ACCURACY
    # =========================
    train_acc = accuracy_score(Y_train, model.predict(X_train_features))
    test_acc = accuracy_score(Y_test, model.predict(X_test_features))

    print(Fore.WHITE + f"Training Accuracy: {round(train_acc*100,2)}%")
    print(Fore.WHITE + f"Test Accuracy: {round(test_acc*100,2)}%")

    # =========================
    # SAVE MODEL
    # =========================
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(Fore.GREEN + "Model trained & saved!")

# =========================
# PREDICTION LOOP
# =========================

while True:
    print("\n-----------------------------------")

    user_input = input("Enter email (type 'exit' to quit): ")

    if user_input.lower() == "exit":
        print(Fore.WHITE + "Exiting...")
        break

    # Clean input
    cleaned_input = clean_text(user_input)

    # Transform
    features = vectorizer.transform([cleaned_input])

    # Predict
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][prediction]

    if prediction == 1:
        print(Fore.RED + "Phishing Email Detected")
    else:
        print(Fore.GREEN + "Safe Email")

    print(Fore.WHITE + f"Confidence: {round(confidence * 100, 2)}%")