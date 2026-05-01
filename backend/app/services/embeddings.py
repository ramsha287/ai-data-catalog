from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2',device='cpu')
    return model


def get_embedding(text):
    # simple lightweight embedding
    text = text.lower()
    return [len(text), sum(ord(c) for c in text) % 1000]