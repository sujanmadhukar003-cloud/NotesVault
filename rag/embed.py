from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def create_embedding(text):
    embedding = model.encode(text)

    return embedding