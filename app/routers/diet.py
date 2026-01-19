from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, utils, database, diet_engine

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

@router.get("/diet-plan", response_class=HTMLResponse)
def diet_plan(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/")
    
    bmr = utils.calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
    tdee = utils.calculate_tdee(bmr, user.activity_level)
    
    plan = diet_engine.generate_diet_plan(tdee)
    
    return templates.TemplateResponse("diet.html", {
        "request": request,
        "user": user,
        "plan": plan
    })

@router.get("/diet/swap/{meal_type}")
def swap_meal(meal_type: str, db: Session = Depends(get_db)):
    # Note: Authentication check is good practice even for simple APIs
    # Here assuming casual usage, but ideally check current user
    
    new_meal = diet_engine.get_random_meal(meal_type)
    if not new_meal:
        return {"error": "Invalid meal type"}
    
    return new_meal
