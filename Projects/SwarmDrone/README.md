# SwarmDrone

Un système de contrôle collaboratif de drones pour la cartographie 3D autonome.

## Aperçu
SwarmDrone est un système avancé qui permet à plusieurs drones de travailler ensemble de manière autonome pour la cartographie 3D et l'analyse environnementale. Le système utilise des algorithmes d'intelligence en essaim pour coordonner les mouvements des drones, optimiser la couverture, et créer des cartes 3D détaillées des environnements.

## Technologies
- **Backend**: ROS (Robot Operating System), Python
- **Frontend**: React.js, Three.js
- **Communication**: WebSocket
- **Visualisation 3D**: Three.js
- **Planification de trajectoire**: Algorithmes personnalisés d'intelligence en essaim

## Fonctionnalités
- Coordination autonome des drones utilisant l'intelligence en essaim
- Visualisation 3D en temps réel des positions des drones et des données collectées
- Interface web interactive pour la planification et le suivi de mission
- Évitement des collisions et planification optimale des trajectoires
- Traitement des données en temps réel et génération de carte 3D
- Enregistrement et relecture des missions

## Installation

### Prérequis
- ROS Noetic ou plus récent
- Python 3.8+
- Node.js 14+
- npm 6+

```bash
# Clone the repository
git clone https://github.com/antoninpicard/swarmdrone.git
cd swarmdrone

# Install ROS dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build ROS workspace
catkin_make

# Install frontend dependencies
cd frontend
npm install
```

## Utilisation

### Démarrer le core ROS et les contrôleurs de drones
```bash
# Terminal 1: Démarrer le core ROS
roscore

# Terminal 2: Lancer le contrôleur d'essaim de drones
roslaunch swarm_controller main.launch

# Terminal 3: Démarrer le serveur web et le pont WebSocket
rosrun swarm_bridge bridge_node.py
```

### Démarrer le frontend
```bash
# Terminal 4: Démarrer le frontend React
cd frontend
npm start
```

## Structure du Projet
```
SwarmDrone/
├── ros/                  # Packages ROS
│   ├── swarm_controller/ # Coordination de l'essaim de drones
│   ├── swarm_bridge/     # Pont WebSocket vers le frontend
│   └── swarm_msgs/       # Définitions de messages personnalisés
├── frontend/             # Frontend React.js
│   ├── src/              # Code source du frontend
│   └── public/           # Ressources statiques
├── scripts/              # Scripts utilitaires
└── docs/                 # Documentation
```

## Licence
MIT

## Liens
- [Dépôt GitHub](https://github.com/antoninpicard/swarmdrone)
