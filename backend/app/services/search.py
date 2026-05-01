import faiss
import numpy as np

# Vector DB
index = faiss.IndexFlatL2(384)

# Store metadata
metadata_store = []


# -----------------------------
# ➕ ADD TO INDEX
# -----------------------------
def add_to_index(embedding, metadata, level="dataset"):
    vector = np.array([embedding]).astype("float32")
    index.add(vector)

    metadata_store.append({
        "data": metadata,
        "level": level
    })

def prioritize_dataset(results):
    dataset = None
    columns = []

    for r in results:
        if r["level"] == "dataset" and dataset is None:
            dataset = r
        else:
            columns.append(r)

    # dataset always first
    if dataset:
        return [dataset] + columns

    return results
# -----------------------------
# 🔍 SEARCH
# -----------------------------
def search(query_embedding, k=10):
    vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(vector, k)

    results = []

    for i, dist in zip(indices[0], distances[0]):
        if i >= 0 and i < len(metadata_store):

            item = metadata_store[i]

            # 🔥 Convert distance → similarity
            score = 1 / (1 + float(dist))

            # 🔥 Boost dataset slightly
            if item["level"] == "dataset":
                score *= 1.2

            # 🔥 Column importance tuning
            if item["level"] == "column":
                col_name = item["data"]["name"].lower()

                # Boost important features
                if "income" in col_name or "spending" in col_name or "age" in col_name:
                    score *= 1.5

                # Penalize useless columns
                if "id" in col_name:
                    score *= 0.5

                if "genre" in col_name:
                    score *= 0.7

            results.append({
                "data": item["data"],
                "level": item["level"],
                "score": float(score)
            })

    # 🔥 SORT
    results.sort(key=lambda x: x["score"], reverse=True)

    # 🔥 REMOVE DUPLICATES
    results = remove_duplicates(results)

    # 🔥 LIMIT DATASET TO ONE
    results = keep_one_dataset(results)

    results = prioritize_dataset(results)

    return results



# -----------------------------
# 🚫 REMOVE DUPLICATES
# -----------------------------
def remove_duplicates(results):
    seen = set()
    unique_results = []

    for r in results:
        if r["level"] == "dataset":
            key = ("dataset", r["data"]["name"])
        else:
            key = ("column", r["data"]["name"])

        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return unique_results


# -----------------------------
# 🎯 KEEP ONLY ONE DATASET
# -----------------------------
def keep_one_dataset(results):
    dataset_added = False
    final_results = []

    for r in results:
        if r["level"] == "dataset":
            if not dataset_added:
                final_results.append(r)
                dataset_added = True
        else:
            final_results.append(r)

    return final_results