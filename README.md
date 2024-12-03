# Générateur de Reçus X

Un service web permettant de générer des reçus stylisés pour les profils X (Twitter), avec une interface moderne et responsive.

## 🌟 Fonctionnalités

- Génération de reçus au format ticket de caisse
- Intégration de l'API X v2
- Mise en cache des requêtes (15 minutes)
- Interface utilisateur moderne avec Tailwind CSS
- Design responsive
- Téléchargement des reçus en PNG
- Animations et effets visuels

## 🔧 Prérequis

- Python 3.11 ou supérieur
- Une clé API X (Bearer Token)

## 📦 Installation

1. Cloner le repository :
   ```bash
   git clone <votre-repo>
   cd generateur-recus-x
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Créer un fichier .env à la racine du projet :
   ```env
   X_API_KEY=votre_bearer_token
   FLASK_APP=main.py
   FLASK_ENV=production
   ```

2. Obtenir une clé API X :
   - Créer un compte développeur sur https://developer.x.com
   - Créer un projet et générer un Bearer Token
   - Ajouter le token dans le fichier .env

## 🚀 Utilisation

1. Démarrer le serveur :
   ```bash
   python main.py
   ```

2. Ouvrir http://localhost:5000 dans votre navigateur
3. Entrer un nom d'utilisateur X (sans @)
4. Cliquer sur "Générer"
5. Télécharger le reçu en PNG si désiré

## 🐳 Déploiement avec Docker

1. Construire l'image :
   ```bash
   docker build -t generateur-recus-x .
   ```

2. Lancer le conteneur :
   ```bash
   docker run -p 5000:5000 -e X_API_KEY=votre_bearer_token generateur-recus-x
   ```

## 🚀 Déploiement sur Coolify

1. Dans votre instance Coolify :
   - Créer un nouveau service
   - Sélectionner 'Docker'
   - Connecter votre dépôt Git

2. Configurer les variables d'environnement :
   - X_API_KEY
   - FLASK_APP=main.py
   - FLASK_ENV=production

3. Déployer !

## 📝 Notes

- Limite de l'API X : 3 requêtes par 15 minutes par utilisateur
- Mise en cache des résultats pendant 15 minutes
- Interface en français
- Design inspiré des tickets de caisse thermiques

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📜 Licence

Ce projet est sous licence MIT.
