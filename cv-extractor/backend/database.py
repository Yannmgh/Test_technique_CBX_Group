import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données
# Format: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cvextractor:cvextractor123@localhost:5432/cvextractor_db"
)

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la SessionLocal pour les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """
    Générateur de session de base de données.
    Utilisé comme dépendance dans FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()