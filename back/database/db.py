# import psycopg2
# import pandas as pd
# def connect_db():
#     conn = psycopg2.connect(
#         dbname='projet_chatbot',
#         user='issaka',
#         password='issaka',
#         host='localhost',
#         port='5432'
#     )
#     return conn

# # def create_tables():
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
#     conn.commit()
#     cursor.close()
#     conn.close()

# def log_chat(question, response="Aucune entité trouvée."):
#     conn = connect_db()
#     cursor = conn.cursor()
#     create_tables()
#     cursor.execute(
#         'INSERT INTO chat_history (question, response) VALUES (%s, %s)',
#         (question, response)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()
# # database.py
# from app.models.models import db

# def add_notification(message):
#     conn = connect_db()
#     cur = conn.cursor()
    
#     cur.execute("INSERT INTO notifications (message) VALUES (%s);", (message,))
#     conn.commit()
#     cur.close()
#     conn.close()


# def create_tables():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS notifications (
#             id SERIAL PRIMARY KEY,
#             message TEXT NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             is_read BOOLEAN DEFAULT FALSE
#         );
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS chat_history (
#             id SERIAL PRIMARY KEY,
#             question TEXT NOT NULL,
#             response TEXT NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     ''')
#     # Créer la table de FAQ
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS faq (
#             id SERIAL PRIMARY KEY,
#             question TEXT NOT NULL,
#             response TEXT NOT NULL,
#             tag TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     ''')
    
#     conn.commit()
#     cursor.close()
#     conn.close()



# def insert_data_from_csv(file_path):
#     # Lire le fichier CSV
#     data = pd.read_csv(file_path)
    
#     conn = connect_db()
#     cursor = conn.cursor()
    
#     # Insérer les données dans la table chat_history
#     for index, row in data.iterrows():
#         cursor.execute(
#             'INSERT INTO chat_history (question, response) VALUES (%s, %s)',
#             (row['question'], row['response'])
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
#             'INSERT INTO faq (question, response, tag) VALUES (%s, %s, %s)',
#             (row['Question'], row['Réponse'], row['Tag'])
#         )
    
#     conn.commit()
#     cursor.close()
#     conn.close()


# # import psycopg2
# # from config import Config

# # def get_db_connection():
# #     conn = psycopg2.connect(
# #         host=Config.DB_HOST,
# #         database=Config.DB_NAME,
# #         user=Config.DB_USER,
# #         password=Config.DB_PASSWORD
# #     )
# #     return conn
