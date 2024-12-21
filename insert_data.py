from db_connection import connect_to_db
import time

def insert_data(table_name, values):
    """
    Insère des données dans une table spécifique sans demander l'ID et le registered_at.

    L'ID est incrémenté automatiquement par la base de données et `registered_at` est ajouté avec un timestamp
    seulement si la colonne existe dans la table.
    
    :param table_name: Nom de la table.
    :param values: Dictionnaire des colonnes et des valeurs à insérer (sans `id` ni `registered_at`).
    """
    try:
        connection = connect_to_db()
        if connection:
            with connection.cursor() as cursor:
                # Vérifier les colonnes de la table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]  # Obtenir toutes les colonnes de la table

                # Ajouter `registered_at` pour `users` et `created_at` pour `tests`
                if table_name == "users" and "registered_at" in columns:
                    values["registered_at"] = time.strftime('%Y-%m-%d %H:%M:%S')  # Timestamp actuel pour `registered_at`
                elif table_name == "tests" and "created_at" in columns:
                    values["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S')  # Timestamp actuel pour `created_at`

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

