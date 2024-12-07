import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm  # For progress bars
from joblib import dump

# Load dataset
def load_data(file_path):
    print("[INFO] Loading dataset...")
    df = pd.read_csv(file_path)
    print(f"[INFO] Dataset loaded with {len(df)} rows.")
    return df

# Preprocess the text data
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-z\s]', '', text)  # Remove non-alphabetic characters
    text = re.sub(r'\bescapenumber\b', '', text)  # Remove specific word
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

# Extract metadata (Example: Length of email)
def extract_metadata(text):
    return [len(text.split()), text.count(' '), text.count('http')]

# Feature extraction: TF-IDF and metadata
def extract_features(df):
    print("[INFO] Preprocessing text data...")
    df['text'] = df['text'].apply(preprocess_text)

    print("[INFO] Extracting TF-IDF features...")
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])
    print("[INFO] TF-IDF feature extraction complete.")

    dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
    
    print("[INFO] Extracting metadata features...")
    metadata = []
    for text in tqdm(df['text'], desc="Metadata extraction"):
        metadata.append(extract_metadata(text))
    metadata = np.array(metadata)

    print("[INFO] Combining TF-IDF and metadata features...")
    features = np.hstack([tfidf_matrix.toarray(), metadata])  # Avoid this for very large datasets
    return features, df['label']

# Main function
def main(file_path):
    # Load the dataset
    df = load_data(file_path)

    # Extract features and labels
    X, y = extract_features(df)

    print("[INFO] Splitting dataset into training, validation, and testing sets...")
    # Train-test-validation split (80% training, 10% testing, 10% validation)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Standardize the data
    print("[INFO] Standardizing the data...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    # Train Logistic Regression model
    print("[INFO] Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("[INFO] Model training complete.")


    dump(model, 'model.joblib')
    
    dump(scaler, 'scaler.joblib')
    print("[INFO] Model, vectorizer, and scaler saved successfully!")

    # Evaluate on training, validation, and test sets
    print("[INFO] Evaluating the model...")
    y_pred_train = model.predict(X_train)
    y_pred_val = model.predict(X_val)
    y_pred_test = model.predict(X_test)

    # Calculate and print the accuracy
    print("Training Accuracy:", accuracy_score(y_train, y_pred_train))
    print("Validation Accuracy:", accuracy_score(y_val, y_pred_val))
    print("Testing Accuracy:", accuracy_score(y_test, y_pred_test))

    # Print classification reports
    print("\nTraining Classification Report:\n", classification_report(y_train, y_pred_train))
    print("\nValidation Classification Report:\n", classification_report(y_val, y_pred_val))
    print("\nTesting Classification Report:\n", classification_report(y_test, y_pred_test))

    # Print confusion matrix
    print("\nConfusion Matrix (Test set):\n", confusion_matrix(y_test, y_pred_test))

if __name__ == "__main__":
    # Install tqdm if necessary: pip install tqdm
    # Path to the CSV file
    file_path = 'combined_data.csv'  # Replace with your file path
    main(file_path)
