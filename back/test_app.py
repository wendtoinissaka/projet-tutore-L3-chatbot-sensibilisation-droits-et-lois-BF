from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import psycopg2

app = Flask(__name__)
CORS(app)

# Charger le modèle NLP entraîné pour les lois et les procédures
nlp = spacy.load("modele_lois_procedures")

# Connexion à la base de données PostgreSQL
def connect_db():
    # Connexion à la base de données
    conn = psycopg2.connect(
        dbname='projet_chatbot',
        user='issaka',
        password='issaka',
        host='localhost',
        port='5432'
)

    return conn

# Fonction pour extraire les entités détectées dans une question
def extraire_entites(doc):
    entites = {}
    for ent in doc.ents:
        entites[ent.label_] = ent.text
    return entites

# Changer la route pour utiliser POST au lieu de GET
@app.route('/question', methods=['POST'])
def traiter_question():
    # Récupérer les données envoyées via POST
    data = request.get_json()
    question = data.get('question')

    # Vérifier si la question a été fournie
    if not question:
        return jsonify({"error": "Aucune question fournie."}), 400

    # Utiliser le modèle NLP pour analyser la question
    doc = nlp(question)
    entites = extraire_entites(doc)

    # Connexion à la base de données
    conn = connect_db()
    cursor = conn.cursor()

    # Si une entité LOI est détectée
    if 'LOI' in entites:
        loi = entites['LOI']
        # Gérer les autres entités si elles sont présentes
        titre = entites.get('TITRE', None)
        chapitre = entites.get('CHAPITRE', None)
        section = entites.get('SECTION', None)
        article = entites.get('ARTICLE', None)

        # Construire une requête dynamique en fonction des entités trouvées
        query = "SELECT Lois.Nom, Titres.Nom, Chapitres.Nom, Sections.Titre, Articles.Article, Articles.Texte FROM Lois"
        query += " LEFT JOIN Titres ON Lois.ID = Titres.Lois_ID"
        query += " LEFT JOIN Chapitres ON Titres.ID = Chapitres.Titres_ID"
        query += " LEFT JOIN Sections ON Chapitres.ID = Sections.Chapitres_ID"
        query += " LEFT JOIN Articles ON Sections.ID = Articles.Sections_ID"
        query += " WHERE Lois.Nom ILIKE %s"

        params = [f'%{loi}%']

        # Ajouter les autres conditions si présentes
        if titre:
            query += " AND Titres.Nom ILIKE %s"
            params.append(f'%{titre}%')
        if chapitre:
            query += " AND Chapitres.Nom ILIKE %s"
            params.append(f'%{chapitre}%')
        if section:
            query += " AND Sections.Titre ILIKE %s"
            params.append(f'%{section}%')
        if article:
            query += " AND Articles.Article ILIKE %s"
            params.append(f'%{article}%')

        cursor.execute(query, tuple(params))
        resultats = cursor.fetchall()

        # Formater les résultats
        lois_data = []
        for row in resultats:
            lois_data.append({
                "loi": row[0],
                "titre": row[1],
                "chapitre": row[2],
                "section": row[3],
                "article": row[4],
                "texte": row[5]
            })

        return jsonify(lois_data)

    # Si une entité PROCEDURE est détectée
    if 'PROCEDURE' in entites:
        procedure = entites['PROCEDURE']
        query = "SELECT titre, description, type_procedure FROM procedures WHERE titre ILIKE %s"
        cursor.execute(query, (f'%{procedure}%',))
        procedure_resultat = cursor.fetchone()

        if procedure_resultat:
            return jsonify({
                "titre": procedure_resultat[0],
                "description": procedure_resultat[1],
                "type_procedure": procedure_resultat[2]
            })
        else:
            return jsonify({"message": "Aucune procédure trouvée."})

    cursor.close()
    conn.close()

    return jsonify({"message": "Aucune entité reconnue."})

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# import spacy
# import psycopg2

# app = Flask(__name__)

# # Charger le modèle NLP entraîné
# nlp = spacy.load("modele_procedures")  # Utiliser le modèle que vous avez sauvegardé

# # Connexion à la base de données PostgreSQL
# def connect_db():
#     conn = psycopg2.connect(
#         dbname="nom_base",
#         user="utilisateur",
#         password="mot_de_passe",
#         host="localhost"
#     )
#     return conn

# @app.route('/procedure', methods=['GET'])
# def get_procedure():
#     question = request.args.get('question')

#     # Utiliser le modèle NLP pour analyser la question
#     doc = nlp(question)
#     entite_detectee = None

#     # Vérifier si une entité spécifique est détect
#     # Vérifier si une entité spécifique est détectée (par exemple "PROCEDURE_ADMIN")
#     for ent in doc.ents:
#         entite_detectee = ent.label_  # Entité comme "PROCEDURE_ADMIN"
#         break

#     # Connexion à la base de données
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Si l'entité détectée est "PROCEDURE_ADMIN"
#     if entite_detectee == "PROCEDURE_ADMIN":
#         # Vous pouvez interroger votre base de données avec les mots-clés dans la question
#         if "documents" in question.lower():
#             query = "SELECT documents_requis FROM procedures_administratives WHERE titre ILIKE %s"
#         elif "délai" in question.lower():
#             query = "SELECT delai FROM procedures_administratives WHERE titre ILIKE %s"
#         else:
#             # Sinon, récupérer toutes les informations sur la procédure
#             query = "SELECT titre, description FROM procedures_administratives WHERE titre ILIKE %s"

#         # Exemple avec "carte d'identité" pour la recherche
#         cursor.execute(query, ("%carte d'identité%",))
#         reponse = cursor.fetchone()

#         if reponse:
#             return jsonify({"reponse": reponse})
#         else:
#             return jsonify({"message": "Aucune information trouvée."})

#     # Gestion d'autres entités à ajouter plus tard (comme DROIT_TRAVAIL, DROIT_CIVIL)

#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Aucune entité détectée."})

# if __name__ == '__main__':
#     app.run(debug=True)
