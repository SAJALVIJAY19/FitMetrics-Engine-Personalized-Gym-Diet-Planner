from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    activity_level: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProgressBase(BaseModel):
    weight: float
    mood: Optional[str] = None
    workout_days_this_week: Optional[int] = 0
    calories_intake: Optional[int] = 0
    notes: Optional[str] = None

class ProgressCreate(ProgressBase):
    pass

class ProgressOut(ProgressBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True
