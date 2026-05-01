import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# -----------------------------
# 🧠 SESSION STATE INIT
# -----------------------------
if "dataset_uploaded" not in st.session_state:
    st.session_state.dataset_uploaded = False

if "df" not in st.session_state:
    st.session_state.df = None

if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = None


# -----------------------------
# ⚙️ PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Data Catalog",
    layout="wide",
    page_icon="🧠"
)

# -----------------------------
# 🎨 STYLING
# -----------------------------
st.markdown("""
<style>
.main {background-color: #0E1117;}
.stButton>button {
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1E1E1E;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 📌 SIDEBAR
# -----------------------------
st.sidebar.title("🧠 AI Data Catalog")
page = st.sidebar.radio("Navigation", ["Upload Dataset", "Search Data"])

if st.session_state.dataset_uploaded:
    st.sidebar.success(f"Loaded: {st.session_state.dataset_name}")

# -----------------------------
# 🎯 TITLE
# -----------------------------
st.title("🚀 AI Data Catalog")

# =====================================================
# 📤 UPLOAD PAGE
# =====================================================
if page == "Upload Dataset":

    st.header("📤 Upload Dataset")

    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file is not None:
        if st.button("Upload & Process"):

            file.seek(0)

            with st.spinner("Processing dataset..."):
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": file}
                )

            if response.status_code == 200:
                st.success("✅ Dataset uploaded successfully!")

                file.seek(0)
                df = pd.read_csv(file)

                st.session_state.dataset_uploaded = True
                st.session_state.df = df
                st.session_state.dataset_name = file.name

            else:
                st.error("❌ Upload failed")

    if st.session_state.dataset_uploaded:

        df = st.session_state.df

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📊 Data Preview")
            st.dataframe(df.head())

        with col2:
            st.subheader("📈 Dataset Info")
            st.metric("Rows", df.shape[0])
            st.metric("Columns", df.shape[1])


# =====================================================
# 🔍 SEARCH PAGE
# =====================================================
elif page == "Search Data":

    st.header("🔍 Semantic Search")

    if not st.session_state.dataset_uploaded:
        st.warning("⚠️ Please upload a dataset first")
        st.stop()

    query = st.text_input(
        "Ask your data:",
        placeholder="e.g. high spending customers"
    )

    # -----------------------------
    # 🔧 SQL EXECUTOR
    # -----------------------------
    def execute_sql(df, sql):
        try:
            sql = sql.lower()

            if "spending_score" in sql and ">" in sql:
                return df[df["Spending_Score"] > 70]

            if "annual_income" in sql and ">" in sql:
                return df[df["Annual_Income_(k$)"] > 60]

            if "age" in sql and "<" in sql:
                return df[df["Age"] < 30]

            if "age" in sql and ">" in sql:
                return df[df["Age"] > 50]

            return df

        except Exception:
            return None

    # -----------------------------
    # 🧠 INSIGHT GENERATOR
    # -----------------------------
    def generate_insight(df):
        if df is None or df.empty:
            return "No meaningful data found."

        avg_spending = df["Spending_Score"].mean()
        avg_income = df["Annual_Income_(k$)"].mean()

        return f"""
- Average Spending Score: {round(avg_spending, 2)}
- Average Income: {round(avg_income, 2)}
- Number of matching customers: {len(df)}
"""

    # -----------------------------
    # 🔍 SEARCH BUTTON
    # -----------------------------
    if st.button("Search"):

        if query.strip() == "":
            st.warning("⚠️ Please enter a query")
        else:
            with st.spinner("Searching..."):

                response = requests.post(
                    f"{API_URL}/search",
                    json={"text": query}
                )

            if response.status_code == 200:

                data = response.json()
                results = data.get("results", [])
                sql_query = data.get("generated_sql", None)

                # -----------------------------
                # 🧾 SQL OUTPUT
                # -----------------------------
                if sql_query:
                    st.markdown("## 🧾 Generated SQL Query")
                    st.code(sql_query, language="sql")

                # -----------------------------
                # 📊 EXECUTE SQL
                # -----------------------------
                if sql_query and st.session_state.df is not None:

                    df = st.session_state.df
                    result_df = execute_sql(df, sql_query)

                    st.markdown("## 📊 Query Result")

                    if result_df is not None and not result_df.empty:
                        st.dataframe(result_df.head())

                        st.markdown("## 🧠 Insights")
                        st.success(generate_insight(result_df))

                    else:
                        st.warning("No data matched the query")

                # -----------------------------
                # 📌 SEARCH RESULTS
                # -----------------------------
                st.subheader("📌 Results")

                if len(results) == 0:
                    st.warning("No results found")
                else:
                    for i, r in enumerate(results):

                        if i == 0:
                            st.success("🔥 Best Match")

                        with st.container():
                            st.markdown('<div class="card">', unsafe_allow_html=True)

                            if r["level"] == "dataset":
                                st.markdown("### 📊 Dataset")
                                st.write(f"**Name:** {r['data']['name']}")
                                st.write(f"Rows: {r['data']['rows']}")
                                st.write(f"Columns: {len(r['data']['columns'])}")
                                st.write(", ".join(r["data"]["columns"]))

                            elif r["level"] == "column":
                                st.markdown("### 🔎 Column")
                                st.write(f"**Name:** {r['data']['name']}")
                                st.write(f"Type: {r['data']['dtype']}")

                            if "score" in r:
                                st.write(f"📊 Score: {round(r['score'], 3)}")

                            st.info(f"💡 {r['explanation']}")

                            st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error("❌ Search failed")