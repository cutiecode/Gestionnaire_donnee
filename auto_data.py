import os
from tabulate import tabulate
from config import Config

# Identifier les données nécessaires
def auto_data(table_name, data_ids=None):
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                # Vérification que la table existe avant d'exécuter la requête
                cursor.execute("SHOW TABLES LIKE %s", (table_name,))
                table_exists = cursor.fetchone()
                if not table_exists:
                    print(f"Erreur : La table `{table_name}` n'existe pas.")
                    return None

                # Récupérer les noms des colonnes de la table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [column[0] for column in cursor.fetchall()]

                # Requête pour récupérer les données
                query = f"SELECT * FROM {table_name} WHERE id IN ({','.join(['%s'] * len(data_ids))})"
                cursor.execute(query, data_ids)
                results = cursor.fetchall()

                # Retourner les résultats avec les noms des colonnes
                return columns, results
    except Exception as e:
        print(f"Erreur lors de l'identification des données : {e}")
        return None
    finally:
        if connection:
            connection.close()