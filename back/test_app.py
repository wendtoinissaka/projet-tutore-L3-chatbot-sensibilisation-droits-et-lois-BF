# from flask import Flask
# from database import create_tables
# from routes import bp as routes_bp

# app = Flask(__name__)

# app.register_blueprint(routes_bp)

# if __name__ == '__main__':
#     create_tables()  # Créer les tables si elles n'existent pas
#     app.run(debug=True)


# # from flask import Flask, request, jsonify, abort
# # from flask_cors import CORS
# # import spacy
# # import psycopg2

# # app = Flask(__name__)
# # CORS(app)

# # # Charger le modèle NLP entraîné pour les lois et les procédures
# # nlp = spacy.load("modele_lois_procedures")

# # # Connexion à la base de données PostgreSQL
# # def connect_db():
# #     # Connexion à la base de données
# #     conn = psycopg2.connect(
# #         dbname='projet_chatbot',
# #         user='issaka',
# #         password='issaka',
# #         host='localhost',
# #         port='5432'
# # )

# #     return conn

# # # Fonction pour extraire les entités détectées dans une question
# # def extraire_entites(doc):
# #     entites = {}
# #     for ent in doc.ents:
# #         entites[ent.label_] = ent.text
# #     return entites
# # def create_tables():
# #     conn = connect_db()
# #     cursor = conn.cursor()
# #     cursor.execute('''
# #         CREATE TABLE IF NOT EXISTS chat_history (
# #             id SERIAL PRIMARY KEY,
# #             question TEXT NOT NULL,
# #             response TEXT NOT NULL,
# #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# #         );
        
# #     ''')
# #     conn.commit()
# #     cursor.close()
# #     conn.close()
# # # Nouvelle fonction pour enregistrer l'historique
# # def log_chat(question, response="Aucune entité trouvée."):
# #     conn = connect_db()
# #     cursor = conn.cursor()
# #     create_tables()
# #     cursor.execute(
# #         'INSERT INTO chat_history (question, response) VALUES (%s, %s)',
# #         (question, response)
# #     )
# #     conn.commit()
# #     cursor.close()
# #     conn.close()

# # def add_notification(message):
# #     conn = connect_db()
# #     cur = conn.cursor()
    
# #     cur.execute("INSERT INTO notifications (message) VALUES (%s);", (message,))
# #     conn.commit()
# #     cur.close()
# #     conn.close()

# # @app.route('/question', methods=['POST'])
# # def traiter_question():
# #     # Récupérer les données envoyées via POST
# #     data = request.get_json()
# #     question = data.get('question')

# #     # Vérifier si la question a été fournie
# #     if not question:
# #         return jsonify({"error": "Aucune question fournie."}), 400

# #     # Utiliser le modèle NLP pour analyser la question
# #     doc = nlp(question)
# #     entites = extraire_entites(doc)

# #     # Connexion à la base de données
# #     conn = connect_db()
# #     cursor = conn.cursor()

# #     response = None  # Initialiser la variable response

# #     # Si une entité LOI est détectée
# #     if 'LOI' in entites:
# #         loi = entites['LOI']
# #         # Gérer les autres entités si elles sont présentes
# #         titre = entites.get('TITRE', None)
# #         chapitre = entites.get('CHAPITRE', None)
# #         section = entites.get('SECTION', None)
# #         article = entites.get('ARTICLE', None)

# #         # Construire une requête dynamique en fonction des entités trouvées
# #         query = "SELECT Lois.Nom, Titres.Nom, Chapitres.Nom, Sections.Titre, Articles.Article, Articles.Texte FROM Lois"
# #         query += " LEFT JOIN Titres ON Lois.ID = Titres.Lois_ID"
# #         query += " LEFT JOIN Chapitres ON Titres.ID = Chapitres.Titres_ID"
# #         query += " LEFT JOIN Sections ON Chapitres.ID = Sections.Chapitres_ID"
# #         query += " LEFT JOIN Articles ON Sections.ID = Articles.Sections_ID"
# #         query += " WHERE Lois.Nom ILIKE %s"

# #         params = [f'%{loi}%']

