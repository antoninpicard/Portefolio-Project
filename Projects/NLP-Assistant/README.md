# Assistant NLP

Un assistant vocal hors ligne utilisant le Traitement du Langage Naturel qui fonctionne localement sur des appareils à faible consommation d'énergie.

## Aperçu
Assistant NLP est un assistant vocal axé sur la confidentialité qui traite toutes les commandes localement sans nécessiter de connexion Internet. Il est conçu pour fonctionner efficacement sur des appareils à faible consommation comme le Raspberry Pi, offrant un contrôle vocal pour la domotique, la gestion des tâches et la recherche d'informations tout en gardant toutes vos données privées.

## Technologies
- **Backend**: Python, PyTorch
- **Frontend**: React Native
- **Traitement Vocal**: WebRTC
- **Modèles NLP**: Architecture basée sur les Transformers optimisée pour les appareils de bordure
- **Reconnaissance Vocale**: Traitée localement à l'aide de modèles optimisés

## Fonctionnalités
- Reconnaissance vocale hors ligne et compréhension du langage naturel
- Automatisation des tâches via commandes vocales
- Intégration à la domotique
- Ensembles de commandes et réponses personnalisables
- Faible consommation de ressources pour les appareils de bordure
- Application mobile multi-plateformes
- Axé sur la confidentialité sans dépendances cloud

## Installation

### Backend (Python)
```bash
# Cloner le dépôt
git clone https://github.com/antoninpicard/nlp-assistant.git
cd nlp-assistant/backend

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sous Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Télécharger les modèles de langage
python download_models.py
```

### Application Mobile (React Native)
```bash
# Naviguer vers le répertoire de l'application
cd ../app

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm start
```

## Utilisation

### Démarrer le Serveur de l'Assistant
```bash
cd backend
python src/main.py
```

### Utiliser l'Application Mobile
1. Connectez votre appareil mobile au même réseau que le serveur de l'assistant
2. Ouvrez l'application Assistant NLP
3. Entrez l'adresse IP du serveur
4. Appuyez sur le bouton du microphone et énoncez votre commande

## Structure du Projet
```
NLP-Assistant/
├── backend/               # Code backend Python
│   ├── src/               # Code source
│   │   ├── asr/           # Reconnaissance Vocale Automatique
│   │   ├── nlu/           # Compréhension du Langage Naturel
│   │   ├── tts/           # Synthèse Vocale
│   │   └── skills/        # Compétences et capacités de l'assistant
│   ├── models/            # Modèles pré-entraînés
│   └── tests/             # Suite de tests
├── app/                   # Application mobile React Native
│   ├── src/               # Code source
│   ├── assets/            # Images, polices, etc.
│   └── __tests__/         # Suite de tests
└── docs/                  # Documentation
```

## Licence
MIT

## Liens
- [Dépôt GitHub](https://github.com/antoninpicard/nlp-assistant)
