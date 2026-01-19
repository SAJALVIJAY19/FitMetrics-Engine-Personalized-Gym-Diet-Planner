from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    age = Column(Integer)
    gender = Column(String) # "male", "female"
    height_cm = Column(Float)
    weight_kg = Column(Float)
    activity_level = Column(String) # "sedentary", "lightly_active", etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    progress_entries = relationship("Progress", back_populates="user")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    weight = Column(Float)
    mood = Column(String)
    workout_days_this_week = Column(Integer)
    calories_intake = Column(Integer)
    notes = Column(String)

    user = relationship("User", back_populates="progress_entries")
