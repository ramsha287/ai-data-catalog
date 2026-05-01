from .llm_service import generate_summary

def generate_metadata(df, filename):
    metadata = {}

    metadata["name"] = filename
    metadata["rows"] = df.shape[0]
    metadata["columns"] = list(df.columns)

    col_info = []
    for col in df.columns:
        col_info.append({
            "name": col,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum())
        })

    metadata["column_details"] = col_info

    # 🔥 LLM summary instead of static
    summary = generate_summary(metadata)

    return metadata, summary