📚 Documentation du Projet AWS Cost Optimization Chatbot
Vue d'ensemble
Votre projet est un chatbot IA alimenté par Mistral AI conçu pour aider les utilisateurs à optimiser leurs coûts AWS. Il combine:

Extraction et analyse des coûts AWS
Interface de chat interactive
Tableaux de bord et rapports
Service d'email pour les notifications
Moteur d'IA pour les recommandations intelligentes
Architecture du Projet
Backend (Python):

app.py - Application Flask principale
chatbot.py - Logique du chatbot
mistral_ai_engine.py - Intégration Mistral AI
aws_cost_extractor.py - Extraction des coûts AWS
email_service.py - Service d'envoi d'emails
database.py - Gestion de la base de données SQLite
scheduler.py - Tâches planifiées
advanced_analytics.py - Analyses avancées
Frontend (React):

ChatInterface.js - Interface de chat
Dashboard.js - Tableau de bord
ReportsPanel.js - Panneau de rapports
InsightsPanel.js - Panneau d'insights
Technologies Utilisées
Backend: Python, Flask, LangChain, ChromaDB, Boto3
Frontend: React.js, HTML/CSS/JavaScript
Base de données: SQLite
IA: Mistral AI
Cloud: AWS
Fonctionnalités Principales
Analyse des coûts AWS - Connexion aux comptes AWS pour récupérer les données de dépenses
Recommandations IA - Suggestions d'optimisation basées sur l'IA
Interface de chat - Interaction conversationnelle avec le chatbot
Rapports et tableaux de bord - Visualisations des tendances de coûts
Support par email - Envoi de rapports et alertes
Guide d'Optimisation AWS
Le projet inclut un guide complet couvrant:

Optimisation du calcul (EC2, Lambda, ECS/EKS)
Optimisation du stockage (S3, EBS)
Optimisation des bases de données (RDS, DynamoDB)
Optimisation réseau (VPC, Load Balancing)
Gestion des coûts (Budgets, Tags, Instances réservées)
Monitoring et analyse (CloudWatch, Cost Explorer)
Meilleures pratiques et feuille de route d'optimisation
Configuration du Service Email
Le projet inclut un service email pour envoyer des inquiries à: maddehclement@gmail.com

Points clés:

Utilise Gmail SMTP
Nécessite une App Password (pas le mot de passe Gmail régulier)
Endpoints API pour envoyer des inquiries et questions
Intégration React pour le formulaire de contact
Installation et Démarrage
Backend:

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
flask run

Copy

Insert

Frontend:

cd frontend
npm install
npm start

Copy

Insert

Structure du Projet (Organisée)
amazon/
├── backend/              # Tous les fichiers backend
├── frontend/             # Application React
├── config/               # Configuration et variables d'environnement
├── tests/                # Tests unitaires
├── scripts/              # Scripts utilitaires
├── docs/                 # Documentation
├── templates/            # Templates HTML
└── requirements.txt      # Dépendances Python
