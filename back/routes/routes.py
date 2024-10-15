from ast import main
import hashlib
import os
import random
import re
import string
import threading
import uuid
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, session
from flask_mail import Mail, Message
from flask_socketio import emit
import psycopg2
import spacy                                                                                                                                                                                                                                                                                                                                                                                                                    
from sqlalchemy import func
from database import add_notification, connect_db, get_all_subscribers, log_chat
from flask_mail import Message
from flask_mail import Mail
from models.models import Avocat, Notification, Procedure, User, UserContext, db, Abonnee  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib  # Pour comparer la similarité des chaînes
import pandas as pd
import re
from flask import jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# from routes.email_sender import send_email_to_subscribers
from templates.email_templates import get_email_content
# main_routes = Blueprint('main_routes', __name__)
# mail = Mail()

load_dotenv()  # Charge les variables d'environnement depuis .env

main_routes = Blueprint('main_routes', __name__)

# Assurez-vous d'avoir importé l'instance de Mail dans ce fichier
mail = Mail()

def init_routes(app, socketio):
    @app.route('/add_notification', methods=['POST'])  # Utilisez app.route ici
    def create_notification():
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({"error": "Message de notification manquant."}), 400

        add_notification(message)

        socketio.emit('new_notification', {'message': message})  # Ajustez selon la version
        return jsonify({"status": "Notification ajoutée avec succès"}), 201

    app.register_blueprint(main_routes)



# Fonction pour prétraiter les textes
def pretraiter_texte(texte):
    # Mise en minuscules
    texte = texte.lower()
    # Suppression des caractères spéciaux et de la ponctuation
    texte = re.sub(r'[^a-z0-9\s]', '', texte)
    # Suppression des espaces multiples
    texte = re.sub(r'\s+', ' ', texte).strip()
    return texte

# Créer une fonction pour calculer la matrice TF-IDF pour toutes les questions
def creer_matrice_tfidf(resultats):
    questions_tag = [pretraiter_texte(row[1]) for row in resultats]
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(questions_tag), vectorizer

# Fonction pour calculer la similarité
def calculer_similarite(question, tfidf_matrix, vectorizer):
    question_pretraitee = pretraiter_texte(question)
    tfidf_question = vectorizer.transform([question_pretraitee])
    similarite = cosine_similarity(tfidf_question, tfidf_matrix)
    return similarite[0]  # Renvoie le vecteur de similarité


# Charger le modèle NLP
# nlp = spacy.load("modele_chatbot_juridique02")
# nlp = spacy.load("modele_chatbot_juridique03")
# nlp = spacy.load("services/modele_chatbot_juridique4")
nlp = spacy.load("services/modele_veenge_maan_chatbot_juridique")


# # Fonction pour calculer la similarité de texte entre deux questions
# def calculer_similarite(question1, question2):
#     doc1 = nlp(question1)
#     doc2 = nlp(question2)
#     return doc1.similarity(doc2)

# # Fonction pour calculer la similarité avec TF-IDF et cosine similarity
# def calculer_similarite(question1, question2):
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform([question1, question2])
#     similarite = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#     return similarite[0][0]


# Fonction pour rechercher un avocat spécifique
def search_lawyer(specialisation, ville):
    # Exemple de requête dans la base de données pour chercher un avocat par spécialisation et ville
    avocat = Avocat.query.filter_by(specialisation=specialisation, ville=ville).first()
    return avocat

# Fonction pour obtenir un avocat aléatoire
def get_random_avocat():
    # Exemple de sélection d'un avocat au hasard dans la base de données
    avocat = Avocat.query.order_by(func.random()).first()
    return avocat

