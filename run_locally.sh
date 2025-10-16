#!/usr/bin/env bash
echo "This helper runs both dev backends (Flask on 5000, FastAPI on 8001)."
echo "Make sure DATABASE_URL env var is set and MySQL is running."
echo
if [ "$1" = "flask" ]; then
  (cd flask_app && python app.py)
elif [ "$1" = "fastapi" ]; then
  (cd fastapi_app && uvicorn main:app --reload --host 0.0.0.0 --port 8001)
else
  echo "Usage: ./run_locally.sh [flask|fastapi]"
fi
