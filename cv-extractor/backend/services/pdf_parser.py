import pdfplumber
from typing import Optional


def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    Extrait le texte brut d'un fichier PDF.
    
    Args:
        file_path: Chemin vers le fichier PDF
        
    Returns:
        Le texte extrait ou None si erreur
        
    Raises:
        Exception: Si le fichier ne peut pas être lu
    """
    try:
        text = ""
        
        # Ouvre le PDF avec pdfplumber
        with pdfplumber.open(file_path) as pdf:
            # Parcourt toutes les pages
            for page in pdf.pages:
                # Extrait le texte de chaque page
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Vérifie qu'on a bien extrait du texte
        if not text.strip():
            raise ValueError("Le PDF ne contient pas de texte extractible")
            
        return text
        
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction du PDF : {str(e)}")


def clean_text(text: str) -> str:
    """
    Nettoie le texte extrait :
    - Supprime les espaces multiples
    - Supprime les sauts de ligne excessifs
    - Normalise les espaces
    
    Args:
        text: Le texte brut à nettoyer
        
    Returns:
        Le texte nettoyé
    """
    if not text:
        return ""
    
    # Remplace les multiples espaces par un seul
    text = " ".join(text.split())
    
    # Remplace les multiples sauts de ligne par un seul
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    text = "\n".join(lines)
    
    return text