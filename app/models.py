from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

try:
    from database import Base
    
except:
    from app.database import Base
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow) 