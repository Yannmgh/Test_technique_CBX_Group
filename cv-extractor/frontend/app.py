import streamlit as st
import requests
import json
import os
from typing import Optional, Dict, List
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="CV Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Désactive la traduction automatique du navigateur
st.markdown("""
    <meta name="google" content="notranslate">
    <meta http-equiv="Content-Language" content="fr">
""", unsafe_allow_html=True)

# URLs de l'API
BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000").replace("/api/v1/upload-cv", "")
UPLOAD_URL = f"{BASE_URL}/api/v1/upload-cv"
HISTORY_URL = f"{BASE_URL}/api/v1/history"

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin: 20px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #d1ecf1;
        border-radius: 5px;
        border-left: 5px solid #17a2b8;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)


def upload_cv_to_backend(file) -> Optional[Dict]:
    """Envoie le fichier CV au backend"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(UPLOAD_URL, files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API : {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error(f" Impossible de se connecter au backend. Vérifiez que le serveur est lancé sur {BASE_URL}")
        return None
    except Exception as e:
        st.error(f" Erreur lors de l'envoi du fichier : {str(e)}")
        return None


def get_history() -> Optional[List[Dict]]:
    """Récupère l'historique des CV"""
    try:
        response = requests.get(HISTORY_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            st.error(f"Erreur lors de la récupération de l'historique : {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error(f" Impossible de se connecter au backend sur {HISTORY_URL}")
        return None
    except Exception as e:
        st.error(f" Erreur : {str(e)}")
        return None


def delete_cv_from_history(cv_id: int) -> bool:
    """Supprime un CV de l'historique"""
    try:
        response = requests.delete(f"{HISTORY_URL}/{cv_id}", timeout=10)
        return response.status_code == 200
    except Exception as e:
        st.error(f" Erreur lors de la suppression : {str(e)}")
        return False


def display_results_page(cv_data: Dict):
    """Page de résultats avec les données extraites"""
    st.cache_data.clear()
    
    st.markdown('<p class="main-title"> Résultats de l\'extraction</p>', unsafe_allow_html=True)
    st.markdown('<div class="success-box"> Le CV a été analysé avec succès et sauvegardé dans la base de données !</div>', unsafe_allow_html=True)
    
    st.markdown("###  Informations extraites (modifiables)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("Prénom", value=cv_data.get("first_name", ""), key="first_name_input")
        email = st.text_input("Email", value=cv_data.get("email", ""), key="email_input")
        degree = st.text_input("Diplôme principal", value=cv_data.get("degree", ""), key="degree_input")
    
    with col2:
        last_name = st.text_input("Nom", value=cv_data.get("last_name", ""), key="last_name_input")
        phone = st.text_input("Téléphone", value=cv_data.get("phone", ""), key="phone_input")
    
    final_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "degree": degree
    }
    
    st.markdown("---")
    st.markdown("### Aperçu des données")
    st.info("ℹ️ Cet aperçu reflète les données actuelles des champs ci-dessus.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(" Prénom", first_name if first_name else "Non renseigné")
        st.metric(" Email", email if email else "Non renseigné")
    
    with col2:
        st.metric(" Nom", last_name if last_name else "Non renseigné")
        st.metric(" Téléphone", phone if phone else "Non renseigné")
    
    with col3:
        degree_display = degree if len(degree) <= 50 else degree[:47] + "..."
        st.metric(" Diplôme", degree_display if degree else "Non renseigné")
    
    st.markdown("---")
    st.markdown("###  Export des données")
    
    json_data = json.dumps(final_data, indent=2, ensure_ascii=False)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.download_button(
            label=" Télécharger en JSON",
            data=json_data,
            file_name="cv_extracted_data.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.markdown("---")
    if st.button("🔄 Analyser un nouveau CV", use_container_width=True):
        st.session_state.cv_data = None
        st.session_state.page = "upload"
        st.rerun()


def display_upload_page():
    """Page d'upload de CV"""
    st.markdown('<p class="main-title">📄 Extracteur Automatique de CV</p>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">🔍 Uploadez votre CV au format PDF ou DOCX pour extraire automatiquement les informations principales.</div>', unsafe_allow_html=True)
    
    st.markdown("### 📤 Sélectionnez votre CV")
    
    uploaded_file = st.file_uploader("Choisissez un fichier", type=["pdf", "docx"], help="Formats acceptés : PDF, DOCX")
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"📁 Nom : {uploaded_file.name}")
        with col2:
            st.info(f"📊 Taille : {uploaded_file.size / 1024:.2f} KB")
        with col3:
            st.info(f"📋 Type : {uploaded_file.type}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button(" Analyser le CV", use_container_width=True, type="primary"):
                with st.spinner(" Analyse en cours..."):
                    cv_data = upload_cv_to_backend(uploaded_file)
                    
                    if cv_data:
                        st.session_state.cv_data = cv_data
                        st.session_state.page = "results"
                        st.success(" Analyse terminée !")
                        st.rerun()


def display_history_page():
    """Page d'historique des CV analysés"""
    st.markdown('<p class="main-title">📚 Historique des CV Analysés</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.rerun()
    
    history = get_history()
    
    if history is None:
        st.warning(" Impossible de récupérer l'historique")
        return
    
    if len(history) == 0:
        st.info(" Aucun CV analysé pour le moment. Commencez par uploader un CV !")
        return
    
    st.success(f" {len(history)} CV analysé(s)")
    
    # Affichage sous forme de tableau
    for cv in history:
        with st.expander(
            f" {cv['first_name']} {cv['last_name']} - {cv['filename']} - {datetime.fromisoformat(cv['created_at']).strftime('%d/%m/%Y %H:%M')}"
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Prénom :** {cv['first_name']}")
                st.write(f"**Nom :** {cv['last_name']}")
                st.write(f"**Email :** {cv['email']}")
            
            with col2:
                st.write(f"**Téléphone :** {cv['phone']}")
                st.write(f"**Diplôme :** {cv['degree']}")
                st.write(f"**Date d'analyse :** {datetime.fromisoformat(cv['created_at']).strftime('%d/%m/%Y à %H:%M:%S')}")
            
            # Bouton de suppression
            if st.button(f" Supprimer", key=f"delete_{cv['id']}"):
                if delete_cv_from_history(cv['id']):
                    st.success(" CV supprimé !")
                    st.rerun()
                else:
                    st.error(" Erreur lors de la suppression")


def main():
    """Fonction principale avec menu de navigation"""
    
    # Initialise l'état de session
    if "cv_data" not in st.session_state:
        st.session_state.cv_data = None
    if "page" not in st.session_state:
        st.session_state.page = "upload"
    
    # Menu latéral
    with st.sidebar:
        st.title(" CV Extractor")
        st.markdown("---")
        
        menu = st.radio(
            "Navigation",
            [" Analyser un CV", "📚 Historique"],
            key="menu"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ À propos")
        st.info("Application d'extraction automatique d'informations depuis des CV (PDF/DOCX)")
        st.markdown("**Version :** 2.0")
        st.markdown("**Backend :** FastAPI + PostgreSQL")
        st.markdown("**Frontend :** Streamlit")
    
    # Gestion de la navigation
    if menu == " Analyser un CV":
        if st.session_state.cv_data is None:
            display_upload_page()
        else:
            display_results_page(st.session_state.cv_data)
    elif menu == "📚 Historique":
        display_history_page()
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>CV Extractor v2.0 | Développé avec ❤️ en Python | Avec PostgreSQL</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()