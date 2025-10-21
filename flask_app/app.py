from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_app.db import engine, Base, SessionLocal
import shared.models as models
from datetime import datetime, date
from sqlalchemy import func

app = Flask(__name__)
CORS(app)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return jsonify({"status": "ok", "message": "Nutrition Workshop API"}), 200

@app.get("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()}), 200

# PARTICIPANTS CRUD
@app.post("/participants")
def create_participant():
    payload = request.get_json(force=True)
    db = SessionLocal()
    try:
        p = models.Participant(
            name=payload["name"],
            gender=payload["gender"],
            email=payload.get("email"),
            phone=payload.get("phone"),
            dob=payload.get("dob"),
            notes=payload.get("notes"),
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return jsonify({"id": p.id, "name": p.name}), 201
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@app.get("/participants")
def list_participants():
    db = SessionLocal()
    participants = db.query(models.Participant).all()
    db.close()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "gender": p.gender,
        "email": p.email,
        "phone": p.phone,
        "dob": p.dob.isoformat() if p.dob else None,
        "notes": p.notes
    } for p in participants]), 200

@app.get("/participants/<int:pid>")
def get_participant(pid):
    db = SessionLocal()
    p = db.query(models.Participant).get(pid)
    db.close()
    if not p:
        return jsonify({"error": "Participant not found"}), 404
    return jsonify({
        "id": p.id,
        "name": p.name,
        "gender": p.gender,
        "email": p.email,
        "phone": p.phone,
        "dob": p.dob.isoformat() if p.dob else None,
        "notes": p.notes
    }), 200

@app.put("/participants/<int:pid>")
def update_participant(pid):
    payload = request.get_json(force=True)
    db = SessionLocal()
    p = db.query(models.Participant).get(pid)
    if not p:
        db.close()
        return jsonify({"error": "Participant not found"}), 404
    for field in ("name", "gender", "email", "phone", "dob", "notes"):
        if field in payload:
            setattr(p, field, payload[field])
    db.commit()
    result = {"id": p.id, "name": p.name}
    db.close()
    return jsonify(result), 200

@app.delete("/participants/<int:pid>")
def delete_participant(pid):
    db = SessionLocal()
    p = db.query(models.Participant).get(pid)
    if not p:
        db.close()
        return jsonify({"error": "Participant not found"}), 404
    db.delete(p)
    db.commit()
    db.close()
    return jsonify({"message": "Deleted"}), 204

# FOOD ITEMS CRUD
@app.post("/food_items")
def create_food_item():
    payload = request.get_json(force=True)
    db = SessionLocal()
    fi = models.FoodItem(
        name=payload["name"],
        calories_per_100g=float(payload.get("calories_per_100g", 0))
    )
    db.add(fi)
    db.commit()
    db.refresh(fi)
    db.close()
    return jsonify({"id": fi.id, "name": fi.name}), 201

@app.get("/food_items")
def list_food_items():
    db = SessionLocal()
    items = db.query(models.FoodItem).all()
    db.close()
    return jsonify([{
        "id": i.id,
        "name": i.name,
        "calories_per_100g": i.calories_per_100g
    } for i in items]), 200

@app.get("/food_items/<int:fid>")
def get_food_item(fid):
    db = SessionLocal()
    i = db.query(models.FoodItem).get(fid)
    db.close()
    if not i:
        return jsonify({"error": "FoodItem not found"}), 404
    return jsonify({
        "id": i.id,
        "name": i.name,
        "calories_per_100g": i.calories_per_100g
    }), 200

@app.put("/food_items/<int:fid>")
def update_food_item(fid):
    payload = request.get_json(force=True)
    db = SessionLocal()
    i = db.query(models.FoodItem).get(fid)
    if not i:
        db.close()
        return jsonify({"error": "FoodItem not found"}), 404
    if "name" in payload:
        i.name = payload["name"]
    if "calories_per_100g" in payload:
        i.calories_per_100g = float(payload["calories_per_100g"])
    db.commit()
    result = {"id": i.id, "name": i.name}
    db.close()
    return jsonify(result), 200

@app.delete("/food_items/<int:fid>")
def delete_food_item(fid):
    db = SessionLocal()
    i = db.query(models.FoodItem).get(fid)
    if not i:
        db.close()
        return jsonify({"error": "FoodItem not found"}), 404
    db.delete(i)
    db.commit()
    db.close()
    return jsonify({"message": "Deleted"}), 204

@app.post("/participants/<int:pid>/food_logs")
def add_food(pid: int):
    payload = request.get_json(force=True)
    db = SessionLocal()
    try:
        food = db.query(models.FoodItem).filter(models.FoodItem.id == payload["food_item_id"]).one()
        qty = float(payload["quantity_g"])
        calories = (food.calories_per_100g or 0.0) * (qty / 100.0)
        fl = models.FoodLog(
            participant_id=pid,
            food_item_id=food.id,
            quantity_g=qty,
            date=payload.get("date", date.today()),
            calories=calories,
            meal_type=payload.get("meal_type"),
            note=payload.get("note"),
        )
        db.add(fl)
        db.commit()
        db.refresh(fl)
        return jsonify({"id": fl.id, "calories": fl.calories}), 201
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# NEW: Calories-per-participant report endpoint
@app.get("/reports/total_calories_today")
def report_total_calories_today():
    db = SessionLocal()
    today = date.today()
    results = db.query(
        models.Participant.id,
        models.Participant.name,
        func.sum(models.FoodLog.calories)
    ).join(models.FoodLog, models.Participant.id == models.FoodLog.participant_id) \
     .filter(models.FoodLog.date == today) \
     .group_by(models.Participant.id, models.Participant.name).all()
    db.close()
    out = []
    for pid, pname, calories in results:
        out.append({
            "participant_id": pid,
            "name": pname,
            "total_calories": calories or 0
        })
    return jsonify(out)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
