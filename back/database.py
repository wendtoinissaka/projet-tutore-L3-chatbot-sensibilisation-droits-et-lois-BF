import csv
import json
from urllib.parse import urlparse
import pandas as pd
import psycopg2
from config import Config
import numpy as np
from models.models import Avocat, db

def connect_db():
    try:
        result = urlparse(Config.SQLALCHEMY_DATABASE_URI)

        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None


def create_tables(app):
    db.init_app(app)  # Initialiser db avec l'application Flask

    with app.app_context():
        db.create_all()  # Crée toutes les tables définies dans les modèles
        create_trigger()  # Crée le trigger après la création des tables


# def create_tables(app):
#     db.init_app(app)

#     with app.app_context():
#         db.create_all()  # Crée toutes les tables définies dans les modèles
#         create_trigger()  # Crée le trigger après la création des tables


def create_trigger():
    """Crée un trigger dans la base de données pour notifier lors de l'insertion d'une nouvelle notification, seulement s'il n'existe pas."""
    conn = connect_db()
    if conn is None:
        print("Connexion à la base de données échouée. Impossible de créer le trigger.")
        return
    
    cursor = conn.cursor()

    # Vérification si le trigger existe déjà
    check_trigger_query = """
    SELECT tgname FROM pg_trigger WHERE tgname = 'new_notification_trigger';
    """

    # Création de la fonction PL/pgSQL pour envoyer une notification sur le canal 'new_notification'
    create_function_query = """
    CREATE OR REPLACE FUNCTION notify_new_notification()
    RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify('new_notification', NEW.message);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    
    # Création du trigger lié à la table 'notifications'
    create_trigger_query = """
    CREATE TRIGGER new_notification_trigger
    AFTER INSERT ON notifications
    FOR EACH ROW EXECUTE FUNCTION notify_new_notification();
    """

    try:
        # Vérifier si le trigger existe déjà
        cursor.execute(check_trigger_query)
        trigger_exists = cursor.fetchone()

        if trigger_exists:
            print("Le trigger 'new_notification_trigger' existe déjà. Aucune action nécessaire.")
        else:
            # Créer la fonction et le trigger
            cursor.execute(create_function_query)
            cursor.execute(create_trigger_query)
            conn.commit()
            print("Trigger 'new_notification_trigger' créé avec succès.")
    except psycopg2.Error as e:
        print(f"Erreur lors de la création du trigger : {e}")
    finally:
        cursor.close()
        conn.close()




# def log_chat(question, response="Aucune entité trouvée."):
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute(
#         'INSERT INTO chat_history (question, response) VALUES (%s, %s)',
#         (question, response)  # Ici, response est déjà une chaîne
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()



def log_chat(question, response="Aucune entité trouvée."):
    # Si la réponse est une chaîne JSON, analyse-la
    if isinstance(response, str):
        try:
            response_data = json.loads(response)  # Analyse la chaîne JSON
            response_message = response_data.get("message", "Aucune entité trouvée.")  # Obtiens le message
        except json.JSONDecodeError:
            response_message = response  # En cas d'erreur, utilise la réponse originale
    else:
        response_message = response  # Si ce n'est pas une chaîne, utilise la réponse originale

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO chat_history (question, response) VALUES (%s, %s)',
        (question, response_message)  # Insère le message extrait
    )
    conn.commit()
    cursor.close()
    conn.close()



def add_notification(message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (message) VALUES (%s);", (message,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_subscribers():
    """Récupère tous les abonnés de la table abonnee."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM abonnee')
    abonnes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [abonne[0] for abonne in abonnes]  # Retourne uniquement les e-mails