def traiter_contact_avocat(question):
    # Spécialisations juridiques possibles et villes supportées
    specialisations_possibles = ['droit du travail', 'travail', 'droit pénal', 'droit civil', 'propriété intellectuelle', 'droit commercial']
    villes_possibles = ['Ouagadougou', 'ouaga', 'Bobo-Dioulasso', 'Ouahigouya', 'Koudougou']

    specialisation = None
    ville = None

    # Vérification de la spécialisation dans la question
    for specialisation_possible in specialisations_possibles:
        if specialisation_possible in question.lower():
            specialisation = specialisation_possible
            break

    # Vérification de la ville dans la question
    for ville_possible in villes_possibles:
        if ville_possible.lower() in question.lower():
            ville = ville_possible
            break

    # Debugging output
    print(f"Question analysée : {question}")
    print(f"Spécialisation détectée : {specialisation}")
    print(f"Ville détectée : {ville}")

    # Si la spécialisation est présente, mais pas la ville
    if specialisation and not ville:
        avocat = Avocat.query.filter_by(specialisation=specialisation).first()
        if avocat:
            response_message = f"Voici un avocat spécialisé en {specialisation} : {avocat.nom_prenom}. Vous pouvez le contacter au {avocat.telephone}."
        else:
            avocat = get_random_avocat()  # Sélectionner un avocat au hasard
            response_message = f"Je vous recommande {avocat.nom_prenom}, un avocat disponible. Vous pouvez le contacter au {avocat.telephone}."

    # Si la ville est présente, mais pas la spécialisation
    elif ville and not specialisation:
        avocat = Avocat.query.filter(Avocat.adresse.ilike(f'%{ville}%')).first()  # Utiliser ilike pour ignorer la casse
        if avocat:
            response_message = f"Voici un avocat à {ville} : {avocat.nom_prenom}. Vous pouvez le contacter au {avocat.telephone}."
        else:
            avocat = get_random_avocat()  # Sélectionner un avocat au hasard
            response_message = f"Je vous recommande {avocat.nom_prenom}, un avocat disponible. Vous pouvez le contacter au {avocat.telephone}."

    # Si les deux informations sont présentes
    elif specialisation and ville:
        avocat = Avocat.query.filter_by(specialisation=specialisation).filter(Avocat.adresse.ilike(f'%{ville}%')).first()
        if avocat:
            response_message = f"L'avocat spécialisé en {specialisation} à {ville} est {avocat.nom_prenom}. Vous pouvez le contacter au {avocat.telephone}."
        else:
            avocat = get_random_avocat()  # Sélectionner un avocat au hasard
            response_message = f"Je vous recommande {avocat.nom_prenom}, un avocat disponible. Vous pouvez le contacter au {avocat.telephone}."

    # Si aucune information n'est mentionnée
    else:
        avocat = get_random_avocat()
        if avocat:
            response_message = f"Je vous recommande {avocat.nom_prenom}, un avocat disponible. Vous pouvez le contacter au {avocat.telephone}."
        else:
            response_message = "Aucun avocat n'est disponible pour le moment."

    return response_message


# # Fonction pour traiter une question sur les procédures
# def traiter_procedure(question):
#     # Récupérer toutes les procédures depuis la base de données
#     procedures = Procedure.query.all()
    
#     if not procedures:
#         return "Aucune procédure trouvée."

#     meilleure_similarite = 0
#     meilleure_procedure = None

#     # Chercher la procédure avec le titre le plus similaire à la question
#     for procedure in procedures:
#         similarite = calculer_similarite(question, procedure.titre)
#         if similarite > meilleure_similarite:
#             meilleure_similarite = similarite
#             meilleure_procedure = procedure

#     # Définir un seuil pour considérer que la question est suffisamment similaire
#     seuil_similarite = 0.6  # Ajuste le seuil en fonction de tes résultats
#     if meilleure_similarite < seuil_similarite:
#         return "Je n'ai pas trouvé de procédure correspondant suffisamment à votre question."

#     # Retourner les détails de la procédure trouvée
#     response_message = (
#         f"Type : {meilleure_procedure.type}\n"
#         f"Titre : {meilleure_procedure.titre}\n"
#         f"Description : {meilleure_procedure.description_texte}\n"
#         f"Pièces à fournir : {meilleure_procedure.description_pieces_a_fournir}\n"
#         f"Coût : {meilleure_procedure.description_cout}\n"
#         f"Conditions d'accès : {meilleure_procedure.description_conditions_acces}\n"
#         f"Source : {meilleure_procedure.source}"
#     )
#     return response_message

# def nettoyer_texte(texte):
#     # Convertir en minuscules et supprimer les caractères spéciaux
#     texte = texte.lower()
#     texte = re.sub(r'[^a-zA-Z0-9\s]', '', texte)
#     return texte

def nettoyer_texte(texte):
    # Convertir en minuscules
    texte = texte.lower()
    # Supprimer la ponctuation et les chiffres
    texte = re.sub(r'[%s]' % re.escape(string.punctuation), '', texte)
    # Supprimer les espaces supplémentaires
    texte = re.sub(r'\s+', ' ', texte).strip()
    return texte

