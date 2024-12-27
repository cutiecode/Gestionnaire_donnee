# Gestion de Base de Données avec Python

Ce projet Python permet de gérer une base de données de manière automatisée avec des fonctionnalités telles que l'insertion, la mise à jour, la suppression, l'affichage, la sélection, l'exportation des données et la validation des enregistrements.

## Fonctionnalités

- **Insertion de données** : Ajoute de nouvelles entrées dans la base de données.
- **Mise à jour de données** : Modifie les informations existantes dans la base de données.
- **Suppression de données** : Supprime des valeurs spécifiques d'une colonne d'une entrée existante.
- **Affichage des données** : Affiche les données d'une table sous forme de tableau.
- **Identification des données** : Permet de rechercher et d'identifier des enregistrements spécifiques dans une table.
- **Exportation des données** : Sauvegarde les données dans un fichier CSV ou sous forme de tableau.
- **Validation des données** : Vérifie l'existence d'un enregistrement par son ID avant de permettre une mise à jour ou suppression.

## Technologies utilisées

- **Python 3.x** : Langage principal du projet.
- **SQL (MySQL)** : Pour la gestion des bases de données.
- **Tabulate** : Pour afficher les données sous forme de tableau.
- **Python MySQL Connector** : Pour interagir avec la base de données MySQL.
- **Pandas** : Optionnellement pour l'exportation des données.

## Prérequis

Avant d'exécuter ce projet, vous devez avoir :

- Python 3.x installé sur votre machine.
- Une base de données MySQL configurée.
- Les bibliothèques suivantes installées via `pip` :
  ```bash
  pip install tabulate mysql-connector-python pandas
