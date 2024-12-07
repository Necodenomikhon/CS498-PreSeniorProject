import tkinter as tk
from tkinter import messagebox
from joblib import load
import numpy as np
import re
from scipy.sparse import hstack

# Email Parsing
from scripts.AzureMailReader import fetch_emails

# Email Parsing (No touchy)
email_text = ""

# Load the saved components
model = load('model.joblib')
tfidf_vectorizer = load('tfidf_vectorizer.joblib')
scaler = load('scaler.joblib')

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-z\s]', '', text)  # Remove non-alphabetic characters
    text = re.sub(r'\bescapenumber\b', '', text)  # Remove specific word
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

# Metadata extraction
def extract_metadata(text):
    return [len(text.split()), text.count(' '), text.count('http')]

# Prediction function
def predict_individual(email_text):
    # Preprocess input
    processed_text = preprocess_text(email_text)

    # Extract features
    tfidf_features = tfidf_vectorizer.transform([processed_text])
    metadata = np.array([extract_metadata(processed_text)])
    features = hstack([tfidf_features, metadata])  # Combine TF-IDF and metadata

    # Standardize features
    standardized_features = scaler.transform(features.toarray())

    # Predict using the model
    prediction = model.predict(standardized_features)
    probability = model.predict_proba(standardized_features)[0][1] * 100  # Probability of class "1" (scam)

    return prediction[0], probability

# Function for Paste Mode
def paste_mode():
    # Create the paste mode GUI
    def on_predict():
        email_text = email_input.get("1.0", tk.END).strip()
        if not email_text:
            messagebox.showwarning("Warning", "Please enter an email text.")
            return

        try:
            prediction, probability = predict_individual(email_text)
            result_text = f"Prediction: {'Scam' if prediction == 1 else 'Not Scam'}\n"
            result_text += f"Probability of being a scam: {probability:.2f}%"
            result_label.config(text=result_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Close the main menu and create the paste mode window
    main_menu.destroy()
    window = tk.Tk()
    window.title("Paste Mode - Email Scam Detector")
    window.geometry("640x480+0+0")  # Width x Height + X_offset + Y_offset
    window.resizable(False, False)

    # Create and place widgets
    tk.Label(window, text="Enter email text below:", font=("Arial", 14)).pack(pady=10)
    email_input = tk.Text(window, wrap=tk.WORD, font=("Arial", 12), width=60, height=15)
    email_input.pack(pady=10)

    predict_button = tk.Button(window, text="Predict", font=("Arial", 14), command=on_predict)
    predict_button.pack(pady=10)

    result_label = tk.Label(window, text="", font=("Arial", 14), wraplength=600, justify="left")
    result_label.pack(pady=10)

    window.mainloop()

# Function for Scan Mode
def scan_mode():
    # Predefined email text for scanning
    email_text = fetch_emails(mode="last")

    try:
        prediction, probability = predict_individual(email_text)
        result = f"Prediction: {'Scam' if prediction == 1 else 'Not Scam'}\n"
        result += f"Probability of being a scam: {probability:.2f}%"
        messagebox.showinfo("Scan Mode Result", result)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main menu GUI
main_menu = tk.Tk()
main_menu.title("Email Scam Detector - Main Menu")
main_menu.geometry("640x480+0+0")
main_menu.resizable(False, False)

tk.Label(main_menu, text="Choose a mode:", font=("Arial", 16)).pack(pady=20)

paste_button = tk.Button(main_menu, text="Paste Mode", font=("Arial", 14), width=20, command=paste_mode)
paste_button.pack(pady=10)

scan_button = tk.Button(main_menu, text="Scan Mode", font=("Arial", 14), width=20, command=scan_mode)
scan_button.pack(pady=10)

main_menu.mainloop()
