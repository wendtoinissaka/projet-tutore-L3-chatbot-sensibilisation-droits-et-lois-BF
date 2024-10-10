from ast import main
import threading
from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_socketio import emit
import psycopg2
import spacy
from database import add_notification, connect_db, get_all_subscribers, log_chat
from flask_mail import Message
from flask_mail import Mail
from models.models import db, Abonnee  # Assurez-vous d'importer le modèle Abonnee

# from routes.email_sender import send_email_to_subscribers
from templates.email_templates import get_email_content
# main_routes = Blueprint('main_routes', __name__)
# mail = Mail()

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


# Charger le modèle NLP
nlp = spacy.load("modele_chatbot_juridique02")

# Fonction pour calculer la similarité de texte entre deux questions
def calculer_similarite(question1, question2):
    doc1 = nlp(question1)
    doc2 = nlp(question2)
    return doc1.similarity(doc2)

# @main_routes.route('/question', methods=['POST'])
# def traiter_question():
#     # Récupérer la question de l'utilisateur
#     data = request.get_json()
#     question = data.get('question')

#     if not question:
#         return jsonify({"message": "Aucune question fournie."}), 400

#     # Utiliser le modèle spaCy pour prédire l'intention de la question
#     doc = nlp(question)
#     predicted_tag = max(doc.cats, key=doc.cats.get)  # Prendre l'intention avec la plus haute probabilité

#     # Connexion à la base de données PostgreSQL
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Récupérer toutes les questions et réponses associées au tag prédit
#     query = "SELECT question, reponse FROM faq WHERE tag = %s"
#     cursor.execute(query, (predicted_tag,))
#     resultats = cursor.fetchall()

#     if not resultats:
#         # Si aucune question n'est trouvée avec ce tag, retourner un message d'erreur
#         response = jsonify({"message": "Aucune question trouvée pour cette catégorie."})
#     else:
#         # Calculer la similarité entre la question utilisateur et celles dans la base de données
#         meilleure_similarite = 0
#         meilleure_question = None
#         meilleure_reponse = None

#         for row in resultats:
#             question_existante = row[0]  # Question stockée dans la base de données
#             reponse_existante = row[1]  # Réponse associée à la question dans la base de données
#             similarite = calculer_similarite(question, question_existante)

#             # Si la similarité est meilleure, on met à jour la meilleure réponse
#             if similarite > meilleure_similarite:
#                 meilleure_similarite = similarite
#                 meilleure_question = question_existante
#                 meilleure_reponse = reponse_existante

#         # Définir un seuil de similarité (ajustable selon les besoins)
#         seuil_similarite = 0.6

#         # Si la similarité est inférieure au seuil, proposer des questions similaires
#         if meilleure_similarite < seuil_similarite:
#             # Renvoyer un message d'incertitude et proposer des questions similaires
#             questions_similaires = [row[0] for row in resultats[:3]]  # Limiter à 5 questions similaires
#             suggestions_formatees = "\n".join(questions_similaires)  # Formater les suggestions en texte
#             # response_message = f"Je ne connais pas la réponse exacte à votre question. Voici des questions similaires :\n{suggestions_formatees}"
#             response_message = f"Je ne connais pas la réponse exacte à votre question. Voici des questions qui pourrait vous intéressez :\n{suggestions_formatees}"
#             response = jsonify({"message": response_message})
#         else:
#             # Retourner la meilleure réponse trouvée si la similarité est suffisante
#             response_message = f"Voici la réponse à votre question : {meilleure_reponse}"
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

    if not question:
        return jsonify({"message": "Aucune question fournie."}), 400

    # Utiliser le modèle spaCy pour prédire l'intention de la question
    doc = nlp(question)
    predicted_tag = max(doc.cats, key=doc.cats.get)

    # Connexion à la base de données PostgreSQL
    conn = connect_db()
    cursor = conn.cursor()

    # Récupérer la catégorie, la question et la réponse associées au tag prédit
    query = "SELECT categorie, question, reponse, article_reference FROM faq WHERE tag = %s"
    cursor.execute(query, (predicted_tag,))
    resultats = cursor.fetchall()

    if not resultats:
        response = jsonify({"message": "Aucune question trouvée pour cette catégorie."})
    else:
        # Ajustement dynamique du seuil de similarité
        questions_tag = [row[1] for row in resultats]
        if len(questions_tag) > 10:
            seuil_similarite = 0.7
        else:
            seuil_similarite = 0.5

        meilleure_similarite = 0
        meilleure_question = None
        meilleure_reponse = None
        article_reference = None

        for row in resultats:
            categorie_existante = row[0]
            question_existante = row[1]
            reponse_existante = row[2]
            article_reference = row[3]
            similarite = calculer_similarite(question, question_existante)

            if similarite > meilleure_similarite:
                meilleure_similarite = similarite
                meilleure_question = question_existante
                meilleure_reponse = reponse_existante
                if categorie_existante == "droit_travail":
                    article_reference = row[3]

        if meilleure_similarite < seuil_similarite:
            questions_similaires = [row[1] for row in resultats[:3]]
            suggestions_formatees = "\n".join(questions_similaires)
            response_message = f"Je ne connais pas la réponse exacte à votre question. Voici des questions qui pourraient vous intéresser :\n{suggestions_formatees}"
            response = jsonify({"message": response_message})
        else:                                                                                                               
            response_message = f"{meilleure_reponse}"
            if article_reference:  # Ajouter l'article de référence si disponible
                response_message += f"\nPour plus de détails, consultez l'article : {article_reference}"
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

