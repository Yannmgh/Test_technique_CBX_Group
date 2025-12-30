from pydantic import BaseModel, Field
from typing import Optional


class CVResult(BaseModel):
    """
    Modèle de données pour le résultat d'extraction d'un CV.
    
    Attributes:
        first_name: Prénom extrait du CV
        last_name: Nom de famille extrait du CV
        email: Adresse email extraite
        phone: Numéro de téléphone extrait
        degree: Diplôme principal extrait
    """
    first_name: Optional[str] = Field(
        default="Non trouvé",
        description="Prénom du candidat"
    )
    last_name: Optional[str] = Field(
        default="Non trouvé",
        description="Nom de famille du candidat"
    )
    email: Optional[str] = Field(
        default="Non trouvé",
        description="Adresse email du candidat"
    )
    phone: Optional[str] = Field(
        default="Non trouvé",
        description="Numéro de téléphone du candidat"
    )
    degree: Optional[str] = Field(
        default="Non trouvé",
        description="Diplôme principal du candidat"
    )

    class Config:
        """Configuration du modèle Pydantic"""
        json_schema_extra = {
            "example": {
                "first_name": "Alain",
                "last_name": "Bernard",
                "email": "alain.bernard@gmail.com",
                "phone": "+33612345678",
                "degree": "Master Informatique"
            }
        }