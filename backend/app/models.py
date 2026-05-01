from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    summary = Column(Text)