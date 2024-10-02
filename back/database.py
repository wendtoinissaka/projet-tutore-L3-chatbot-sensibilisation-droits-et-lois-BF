from urllib.parse import urlparse
import pandas as pd
import psycopg2
from config import Config
import numpy as np
from models.models import db

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


# def connect_db():
#     conn = psycopg2.connect(
#         dbname=Config.DATABASE_NAME,
#         user=Config.DATABASE_USER,
#         password=Config.DATABASE_PASSWORD,
#         host=Config.DATABASE_HOST,
#         port=Config.DATABASE_PORT
#     )
#     return conn

# def create_tables():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS chat_history (
#             id SERIAL PRIMARY KEY,
#             question TEXT NOT NULL,
#             response TEXT NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS notifications (
#             id SERIAL PRIMARY KEY,
#             message TEXT NOT NULL,
#             is_read BOOLEAN DEFAULT FALSE
#         );
#     ''')

#     # Créer la table de FAQ avec la nouvelle structure
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS faq (
#             id SERIAL PRIMARY KEY,
#             categorie TEXT NOT NULL,
#             tag TEXT,
#             sous_categorie TEXT,
#             question TEXT NOT NULL,
#             reponse TEXT NOT NULL,
#             article_reference TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     ''')

#         # Créer la table de abonne
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS abonnee (
#             id SERIAL PRIMARY KEY,
#             email VARCHAR(255) UNIQUE,
#             numero VARCHAR(20) UNIQUE,
#             date_abonnement TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );

#     ''')
#         # Créer un trigger
#     cursor.execute('''
#         -- DROP TRIGGER IF EXISTS trigger_new_notification ON notifications;
#         DROP TRIGGER IF EXISTS trigger_new_notification ON notifications;
#         CREATE OR REPLACE FUNCTION notify_new_notification() RETURNS trigger AS $$
#         BEGIN
#             PERFORM pg_notify('new_notification', NEW.message);
#             RETURN NEW;
#         END;
#         $$ LANGUAGE plpgsql;

#         CREATE TRIGGER trigger_new_notification
#         AFTER INSERT ON notifications
#         FOR EACH ROW
#         EXECUTE FUNCTION notify_new_notification();


#     ''')

    
    
#     conn.commit()
#     cursor.close()
#     conn.close()


def create_tables(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Crée toutes les tables définies dans les modèles




def log_chat(question, response="Aucune entité trouvée."):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO chat_history (question, response) VALUES (%s, %s)',
        (question, response)
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



