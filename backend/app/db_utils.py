from .database import SessionLocal
from .models import Dataset

def save_dataset(name, summary):
    db = SessionLocal()
    dataset = Dataset(name=name, summary=summary)
    db.add(dataset)
    db.commit()
    db.close()

def get_all_datasets():
    db = SessionLocal()
    data = db.query(Dataset).all()
    db.close()
    return data