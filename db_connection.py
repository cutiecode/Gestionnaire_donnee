import pymysql
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def connect_to_db():
    try:
        # Utiliser les variables d'environnement pour se connecter à la base de données
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'))
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur de connexion : {e}")
        return None
