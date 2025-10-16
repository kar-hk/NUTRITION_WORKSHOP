# shared/models.py
from sqlalchemy import Column, Integer, String, Date, Text, Float, ForeignKey, Boolean, JSON, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base
import enum

class GenderEnum(str, enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date)
    gender = Column(Enum(GenderEnum), default=GenderEnum.other)
    phone = Column(String(20))
    email = Column(String(255))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    plans = relationship('ParticipantPlan', back_populates='participant', cascade='all, delete-orphan')
    measurements = relationship('Measurement', back_populates='participant', cascade='all, delete-orphan')
    food_logs = relationship('FoodLog', back_populates='participant', cascade='all, delete-orphan')

class NutritionPlan(Base):
    __tablename__ = 'nutrition_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    calories_target = Column(Integer)
    created_by = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    assignments = relationship('ParticipantPlan', back_populates='plan')

class ParticipantPlan(Base):
    __tablename__ = 'participant_plans'
    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey('participants.id'))
    nutrition_plan_id = Column(Integer, ForeignKey('nutrition_plans.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    active = Column(Boolean, default=True)

    participant = relationship('Participant', back_populates='plans')
    plan = relationship('NutritionPlan', back_populates='assignments')

class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    calories_per_100g = Column(Float)
    protein_g = Column(Float)
    carbs_g = Column(Float)
    fat_g = Column(Float)
    micronutrients = Column(JSON)

class FoodLog(Base):
    __tablename__ = 'food_logs'
    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey('participants.id'))
    food_item_id = Column(Integer, ForeignKey('food_items.id'))
    date = Column(Date, nullable=False)
    quantity_g = Column(Float, nullable=False)
    calories = Column(Float)
    meal_type = Column(String(50))
    note = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    participant = relationship('Participant', back_populates='food_logs')
    food_item = relationship('FoodItem')

class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey('participants.id'))
    date = Column(Date, nullable=False)
    weight_kg = Column(Float)
    waist_cm = Column(Float)
    bmi = Column(Float)
    note = Column(Text)

    participant = relationship('Participant', back_populates='measurements')
