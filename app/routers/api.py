from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models, ml_model, chat_adapter, database

router = APIRouter(prefix="/api")

class PredictRequest(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    activity: str

class ChatRequest(BaseModel):
    message: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict-calories")
def predict_calories_api(data: PredictRequest):
    prediction = ml_model.predict_calories(
        data.age, data.gender, data.height, data.weight, data.activity
    )
    return {"predicted_calories": prediction}

@router.post("/chat")
def chat_api(request: Request, data: ChatRequest):
    user_id = request.session.get("user_id")
    response = chat_adapter.chat_adapter.respond(user_id, data.message)
    return {"response": response}

@router.get("/progress-data")
def get_progress_data(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"labels": [], "data": []}
    
    entries = db.query(models.Progress).filter(models.Progress.user_id == user_id).order_by(models.Progress.date.asc()).limit(12).all()
    
    labels = [e.date.strftime("%Y-%m-%d") for e in entries]
    data = [e.weight for e in entries]
    
    return {"labels": labels, "data": data}
