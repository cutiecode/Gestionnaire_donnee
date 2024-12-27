import os
from config import Config

def delete_data(table_name, record_id, column_name):
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                # Obtenir les colonnes de la table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]
                
                # Exclure la première et la dernière colonne
                if column_name not in columns[1:-1]:
                    print(f"La colonne `{column_name}` est invalide. Vous ne pouvez pas modifier les colonnes `{columns[0]}` ou `{columns[-1]}`.")
                    return False
                
                # Vérifier si l'ID existe
                cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = %s", (record_id,))
                if cursor.fetchone() is None:
                    print(f"L'ID {record_id} n'existe pas dans la table `{table_name}`.")
                    return False

                # Vider la colonne pour l'ID donné
                query = f"UPDATE {table_name} SET {column_name} = NULL WHERE id = %s"
                cursor.execute(query, (record_id,))
                connection.commit()
                print(f"La colonne `{column_name}` pour l'ID {record_id} a été vidée avec succès dans la table `{table_name}`.")
                return True
    except Exception as e:
        print(f"Erreur lors de la suppression des données dans la colonne `{column_name}` : {e}")
    finally:
        if connection:
            connection.close()
