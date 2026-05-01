from fastapi import APIRouter
from pydantic import BaseModel
from ..services.sql_generator import generate_sql

from ..services.embeddings import get_embedding
from ..services.search import search

router = APIRouter()

# Request schema
class Query(BaseModel):
    text: str


#  Query enrichment (important)
def enrich_query(query):
    query = query.lower()

    if "high value" in query:
        query += " income spending score"

    if "segmentation" in query:
        query += " clustering groups customers"

    if "behavior" in query:
        query += " spending patterns actions"

    if "targeting" in query:
        query += " segmentation marketing audience"

    if "income" in query:
        query += " salary earnings"

    return query


# Fast explanation (NO LLM)
def generate_explanation(query, result):
    name = result["data"].get("name", "").lower()

    if result["level"] == "dataset":
        return f"This dataset matches '{query}' because it contains customer features like income, age, and spending."

    if result["level"] == "column":
        if "income" in name:
            return "This column represents customer income, useful for identifying high-value customers."

        if "spending" in name:
            return "This column shows spending behavior, important for segmentation."

        if "age" in name:
            return "Age helps group customers into demographic segments."

        if "id" in name:
            return "This is an identifier column, useful for tracking but not for analysis."

        return f"This column '{name}' is relevant to '{query}'."

    return "Relevant result based on semantic similarity."

@router.post("/search")
def search_data(query: Query):

    enriched_query = enrich_query(query.text)
    embedding = get_embedding(enriched_query)

    results = search(embedding)

    explained_results = []

    dataset_metadata = None

    for r in results:
        if r["level"] == "dataset":
            dataset_metadata = r["data"]
            break   # 🔥 important fix

    for r in results:
        explanation = generate_explanation(query.text, r)

        explained_results.append({
            "level": r.get("level", "unknown"),
            "data": r.get("data", {}),
            "score": r.get("score", 0),
            "explanation": explanation
        })

    # 🔥 GENERATE SQL (FIXED)
    sql_query = None
    if dataset_metadata and "columns" in dataset_metadata:
        sql_query = generate_sql(enriched_query, dataset_metadata)

    return {
        "results": explained_results,
        "generated_sql": sql_query
    }