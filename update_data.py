import os
import time
from config import Config

def update_data(table_name, record_id, values):
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                 # Vérifier les colonnes de la table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]  
            
                # Vérifier si l'ID existe
                cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = %s", (record_id,))
                if cursor.fetchone() is None:
                    print(f"L'ID {record_id} n'existe pas dans la table `{table_name}`.")
                    return False  # Retourner False si l'ID n'existe pas

                
                if table_name == "users" and "registered_at" in columns:
                    values["registered_at"] = time.strftime('%Y-%m-%d %H:%M:%S')  
                elif table_name == "tests" and "created_at" in columns:
                    values["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S')  
                elif table_name == "results" and "completed_at" in columns:
                    values["completed_at"] = time.strftime('%Y-%m-%d %H:%M:%S')  
                
               # Création dynamique de la requête SQL
                set_clause = ", ".join([f"{col} = %s" for col in values.keys()])
                sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
                
                # Ajouter l'ID du record à la fin des valeurs pour la condition WHERE
                cursor.execute(sql, list(values.values()) + [record_id])
                connection.commit()
                print(f"Données mises à jour avec succès dans la table `{table_name}` !")
    except Exception as e:
        print(f"Erreur lors de la mise à jour des données dans `{table_name}` : {e}")
    finally:
        if connection:
            connection.close()