import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec
import re

# Sample email text
email_text = "Congratulations! You have won a prize. Please click here to claim your reward."

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
print("TF-IDF Features:")
print(tfidf_feature_names)
print(tfidf_matrix.toarray())

# Generating Word Embeddings
embeddings = compute_word_embeddings([processed_text])
print("\nWord Embeddings:")
for word, vector in embeddings.items():
    print(f"{word}: {vector[:5]}...")  # Print first 5 values for brevity

# Extracting N-grams (Example: Bigrams)
ngrams_matrix, ngrams_feature_names = compute_ngrams([processed_text], n=2)
print("\nBigrams:")
print(ngrams_feature_names)
print(ngrams_matrix.toarray())