# AI-Based Phishing Email Detection System

## Overview

This project is an AI-powered system that detects whether an email is **Safe** or a **Phishing attempt** using Machine Learning.
It analyzes email content (and optionally sender information) to identify suspicious patterns and classify emails in real time.

---

## Problem Statement

Phishing emails are one of the most common cyber threats. Attackers send fake emails that appear legitimate to:

* Steal sensitive information (passwords, OTPs, bank details)
* Trick users into clicking malicious links
* Gain unauthorized access to accounts

Most users cannot easily differentiate between real and phishing emails.

---

## Solution

This system uses Machine Learning to:

* Analyze email text and patterns
* Detect suspicious keywords and urgency-based language
* Classify emails as **Safe** or **Phishing**
* Provide a confidence score for predictions

---

## Features

* Real-time phishing detection
* Confidence score output
* Detects suspicious patterns like “click here”, “verify now”
* Clean and simple web interface (Flask)
* Model persistence using Joblib
* Easily extendable for mobile/web integration

---

## Technologies Used

* **Python**
* **Pandas** – Data processing
* **Scikit-learn** – Machine Learning
* **TF-IDF Vectorizer** – Feature extraction
* **Logistic Regression** – Classification model
* **Flask** – Web application
* **Joblib** – Model saving/loading

---

## Project Structure

```
AI-PHISHING-CHECK-MASTER/
│
├── dataset/
│   └── Phishing_Email.csv
│
├── model/
│   ├── phishing-model.joblib
│   └── vectorizer.joblib
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── phishing.py        # Model training + CLI testing
├── app.py             # Flask web app
├── requirements.txt
└── README.md
```

## Future Enhancements

* URL detection and analysis
* Sender domain verification
* Risk scoring system
* Gmail/Outlook integration
* Mobile app deployment


## Author
Pratik Singh
