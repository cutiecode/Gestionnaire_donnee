from insert_data import insert_data
from update_data import update_data
from delete_data import delete_data
from data_export import data_export
from config import Config
from tabulate import tabulate
from auto_data import auto_data


# Fonction pour afficher les données d'une table
def show_data(table_name):
    """
    Affiche les données d'une table sous forme de tableau.
    :param table_name: Nom de la table.
    """
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                # Récupérer toutes les données de la table
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                # Obtenir les noms des colonnes
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = [row[0] for row in cursor.fetchall()]

                # Vérifier si la table est vide
                if not rows:
                    print(f"La table `{table_name}` est vide.")
                    return

                # Afficher les données sous forme de tableau
                print("\n" + tabulate(rows, headers=columns, tablefmt="fancy_grid"))
    except Exception as e:
        print(f"Erreur lors de l'affichage des données dans `{table_name}` : {e}")
    finally:
        if connection:
            connection.close()


# Fonction pour valider l'existence d'un ID
def validate_record_id(table_name, record_id):
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = %s", (record_id,))
                if cursor.fetchone() is None:
                    return False  
                return True  
    except Exception as e:
        print(f"Erreur de validation de l'ID : {e}")
        return False
    finally:
        if connection:
            connection.close()


# Fonction pour sélectionner la table
def select_table(exclude_results=False):
    while True:
        print("\n--- Tables disponibles ---")
        print("1. users")
        print("2. tests")
        if not exclude_results:
            print("3. results") 
        
        choice = input("Sélectionnez une table (1 ou 2, ou 3 si disponible) : ").strip()
        
        if choice == "1":
            return "users"
        elif choice == "2":
            return "tests"
        elif choice == "3" and not exclude_results:
            return "results"
        else:
            print("Choix invalide, veuillez réessayer.")


# Fonction pour collecter les colonnes
def collect_column_values(table_name):
    try:
        connection = Config()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]
                
                if table_name == "users":
                    columns = [col for col in columns if col not in ["id", "registered_at"]]
                elif table_name == "tests":
                    columns = [col for col in columns if col not in ["id", "created_at"]]
                elif table_name == "results":
                    columns = [col for col in columns if col not in ["id", "user_id", "test_id", "completed_at"]]

                values = {}
                for column in columns:
                    value = input(f"Entrez une valeur pour `{column}` (laisser vide pour NULL) : ").strip()
                    values[column] = value if value else None
                return values
    except Exception as e:
        print(f"Erreur lors de la collecte des colonnes : {e}")
    finally:
        if connection:
            connection.close()