# def traiter_procedure(question):
#     # Nettoyer la question
#     question = nettoyer_texte(question)

#     # Récupérer toutes les procédures depuis la base de données
#     procedures = Procedure.query.all()
    
#     if not procedures:
#         return "Aucune procédure trouvée."

#     meilleure_similarite = 0
#     meilleure_procedure = None

#     for procedure in procedures:
#         titre_nettoye = nettoyer_texte(procedure.titre)  # Nettoyer le titre
#         description_nettoyee = nettoyer_texte(procedure.description_texte)  # Nettoyer la description

#         # Calculer la similarité avec le titre et la description
#         similarite_titre = calculer_similarite(question, titre_nettoye)
#         similarite_description = calculer_similarite(question, description_nettoyee)

#         # Prendre le maximum des similarités
#         similarite = max(similarite_titre, similarite_description)
#         print(f"Similarité avec '{procedure.titre}': {similarite}")  # Afficher la similarité
#         if similarite > meilleure_similarite:
#             meilleure_similarite = similarite
#             meilleure_procedure = procedure

#     seuil_similarite = 0.5  # Ajuste le seuil si nécessaire
#     if meilleure_similarite < seuil_similarite:
#         return "Je n'ai pas trouvé de procédure correspondant suffisamment à votre question."

#     response_message = (
#         f"Type : {meilleure_procedure.type}\n"
#         f"Titre : {meilleure_procedure.titre}\n"
#         f"Description : {meilleure_procedure.description_texte}\n"
#         f"Pièces à fournir : {meilleure_procedure.description_pieces_a_fournir}\n"
#         f"Coût : {meilleure_procedure.description_cout}\n"
#         f"Conditions d'accès : {meilleure_procedure.description_conditions_acces}\n"
#         f"Source : {meilleure_procedure.source}"
#     )
#     return response_message



# def traiter_procedure(question):
#     # Nettoyer la question
#     question = nettoyer_texte(question)

#     # Récupérer toutes les procédures depuis la base de données
#     procedures = Procedure.query.all()

#     if not procedures:
#         return "Je n'ai trouvé aucune procédure correspondant à votre demande."

#     # Trouver la procédure la plus similaire à la question
#     titres_procedures = [procedure.titre for procedure in procedures]
#     meilleur_titre = difflib.get_close_matches(question, titres_procedures, n=1)

#     if not meilleur_titre:
#         return "Je n'ai trouvé aucune procédure correspondant à votre demande."

#     # Récupérer la procédure correspondante
#     procedure_choisie = next(procedure for procedure in procedures if procedure.titre == meilleur_titre[0])

#     # Générer une réponse structurée
#     response_message = (
#         f"**Question :** {procedure_choisie.titre}\n"
#         f"**Réponse :** Voici comment procéder :\n"
#         f"1. **Description** : {procedure_choisie.description_texte}\n"
#         f"2. **Pièces à fournir** : {procedure_choisie.description_pieces_a_fournir or 'Aucune pièce requise.'}\n"
#         f"3. **Coût** : {procedure_choisie.description_cout or 'Non spécifié'}\n"
#         f"4. **Conditions d'accès** : {procedure_choisie.description_conditions_acces or 'Non spécifiées'}.\n\n"
#         f"Pour plus de détails, consultez la source officielle : [Lien vers la source]({procedure_choisie.source})"
#     )

#     return response_message




