# CV Extractor - Application d'Extraction Automatique de CV

Application full-stack Python permettant d'extraire automatiquement les informations d'un CV (PDF ou DOCX) sans utiliser d'IA. L'extraction se fait via des expressions régulières et du parsing de documents, avec **sauvegarde en base de données PostgreSQL** et **gestion d'historique**.

## Fonctionnalités

### Extraction de CV
- Upload de CV au format **PDF** ou **DOCX**
- Extraction automatique des informations :
  - Prénom et Nom
  - Email
  - Numéro de téléphone
  - Diplôme principal
- Modification des données extraites
- Export au format **JSON**

### Base de données & Historique
- **Sauvegarde automatique** en base de données PostgreSQL
- **Historique complet** des CV analysés
- **Consultation de l'historique** avec date et heure
- **Suppression** de CV de l'historique
- **Persistance des données** via Docker volumes

### Interface & API
- Interface web intuitive avec **Streamlit**
- **Menu de navigation** avec sidebar
- API REST avec **FastAPI**
- Documentation API interactive (Swagger)
- **Dockerisation** complète
- Tests unitaires

## Architecture du Projet

```
cv-extractor/
│
├── backend/                      # API FastAPI
│   ├── main.py                   # Point d'entrée de l'API
│   ├── database.py               # Configuration SQLAlchemy
│   ├── init_db.py                # Script d'initialisation BDD
│   ├── requirements.txt          # Dépendances backend
│   ├── services/                 # Logique métier
│   │   ├── pdf_parser.py         # Extraction texte PDF
│   │   ├── docx_parser.py        # Extraction texte DOCX
│   │   └── extractor.py          # Extraction des informations
│   ├── models/                   # Modèles de données
│   │   ├── cv_result.py          # Structure de réponse API
│   │   └── cv_database.py        # Modèle SQLAlchemy
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
│   └── docker-compose.yml        # Orchestration (3 services)
│
├── .env.example                  # Variables d'environnement
└── README.md                     # Documentation
```

## Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide
- **Uvicorn** : Serveur ASGI
- **SQLAlchemy** : ORM pour la base de données
- **PostgreSQL** : Base de données relationnelle
- **PDFPlumber** : Extraction de texte depuis PDF
- **python-docx** : Extraction de texte depuis DOCX
- **Pydantic** : Validation des données
- **Pytest** : Tests unitaires

### Frontend
- **Streamlit** : Framework pour applications web interactives
- **Requests** : Communication HTTP avec le backend
- **Pandas** : Manipulation de données (optionnel)

