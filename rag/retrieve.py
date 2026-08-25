import faiss
import pickle
import numpy as np
from .embed import create_embedding

index = faiss.read_index("vector_db/faiss.index")

with open("vector_db/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def retrieve_chunks(query, top_k=5):

    query_vector = create_embedding(query)

    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    # indices[0] works because FAISS returns a list-of-lists, and [0] extracts results of the first query
    for idx in indices[0]:
        results.append(metadata[idx])

    return results
# if __name__ == "__main__":

#     query = "What is decision tree?"

#     results = retrieve_chunks(query)

#     for r in results:
#         print("\n")
#         print(r["semester"])
#         print(r["subject"])
#         print(r["unit"])
#         print(r["text"])