def traiter_procedure(question):
    # Nettoyer la question
    question = nettoyer_texte(question)

    # Récupérer toutes les procédures depuis la base de données
    procedures = Procedure.query.all()

    if not procedures:
        return "Je n'ai trouvé aucune procédure correspondant à votre demande."

    # Normaliser les titres des procédures
    titres_procedures = [nettoyer_texte(procedure.titre) for procedure in procedures]

    # Créer une matrice TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([question] + titres_procedures)

    # Calculer la similarité cosinus
    similarites = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Trouver l'index de la procédure avec la plus grande similarité
    index_max = similarites.argmax()
    similarite_max = similarites[index_max]

    # Seuil de similarité
    seuil_similarite = 0.1  # Vous pouvez ajuster ce seuil

    if similarite_max < seuil_similarite:
        return "Je n'ai trouvé aucune procédure correspondant à votre demande."

    # Récupérer la procédure correspondante
    procedure_choisie = procedures[index_max]

    # Générer une réponse structurée
    response_message = (
        # f"**Question :** {procedure_choisie.titre}\n"
        # f"**Réponse :** Voici comment procéder :\n"
        # f"1. **Description** : {procedure_choisie.description_texte}\n"
        f"{procedure_choisie.description_texte}\n"
        f"**Pièces à fournir** : {procedure_choisie.description_pieces_a_fournir or 'Aucune pièce requise.'}\n"
        f"**Coût** : {procedure_choisie.description_cout or 'Non spécifié'}\n"
        f"**Conditions d'accès** : {procedure_choisie.description_conditions_acces or 'Non spécifiées'}.\n\n"
        f"Pour plus de détails, consultez la source officielle : [Lien vers la source]({procedure_choisie.source})"
    )

    return response_message



# @main_routes.route('/question', methods=['POST'])
# def traiter_question():
#     # Récupérer la question de l'utilisateur
#     data = request.get_json()
#     question = data.get('question')
#     user_id = data.get('user_id')  # Assurons -nous  que l'ID de l'utilisateur est fourni

#     if not question:
#         return jsonify({"message": "Aucune question fournie."}), 400

#     # Utiliser le modèle spaCy pour prédire l'intention de la question
#     doc = nlp(question)
#     predicted_tag = max(doc.cats, key=doc.cats.get)
    
#     # Gérer le tag "contact_avocat"
#     if predicted_tag == "contact_avocat":
#         response_message = traiter_contact_avocat(question)  # Appel de la fonction qui traite ce tag
#         return jsonify({"message": response_message}), 200

#     # Si le tag prédit est "procedure", on traite la procédure
#     elif predicted_tag == "procedure":
#         response_message = traiter_procedure(question)
#         return jsonify({"message": response_message}), 200
                            
#     elif predicted_tag == "greeting":
#         return jsonify({"message": "Bonjour ! Je suis ravi de vous voir. Comment puis-je vous aider aujourd'hui?"})
#     elif predicted_tag == "introduce_self":
#         return jsonify({"message": "Je suis votre assistant virtuel dédié à vous fournir des informations juridiques. N'hésitez pas à poser vos questions."})
#     elif predicted_tag == "goodbye":
#         return jsonify({"message": "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions ou besoins d'informations."})
#     elif predicted_tag == "thank_you":
#         return jsonify({"message": "Je vous en prie ! C'est un plaisir de vous aider. Si vous avez d'autres questions, je suis là."})
#     elif predicted_tag == "chatbot_info":
#         return jsonify({"message": "Je suis un chatbot conçu pour répondre à vos questions juridiques concernant vos droits et les lois au Burkina Faso. Posez-moi vos questions!"})

#     # Connexion à la base de données PostgreSQL
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Récupérer la catégorie, la question et la réponse associées au tag prédit
#     query = "SELECT categorie, question, reponse, article_reference FROM faq WHERE tag = %s"
#     cursor.execute(query, (predicted_tag,))
#     resultats = cursor.fetchall()

#     if not resultats:
#         response = jsonify({"message": "Aucune question trouvée pour cette catégorie."})
#     else:
#         # Ajustement dynamique du seuil de similarité
#         questions_tag = [row[1] for row in resultats]
#         if len(questions_tag) > 10:
#             seuil_similarite = 0.7
#         else:
#             seuil_similarite = 0.5

#         meilleure_similarite = 0
#         meilleure_question = None
#         meilleure_reponse = None
#         article_reference = None

#         for row in resultats:
#             categorie_existante = row[0]
#             question_existante = row[1]
#             reponse_existante = row[2]
#             article_reference = row[3]
#             similarite = calculer_similarite(question, question_existante)

#             if similarite > meilleure_similarite:
#                 meilleure_similarite = similarite
#                 meilleure_question = question_existante
#                 meilleure_reponse = reponse_existante
#                 if categorie_existante == "droit_travail":
#                     article_reference = row[3]

