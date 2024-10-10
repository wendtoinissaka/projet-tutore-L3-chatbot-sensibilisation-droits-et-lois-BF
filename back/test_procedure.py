from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import psycopg2
import spacy

app = Flask(__name__)

# Charger le modèle SpaCy
nlp = spacy.load("fr_core_news_md")  # Modèle médium pour de meilleures embeddings

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Fonction pour créer la base de données
def create_database(dbname, user, password, host):
    # Connexion à la base de données par défaut pour pouvoir créer une nouvelle base
    conn = psycopg2.connect(
        dbname="postgres",  # Connexion à la base par défaut
        user=user,
        password=password,
        host=host
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Nécessaire pour créer une DB

    cursor = conn.cursor()
    
    # Vérifier si la base de données existe déjà
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{dbname}';")
    exists = cursor.fetchone()

    if not exists:
        # Créer la base de données si elle n'existe pas
        cursor.execute(f"CREATE DATABASE {dbname};")
        print(f"Base de données {dbname} créée avec succès.")
    else:
        print(f"La base de données {dbname} existe déjà.")

    cursor.close()
    conn.close()

# Fonction pour créer la table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Vérifier si la table existe déjà
    cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'legal_information'
    );
    """)
    exists = cursor.fetchone()[0]

    if not exists:
        # Créer la table si elle n'existe pas
        cursor.execute("""
        CREATE TABLE legal_information (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            vector FLOAT8[]  -- Pour stocker le vecteur comme un tableau de float
        );
        """)
        conn.commit()
        print("Table legal_information créée avec succès.")
    else:
        print("La table legal_information existe déjà.")

    cursor.close()
    conn.close()


# Exemple de fonction pour pré-calculer les embeddings
def get_embedding(text):
    doc = nlp(text)
    return np.mean([token.vector for token in doc], axis=0)

# Stocker les embeddings dans PostgreSQL
def store_embedding_in_db(id, text, conn):
    embedding = get_embedding(text)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE lois
        SET embedding = %s
        WHERE id = %s
    """, (embedding.tolist(), id))
    conn.commit()




# Fonction de connexion à la base de données
def connect_db():
    return psycopg2.connect(
        dbname="burkina_db2",
        user="postgres",
        password="postgres",
        host="localhost"
    )


# Vérification de l'existence d'une question
def question_exists(question):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Requête pour vérifier si la question existe déjà
    cursor.execute("SELECT COUNT(*) FROM legal_information WHERE question = %s;", (question,))
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    # Si le count est supérieur à 0, la question existe
    return count > 0

# # Fonction d'insertion des données avec vérification
# def insert_legal_data(question, answer):
#     try:
#         # Vérifier si la question existe déjà (optionnel si contrainte UNIQUE déjà présente)
#         if not question_exists(question):
#             conn = connect_db()
#             cursor = conn.cursor()
            
#             # Obtenir le vecteur de la question
#             question_doc = nlp(question)
#             question_vector = question_doc.vector.tolist()
            
#             # Insérer la question, la réponse et le vecteur dans la base de données
#             cursor.execute(
#                 "INSERT INTO legal_information (question, answer, vector) VALUES (%s, %s, %s);",
#                 (question, answer, question_vector)
#             )
            
#             conn.commit()
#             cursor.close()
#             conn.close()
#             print(f"Insertion réussie pour la question : {question}")
#     except psycopg2.errors.UniqueViolation:
#         # Gérer l'erreur de duplication
#         print(f"La question existe déjà et ne sera pas insérée : {question}")

# Fonction d'insertion des données avec vérification
def insert_legal_data(question, answer):
    # Vérifier si la question est vide ou non valide
    if pd.isna(question) or question.strip() == "":
        print("Question vide ou non valide, ignorée.")
        return
    
    # Vérifier si la question existe déjà
    if not question_exists(question):
        conn = connect_db()
        cursor = conn.cursor()
        
        # Obtenir le vecteur de la question
        question_doc = nlp(question)
        question_vector = question_doc.vector.tolist()
        
        # Insérer la question, la réponse et le vecteur dans la base de données
        cursor.execute(
            "INSERT INTO legal_information (question, answer, vector) VALUES (%s, %s, %s);",
            (question, answer, question_vector)
        )
        
        # Confirmer les changements
        conn.commit()
        
        cursor.close()
        conn.close()
        print(f"Insertion réussie pour la question : {question}")
    else:
        print(f"La question existe déjà : {question}")


# Fonction principale pour lire le CSV et insérer les données
def insert_data_from_csv(file_path):
    # Lire le fichier CSV
    data = pd.read_csv(file_path)
    
    # Parcourir les lignes du DataFrame
    for index, row in data.iterrows():
        question = row['Question']
        answer = row['Réponse']
        
        # Insérer dans la base de données
        insert_legal_data(question, answer)





