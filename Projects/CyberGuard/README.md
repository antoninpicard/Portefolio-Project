# CyberGuard

Une plateforme de cybersécurité open-source pour les réseaux domestiques, fonctionnant sur Raspberry Pi.

## Aperçu
CyberGuard fournit une surveillance réseau en temps réel et une détection d'intrusion pour les réseaux domestiques à l'aide d'algorithmes d'apprentissage automatique. Le système fonctionne sur du matériel Raspberry Pi abordable, rendant la cybersécurité avancée accessible à tous.

## Technologies
- **Backend**: Python, TensorFlow
- **Frontend**: React.js
- **Serveur**: Node.js
- **Base de données**: MongoDB

## Fonctionnalités
- Détection d'intrusion basée sur l'apprentissage automatique
- Surveillance du trafic réseau en temps réel
- Tableau de bord web convivial
- Visualisation et rapport des menaces
- Réponse automatisée aux menaces
- Alertes par email/SMS pour les activités suspectes

## Installation
```bash
# Cloner le dépôt
git clone https://github.com/antoninpicard/cyberguard.git
cd cyberguard

# Installer les dépendances du backend
pip install -r requirements.txt

# Installer les dépendances du frontend
cd frontend
npm install
```

## Utilisation
```bash
# Démarrer le serveur backend
python src/main.py

# Dans un terminal séparé, démarrer le frontend
cd frontend
npm start
```

## Structure du Projet
```
CyberGuard/
├── src/                 # Code backend Python
│   ├── ml/              # Modèles d'apprentissage automatique
│   ├── network/         # Modules de surveillance réseau
│   └── api/             # Points de terminaison API
├── frontend/            # Frontend React.js
├── docs/                # Documentation
└── tests/               # Suite de tests
```

## Licence
MIT

## Liens
- [Dépôt GitHub](https://github.com/antoninpicard/cyberguard)
