from flask import Flask, render_template, request
import joblib
import re

app = Flask(__name__)

# Load model + vectorizer
model = joblib.load("model/phishing-model.joblib")
vectorizer = joblib.load("model/vectorizer.joblib")

# Clean text (same as training)
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', ' url ', text)
    text = re.sub(r'\d+', ' number ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence = None

    if request.method == "POST":
        email = request.form["email"]

        cleaned = clean_text(email)
        features = vectorizer.transform([cleaned])

        prediction = model.predict(features)[0]
        confidence = model.predict_proba(features)[0][prediction]

        if prediction == 1:
            result = "Phishing Email"
        else:
            result = "Safe Email"

    return render_template("index.html", result=result, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)