def find_best_answer(user_question):
    best_similarity = 0
    best_answer = "Désolé, je n'ai pas compris votre question. Pouvez-vous reformuler ?"
    
    user_doc = nlp(user_question)
    user_vector = user_doc.vector

    legal_data = get_legal_data()  # Suppose que cela récupère les questions et leurs vecteurs
   
    for question, answer, vector in legal_data:
        similarity = cosine_similarity(user_vector, vector)  # Utilisez une fonction pour calculer la similarité cosinus

        if similarity > best_similarity:
            best_similarity = similarity
            best_answer = answer

    return best_answer


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))



# Récupérer toutes les questions et réponses de la base de données
def get_legal_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM legal_information;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# # Calculer la similarité entre la question de l'utilisateur et les questions de la base de données
# def find_best_answer(user_question):
#     best_similarity = 0
#     best_answer = "Désolé, je n'ai pas compris votre question. Pouvez-vous reformuler ?"
    
#     user_doc = nlp(user_question)
#     legal_data = get_legal_data()
    
#     for question, answer in legal_data:
#         question_doc = nlp(question)
#         similarity = user_doc.similarity(question_doc)

#         if similarity > best_similarity:
#             best_similarity = similarity
#             best_answer = answer

#     return best_answer

def find_best_answer(user_question):
    threshold = 0.75  # Définir un seuil de similarité
    best_similarity = 0
    best_answer = None
    
    user_doc = nlp(user_question)
    legal_data = get_legal_data()
    
    for question, answer in legal_data:
        question_doc = nlp(question)
        similarity = user_doc.similarity(question_doc)

        if similarity > best_similarity:
            best_similarity = similarity
            best_answer = answer

    if best_similarity < threshold:
        return "Désolé, je n'ai pas de réponse précise à votre question. Voici des suggestions : ..."
    return best_answer


# Route pour poser une question
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")
    response = find_best_answer(user_question)
    return jsonify({"response": response})

if __name__ == "__main__":
    # Chemin vers votre fichier CSV
    file_path = 'resultat_combined.csv'
    # Appeler la fonction pour insérer les données
    create_database("burkina_db2", "postgres", "postgres", "localhost")
    # Créer la table legal_information
    create_table()
    # insert_data_from_csv(file_path)
    app.run(debug=True)






# from flask import Flask, request, jsonify
# import spacy
# import psycopg2

# app = Flask(__name__)

# # Charger le modèle NLP
# nlp = spacy.load("modele_juridique_chatbot_info")

# # Connexion à la base de données PostgreSQL
# def connect_db():
#     # Connexion à la base de données
#     conn = psycopg2.connect(
#         dbname='projet_chatbot',
#         user='issaka',
#         password='issaka',
#         host='localhost',
#         port='5432'
#     )
#     return conn

# @app.route('/procedure', methods=['GET'])
# def get_procedure():
#     question = request.args.get('question')

#     # Utiliser le modèle NLP pour analyser la question
#     doc = nlp(question)
#     entite_detectee = None

#     # Vérifier si une entité spécifique est détectée (par exemple PROCEDURE_ADMIN)
#     for ent in doc.ents:
#         entite_detectee = ent.label_  # Entité comme "PROCEDURE_ADMIN", "DROIT_TRAVAIL"
#         break

#     # Connexion à la base de données
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Exemple pour une entité PROCEDURE_ADMIN (pour une procédure administrative)
#     if entite_detectee == "PROCEDURE_ADMIN":
#         # Identifier les mots-clés dans la question pour savoir quoi interroger
#         if "documents" in question.lower():
#             # Si la question concerne les documents requis, interroger ce champ spécifique
#             query = "SELECT documents_requis FROM procedures_administratives WHERE titre ILIKE %s"
#         elif "délai" in question.lower():
#             # Si la question concerne le délai, interroger le champ 'delai'
#             query = "SELECT delai FROM procedures_administratives WHERE titre ILIKE %s"
#         else:
#             # Sinon, récupérer toutes les informations générales sur la procédure
#             query = "SELECT titre, description FROM procedures_administratives WHERE titre ILIKE %s"

#         # Exécuter la requête SQL avec un paramètre de recherche basé sur la question
#         cursor.execute(query, ("%carte d'identité%",))
#         reponse = cursor.fetchone()

#         if reponse:
#             return jsonify({"reponse": reponse})
#         else:
#             return jsonify({"message": "Aucune information trouvée."})

#     # Vous pouvez ajouter une logique similaire pour d'autres entités (comme DROIT_TRAVAIL)

#     cursor.close()
#     conn.close()

# if __name__ == '__main__':
#     app.run(debug=True)
