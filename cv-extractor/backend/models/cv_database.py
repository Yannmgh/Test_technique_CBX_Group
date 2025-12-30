from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import sys
from pathlib import Path

# Ajoute le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Base


class CVExtraction(Base):
    """
    Modèle de table pour stocker les extractions de CV.
    """
    __tablename__ = "cv_extractions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(50))
    degree = Column(String(500))
    filename = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CVExtraction(id={self.id}, name={self.first_name} {self.last_name})>"
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "degree": self.degree,
            "filename": self.filename,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }