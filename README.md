Nutrition Workshop Manager — Full Project Bundle
================================================

Contents
- flask_app/           -> Minimal Flask app + SQLAlchemy models + CLI
- fastapi_app/         -> FastAPI app + Pydantic schemas + async endpoints
- shared/              -> Shared models/db config used by both examples
- samples/             -> sample CSV data
- docker-compose.yml   -> MySQL + Adminer + option to build Flask or FastAPI
- requirements.txt     -> Combined requirements for both apps (venv recommended)
- run_locally.sh       -> Helper script to run a dev server (Linux/mac)
- tests/               -> Basic pytest tests for both apps

How to use (quick)
1. Unzip and create a Python venv:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
2. Start MySQL locally (docker-compose):
   docker-compose up -d db adminer
   # Wait until MySQL is ready, then create DB or use env defaults.
3. Start the desired backend:
   # Flask:
   cd flask_app
   export DATABASE_URL='mysql+mysqlconnector://workshop:workshop_pass@127.0.0.1:3306/nutrition_workshop'
   python app.py

   # FastAPI:
   cd fastapi_app
   export DATABASE_URL='mysql+aiomysql://workshop:workshop_pass@127.0.0.1:3306/nutrition_workshop'
   uvicorn main:app --reload --host 0.0.0.0 --port 8001

Notes
- The bundle is a starter template. For production readiness, follow the README in each app directory.
- Use Alembic for migrations in production. This bundle uses SQLAlchemy's create_all for dev convenience.
