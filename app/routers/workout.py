from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, utils, database, workout_engine, ml_model

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()

@router.get("/workout-plan", response_class=HTMLResponse)
def workout_plan(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/")
    
    bmi = utils.calculate_bmi(user.weight_kg, user.height_cm)
    predicted_calories = ml_model.predict_calories(
        user.age, user.gender, user.height_cm, user.weight_kg, user.activity_level
    )
    
    plan = workout_engine.generate_workout_plan(bmi, predicted_calories, user.weight_kg)
    
    return templates.TemplateResponse("workout.html", {
        "request": request,
        "user": user,
        "plan": plan
    })