def insert_data_from_csv(file_path):
    # Lire le fichier CSV
    data = pd.read_csv(file_path)
    
    # Remplacer les NaN dans la colonne 'Question' par une chaîne vide
    data['Question'].replace(np.nan, '', inplace=True)
    
    conn = connect_db()
    cursor = conn.cursor()

    # Insérer les données dans la table FAQ
    for index, row in data.iterrows():
        # Ignorer les lignes avec une question vide
        if row['Question'] == '':
            print(f"Ligne {index} ignorée : question manquante.")
            continue
        
        # Vérifier si la question existe déjà
        cursor.execute('SELECT 1 FROM faq WHERE question = %s', (row['Question'],))
        exists = cursor.fetchone()

        if exists:
            print(f"La question '{row['Question']}' existe déjà. Ignorée.")
        else:
            cursor.execute(
                '''
                INSERT INTO faq (categorie, tag, sous_categorie, question, reponse, article_reference) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (row['Categorie'], row['Tag'], row['Sous categorie'], row['Question'], row['Réponse'], row['Article_reference'])
            )
    
    conn.commit()
    cursor.close()
    conn.close()

# def insert_data_from_json(filename):
#     conn = connect_db()
#     if conn is None:
#         return

#     cursor = conn.cursor()
#     with open(filename, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     for type_procedure, categories in data["procedures_juridiques_et_administratives"].items():
#         for procedure_key, procedure in categories.items():
#             if "description" in procedure:
#                 description = procedure["description"]
                
#                 # Vérifier si la procédure existe déjà
#                 cursor.execute(
#                     "SELECT COUNT(*) FROM procedures WHERE titre = %s AND type = %s",
#                     (procedure["titre"], type_procedure)
#                 )
#                 exists = cursor.fetchone()[0] > 0

#                 if not exists:  # Si la procédure n'existe pas, insérer
#                     cursor.execute(
#                         "INSERT INTO procedures (type, titre, description_texte, description_pieces_a_fournir, description_cout, description_conditions_acces, source) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#                         (
#                             type_procedure,
#                             procedure["titre"],
#                             description.get("texte", ""),
#                             ', '.join(description.get("pieces_a_fournir", [])),
#                             description.get("cout", ""),
#                             ', '.join(description.get("conditions_acces", [])),
#                             procedure["source"]
#                         )
#                     )
#                 else:
#                     print(f"Procedure '{procedure['titre']}' existe déjà, sautée.")
#             else:
#                 print(f"Procedure '{procedure['titre']}' sans description, sautée.")

#     conn.commit()
#     cursor.close()
#     conn.close()

def insert_precedure_data_from_csv(filename):
    conn = connect_db()
    if conn is None:
        print("Erreur de connexion à la base de données.")
        return

    cursor = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Utiliser DictReader pour lire le CSV en tant que dictionnaire

        for row in reader:
            print("Ligne lue :", row)  # Affiche chaque ligne
            try:
                titre = row['Titre']
                # Vérifiez si 'Type' est nécessaire ; si non, commentez ou supprimez cette ligne
                # type_procedure = row['Type']  
            except KeyError as e:
                # print(f"Erreur : La clé {str(e)} n'existe pas dans la ligne : {row}")
                continue  # Ignorez cette ligne si une clé est manquante

            print(f"Vérification de l'existence de la procédure : Titre = '{titre}'")
            cursor.execute(
                "SELECT COUNT(*) FROM procedures WHERE titre = %s",
                (titre,)
            )
            exists = cursor.fetchone()[0] > 0

            if not exists:  # Si la procédure n'existe pas, insérer
                print(f"Insertion de la procédure : Titre = '{titre}'")
                cursor.execute(
                    # "INSERT INTO procedures (titre, description_texte, description_pieces_a_fournir, description_cout, description_conditions_acces, source) VALUES (%s, %s, %s, %s, %s, %s)",
                    "INSERT INTO procedures (titre, description_texte, description_pieces_a_fournir, description_cout, description_conditions_acces, source, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
                    (
                        titre,
                        row.get('Description', ""),
                        row.get('Pièces à fournir', ""),
                        row.get('Coût', ""),
                        row.get('Conditions d\'accès', ""),
                        row.get('Source', "")
                    )
                )
            else:
                print(f"Procedure '{titre}' existe déjà, sautée.")

    conn.commit()
    cursor.close()
    conn.close()


def insert_avocats_from_csv(file_path):
    """
    Fonction pour insérer des contacts avocats à partir d'un fichier CSV dans la table 'avocats'.
    """

    # Lire le fichier CSV dans un DataFrame
    data = pd.read_csv(file_path)
    
    # Remplacer les NaN dans les colonnes par des chaînes vides
    data.fillna('', inplace=True)

    # Se connecter à la base de données
    conn = connect_db()
    cursor = conn.cursor()

    # Parcourir les lignes du DataFrame et insérer les données dans la base de données
    for index, row in data.iterrows():
        # Vérifier si l'avocat existe déjà (en fonction de nom_prenom et email)
        cursor.execute(
            "SELECT 1 FROM avocats WHERE nom_prenom = %s AND email = %s", 
            (row['nom_prenom'], row['email'])
        )
        exists = cursor.fetchone()

        if exists:
            pass
            # print(f"L'avocat '{row['nom_prenom']}' existe déjà. Ignoré.")
        else:
            # Insérer l'avocat dans la base de données
            cursor.execute(
                '''
                INSERT INTO avocats (nom_prenom, adresse, telephone, email, specialisation, ville) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (row['nom_prenom'], row['adresse'], row['telephone'], row['email'], row['specialisation'], row['ville'])
            )
            # print(f"L'avocat '{row['nom_prenom']}' a été ajouté.")

    # Valider les modifications dans la base de données
    conn.commit()

    # Fermer le curseur et la connexion
    cursor.close()
    conn.close()
    print("Insertion des avocats terminée.")


# def insert_data_from_csv(file_path):
#     # Lire le fichier CSV
#     data = pd.read_csv(file_path)
    
#     conn = connect_db()
#     cursor = conn.cursor()
    
#     # Insérer les données dans la table FAQ
#     for index, row in data.iterrows():
#         cursor.execute(
#             'INSERT INTO faq (question, response, tag) VALUES (%s, %s, %s)',
#             (row['Question'], row['Réponse'], row['Tag'])
#         )
    
#     conn.commit()
#     cursor.close()
#     conn.close()

# def insert_data_from_csv(file_path):
#     # Lire le fichier CSV
#     data = pd.read_csv(file_path)
    
#     conn = connect_db()
#     cursor = conn.cursor()
    
#     # Insérer les données dans la table FAQ
#     for index, row in data.iterrows():
#         cursor.execute(
#             '''
#             INSERT INTO faq (categorie, tag, sous_categorie, question, reponse, article_reference) 
#             VALUES (%s, %s, %s, %s, %s, %s)
#             ''',
#             (row['Categorie'], row['Tag'], row['Sous categorie'], row['Question'], row['Réponse'], row['Article_reference'])
#         )
    
#     conn.commit()
#     cursor.close()
#     conn.close()