#         if meilleure_similarite < seuil_similarite:
#             questions_similaires = [row[1] for row in resultats[:3]]
#             suggestions_formatees = "\n".join(questions_similaires)
#             # response_message = f"Je ne connais pas la réponse exacte à votre question. Voici des questions qui pourraient vous intéresser :\n\n{suggestions_formatees}"
#             response_message = f"Désolé, je ne connais pas encore la réponse à cette question. Je suis en constante amélioration, donc n'hésitez pas à me poser d'autres questions !"
#             # response_message = f"Je n'ai pas trouvé de réponse précise. Est-ce que l'une de ces questions est similaire à la vôtre ? Oui/Non :\n\n{suggestions_formatees}"
#             response = jsonify({"message": response_message})
#         else:                                                                                                               
#             response_message = f"{meilleure_reponse}"
#             if article_reference:  # Ajouter l'article de référence si disponible
#                 response_message += f"\n\nPour plus de détails, consultez l'article : {article_reference}"
#             response = jsonify({"message": response_message})

#     # Loguer la conversation dans la base de données
#     log_chat(question, response.get_data(as_text=True))
    

#     # Fermer la connexion à la base de données
#     cursor.close()
#     conn.close()

#     return response



@main_routes.route('/question', methods=['POST'])
def traiter_question():
        # Récupérer la question de l'utilisateur
        data = request.get_json()
        question = data.get('question')
        user_id = data.get('user_id')  # Assurons -nous  que l'ID de l'utilisateur est fourni

        if not question:
            return jsonify({"message": "Aucune question fournie."}), 400

        # Utiliser le modèle spaCy pour prédire l'intention de la question
        doc = nlp(question)
        predicted_tag = max(doc.cats, key=doc.cats.get)
        
        # Gérer le tag "contact_avocat"
        if predicted_tag == "contact_avocat":
            response_message = traiter_contact_avocat(question)
            return jsonify({"message": response_message}), 200

        # Si le tag prédit est "procedure", on traite la procédure
        elif predicted_tag == "procedure":
            response_message = traiter_procedure(question)
            return jsonify({"message": response_message}), 200
                                
        # Gérer d'autres tags comme les salutations, présentations, etc.
        elif predicted_tag == "greeting":
            return jsonify({"message": "Bonjour ! Je suis ravi de vous voir. Comment puis-je vous aider aujourd'hui?"})
        elif predicted_tag == "introduce_self":
            return jsonify({"message": "Je suis votre assistant virtuel dédié à vous fournir des informations juridiques. N'hésitez pas à poser vos questions."})
        elif predicted_tag == "goodbye":
            return jsonify({"message": "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions ou besoins d'informations."})
        elif predicted_tag == "thank_you":
            return jsonify({"message": "Je vous en prie ! C'est un plaisir de vous aider. Si vous avez d'autres questions, je suis là."})
        elif predicted_tag == "chatbot_info":
            return jsonify({"message": "Je suis un chatbot conçu pour répondre à vos questions juridiques concernant vos droits et les lois au Burkina Faso. Posez-moi vos questions!"})

        # Connexion à la base de données PostgreSQL
        conn = connect_db()
        cursor = conn.cursor()

        # Récupérer la catégorie, la question et la réponse associées au tag prédit
        query = "SELECT categorie, question, reponse, article_reference FROM faq WHERE tag = %s"
        cursor.execute(query, (predicted_tag,))
        resultats = cursor.fetchall()

        if not resultats:
            response = jsonify({"message": "Désolé, je ne connais pas encore la réponse à cette question. Je suis en constante amélioration,  donc n'hésitez pas à reformuler votre question ou à me poser d'autres questions !"})
        else:
            # Créer la matrice TF-IDF une seule fois
            tfidf_matrix, vectorizer = creer_matrice_tfidf(resultats)

            # Ajustement dynamique du seuil de similarité
            questions_tag = [row[1] for row in resultats]
            seuil_similarite = 0.7 if len(questions_tag) > 10 else 0.5

            meilleure_similarite = 0
            meilleure_question = None
            meilleure_reponse = None
            article_reference = None

            # Calculer la similarité pour toutes les questions
            similarites = calculer_similarite(question, tfidf_matrix, vectorizer)

            for i, row in enumerate(resultats):
                categorie_existante = row[0]
                question_existante = row[1]
                reponse_existante = row[2]
                article_reference = row[3]
                similarite = similarites[i]

                if similarite > meilleure_similarite:
                    meilleure_similarite = similarite
                    meilleure_question = question_existante
                    meilleure_reponse = reponse_existante
                    if categorie_existante == "droit_travail":
                        article_reference = row[3]

            if meilleure_similarite < seuil_similarite:
                questions_similaires = [row[1] for row in resultats[:3]]
                suggestions_formatees = "\n".join(questions_similaires)
                response_message = f"Désolé, je ne connais pas encore la réponse à cette question. Je suis en constante amélioration, donc n'hésitez pas à me poser d'autres questions !"
                response = jsonify({"message": response_message})
            else:                                                                                                               
                response_message = f"{meilleure_reponse}"
                if article_reference !="":  # Ajouter l'article de référence si disponible
                    response_message += f"\n\nPour plus de détails, consultez l'article : {article_reference}"
                response = jsonify({"message": response_message})

        # Loguer la conversation dans la base de données
        log_chat(question, response.get_data(as_text=True))
        
        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()

        return response