# @main_routes.route("/notifications", methods=["GET"])
# def get_notifications():
#     conn = connect_db()
#     cur = conn.cursor()
    
#     cur.execute("SELECT * FROM notifications WHERE is_read = FALSE;")
#     notifications = cur.fetchall()

#     for notification in notifications:
#         cur.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s;", (notification[0],))
    
#     conn.commit()
#     cur.close()
#     conn.close()
    
#     return jsonify(notifications)

# @main_routes.route("/notifications", methods=["GET"])
# def get_notifications():
#     conn = connect_db()
#     cur = conn.cursor()

#     cur.execute("SELECT id, message, created_at, is_read FROM notifications WHERE is_read = FALSE;")
#     rows = cur.fetchall()

#     # Transformer chaque ligne en un dictionnaire
#     notifications = [
#         {
#             "id": row[0],
#             "message": row[1],
#             "created_at": row[2],
#             "is_read": row[3]
#         }
#         for row in rows
#     ]

#     # Marquer les notifications comme lues
#     for notification in notifications:
#         cur.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s;", (notification["id"],))

#     conn.commit()
#     cur.close()
#     conn.close()

#     return jsonify(notifications)

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




# Route pour les notifications
@main_routes.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    message = data.get('message')

    if message:
        # Émettre une notification via WebSocket
        emit('new_notification', {'message': message}, broadcast=True)
        return jsonify({"status": "Notification envoyée"}), 200
    else:
        return jsonify({"error": "Aucun message fourni"}), 400




# @main_routes.route("/notifications", methods=["GET"])
# def get_notifications():
#     conn = connect_db()
#     cur = conn.cursor()
    
#     cur.execute("SELECT * FROM notifications WHERE is_read = FALSE;")
#     notifications = cur.fetchall()

#     for notification in notifications:
#         cur.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s;", (notification[0],))
    
#     conn.commit()
#     cur.close()
#     conn.close()
    
#     return jsonify(notifications)



# # Route pour ajouter une nouvelle notification
# @main_routes.route('/add_notification', methods=['POST'])
# def create_notification():
#     data = request.get_json()
#     message = data.get('message')
    
#     if not message:
#         return jsonify({"error": "Message de notification manquant."}), 400

#     # Ajouter la notification à la base de données
#     add_notification(message)

#     # Émettre l'événement de nouvelle notification via SocketIO
#     socketio.emit('new_notification', {'message': message})

#     return jsonify({"status": "Notification ajoutée avec succès"}), 201


# @main_routes.route('/send_email', methods=['POST'])
# def send_email():
#     data = request.json
#     subject = data.get('subject')
#     recipient = data.get('recipient')
#     body = data.get('body')

#     if subject and recipient and body:
#         try:
#             msg = Message(subject=subject, recipients=[recipient], body=body)
#             mail.send(msg)  # Utilisez l'instance mail ici
#             return jsonify({"status": "Email envoyé"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"error": "Données manquantes"}), 400


# @main_routes.route('/send_email', methods=['POST'])
# def send_email():
#     """Envoie un e-mail à tous les abonnés après l'ajout d'une notification."""
#     # Récupérer le message de la notification
#     notification_message = request.form.get('message')
    
#     if not notification_message:
#         return jsonify({"error": "Le message de notification est requis"}), 400

#     # Ajouter la notification dans la base de données
#     add_notification(notification_message)
    
#     # Récupérer tous les abonnés
#     abonnes = get_all_subscribers()

#     if not abonnes:
#         return jsonify({"error": "Aucun abonné trouvé"}), 404
    
#     # Envoyer un e-mail à chaque abonné
#     for email in abonnes:
#         msg = Message(subject="VEENGE-MAAN-CHATBOT : Nouvelle évolution législative",
#                       sender="lacapacitee@gmail.com",
#                       recipients=[email])
        
#         # Utiliser le contenu HTML pour le corps de l'e-mail
#         msg.html = get_email_content(notification_message)  # Utiliser le contenu HTML
        
#         try:
#             mail.send(msg)  # Envoyer l'e-mail
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     return jsonify({"success": f"Emails envoyes a {len(abonnes)} abonnes"}), 200



# @main_routes.route('/send_email', methods=['POST'])
# def send_email():
#     data = request.json
#     subject = data.get('subject')
#     recipient = data.get('recipient')
#     body = data.get('body')

#     if subject and recipient and body:
#         try:
#             msg = Message(subject=subject, recipients=[recipient], body=body)
#             main.send(msg)
#             return jsonify({"status": "Email envoyé"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"error": "Données manquantes"}), 400


# @app.route('/notify_all_mail', methods=['POST'])
# def notify_all():
#     try:
#         # Récupérer tous les utilisateurs de la base de données (exemple)
#         users = User.query.all()  # Assure-toi d'avoir un modèle User configuré avec leurs emails

#         # Message à envoyer
#         message_content = "Une nouvelle loi a été ajoutée. Consultez votre chatbot pour plus de détails."

#         # Envoyer un email à chaque utilisateur
#         for user in users:
#             msg = Message('Nouvelle notification légale',
#                           recipients=[user.email])
#             msg.body = message_content
#             mail.send(msg)

#         return "Emails envoyés à tous les utilisateurs", 200
#     except Exception as e:
#         return str(e), 500
