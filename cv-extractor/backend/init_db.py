"""
Script pour initialiser la base de données.
Crée toutes les tables définies dans les modèles.
"""
from database import engine, Base
from models.cv_database import CVExtraction

def init_database():
    """Crée toutes les tables dans la base de données"""
    print("🔧 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print(" Tables créées avec succès !")

if __name__ == "__main__":
    init_database()