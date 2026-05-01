from fastapi import FastAPI
from .routes import upload, search

# ✅ ADD THESE IMPORTS
from .database import engine
from .models import Base

app = FastAPI()

# ✅ CREATE TABLES HERE (runs once when app starts)
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(upload.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"message": "AI Data Catalog Running"}