# Fonction principale du menu
def main_menu():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Insérer des données")
        print("2. Mettre à jour des données")
        print("3. Supprimer des données")
        print("4. Afficher les données")
        print("5. Identifier les données")
        print("6. Exporter les données")
        print("7. Terminer")
        
        choice = input("Choisissez une option (1-5) : ").strip()

        if choice == "1":  # Insertion
            table_name = select_table(exclude_results=True)
            print(f"\nInsertion dans la table `{table_name}` :")
            values = collect_column_values(table_name)
            if values:
                insert_data(table_name, values)

        elif choice == "2":  # Mise à jour
            table_name = select_table()
            print(f"\nMise à jour dans la table `{table_name}` :")
            while True:
                record_id = input_with_validation("Entrez l'ID de l'entrée à mettre à jour (ou entrez 0 pour quitter) : ", int)
                if record_id == 0:
                    print("Vous avez choisi de quitter.")
                    break
                
                if not validate_record_id(table_name, record_id):
                    print(f"L'ID {record_id} n'existe pas dans la table `{table_name}`.")
                    continue
                
                values = collect_column_values(table_name)
                if values:
                    update_data(table_name, record_id, values)
                    break
        elif choice == "3":  # Suppression de données d'une colonne
            table_name = select_table(exclude_results=True)
            print(f"\nSuppression dans la table `{table_name}` :")

            while True:
                try:
                    # Demander l'ID de l'entrée à modifier
                    record_id = input("Entrez l'ID de l'entrée pour modifier une colonne (ou entrez 0 pour quitter) : ")

                    if not record_id.isdigit():
                        print("L'ID doit être un nombre entier. Réessayez.")
                        continue

                    record_id = int(record_id)

                    if record_id == 0:  # Quitter si l'utilisateur entre 0
                        print("Vous avez choisi de quitter.")
                        break

                    # Vérifier si l'ID existe dans la table
                    connection = Config()
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = %s", (record_id,))
                        if cursor.fetchone() is None:
                            print(f"L'ID {record_id} n'existe pas dans la table `{table_name}`.")
                            continue

                        # Obtenir les colonnes disponibles
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = [row[0] for row in cursor.fetchall()]

                    # Exclure la première et la dernière colonne
                    editable_columns = columns[1:-1]
                    if not editable_columns:
                        print("Aucune colonne modifiable dans cette table.")
                        break

                    # Afficher les colonnes modifiables
                    print(f"Colonnes modifiables : {', '.join(editable_columns)}")
                    column_name = input("Entrez le nom de la colonne à vider : ")

                    if column_name not in editable_columns:
                        print(f"Colonne `{column_name}` invalide. Veuillez choisir parmi : {', '.join(editable_columns)}.")
                        continue

                    # Appeler la fonction de suppression pour la colonne spécifique
                    if delete_data(table_name, record_id, column_name):
                        break
                except ValueError:
                    print("Veuillez entrer une valeur valide.")
                except Exception as e:
                    print(f"Une erreur est survenue : {e}")
                
        elif choice == "4":  # Affichage
            table_name = select_table()
            print(f"\nAffichage des données dans la table `{table_name}` :")
            show_data(table_name)

        elif choice == "5":  # Identifier les données
            print("\n=== Identification des données ===")

            # Demander à l'utilisateur de spécifier la table à identifier
            table_name = input("Entrez le nom de la table à identifier : ")

            # Vérifier que le nom de la table est non vide
            if not table_name.strip():
                print("Erreur : Le nom de la table ne peut pas être vide.")
                continue

            # Demander les IDs des données à identifier, permettre plusieurs IDs séparés par des virgules
            data_ids_input = input(f"Entrez les IDs des données à identifier dans la table `{table_name}` (séparés par des virgules) : ")
            # Séparer les IDs et les convertir en entiers
            data_ids = [int(id.strip()) for id in data_ids_input.split(",") if id.strip().isdigit()]

            # Afficher un message si aucune ID n'est entrée
            if not data_ids:
                print("Erreur : Aucune ID valide saisie.")
                continue

            print("\nIdentification des données...")
            columns, data = auto_data(table_name=table_name, data_ids=data_ids)  

            if data:
                print(f"\nDonnées identifiées avec succès dans la table `{table_name}`. Voici les données :")
                
                # Afficher les résultats dans un tableau avec tabulate
                print(tabulate(data, headers=columns, tablefmt="pretty"))
            else:
                print(f"Aucune donnée trouvée pour les IDs spécifiés dans la table `{table_name}`.")
        
        elif choice == "6":  # Exportation des données
            table_name = input("Entrez le nom de la table à exporter : ")
            file_name = input("Entrez le nom du fichier de sortie (ex: data.csv ou data.txt) : ")
            export_format = input("Choisissez le format d'exportation (csv ou tableau) : ").strip().lower()

            if export_format not in ["csv", "tableau"]:
                print("Format d'exportation non supporté. Choisissez 'csv' ou 'tableau'.")
                continue  # Demander à nouveau si l'utilisateur entre un mauvais format

            # Appel de la fonction d'exportation
            data_export(table_name, file_name, export_format)

        elif choice == "7":  # terminer
            print("Vous avez choisi de terminer.")
            break

        else:
            print("Option invalide, veuillez réessayer.")


# Fonction pour valider et convertir les entrées utilisateur
def input_with_validation(prompt, data_type):
    while True:
        try:
            return data_type(input(prompt).strip())
        except ValueError:
            print(f"Veuillez entrer une valeur valide pour le type {data_type.__name__}.")

if __name__ == "__main__":
    main_menu() 

