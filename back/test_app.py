from flask import Flask, request, jsonify
import spacy
import psycopg2

app = Flask(__name__)

# Charger le modèle NLP entraîné
nlp = spacy.load("modele_procedures")  # Utiliser le modèle que vous avez sauvegardé

# Connexion à la base de données PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname="nom_base",
        user="utilisateur",
        password="mot_de_passe",
        host="localhost"
    )
    return conn

@app.route('/procedure', methods=['GET'])
def get_procedure():
    question = request.args.get('question')

    # Utiliser le modèle NLP pour analyser la question
    doc = nlp(question)
    entite_detectee = None

    # Vérifier si une entité spécifique est détect
    # Vérifier si une entité spécifique est détectée (par exemple "PROCEDURE_ADMIN")
    for ent in doc.ents:
        entite_detectee = ent.label_  # Entité comme "PROCEDURE_ADMIN"
        break

    # Connexion à la base de données
    conn = connect_db()
    cursor = conn.cursor()

    # Si l'entité détectée est "PROCEDURE_ADMIN"
    if entite_detectee == "PROCEDURE_ADMIN":
        # Vous pouvez interroger votre base de données avec les mots-clés dans la question
        if "documents" in question.lower():
            query = "SELECT documents_requis FROM procedures_administratives WHERE titre ILIKE %s"
        elif "délai" in question.lower():
            query = "SELECT delai FROM procedures_administratives WHERE titre ILIKE %s"
        else:
            # Sinon, récupérer toutes les informations sur la procédure
            query = "SELECT titre, description FROM procedures_administratives WHERE titre ILIKE %s"

        # Exemple avec "carte d'identité" pour la recherche
        cursor.execute(query, ("%carte d'identité%",))
        reponse = cursor.fetchone()

        if reponse:
            return jsonify({"reponse": reponse})
        else:
            return jsonify({"message": "Aucune information trouvée."})

    # Gestion d'autres entités à ajouter plus tard (comme DROIT_TRAVAIL, DROIT_CIVIL)

    cursor.close()
    conn.close()

    return jsonify({"message": "Aucune entité détectée."})

if __name__ == '__main__':
    app.run(debug=True)
