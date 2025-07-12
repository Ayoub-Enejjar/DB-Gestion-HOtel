# 🏨 Système de Gestion Hôtelière

Un système de gestion hôtelière complet développé avec **Streamlit** et **SQLite** pour la gestion des réservations, clients, chambres et hôtels.

## 📋 Table des matières

- [Description du projet](#description-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure de la base de données](#structure-de-la-base-de-données)
- [Démonstration vidéo](#démonstration-vidéo)
- [Auteur](#auteur)

## 📖 Description du projet

Ce projet est un système de gestion hôtelière développé dans le cadre du cours **Bases de Données INFS4** sous la direction du **Pr. J.ZAHIR**. L'application permet de gérer efficacement les réservations, les clients, les chambres et les hôtels avec une interface web moderne et intuitive.

## ✨ Fonctionnalités

### 🔍 Consultation et recherche
- **Consulter les réservations** : Affichage de toutes les réservations avec détails clients et hôtels
- **Consulter les clients** : Liste complète des clients enregistrés
- **Rechercher les chambres disponibles** : Recherche par période avec filtres avancés

### ➕ Gestion des données
- **Ajouter un client** : Formulaire complet pour l'enregistrement de nouveaux clients
- **Ajouter une réservation** : Création de réservations avec vérification de disponibilité
- **Validation automatique** : Contrôles d'intégrité et de cohérence des données

### 🏗️ Architecture de la base de données
- **7 tables principales** : Hotel, Client, Chambre, Reservation, Type_Chambre, Prestation, Evaluation
- **Clés étrangères** : Relations intégrées pour maintenir l'intégrité des données
- **Contraintes** : Validation automatique des dates et données

## 🛠️ Technologies utilisées

- **Frontend** : Streamlit (interface web moderne)
- **Backend** : Python 3.x
- **Base de données** : SQLite
- **Traitement des données** : Pandas
- **Interface utilisateur** : Streamlit Components

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone <url-du-repo>
   cd DB-Gestion-HOtel
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialiser la base de données**
   ```bash
   python database_setup.py
   ```

4. **Lancer l'application**
   ```bash
   streamlit run app.py
   ```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 📱 Utilisation

### Interface principale
L'application propose un menu latéral avec les fonctionnalités suivantes :

1. **Consulter les réservations**
   - Affichage de toutes les réservations
   - Tri par date d'arrivée
   - Informations détaillées (client, hôtel, chambre, dates)

2. **Consulter les clients**
   - Liste complète des clients
   - Informations de contact
   - Tri alphabétique

3. **Consulter les chambres disponibles**
   - Sélection de période (arrivée/départ)
   - Affichage des chambres libres
   - Informations détaillées (type, tarif, étage, fumeurs)

4. **Ajouter un client**
   - Formulaire complet
   - Validation des champs obligatoires
   - Contrôle d'unicité de l'email

5. **Ajouter une réservation**
   - Sélection du client
   - Choix des dates
   - Sélection de chambre disponible
   - Validation automatique des conflits

### Fonctionnalités avancées
- **Validation en temps réel** des dates de réservation
- **Contrôle de disponibilité** automatique des chambres
- **Interface responsive** adaptée à tous les écrans
- **Messages d'erreur** informatifs et guidés

## 🗄️ Structure de la base de données

### Tables principales

| Table | Description | Clés |
|-------|-------------|------|
| **Hotel** | Informations des hôtels | Id_Hotel (PK) |
| **Client** | Données des clients | Id_Client (PK), Email (UNIQUE) |
| **Chambre** | Chambres des hôtels | Id_Chambre (PK), Id_Hotel (FK), Id_Type (FK) |
| **Reservation** | Réservations clients | Id_Reservation (PK), Id_Client (FK), Id_Chambre (FK) |
| **Type_Chambre** | Types et tarifs | Id_Type (PK) |
| **Prestation** | Services proposés | Id_Prestation (PK) |
| **Evaluation** | Avis clients | Id_Evaluation (PK), Id_Reservation (FK) |

### Relations
- **Hotel** ↔ **Chambre** (1:N)
- **Client** ↔ **Reservation** (1:N)
- **Chambre** ↔ **Reservation** (1:N)
- **Type_Chambre** ↔ **Chambre** (1:N)
- **Reservation** ↔ **Evaluation** (1:1)

## 🎥 Démonstration vidéo

**Vidéo de démonstration complète :**
https://drive.google.com/file/d/159xs9zBFuiCUNigmXbKR0nP9VHEnzQLJ/view

Cette vidéo présente l'utilisation complète du système, incluant :
- Navigation dans l'interface
- Consultation des données
- Ajout de clients et réservations
- Recherche de chambres disponibles

## 👨‍💻 Auteur

**Projet développé par :** [Votre nom]
**Cours :** Bases de Données INFS4
**Professeur :** Pr. J.ZAHIR
**Institution :** [Nom de l'institution]

---

## 📝 Notes techniques

### Fonctionnalités de sécurité
- Validation des contraintes d'intégrité
- Contrôle des clés étrangères
- Gestion des erreurs SQLite

### Performance
- Requêtes optimisées avec JOIN
- Index automatiques sur les clés primaires
- Pagination des résultats pour les grandes listes

### Extensibilité
- Architecture modulaire
- Code commenté et documenté
- Structure extensible pour de nouvelles fonctionnalités

---

*Dernière mise à jour : Janvier 2025*