### DevOps
- **Docker** : Conteneurisation
- **Docker Compose** : Orchestration multi-conteneurs
- **PostgreSQL** : Base de données en container

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Docker et Docker Compose (pour le déploiement Docker)
- PostgreSQL (pour l'installation locale)

### Option 1 : Installation Locale

#### 1. Cloner le repository

```bash
git clone <url-du-repo>
cd cv-extractor
```

#### 2. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env si nécessaire
```

#### 3. Installer PostgreSQL

```bash

# Créer la base de données
createdb cvextractor_db
```

#### 4. Installer le Backend

```bash
cd backend
pip install -r requirements.txt

# Initialiser la base de données
python init_db.py
```

#### 5. Installer le Frontend

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

#### Terminal 1 - PostgreSQL
Assurez-vous que PostgreSQL est démarré avec la base `cvextractor_db`.

#### Terminal 2 - Backend
```bash
cd backend
python main.py
```

Le backend sera accessible sur : `http://localhost:8000`

#### Terminal 3 - Frontend
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
- **Frontend** : `http://localhost:8501`
- **Backend API** : `http://localhost:8000`
- **PostgreSQL** : `localhost:5432`
- **pgAdmin** (si ajouté) : `http://localhost:5050`


## Tests

### Lancer les tests unitaires

```bash
cd backend
python -m pytest tests/test_extractor.py -v
```


## Accès à la Base de Données

### Ligne de commande

```bash
# Se connecter à PostgreSQL
docker exec -it cv-extractor-postgres psql -U cvextractor -d cvextractor_db
```

Commandes SQL utiles :
```sql
-- Voir la structure de la table
\d cv_extractions

-- Voir tous les CV
SELECT * FROM cv_extractions;

-- Supprimer un CV
DELETE FROM cv_extractions WHERE id = 1;

-- Quitter
\q
```

## Utilisation de l'API

### Endpoints Disponibles

#### 1. Upload et analyse de CV
**POST** `/api/v1/upload-cv`

```bash
curl -X POST \
  http://localhost:8000/api/v1/upload-cv \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/chemin/vers/cv.pdf"
```

**Réponse :**
```json
{
  "first_name": "Yann",
  "last_name": "Houndjo",
  "email": "yannmgh@gmail.com",
  "phone": "0771899574",
  "degree": "Bachelor Développement d'application (Bac+3)"
}
```

#### 2. Récupérer l'historique
**GET** `/api/v1/history?limit=50`

```bash
curl http://localhost:8000/api/v1/history
```

**Réponse :**
```json
{
  "count": 3,
  "data": [
    {
      "id": 1,
      "first_name": "Yann",
      "last_name": "Houndjo",
      "email": "yannmgh@gmail.com",
      "phone": "0771899574",
      "degree": "Bachelor CDA",
      "filename": "cv.pdf",
      "created_at": "2025-12-30T10:58:35.707889"
    }
  ]
}
```

#### 3. Supprimer un CV
**DELETE** `/api/v1/history/{cv_id}`

```bash
curl -X DELETE http://localhost:8000/api/v1/history/1
```

**Réponse :**
```json
{
  "message": "CV 1 supprimé avec succès"
}
```

### Documentation Interactive

Une fois le backend lancé, accédez à la documentation Swagger :

 `http://localhost:8000/docs`

## Interface Utilisateur

### Page d'Upload
1. Cliquez sur " Analyser un CV" dans le menu latéral
2. Sélectionnez un CV (PDF ou DOCX)
3. Cliquez sur " Analyser le CV"
4. Attendez l'extraction (quelques secondes)

### Page de Résultats
1. Visualisez les informations extraites
2. Modifiez les champs si nécessaire
3. Consultez l'aperçu en temps réel
4. Téléchargez le résultat en JSON

### Page d'Historique
1. Cliquez sur " Historique" dans le menu latéral
2. Consultez tous les CV analysés
3. Cliquez sur un CV pour voir les détails
4. Utilisez le bouton  pour supprimer un CV
5. Cliquez sur pour rafraîchir la liste

## Méthodologie d'Extraction

L'extraction se fait **SANS IA**, uniquement avec :

### 1. Parsing de Documents
- **PDF** : PDFPlumber extrait le texte brut
- **DOCX** : python-docx lit les paragraphes et tableaux

### 2. Expressions Régulières (Regex)
- **Email** : Pattern standard RFC 5322
- **Téléphone** : Formats français (06, +33, 0033, espaces)
- **Nom** : Détection de patterns "Prénom NOM" avec gestion des espaces
- **Diplôme** : Mots-clés (Bachelor, Master, Licence, BTS, DUT, BUT, Ingénieur, etc.)

### 3. Nettoyage du Texte
- Suppression des espaces multiples
- Normalisation des sauts de ligne
- Gestion des caractères spéciaux et accents
- Gestion des PDF sur une seule ligne

## Base de Données

### Schéma de la table `cv_extractions`

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | Clé primaire auto-incrémentée |
| first_name | VARCHAR(100) | Prénom extrait |
| last_name | VARCHAR(100) | Nom extrait |
| email | VARCHAR(255) | Email extrait |
| phone | VARCHAR(50) | Téléphone extrait |
| degree | VARCHAR(500) | Diplôme extrait |
| filename | VARCHAR(255) | Nom du fichier uploadé |
| created_at | TIMESTAMP | Date et heure d'analyse |


## Améliorations Futures

### Fonctionnalités
- [ ] Extraction de plus d'informations (adresse, compétences, expériences)
- [ ] Support de plus de formats (TXT, ODT, RTF)
- [ ] Extraction multilingue (anglais, espagnol, etc.)
- [ ] Détection automatique de la langue du CV
- [ ] Score de qualité du CV
- [ ] Export en CSV/Excel de l'historique
- [ ] Recherche et filtres dans l'historique
- [ ] Statistiques et dashboards

### Technique
- [ ] API d'authentification (JWT)
- [ ] Rate limiting sur l'API
- [ ] Upload multiple de CV
- [ ] Traitement asynchrone (Celery + Redis)
- [ ] Cache Redis pour les résultats
- [ ] Optimisation des regex
- [ ] Migration vers FastAPI avec async/await complet
- [ ] API GraphQL en alternative à REST

### DevOps
- [ ] CI/CD avec GitHub Actions
- [ ] Monitoring avec Prometheus + Grafana
- [ ] Logs centralisés avec ELK Stack
- [ ] Backups automatiques de la base de données
- [ ] Déploiement sur AWS/GCP/Azure
- [ ] Kubernetes pour l'orchestration
- [ ] HTTPS avec certificats SSL


**Technologies utilisées :**
- Python 3.11
- FastAPI
- Streamlit
- PostgreSQL
- Docker
- SQLAlchemy

## Remerciements

Projet réalisé dans le cadre d'un exercice technique de développement Full Stack Python.

---

