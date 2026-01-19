from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, utils, database, ml_model
import datetime

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

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/")
    
    bmi = utils.calculate_bmi(user.weight_kg, user.height_cm)
    bmr = utils.calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
    tdee = utils.calculate_tdee(bmr, user.activity_level)
    
    # ML Prediction
    predicted_calories = ml_model.predict_calories(
        user.age, user.gender, user.height_cm, user.weight_kg, user.activity_level
    )

    # Calculation Explanations
    height_m = user.height_cm / 100
    bmi_explanation = f"Weight ({user.weight_kg} kg) / Height² ({height_m} m)² = {bmi}"
    
    if user.gender.lower() == "male":
        bmr_formula = f"(10 × {user.weight_kg}) + (6.25 × {user.height_cm}) - (5 × {user.age}) + 5"
    else:
        bmr_formula = f"(10 × {user.weight_kg}) + (6.25 × {user.height_cm}) - (5 × {user.age}) - 161"
    bmr_explanation = f"Mifflin-St Jeor Equation: {bmr_formula} = {int(bmr)}"

    activity_multipliers = {
        "sedentary": 1.2, "lightly_active": 1.375, "moderately_active": 1.55, 
        "very_active": 1.725, "super_active": 1.9
    }
    multiplier = activity_multipliers.get(user.activity_level.lower(), 1.2)
    tdee_explanation = f"BMR ({int(bmr)}) × Activity Level ({multiplier}) = {int(tdee)}"
    
    predicted_explanation = "Predicted by our AI model based on your unique profile data (Age, Gender, Height, Weight, Activity Level)."
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "bmi": bmi,
        "bmr": int(bmr),
        "tdee": int(tdee),
        "predicted_calories": predicted_calories,
        "bmi_explanation": bmi_explanation,
        "bmr_explanation": bmr_explanation,
        "tdee_explanation": tdee_explanation,
        "predicted_explanation": predicted_explanation
    })

@router.get("/progress", response_class=HTMLResponse)
def progress_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/")
    
    entries = db.query(models.Progress).filter(models.Progress.user_id == user.id).order_by(models.Progress.date.desc()).all()
    
    return templates.TemplateResponse("progress.html", {
        "request": request,
        "user": user,
        "entries": entries
    })

@router.post("/progress")
def add_progress(
    request: Request,
    weight: float = Form(...),
    mood: str = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/")
    
    new_entry = models.Progress(
        user_id=user.id,
        weight=weight,
        mood=mood,
        notes=notes,
        date=datetime.datetime.utcnow()
    )
    
    # Update user current weight
    user.weight_kg = weight
    
    db.add(new_entry)
    db.commit()
    
    return RedirectResponse(url="/progress", status_code=303)
