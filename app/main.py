from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .database import engine, Base
from .routers import auth, dashboard, diet, workout, api
import os

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Fitness Planner")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Session Middleware (Secret key should be env var in prod)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# Include Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(diet.router)
app.include_router(workout.router)
app.include_router(api.router)

@app.get("/chat")
def chat_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("chat.html", {"request": request})

