from flask import current_app
from flask_mail import Message
from database import get_all_subscribers
from templates.email_templates import get_email_content
from flask_mail import Mail

def send_email_to_subscribers(notification_message):
    """Envoie un e-mail à tous les abonnés avec un message donné."""
    
    abonnes = get_all_subscribers()
    if not abonnes:
        return {"error": "Aucun abonné trouvé"}
    
    # Créer une instance de Mail dans le contexte d'application
    mail = Mail(current_app)

    for email in abonnes:
        msg = Message(subject="Nouvelle Notification",
                      sender="lacapacitee@gmail.com",
                      recipients=[email])
        
        # Utiliser le contenu HTML pour le corps de l'e-mail
        msg.html = get_email_content(notification_message)  # Utiliser le contenu HTML
        
        try:
            # Envelopper l'envoi d'e-mail dans un contexte d'application
            with current_app.app_context():
                mail.send(msg)  # Utiliser l'instance de Mail pour envoyer le message
                print(f"Email envoyé à : {email}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email à {email}: {str(e)}")
    
    return {"success": f"Emails envoyés à {len(abonnes)} abonnés"}

# from flask import current_app
# from flask_mail import Message

# from database import get_all_subscribers
# from templates.email_templates import get_email_content

# def send_email_to_subscribers(notification_message):
#     """Envoie un e-mail à tous les abonnés avec un message donné."""
    
#     abonnes = get_all_subscribers()
#     if not abonnes:
#         return {"error": "Aucun abonné trouvé"}
    
#     for email in abonnes:
#         msg = Message(subject="Nouvelle Notification",
#                       sender="lacapacitee@gmail.com",
#                       recipients=[email])
        
#         # Utiliser le contenu HTML pour le corps de l'e-mail
#         msg.html = get_email_content(notification_message)  # Utiliser le contenu HTML
        
#         try:
#             # Envelopper l'envoi d'e-mail dans un contexte d'application
#             with current_app.app_context():
#                 email.send(msg)
#                 print(f"Email envoyé à : {email}")
#         except Exception as e:
#             print(f"Erreur lors de l'envoi de l'email à {email}: {str(e)}")
    
#     return {"success": f"Emails envoyés à {len(abonnes)} abonnés"}




# from flask_mail import Message
# from app import mail
# from database import get_all_subscribers
# from templates.email_templates import get_email_content

# def send_email_to_subscribers(notification_message):
#     """Envoie un e-mail à tous les abonnés avec un message donné."""
    
#     abonnes = get_all_subscribers()
#     if not abonnes:
#         return {"error": "Aucun abonné trouvé"}
    
#     for email in abonnes:
#         msg = Message(subject="Nouvelle Notification",
#                       sender="lacapacitee@gmail.com",
#                       recipients=[email])
        
#         # Utiliser le contenu HTML pour le corps de l'e-mail
#         msg.html = get_email_content(notification_message)  # Utiliser le contenu HTML
#         # try:
#         #     mail.send(msg)
#         # except Exception as e:
#         #     return {"error": str(e)}
#         try:
#              mail.send(msg)
#              print(f"Email envoyé à : {email}")
#         except Exception as e:
#              print(f"Erreur lors de l'envoi de l'email à {email}: {str(e)}")

    
#     return {"success": f"Emails envoyés à {len(abonnes)} abonnés"}
