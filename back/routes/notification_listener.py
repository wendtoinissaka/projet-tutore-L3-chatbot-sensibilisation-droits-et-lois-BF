import psycopg2
import threading
from database import connect_db
from flask import current_app

# def listen_for_notifications(app):
#     """Écoute les notifications et envoie automatiquement des e-mails quand une nouvelle notification est insérée."""
    
#     from routes.email_sender import send_email_to_subscribers  # Import local

#     conn = connect_db()
#     conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#     cursor = conn.cursor()

#     # Écouter les notifications sur le canal 'new_notification'
#     cursor.execute("LISTEN new_notification;")
#     print("Écoute des nouvelles notifications...")
    
#     while True:
#         conn.poll()
#         while conn.notifies:
#             notify = conn.notifies.pop(0)
#             notification_message = notify.payload
#             print(f"Notification reçue : {notification_message}")

#             # Créer un contexte d'application ici
#             with app.app_context():
#                 send_email_to_subscribers(notification_message)

import time

def listen_for_notifications(app):
    """Écoute les notifications et envoie automatiquement des e-mails quand une nouvelle notification est insérée."""
    
    from routes.email_sender import send_email_to_subscribers  # Import local

    conn = connect_db()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Écouter les notifications sur le canal 'new_notification'
    cursor.execute("LISTEN new_notification;")
    print("Écoute des nouvelles notifications...")
    
    while True:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            notification_message = notify.payload
            print(f"Notification reçue : {notification_message}")

            # Créer un contexte d'application ici
            with app.app_context():
                send_email_to_subscribers(notification_message)

        # Attendre un peu avant de poller à nouveau
        time.sleep(30)  # Attendre 5 secondes avant de vérifier à nouveau


# Fonction pour démarrer le thread d'écoute avec l'application
def start_notification_listener(app):
    thread = threading.Thread(target=listen_for_notifications, args=(app,))
    thread.daemon = True
    thread.start()




# def listen_for_notifications():
#     """Écoute les notifications et envoie automatiquement des e-mails quand une nouvelle notification est insérée."""
    
#     from routes.email_sender import send_email_to_subscribers  # Import local

#     conn = connect_db()
#     conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#     cursor = conn.cursor()

#     # Écouter les notifications sur le canal 'new_notification'
#     cursor.execute("LISTEN new_notification;")

#     print("Écoute des nouvelles notifications...")
#     while True:
#         conn.poll()
#         while conn.notifies:
#             notify = conn.notifies.pop(0)
#             notification_message = notify.payload
#             print(f"Notification reçue : {notification_message}")

#             # Utiliser le contexte de l'application ici
#             with current_app.app_context():
#                 send_email_to_subscribers(notification_message)

# def start_notification_listener():
#     """Démarre l'écoute des notifications dans un thread séparé."""
#     thread = threading.Thread(target=listen_for_notifications)
#     thread.daemon = True
#     thread.start()



# import psycopg2
# import threading
# from database import connect_db
# from flask import current_app

# def listen_for_notifications():
#     """Écoute les notifications et envoie automatiquement des e-mails quand une nouvelle notification est insérée."""
    
#     from routes.email_sender import send_email_to_subscribers  # Import local

#     conn = connect_db()
#     conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#     cursor = conn.cursor()

#     # Écouter les notifications sur le canal 'new_notification'
#     cursor.execute("LISTEN new_notification;")

#     print("Écoute des nouvelles notifications...")
#     while True:
#         conn.poll()
#         while conn.notifies:
#             notify = conn.notifies.pop(0)
#             notification_message = notify.payload
#             print(f"Notification reçue : {notification_message}")

#             # Utiliser le contexte de l'application ici
#             with current_app.app_context():  # Assurez-vous que cela est bien utilisé ici
#                 send_email_to_subscribers(notification_message)

# # Démarrer la fonction dans un thread séparé
# def start_notification_listener():
#     thread = threading.Thread(target=listen_for_notifications)
#     thread.daemon = True
#     thread.start()





# # Démarrer la fonction dans un thread séparé
# def start_notification_listener():
#     thread = threading.Thread(target=listen_for_notifications)
#     thread.daemon = True
#     thread.start()


