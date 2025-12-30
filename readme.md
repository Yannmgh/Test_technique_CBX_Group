# 📄 CV Extractor - Application d'Extraction Automatique de CV

Application full-stack Python permettant d'extraire automatiquement les informations d'un CV (PDF ou DOCX) sans utiliser d'IA. L'extraction se fait via des expressions régulières et du parsing de documents.

## Fonctionnalités

- Upload de CV au format **PDF** ou **DOCX**
- Extraction automatique des informations :
  - Prénom et Nom
  - Email
  - Numéro de téléphone
  - Diplôme principal
- Interface web intuitive avec **Streamlit**
- API REST avec **FastAPI**
- Modification des données extraites
- Export au format **JSON**
- **Dockerisation** complète
- Tests unitaires

## Architecture du Projet

```
cv-extractor/
│
├── backend/                      # API FastAPI
│   ├── main.py                   # Point d'entrée de l'API
│   ├── requirements.txt          # Dépendances backend
│   ├── services/                 # Logique métier
│   │   ├── pdf_parser.py         # Extraction texte PDF
│   │   ├── docx_parser.py        # Extraction texte DOCX
│   │   └── extractor.py          # Extraction des informations
│   ├── models/                   # Modèles de données
│   │   └── cv_result.py          # Structure de réponse
│   └── tests/                    # Tests unitaires
│       └── test_extractor.py     # Tests des extracteurs
│
├── frontend/                     # Interface Streamlit
│   ├── app.py                    # Application Streamlit
│   └── requirements.txt          # Dépendances frontend
│
├── docker/                       # Configuration Docker
│   ├── Dockerfile.backend        # Image Docker backend
│   ├── Dockerfile.frontend       # Image Docker frontend
│   └── docker-compose.yml        # Orchestration
│
└── README.md                     # Documentation
```

## Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide
- **Uvicorn** : Serveur ASGI
- **PDFPlumber** : Extraction de texte depuis PDF
- **python-docx** : Extraction de texte depuis DOCX
- **Pydantic** : Validation des données
- **Pytest** : Tests unitaires

### Frontend
- **Streamlit** : Framework pour applications web interactives
- **Requests** : Communication HTTP avec le backend

### DevOps
- **Docker** : Conteneurisation
- **Docker Compose** : Orchestration multi-conteneurs

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Docker et Docker Compose (pour le déploiement Docker)

### Option 1 : Installation Locale

#### 1. Cloner le repository

```bash
git clone <url-du-repo>
cd cv-extractor
```

#### 2. Installer le Backend

```bash
cd backend
pip install -r requirements.txt
```

#### 3. Installer le Frontend

```bash
cd ../frontend
pip install -r requirements.txt
```

### Option 2 : Installation avec Docker

```bash
cd docker
docker-compose up --build
```

## Lancement de l'Application

### Option 1 : Lancement Local

#### Terminal 1 - Backend
```bash
cd backend
python main.py
```

Le backend sera accessible sur : `http://localhost:8000`

#### Terminal 2 - Frontend
```bash
cd frontend
streamlit run app.py
```

Le frontend sera accessible sur : `http://localhost:8501`

### Option 2 : Lancement avec Docker

```bash
cd docker
docker-compose up
```

Les services seront disponibles sur :
- **Backend** : `http://localhost:8000`
- **Frontend** : `http://localhost:8501`

#### Commandes Docker Utiles

```bash
# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Reconstruire les images
docker-compose up --build
```

## Tests

### Lancer les tests unitaires

```bash
cd backend
python -m pytest tests/test_extractor.py -v
```


##  Utilisation de l'API

### Endpoint Principal

**POST** `/api/v1/upload-cv`

#### Exemple avec cURL

```bash
curl -X POST \
  http://localhost:8000/api/v1/upload-cv \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/chemin/vers/cv.pdf"
```

#### Réponse JSON

```json
{
  "first_name": "Yann",
  "last_name": "Houndjo",
  "email": "yannmgh@gmail.com",
  "phone": "0771899574",
  "degree": "Bachelor Développement d'application (Bac+3)"
}
```

### Documentation Interactive

Une fois le backend lancé, accédez à la documentation Swagger :

👉 `http://localhost:8000/docs`

## Interface Utilisateur

### Page d'Upload
1. Sélectionnez un CV (PDF ou DOCX)
2. Cliquez sur "Analyser le CV"
3. Attendez l'extraction

### Page de Résultats
1. Visualisez les informations extraites
2. Modifiez les champs si nécessaire
3. Téléchargez le résultat en JSON

## Méthodologie d'Extraction

L'extraction se fait **SANS IA**, uniquement avec :

### 1. Parsing de Documents
- **PDF** : PDFPlumber extrait le texte brut
- **DOCX** : python-docx lit les paragraphes et tableaux

### 2. Expressions Régulières (Regex)
- **Email** : Pattern standard RFC 5322
- **Téléphone** : Formats français (06, +33, etc.)
- **Nom** : Détection de patterns "Prénom NOM"
- **Diplôme** : Mots-clés (Bachelor, Master, Licence, BTS, etc.)

### 3. Nettoyage du Texte
- Suppression des espaces multiples
- Normalisation des sauts de ligne
- Gestion des caractères spéciaux

## Exemples de CV Supportés

L'application gère différents formats de CV :

✅ CV avec mise en page classique  
✅ CV avec tableaux  
✅ CV multilingues (français/anglais)  
✅ CV avec espaces entre lettres  
✅ Formats téléphone variés (+33, 06, espaces)  

## Résolution des Problèmes

### Le backend ne répond pas

```bash
# Vérifiez que le serveur est lancé
curl http://localhost:8000

# Relancez le backend
cd backend
python main.py
```

### Le frontend ne se connecte pas au backend

Vérifiez que le backend est bien accessible sur `http://localhost:8000`

### Docker : Port déjà utilisé

```bash
# Arrêtez les services locaux si ils tournent
# Terminal backend : Ctrl+C
# Terminal frontend : Ctrl+C

# Puis relancez Docker
docker-compose up
```

### Tests qui échouent

```bash
# Réinstallez les dépendances
cd backend
pip install -r requirements.txt

# Relancez les tests
python -m pytest tests/test_extractor.py -v
```

## 📝 Améliorations Futures

- [ ] Support de plus de formats (TXT, ODT)
- [ ] Extraction de plus d'informations (adresse, compétences)
- [ ] API d'authentification
- [ ] Base de données pour stocker les résultats
- [ ] Interface d'administration
- [ ] Export en CSV/Excel
- [ ] Multi-langue (interface en anglais)


## 🙏 Remerciements

Projet réalisé dans le cadre d'un exercice technique de développement Full Stack Python.

---

