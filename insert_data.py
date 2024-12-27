import os
import time
from config import Config

def insert_data(table_name, values):
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                # Vérifier les colonnes de la table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]  

                if table_name == "users" and "registered_at" in columns:
                    values["registered_at"] = time.strftime('%Y-%m-%d %H:%M:%S') 
                elif table_name == "tests" and "created_at" in columns:
                    values["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S') 

                # Création dynamique de la requête SQL
                columns_list = ", ".join(values.keys())
                placeholders = ", ".join(["%s"] * len(values))
                sql = f"INSERT INTO {table_name} ({columns_list}) VALUES ({placeholders})"
                cursor.execute(sql, list(values.values()))
                connection.commit()
                print(f"Données insérées avec succès dans la table `{table_name}` !")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données dans `{table_name}` : {e}")
    finally:
        if connection:
           connection.close()

