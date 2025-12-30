import sys
from pathlib import Path

# Ajoute le dossier backend au path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from services.extractor import (
    extract_email,
    extract_phone,
    extract_name,
    extract_degree,
    extract_cv_info
)


class TestExtractEmail:
    """Tests pour l'extraction d'email"""
    
    def test_email_simple(self):
        """Test avec un email simple"""
        text = "Contactez-moi à john.doe@example.com pour plus d'infos"
        result = extract_email(text)
        assert result == "john.doe@example.com"
    
    def test_email_avec_chiffres(self):
        """Test avec un email contenant des chiffres"""
        text = "Mon email : user123@domain456.com"
        result = extract_email(text)
        assert result == "user123@domain456.com"
    
    def test_email_avec_tirets(self):
        """Test avec un email contenant des tirets"""
        text = "Email professionnel: jean-pierre@mon-entreprise.fr"
        result = extract_email(text)
        assert result == "jean-pierre@mon-entreprise.fr"
    
    def test_email_absent(self):
        """Test sans email dans le texte"""
        text = "Aucun email ici, juste du texte"
        result = extract_email(text)
        assert result is None
    
    def test_email_gmail(self):
        """Test avec un email Gmail"""
        text = "yannmgh@gmail.com"
        result = extract_email(text)
        assert result == "yannmgh@gmail.com"


class TestExtractPhone:
    """Tests pour l'extraction de numéro de téléphone"""
    
    def test_phone_format_international(self):
        """Test avec format international +33"""
        text = "Appelez-moi au +33612345678"
        result = extract_phone(text)
        assert result == "+33612345678"
    
    def test_phone_format_francais(self):
        """Test avec format français 06"""
        text = "Mon numéro : 0612345678"
        result = extract_phone(text)
        assert result == "0612345678"
    
    def test_phone_avec_espaces(self):
        """Test avec espaces entre les chiffres"""
        text = "Téléphone : 06 12 34 56 78"
        result = extract_phone(text)
        assert result == "0612345678"
    
    def test_phone_format_international_espaces(self):
        """Test format international avec espaces"""
        text = "+33 6 12 34 56 78"
        result = extract_phone(text)
        assert result == "+33612345678"
    
    def test_phone_absent(self):
        """Test sans numéro de téléphone"""
        text = "Pas de téléphone ici"
        result = extract_phone(text)
        assert result is None
    
    def test_phone_reel(self):
        """Test avec un numéro réel"""
        text = "0771899574"
        result = extract_phone(text)
        assert result == "0771899574"


class TestExtractName:
    """Tests pour l'extraction du nom et prénom"""
    
    def test_name_format_standard(self):
        """Test avec format Prénom NOM"""
        text = "Yann HOUNDJO\nDéveloppeur Full Stack"
        result = extract_name(text)
        assert result["first_name"] == "Yann"
        assert result["last_name"] == "Houndjo"
    
    def test_name_majuscules(self):
        """Test avec nom tout en majuscules"""
        text = "JEAN DUPONT\nIngénieur"
        result = extract_name(text)
        assert result["first_name"] == "Jean"
        assert result["last_name"] == "Dupont"
    
    def test_name_accent(self):
        """Test avec accents"""
        text = "François LÉGER\nConsultant"
        result = extract_name(text)
        assert result["first_name"] == "François"
        assert result["last_name"] in ["Léger", "LÉGER"]
    
    def test_name_absent(self):
        """Test sans nom détectable"""
        text = "123456 Développeur Senior"
        result = extract_name(text)
        assert result["first_name"] is None
        assert result["last_name"] is None


class TestExtractDegree:
    """Tests pour l'extraction du diplôme"""
    
    def test_degree_bachelor(self):
        """Test avec un Bachelor"""
        text = "Bachelor Développement d'application (Bac+3)"
        result = extract_degree(text)
        assert result is not None
        assert "Bachelor" in result
    
    def test_degree_master(self):
        """Test avec un Master"""
        text = "Master en Intelligence Artificielle"
        result = extract_degree(text)
        assert result is not None
        assert "Master" in result
    
    def test_degree_bts(self):
        """Test avec un BTS"""
        text = "BTS Informatique et Réseaux"
        result = extract_degree(text)
        assert result is not None
        assert "BTS" in result
    
    def test_degree_licence(self):
        """Test avec une Licence"""
        text = "Licence professionnelle en Développement Web"
        result = extract_degree(text)
        assert result is not None
        assert "Licence" in result
    
    def test_degree_bac_plus(self):
        """Test avec format Bac+X"""
        text = "Bac+5 en Informatique"
        result = extract_degree(text)
        assert result is not None
        assert "Bac" in result or "BAC" in result
    
    def test_degree_absent(self):
        """Test sans diplôme"""
        text = "Expérience professionnelle : 5 ans"
        result = extract_degree(text)
        # Peut retourner None ou un résultat vide selon l'implémentation
        assert result is None or result == ""


class TestExtractCVInfo:
    """Tests d'intégration pour l'extraction complète"""
    
    def test_cv_complet(self):
        """Test avec un CV complet"""
        text = """
        Yann HOUNDJO
        Développeur Full Stack
        
        Email : yannmgh@gmail.com
        Téléphone : 0771899574
        
        Formation :
        Bachelor Développement d'application (Bac+3)
        ECE Paris Tech
        """
        
        result = extract_cv_info(text)
        
        assert result["first_name"] == "Yann"
        assert result["last_name"] == "Houndjo"
        assert result["email"] == "yannmgh@gmail.com"
        assert result["phone"] == "0771899574"
        assert "Bachelor" in result["degree"]
    
    def test_cv_incomplet(self):
        """Test avec un CV incomplet"""
        text = """
        Contact : john@example.com
        Téléphone : 0612345678
        """
        
        result = extract_cv_info(text)
        
        assert result["email"] == "john@example.com"
        assert result["phone"] == "0612345678"
        assert result["first_name"] == "Non trouvé"
        assert result["last_name"] == "Non trouvé"
        assert result["degree"] == "Non trouvé"
    
    def test_cv_vide(self):
        """Test avec un texte vide"""
        text = ""
        
        result = extract_cv_info(text)
        
        assert result["first_name"] == "Non trouvé"
        assert result["last_name"] == "Non trouvé"
        assert result["email"] == "Non trouvé"
        assert result["phone"] == "Non trouvé"
        assert result["degree"] == "Non trouvé"


if __name__ == "__main__":
    # Lance les tests avec pytest
    pytest.main([__file__, "-v"])