# AUTHORS   : Alex Wise, Will Alexander, Cole Craig Craig
# CLASS     : CS498
# DATE      : 11/08/2024
# PROGRAM   : PreSeniorProject.py

import tkinter as tk
from tkinter import ttk
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec
import re

# Email Parsing
from scripts.AzureMailReader import fetch_emails

# Sample email text

# Email Parsing (No touchy)
email_text = fetch_emails(mode="last")
print(email_text)
#email_text = "Congratulations! You have won a prize. Please click here to claim your reward."
displaytext = ""
def preprocess_text(text):
    # Basic preprocessing to clean the text
    text = text.lower()  # Lowercase
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    return text

# Step 1: TF-IDF Vectorization
def compute_tfidf_vector(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer.get_feature_names_out()

# Step 2: Word Embeddings
def compute_word_embeddings(texts):
    # Tokenize sentences for word embeddings
    tokenized_sentences = [text.split() for text in texts]
    word2vec_model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)
    embeddings = {word: word2vec_model.wv[word] for word in word2vec_model.wv.index_to_key}
    return embeddings

# Step 3: N-gram Extraction
def compute_ngrams(texts, n=2):
    vectorizer = CountVectorizer(ngram_range=(n, n))
    ngrams_matrix = vectorizer.fit_transform(texts)
    return ngrams_matrix, vectorizer.get_feature_names_out()

# Process the email text
processed_text = preprocess_text(email_text)

# Applying the TF-IDF Vectorization
tfidf_matrix, tfidf_feature_names = compute_tfidf_vector([processed_text])
# Convert both feature arrays to strings before concatenating
displaytext = displaytext + "TF-IDF Features:\n"
displaytext += '\n'.join(tfidf_feature_names)  # Join TF-IDF features as a string, with each feature on a new line

displaytext = displaytext + "\nTF-IDF Matrix:\n" + str(tfidf_matrix.toarray()) + "\n"

# Generating Word Embeddings
embeddings = compute_word_embeddings([processed_text])

# Print first 5 values for brevity
for word, vector in embeddings.items():
    displaytext += f"{word}: {vector[:5]}...\n"  # Add first 5 values for each word embedding

# Extracting N-grams (Example: Bigrams)
ngrams_matrix, ngrams_feature_names = compute_ngrams([processed_text], n=2)

displaytext += "\nBigrams:\n"
displaytext += '\n'.join(ngrams_feature_names)  # Join n-grams as a string, with each n-gram on a new line
displaytext += "\nN-grams Matrix:\n" + str(ngrams_matrix.toarray())

# Now when you call `receive_text`, it will properly display the content without errors.


class Overlay:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.attributes('-transparentcolor', '#abcdef')  # Set transparent color

        self.text_label = tk.Label(self.root, text="", font=("Arial", 24), bg="#ffffff", fg="black")
        self.text_label.pack()

        self.update_text("")

    def update_text(self, text):
        self.text_label.config(text=text)

def main():
    print(displaytext)
    root = tk.Tk()
    overlay = Overlay(root)

    # Simulate receiving text from a separate program
    def receive_text():
        overlay.update_text(displaytext)
        root.after(1000, receive_text)  # Update text every 1 second
    def quit_program(event=None):
        root.destroy()

    #pressing escape key will quit the program
    root.bind("<Escape>", quit_program)
    receive_text()

    root.mainloop()

if __name__ == "__main__":
    main()