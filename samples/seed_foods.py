# samples/seed_foods.py
from shared.db import SessionLocal, engine, Base
import shared.models as models
Base.metadata.create_all(bind=engine)
db = SessionLocal()
foods = [
    dict(name='Rice (cooked)', calories_per_100g=130.0, protein_g=2.7, carbs_g=28.0, fat_g=0.3),
    dict(name='Chicken breast (cooked)', calories_per_100g=165.0, protein_g=31.0, carbs_g=0.0, fat_g=3.6)
]
for f in foods:
    fi = models.FoodItem(**f)
    db.add(fi)
db.commit()
print('Seeded', len(foods), 'food items')