@main_routes.route("/laws", methods=["GET"])
def get_law():
    code = request.args.get('code')
    number = request.args.get('number')

    if not code or not number:
        return jsonify({"error": "Paramètres 'code' et 'number' sont requis"}), 400

    code_to_table = {
        'civil': 'code_civil',
        'famille': 'code_famille',
        'penale': 'code_penale',
        'travail': 'code_travail'
    }

    if code not in code_to_table:
        return jsonify({"error": f"Code {code} non supporté"}), 400

    table = code_to_table[code]

    conn = connect_db()
    cur = conn.cursor()

    try:
        query = f"SELECT texte FROM {table} WHERE article_num = %s"
        cur.execute(query, (number,))

        result = cur.fetchone()

        if result:
            return jsonify({"code": code, "article_num": number, "texte": result[0]})
        else:
            return jsonify({"error": f"Article {number} non trouvé dans le code {code}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@main_routes.route('/notification_signup', methods=['POST'])
def notification_signup():
    data = request.json
    email = data.get('email')
    numero = data.get('numero')

    # Vérification si au moins un champ est fourni
    if not email and not numero:
        return jsonify({"error": "Au moins un des champs (email ou numéro) est requis"}), 400

    # Vérifiez si l'abonné existe déjà (si l'email est fourni)
    if email and abonne_exists(email):
        return jsonify({"error": "L'email est déjà utilisé"}), 400

    # Insérer l'abonné dans la base de données
    new_abonnee = Abonnee(email=email, numero=numero)
    try:
        db.session.add(new_abonnee)  # Ajoute le nouvel abonné
        db.session.commit()  # Validez la transaction
        return jsonify({"status": "Inscription réussie"}), 201
    except Exception as e:
        db.session.rollback()  # Annulez la transaction en cas d'erreur
        print(f"Erreur lors de l'inscription : {e}")
        return jsonify({"error": "Erreur lors de l'inscription"}), 500


def abonne_exists(email):
    return db.session.query(Abonnee).filter_by(email=email).first() is not None





@main_routes.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.order_by(Notification.created_at.desc()).limit(3).all()
    return jsonify([{
        'id': n.id,
        'message': n.message,
        'created_at': n.created_at.isoformat(),  # Formatage de la date au format ISO
        'is_read': n.is_read
    } for n in notifications])


@main_routes.route('/', methods=['GET'])
def home():
    api_url = os.getenv("API_URL")  # Récupère l'URL de l'API
    return jsonify({
        "status": "L'application fonctionne correctement.",
        "api_link": api_url  # Utilise la variable d'environnement
    }), 200



@main_routes.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Vérifiez si l'utilisateur existe déjà
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'type': 'error', 'resultCode': 'UserAlreadyExists'}), 409

    # Générer un sel et un mot de passe haché
    salt = os.urandom(16).hex()  # Générer un sel aléatoire
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # Créer un nouvel utilisateur
    new_user = User(email=email, password=hashed_password, salt=salt)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'type': 'success', 'resultCode': 'UserCreated'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'inscription : {e}")
        return jsonify({"error": "Erreur lors de l'inscription"}), 500


@main_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'type': 'error', 'resultCode': 'InvalidInput'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'type': 'error', 'resultCode': 'InvalidCredentials'}), 401

    hashed_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
    if hashed_password != user.password:
        return jsonify({'type': 'error', 'resultCode': 'InvalidCredentials'}), 401

    # Authentification réussie
    return jsonify({'type': 'success', 'resultCode': 'UserLoggedIn'}), 200
