# NutriWise – Data-Driven Meal Planner
## Overview
NutriWise is a modern, local-first meal planning app that generates personalized meal plans using machine learning. It clusters meals by nutrition with a Gaussian Mixture Model (GMM) and selects balanced plans that match your daily calorie target. The project was upgraded from a Tkinter desktop app to a full-stack web app with a Python backend and a Vue 3 + Tailwind frontend scaffold.
## Features
1. GMM-based meal recommendations with varied results on each request
2. Daily calorie target via Mifflin–St Jeor + activity/goal multipliers
3. Dietary preferences: Vegetarian or Mixed
4. Direct PostgreSQL integration (SQLAlchemy + psycopg2) with automatic table creation and Excel migration
5. Robust fallbacks: PostgreSQL → Excel → sample meals
6. Modern UI scaffold (Vue 3 + Tailwind + Vite) and one-click runner `RUN_NUTRIWISE.py`
## Installation & Setup
1. Clone the Repository
```bash
git clone https://github.com/shreymadd/Nutriwise-Data-Driven_Meal_Planner.git
cd Nutriwise-Data-Driven_Meal_Planner
```
2. Create a Virtual Environment (Recommended)
```bash
python -m venv .venv
```
For Windows:
```bash
.\.venv\Scripts\activate
``` 
For macOS/Linux:
```bash
source .venv/bin/activate
```  
3. Install Dependencies
```bash
pip install -r Requirements.txt
```
## How to Run the Application
You can run the backend-only demo API or use the launcher to coordinate frontend and backend.

Option A — Backend only (http://localhost:8000)
```bash
python backend/demo_server.py
```
Then open http://localhost:8000/health and http://localhost:8000/docs

Option B — One‑click launcher (interactive)
```bash
python RUN_NUTRIWISE.py
```
In the prompt:
- Choose 2 to start Backend Only in one terminal.
- Open a second terminal, run the script again and choose 3 to start Frontend Only.

Frontend (optional, Vite dev server):
```bash
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite (usually http://localhost:5173).
## Project Structure
```plaintext
Nutriwise-Data-Driven_Meal_Planner/
│-- Data/
│   └── Updated_500_Indian_Food_Nutritional_Data.xlsx
│-- backend/
│   ├── demo_server.py            # Demo HTTP API with PostgreSQL + GMM integration
│   └── database.py               # SQLAlchemy engine, table creation, Excel migration
│-- frontend/                     # Vue 3 + Tailwind + Vite scaffold (dev server)
│-- modules/
│   ├── gmm_model.py              # GMM model wrapper (joblib persistence)
│   └── ...
│-- RUN_NUTRIWISE.py              # Interactive launcher
│-- Requirements.txt              # Python dependencies
│-- .env.example                  # Template environment variables
│-- README.md                     # This file
│-- .gitignore                    # Git ignore rules
│-- QUICK_START.md                # Extra quick start notes
│-- License.txt                   # License file
```
## Usage Guide
### 1) Backend API
Use Swagger at http://localhost:8000/docs and call POST `/recommendations` with a JSON body like:
```json
{
  "age": 28,
  "weight": 70,
  "height": 175,
  "gender": "male",
  "activityLevel": "moderate",
  "goal": "maintain",
  "dietaryPreference": "mixed"
}
```
### 2) Frontend
Run the Vite dev server and use the UI to input your profile and generate a plan. Each click generates a new plan from the appropriate GMM cluster.
## Technologies Used
1. Python, pandas, numpy, scikit‑learn, joblib
2. PostgreSQL, SQLAlchemy, psycopg2-binary
3. Environment: python-dotenv
4. Frontend: Vue 3 + Tailwind + Vite (optional during development)
5. Dev: FastAPI/uvicorn ready for future expansion
## Troubleshooting & Common Issues
1) PostgreSQL not installed or `psql` missing: install PostgreSQL for Windows and ensure the service is running on port 5432. The app will still work via Excel/sample fallbacks.
2) Import warnings in IDE: set interpreter to `.venv/Scripts/python.exe`.
3) If `RUN_NUTRIWISE.py` opens port 3000 but Vite logs 5173, use the Vite URL.
## License
This project is licensed under the MIT License – you are free to use and modify it.
