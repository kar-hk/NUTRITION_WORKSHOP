# flask_app/db.py
from sqlalchemy import create_engine  # core engine [web:143]
from sqlalchemy.orm import sessionmaker, declarative_base  # ORM base/session [web:143]

# Use your existing MySQL URL; adjust user/pass/port as needed.
DATABASE_URL = "mysql+mysqlconnector://nw_user:StrongPwd!23@localhost/nutrition_workshop"  # same as earlier

# Create the SQLAlchemy engine (pooled connection to MySQL)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)  # robust engine [web:42][web:143]

# Declarative Base for your models to inherit from
Base = declarative_base()  # models.Base [web:143]

# Session factory for request-scoped DB sessions
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)  # session factory [web:42][web:143]
