# FitMetrics Engine

**Personalized Gym & Diet Planner**

A full-stack metabolic intelligence system and fitness planner using FastAPI, SQLAlchemy, Jinja2, and scikit-learn.

## Features
- **User Authentication**: Register and Login.
- **Dashboard**: View BMI, BMR, TDEE, and predicted calorie needs.
- **Diet Plan**: Generate diet plans using OpenFoodFacts.
- **Workout Plan**: Generate workout plans based on BMI and ML predictions.
- **Progress Tracking**: Track weight and view progress charts.
- **AI Chat Coach**: Chat with an AI coach (simulated or connected to LLM).

## Tech Stack
- **Backend**: FastAPI
- **Database**: SQLite (SQLAlchemy)
- **Frontend**: Jinja2 Templates + Bootstrap 5
- **ML**: scikit-learn (RandomForestRegressor)

## Run Instructions

### Prerequisites
- Python 3.9+
- Docker (optional)

## Screenshots 
<img width="1090" height="600" alt="Screenshot 2026-05-12 175212" src="https://github.com/user-attachments/assets/8f7a80f3-ed4a-432d-81bc-3701efd80d1a" />
<img width="1083" height="591" alt="Screenshot 2026-05-12 175200" src="https://github.com/user-attachments/assets/5f4ad2c7-4da3-46d7-ab2c-cfe568024322" />
<img width="1034" height="649" alt="Screenshot 2026-05-12 175141" src="https://github.com/user-attachments/assets/ec9150fe-f92e-4450-a494-ac89da8beb67" />
<img width="1156" height="606" alt="Screenshot 2026-05-12 175131" src="https://github.com/user-attachments/assets/2229c494-03c1-44e3-b8fa-c6036c59a0f1" />

### Local Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Train the ML model:
   ```bash
   python app/train_model.py
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Open http://127.0.0.1:8000 in your browser.

### Docker Setup
1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Open http://127.0.0.1:8000 in your browser.

## How to demo to teacher/recruiter
1. **Setup**: Ensure `ML/model.pkl` exists (run `python app/train_model.py` if not).
2. **Run**: Start the server with `uvicorn app.main:app --reload`.
3. **Login/Register**: Go to `http://127.0.0.1:8000`. Click "Register" to create a new account.
4. **Dashboard**: After login, show the Dashboard with calculated metrics.
5. **Diet**: Click "Diet Plan" to show the generated meal plan.
6. **Workout**: Click "Workout Plan" to show the generated workout routine.
7. **Progress**: Click "Progress" and add a new weight entry. Show the chart updating.
8. **Chat**: Click "AI Coach" and ask a question (e.g., "How do I lose weight?").
