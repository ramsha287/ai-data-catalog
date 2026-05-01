# 🧠 AI Data Catalog with Semantic Search & SQL Generation

An AI-powered data discovery platform that allows users to **search datasets using natural language**, understand data structure, and generate SQL queries automatically.

---

## 🚀 Features

### 🔍 Semantic Search

* Search datasets using natural language queries
* Understands intent like:

  * "customer segmentation dataset"
  * "data to analyze spending habits"
  * "high value customers"

---

### 📊 Dataset & Column Intelligence

* Automatically extracts:

  * Dataset metadata (rows, columns)
  * Column details (type, missing values)
* Identifies **relevant columns** for a query

---

### 🧾 SQL Generation (Schema-Aware)

* Converts natural language → SQL
* Uses **actual dataset columns (no hallucination)**
* Example:

```sql
SELECT * FROM Mall_Customers WHERE Spending_Score > 70;
```

---

### 🧠 Query Understanding

* Query enrichment improves search quality
* Maps business terms:

  * "high value" → income + spending
  * "segmentation" → clustering

---

### 📌 Ranking & Deduplication

* Intelligent ranking system
* Removes duplicate results
* Prioritizes:

  * Dataset first
  * Important columns (income, spending, age)

---

### 💡 Smart Explanations

* Explains **why a dataset/column is relevant**
* No LLM dependency → fast & reliable

---

### 🖥️ Interactive UI (Streamlit)

* Upload dataset
* Search using natural language
* View:

  * Dataset preview
  * Search results
  * Generated SQL

---

## 🏗️ Tech Stack

| Layer           | Tech                 |
| --------------- | -------------------- |
| Backend         | FastAPI              |
| Frontend        | Streamlit            |
| Embeddings      | SentenceTransformers |
| Vector Search   | FAISS                |
| LLM             | Ollama               |
| Data Processing | Pandas               |

---

## 📂 Project Structure

```
AI-Data-Catalog/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   └── search.py
│   │   ├── services/
│   │   │   ├── embeddings.py
│   │   │   ├── search.py
│   │   │   ├── sql_generator.py
│   │   │   └── profiling.py
│
├── frontend/
│   └── streamlit_app.py
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-data-catalog.git
cd ai-data-catalog
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
pip install streamlit
streamlit run streamlit_app.py
```

---

### 4️⃣ Run LLM with Ollama

Install Ollama and run:

```bash
ollama run llama3
```

---

## 🧪 Example Queries

Try these in the app:

### 📊 Dataset-level

* "customer segmentation dataset"
* "dataset for marketing analysis"

### 🔎 Column-level

* "which column has income"
* "find customer id"

### 🧠 Analytical

* "data to analyze spending habits"
* "customer behavior analysis"

---

## 🎯 Key Highlights

* Schema-aware SQL generation 
* Column-level semantic search
* Query understanding using enrichment
* Real-world data catalog design
* Clean modular architecture

---

## 🧠 Future Improvements

* Multi-dataset support
* Chat-based interface (like ChatGPT for data)
* Dataset similarity search

---

## 📸 Demo (Add screenshots here)

* Upload Dataset
  <img width="1559" height="287" alt="image" src="https://github.com/user-attachments/assets/ead4b616-61b2-463a-ba55-00a838333093" />

* Semantic Search
  <img width="1881" height="846" alt="image" src="https://github.com/user-attachments/assets/af8b7072-8001-4d43-afd9-855f51070a31" />

---

## 🙌 Acknowledgements

* FAISS for vector search
* SentenceTransformers for embeddings
* LLM for query generation and enrichment
* Streamlit for UI
* FastAPI for backend

---



## ⭐ If you like this project, give it a star!
