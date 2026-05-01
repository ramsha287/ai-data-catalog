import re

def find_column(columns, keyword):
    """
    Find best matching column based on keyword
    """
    keyword = keyword.lower()

    for col in columns:
        col_clean = col.lower().replace("_", " ").replace("(", "").replace(")", "")
        if keyword in col_clean:
            return col

    return None


def generate_sql(query, metadata):
    query = query.lower()

    table_name = metadata["name"].replace(".csv", "")
    columns = metadata["columns"]

    sql = f"SELECT * FROM {table_name}"
    conditions = []

    # 🔥 FIND REAL COLUMNS
    spending_col = find_column(columns, "spending")
    income_col = find_column(columns, "income")
    age_col = find_column(columns, "age")

    # -----------------------------
    # APPLY RULES (ONLY IF COLUMN EXISTS)
    # -----------------------------

    if ("high spending" in query or "spending habits" in query) and spending_col:
        conditions.append(f"{spending_col} > 70")

    if ("high income" in query or "rich customers" in query) and income_col:
        conditions.append(f"{income_col} > 60")

    if "young" in query and age_col:
        conditions.append(f"{age_col} < 30")

    if "old" in query and age_col:
        conditions.append(f"{age_col} > 50")

    # -----------------------------
    # BUILD SQL
    # -----------------------------
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    return sql