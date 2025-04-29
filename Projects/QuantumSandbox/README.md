# QuantumSandbox

Un simulateur basé sur navigateur pour les algorithmes et circuits quantiques.

## Aperçu
QuantumSandbox est une application web interactive qui permet aux utilisateurs de concevoir, visualiser et simuler des circuits quantiques directement dans le navigateur. Développée avec Qiskit, WebAssembly, React.js et D3.js, elle offre une plateforme accessible pour apprendre les concepts de l'informatique quantique sans nécessiter d'installations complexes ou de matériel puissant.

## Technologies
- **Backend**: Python, Qiskit, Flask
- **Frontend**: React.js, D3.js
- **Compilation**: WebAssembly (via Pyodide)
- **Visualisation**: D3.js pour la visualisation des circuits et des états
- **Déploiement**: Docker, Netlify

## Fonctionnalités
- Constructeur de circuits quantiques interactif avec interface glisser-déposer
- Simulation en temps réel des circuits quantiques
- Visualisation des états quantiques et des probabilités de mesure
- Bibliothèque d'algorithmes quantiques préconstruits (Grover, Shor, Transformée de Fourier Quantique, etc.)
- Tutoriels éducatifs et explications des concepts d'informatique quantique
- Exportation/importation de circuits au format Qiskit
- Aucune installation requise - fonctionne entièrement dans le navigateur

## Installation

### Configuration de Développement
```bash
# Cloner le dépôt
git clone https://github.com/antoninpicard/quantum-sandbox.git
cd quantum-sandbox

# Installer les dépendances du frontend
cd frontend
npm install
npm start

# Dans un terminal séparé, configurer le backend
cd ../backend
python -m venv venv
source venv/bin/activate  # Sous Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Configuration Docker
```bash
# Construire et exécuter avec Docker Compose
docker-compose up -d
```

## Utilisation
1. Ouvrez votre navigateur et accédez à `http://localhost:3000`
2. Utilisez le constructeur de circuits pour glisser-déposer des portes quantiques sur les qubits
3. Exécutez la simulation pour voir les résultats
4. Explorez la visualisation des états quantiques
5. Essayez les exemples d'algorithmes préconstruits

## Structure du Projet
```
QuantumSandbox/
├── frontend/              # Frontend React.js
│   ├── public/            # Ressources statiques
│   ├── src/               # Code source
│   │   ├── components/    # Composants React
│   │   ├── hooks/         # Hooks React personnalisés
│   │   ├── pages/         # Composants de pages
│   │   ├── utils/         # Fonctions utilitaires
│   │   └── wasm/          # Intégration WebAssembly
│   └── package.json       # Dépendances du frontend
├── backend/               # Backend Python
│   ├── app.py             # Application Flask
│   ├── quantum/           # Code de simulation quantique
│   └── requirements.txt   # Dépendances Python
├── docker/                # Configuration Docker
└── docs/                  # Documentation
```

## Licence
MIT

## Liens
- [Dépôt GitHub](https://github.com/antoninpicard/quantum-sandbox)
