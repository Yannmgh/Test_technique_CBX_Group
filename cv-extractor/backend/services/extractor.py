import re
from typing import Optional, Dict


def extract_email(text: str) -> Optional[str]:
    """
    Extrait l'adresse email du texte.
    
    Args:
        text: Le texte du CV
        
    Returns:
        L'email trouvé ou None
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    match = re.search(email_pattern, text)
    
    if match:
        return match.group(0)
    
    return None


def extract_phone(text: str) -> Optional[str]:
    """
    Extrait le numéro de téléphone du texte.
    Supporte les formats français et internationaux.
    
    Args:
        text: Le texte du CV
        
    Returns:
        Le téléphone trouvé ou None
    """
    phone_patterns = [
        r'\+33\s?[1-9](?:\s?\d{2}){4}',
        r'0[1-9](?:\s?\d{2}){4}',
        r'\+33[1-9]\d{8}',
        r'0[1-9]\d{8}',
        r'\(\+33\)\s?[1-9](?:\s?\d{2}){4}',
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            phone = match.group(0).replace(" ", "")
            return phone
    
    return None


def clean_spaced_text(text: str) -> str:
    """
    Nettoie les textes avec espaces entre chaque lettre.
    Exemple: "Y a n n" -> "Yann"
    
    Args:
        text: Texte avec espaces
        
    Returns:
        Texte nettoyé
    """
    cleaned = re.sub(r'(?<=[A-ZÀ-Ÿa-zà-ÿ])\s+(?=[A-ZÀ-Ÿa-zà-ÿ](?:\s|$))', '', text)
    return cleaned


def extract_name(text: str) -> Dict[str, Optional[str]]:
    """
    Tente d'extraire le nom et prénom du texte.
    Amélioration: gère les noms avec espaces entre lettres et les PDF sur une seule ligne.
    
    Args:
        text: Le texte du CV
        
    Returns:
        Dictionnaire avec first_name et last_name
    """
    result = {
        "first_name": None,
        "last_name": None
    }
    
    # DEBUG: Affiche le début du texte
    print("=== DEBUG: Début du CV (200 premiers caractères) ===")
    print(text[:200])
    print("=" * 50)
    
    # Stratégie 1: Chercher "Prénom NOM" au tout début du texte (500 premiers caractères)
    text_start = text[:500]
    
    name_pattern = r'\b([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]{2,})\s+([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ]{2,})\b'
    match = re.search(name_pattern, text_start)
    
    if match:
        print(f" Nom trouvé au début du texte: {match.group(1)} {match.group(2)}")
        result["first_name"] = match.group(1)
        result["last_name"] = match.group(2).capitalize()
        return result
    
    # Stratégie 2: Si échec, essayer avec les lignes
    lines = text.split("\n")[:15]
    
    for line in lines:
        line = line.strip()
        
        if len(line) < 3:
            continue
        
        if len(line) > 200:
            line = line[:200]
        
        cleaned_line = clean_spaced_text(line)
        
        name_pattern1 = r'^([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+)\s+([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇa-zàâäéèêëïîôùûüç]+)'
        match = re.search(name_pattern1, cleaned_line)
        
        if match:
            print(f" Nom trouvé avec pattern 1: {match.group(1)} {match.group(2)}")
            result["first_name"] = match.group(1)
            result["last_name"] = match.group(2)
            return result
        
        name_pattern2 = r'^([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ]{2,})\s+([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ]{2,})'
        match = re.search(name_pattern2, cleaned_line)
        
        if match:
            print(f" Nom trouvé avec pattern 2: {match.group(1)} {match.group(2)}")
            result["first_name"] = match.group(1).capitalize()
            result["last_name"] = match.group(2).capitalize()
            return result
    
    print(" Aucun nom trouvé")
    return result


def extract_degree(text: str) -> Optional[str]:
    """
    Extrait le diplôme principal du texte.
    Amélioration: meilleure détection des diplômes français.
    
    Args:
        text: Le texte du CV
        
    Returns:
        Le diplôme trouvé ou None
    """
    degree_patterns = [
        r'Bachelor\s+[^\n.;]{3,80}(?:\(Bac\+\d\))?',
        r'Master\s+[^\n.;]{3,80}(?:\(Bac\+\d\))?',
        r'Licence\s+(?:professionnelle\s+)?[^\n.;]{3,80}',
        r'Doctorat\s+(?:en\s+)?[^\n.;]{3,80}',
        r'Ingénieur\s+[^\n.;]{3,80}',
        r"Diplôme\s+d['']ingénieur\s+[^\n.;]{3,80}",
        r'MBA\s+[^\n.;]{0,50}',
        r'BTS\s+[^\n.;]{3,60}',
        r'DUT\s+[^\n.;]{3,60}',
        r'BUT\s+[^\n.;]{3,60}',
        r'Bac\+\d\s+en\s+[^\n.;]{3,80}',
        r'BAC\+\d\s+en\s+[^\n.;]{3,80}',
        r'Certificat\s+[^\n.;]{3,60}',
    ]
    
    found_degrees = []
    
    for pattern in degree_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            degree = match.group(0).strip()
            degree = re.sub(r'[,;:\s]+$', '', degree)
            
            if degree.endswith((' à', ' de', ' en', ' l')):
                extended_pattern = re.escape(degree) + r'\s*[\w\s]{0,30}'
                extended_match = re.search(extended_pattern, text, re.IGNORECASE)
                if extended_match:
                    degree = extended_match.group(0).strip()
            
            if len(degree) > 120:
                degree = degree[:120].rsplit(' ', 1)[0]
            
            if degree not in found_degrees and len(degree) > 5:
                found_degrees.append(degree)
    
    if found_degrees:
        print(f" Diplômes trouvés: {found_degrees}")
        return found_degrees[0]
    
    simple_patterns = [
        r'Bac\+\d',
        r'BAC\+\d',
        r'Baccalauréat\s+\w+',
        r'Baccalauréat',
    ]
    
    for pattern in simple_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def extract_cv_info(text: str) -> Dict[str, Optional[str]]:
    """
    Fonction principale qui extrait toutes les informations du CV.
    
    Args:
        text: Le texte brut du CV
        
    Returns:
        Dictionnaire avec toutes les informations extraites
    """
    email = extract_email(text)
    phone = extract_phone(text)
    name_info = extract_name(text)
    degree = extract_degree(text)
    
    return {
        "first_name": name_info["first_name"] or "Non trouvé",
        "last_name": name_info["last_name"] or "Non trouvé",
        "email": email or "Non trouvé",
        "phone": phone or "Non trouvé",
        "degree": degree or "Non trouvé"
    }