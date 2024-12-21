import pymysql
import csv
from db_connection import connect_to_db

def data_export(table_name, file_name, export_format="csv"):
    """
    Exporte le contenu d'une table dans un fichier CSV ou sous forme de tableau.
    :param table_name: Nom de la table.
    :param file_name: Nom du fichier à créer.
    :param export_format: Format d'exportation ('csv' ou 'tableau').
    """
    try:
        connection = connect_to_db()
        if connection:
            with connection.cursor() as cursor:
                # Récupérer les données de la table
                cursor.execute(f"SELECT * FROM {table_name}")
                results = cursor.fetchall()

                # Obtenir les noms des colonnes
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]

                if export_format == "csv":
                    # Exporter vers CSV
                    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(columns)  # En-têtes
                        writer.writerows(results)  # Données
                    print(f"Données exportées avec succès dans `{file_name}` en format CSV !")
                elif export_format == "tableau":
                    # Exporter vers tableau formaté
                    with open(file_name, mode="w", encoding="utf-8") as file:
                        file.write("Table: " + table_name + "\n\n")
                        # Ajouter les colonnes comme en-têtes
                        file.write(" | ".join(columns) + "\n")
                        file.write("-" * (len(columns) * 2) + "\n")  # Ligne de séparation
                        for row in results:
                            file.write(" | ".join(str(cell) for cell in row) + "\n")
                    print(f"Données exportées avec succès dans `{file_name}` en format Tableau !")
                else:
                    print("Format d'exportation non supporté. Choisissez 'csv' ou 'tableau'.")
                    return
    except Exception as e:
        print(f"Erreur d'exportation : {e}")
    finally:
        if connection:
            connection.close()
