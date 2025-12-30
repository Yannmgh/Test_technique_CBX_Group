import sys
import os
from pathlib import Path

# Configure le PYTHONPATH AVANT tous les autres imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import des services et modèles
from services.pdf_parser import extract_text_from_pdf, clean_text as clean_pdf_text
from services.docx_parser import extract_text_from_docx, clean_text as clean_docx_text
from services.extractor import extract_cv_info
from models.cv_result import CVResult
from models.cv_database import CVExtraction
from database import get_db, engine, Base

# Crée les tables au démarrage
Base.metadata.create_all(bind=engine)

# Création de l'application FastAPI
app = FastAPI(
    title="CV Extractor API",
    description="API pour extraire automatiquement les informations d'un CV",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossier temporaire pour stocker les fichiers uploadés
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Endpoint racine pour vérifier que l'API fonctionne"""
    return {
        "message": "CV Extractor API is running!",
        "version": "2.0.0",
        "database": "PostgreSQL",
        "endpoints": {
            "upload": "/api/v1/upload-cv",
            "history": "/api/v1/history",
            "docs": "/docs"
        }
    }


@app.post("/api/v1/upload-cv", response_model=CVResult)
async def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Endpoint principal pour uploader et analyser un CV"""
    
    # 1. Validation du fichier
    if not file.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")
    
    file_extension = file.filename.split(".")[-1].lower()
    
    if file_extension not in ["pdf", "docx"]:
        raise HTTPException(
            status_code=400,
            detail=f"Format de fichier non supporté. Utilisez PDF ou DOCX. Reçu: {file_extension}"
        )
    
    # 2. Sauvegarde temporaire du fichier
    file_path = UPLOAD_DIR / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la sauvegarde du fichier: {str(e)}"
        )
    
    # 3. Extraction du texte selon le format
    try:
        if file_extension == "pdf":
            raw_text = extract_text_from_pdf(str(file_path))
            cleaned_text = clean_pdf_text(raw_text)
        else:  # docx
            raw_text = extract_text_from_docx(str(file_path))
            cleaned_text = clean_docx_text(raw_text)
        
        if not cleaned_text:
            raise ValueError("Aucun texte extrait du fichier")
            
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction du texte: {str(e)}"
        )
    
    # 4. Extraction des informations
    try:
        cv_data = extract_cv_info(cleaned_text)
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction des informations: {str(e)}"
        )
    
    # 5. Nettoyage : supprime le fichier temporaire
    try:
        if file_path.exists():
            os.remove(file_path)
    except Exception:
        pass
    
    # 6. Sauvegarde dans la base de données
    try:
        cv_entry = CVExtraction(
            first_name=cv_data.get("first_name"),
            last_name=cv_data.get("last_name"),
            email=cv_data.get("email"),
            phone=cv_data.get("phone"),
            degree=cv_data.get("degree"),
            filename=file.filename
        )
        db.add(cv_entry)
        db.commit()
        db.refresh(cv_entry)
        print(f"✅ CV sauvegardé en base de données (ID: {cv_entry.id})")
    except Exception as e:
        print(f"⚠️ Erreur lors de la sauvegarde en BDD : {str(e)}")
    
    # 7. Retourne le résultat
    return CVResult(**cv_data)


@app.get("/api/v1/history")
async def get_history(limit: int = 50, db: Session = Depends(get_db)):
    """Récupère l'historique des CV extraits"""
    try:
        cv_list = db.query(CVExtraction).order_by(
            CVExtraction.created_at.desc()
        ).limit(limit).all()
        
        return {
            "count": len(cv_list),
            "data": [cv.to_dict() for cv in cv_list]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de l'historique: {str(e)}"
        )


@app.delete("/api/v1/history/{cv_id}")
async def delete_cv(cv_id: int, db: Session = Depends(get_db)):
    """Supprime un CV de l'historique"""
    try:
        cv_entry = db.query(CVExtraction).filter(CVExtraction.id == cv_id).first()
        
        if not cv_entry:
            raise HTTPException(status_code=404, detail="CV non trouvé")
        
        db.delete(cv_entry)
        db.commit()
        
        return {"message": f"CV {cv_id} supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Endpoint de santé"""
    return {
        "status": "healthy",
        "service": "cv-extractor-backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )