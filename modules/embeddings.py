from sentence_transformers import SentenceTransformer
import numpy as np

# Load model lazily
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _model

def get_skill_embeddings(skills):
    if not skills:
        return np.zeros(384)
    model = get_model()
    embeddings = model.encode(skills)
    # Average embeddings to create candidate vector
    candidate_vector = np.mean(embeddings, axis=0)
    return candidate_vector
