# app/embeddings.py
# from sentence_transformers import SentenceTransformer
import numpy as np

# Oooh, mini model for embeddings (temporarily disabled)
# model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    # Temporary stub - returns random vector
    return np.random.rand(384)  # MiniLM vector size

def similarity(vec1, vec2):
    # Cosine similarity
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
