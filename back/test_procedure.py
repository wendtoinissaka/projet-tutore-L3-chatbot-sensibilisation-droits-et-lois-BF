from flask import Flask, request, jsonify
import spacy
import psycopg2

app = Flask(__name__)

# Charger le modèle NLP
nlp = spacy.load("modele_juridique_chatbot_info")

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

@app.route('/procedure', methods=['GET'])
def get_procedure():
    question = request.args.get('question')

    # Utiliser le modèle NLP pour analyser la question
    doc = nlp(question)
    entite_detectee = None

    # Vérifier si une entité spécifique est détectée (par exemple PROCEDURE_ADMIN)
    for ent in doc.ents:
        entite_detectee = ent.label_  # Entité comme "PROCEDURE_ADMIN", "DROIT_TRAVAIL"
        break

    # Connexion à la base de données
    conn = connect_db()
    cursor = conn.cursor()

    # Exemple pour une entité PROCEDURE_ADMIN (pour une procédure administrative)
    if entite_detectee == "PROCEDURE_ADMIN":
        # Identifier les mots-clés dans la question pour savoir quoi interroger
        if "documents" in question.lower():
            # Si la question concerne les documents requis, interroger ce champ spécifique
            query = "SELECT documents_requis FROM procedures_administratives WHERE titre ILIKE %s"
        elif "délai" in question.lower():
            # Si la question concerne le délai, interroger le champ 'delai'
            query = "SELECT delai FROM procedures_administratives WHERE titre ILIKE %s"
        else:
            # Sinon, récupérer toutes les informations générales sur la procédure
            query = "SELECT titre, description FROM procedures_administratives WHERE titre ILIKE %s"

        # Exécuter la requête SQL avec un paramètre de recherche basé sur la question
        cursor.execute(query, ("%carte d'identité%",))
        reponse = cursor.fetchone()

        if reponse:
            return jsonify({"reponse": reponse})
        else:
            return jsonify({"message": "Aucune information trouvée."})

    # Vous pouvez ajouter une logique similaire pour d'autres entités (comme DROIT_TRAVAIL)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