# #         # Ajouter les autres conditions si présentes
# #         if titre:
# #             query += " AND Titres.Nom ILIKE %s"
# #             params.append(f'%{titre}%')
# #         if chapitre:
# #             query += " AND Chapitres.Nom ILIKE %s"
# #             params.append(f'%{chapitre}%')
# #         if section:
# #             query += " AND Sections.Titre ILIKE %s"
# #             params.append(f'%{section}%')
# #         if article:
# #             query += " AND Articles.Article ILIKE %s"
# #             params.append(f'%{article}%')

# #         cursor.execute(query, tuple(params))
# #         resultats = cursor.fetchall()

# #         # Formater les résultats
# #         lois_data = []
# #         for row in resultats:
# #             lois_data.append({
# #                 "loi": row[0],
# #                 "titre": row[1],
# #                 "chapitre": row[2],
# #                 "section": row[3],
# #                 "article": row[4],
# #                 "texte": row[5]
# #             })

# #         response = jsonify(lois_data)

# #     # Si une entité PROCEDURE est détectée
# #     elif 'PROCEDURE' in entites:
# #         procedure = entites['PROCEDURE']
# #         query = "SELECT titre, description, type_procedure FROM procedures WHERE titre ILIKE %s"
# #         cursor.execute(query, (f'%{procedure}%',))
# #         procedure_resultat = cursor.fetchone()

# #         if procedure_resultat:
# #             response = jsonify({
# #                 "titre": procedure_resultat[0],
# #                 "description": procedure_resultat[1],
# #                 "type_procedure": procedure_resultat[2]
# #             })
# #         else:
# #             response = jsonify({"message": "Aucune procédure trouvée."})

# #     # Enregistrer dans l'historique, même si aucune entité n'a été trouvée
# #     if response is None:
# #         response = jsonify({"message": "Aucune entité reconnue."})

# #     log_chat(question, response.get_data(as_text=True))

# #     cursor.close()
# #     conn.close()

# #     return response

# # # Route pour récupérer un article depuis la base de données
# # @app.route("/laws", methods=["GET"])
# # def get_law():
# #     code = request.args.get('code')  # Exemple de code 'civil', 'penal', 'travail'
# #     number = request.args.get('number')  # Numéro d'article à rechercher

# #     # Validation des paramètres
# #     if not code or not number:
# #         return jsonify({"error": "Paramètres 'code' et 'number' sont requis"}), 400

# #     # Dictionnaire pour mapper les types de code aux tables correspondantes
# #     code_to_table = {
# #         'civil': 'code_civil',
# #         'famille': 'code_famille',
# #         'penale': 'code_penale',
# #         'travail': 'code_travail'
# #     }

# #     # Vérification si le code est supporté
# #     if code not in code_to_table:
# #         return jsonify({"error": f"Code {code} non supporté"}), 400

# #     # Récupérer la table correspondante au code
# #     table = code_to_table[code]

# #     # Se connecter à la base de données
# #     conn = connect_db()
# #     cur = conn.cursor()

# #     try:
# #         # Préparer la requête SQL pour récupérer l'article depuis la bonne table
# #         query = f"SELECT texte FROM {table} WHERE article_num = %s"
# #         cur.execute(query, (number,))

# #         # Récupérer le résultat
# #         result = cur.fetchone()

# #         # Si l'article est trouvé, le retourner en JSON
# #         if result:
# #             return jsonify({"code": code, "article_num": number, "texte": result[0]})
# #         else:
# #             return jsonify({"error": f"Article {number} non trouvé dans le code {code}"}), 404
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500
# #     finally:
# #         cur.close()
# #         conn.close()

# # @app.route("/notifications", methods=["GET"])
# # def get_notifications():
# #     conn = connect_db()
# #     cur = conn.cursor()
    
# #     cur.execute("SELECT * FROM notifications WHERE is_read = FALSE;")
# #     notifications = cur.fetchall()

# #     # Marquer les notifications comme lues
# #     for notification in notifications:
# #         cur.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s;", (notification[0],))
    
# #     conn.commit()
# #     cur.close()
# #     conn.close()
    
# #     return jsonify(notifications)

# # # Enregistrer les routes
# # # app.register_blueprint(main_routes)

# # if __name__ == '__main__':
# #     app.run(debug=True)

