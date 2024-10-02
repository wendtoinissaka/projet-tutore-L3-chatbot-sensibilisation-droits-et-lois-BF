from flask import Flask
from flask_mail import Mail
from flask_socketio import SocketIO
from config import Config
from database import create_tables, insert_data_from_csv
from routes.routes import init_routes
from routes.notification_listener import start_notification_listener

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialiser les routes
init_routes(app, socketio)

# Démarrer l'écoute des notifications dans le bon contexte
if __name__ == '__main__':
    create_tables(app)  # Crée les tables de la base de données
    # insert_data_from_csv('QUESTIONS_CHATBOT_JURIDIQUE.csv')
    # insert_data_from_csv('./resultat_combined.csv')
    start_notification_listener(app)  # Démarre le listener en passant l'application
    print("Notification listener démarré")
    socketio.run(app, debug=True)  # Démarre l'application Flask



# from flask import Flask
# from flask_mail import Mail
# from flask_socketio import SocketIO
# from config import Config
# from database import create_tables
# from routes.routes import init_routes
# from routes.notification_listener import start_notification_listener

# app = Flask(__name__)
# app.config.from_object(Config)

# mail = Mail(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Initialiser les routes
# init_routes(app, socketio)

# # Démarrer l'écoute des notifications dans le bon contexte
# if __name__ == '__main__':
#     start_notification_listener()  # Démarre le listener
#     create_tables()  # Crée les tables de la base de données
#     socketio.run(app, debug=True)  # Démarre l'application Flask








# from flask import Flask
# from flask_mail import Mail
# from flask_socketio import SocketIO
# from config import Config
# from database import create_tables
# from routes.routes import init_routes
# from routes.notification_listener import start_notification_listener

# app = Flask(__name__)
# app.config.from_object(Config)

# mail = Mail(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Initialiser les routes
# init_routes(app, socketio)

# # Démarrer l'écoute des notifications
# # start_notification_listener()

# if __name__ == '__main__':
        
#     # Démarrer l'écoute des notifications
#     start_notification_listener()
#     create_tables()
#     socketio.run(app, debug=True)



# # from flask import Flask
# # from database import create_tables
# from routes.routes import main_routes
# # from flask_socketio import SocketIO
# from config import app, mail
# from mailbox import Message
# # app = Flask(__name__)
# # # socketio = SocketIO(app)  # Initialisation de SocketIO
# # socketio = SocketIO(app, cors_allowed_origins="*")  # Autoriser les origines cross-domain
# # # Enregistrer le blueprint
# # app.register_blueprint(main_routes)


# # if __name__ == '__main__':
# #     create_tables()  # Créer les tables si elles n'existent pas
# #     socketio.run(app, debug=True)  # Utilisation de socketio.run au lieu de app.run
# from flask import Flask, jsonify, request
# from flask_socketio import SocketIO, emit

# # from database import create_tables
# # from db import insert_data_from_csv
# from database import create_tables, insert_data_from_csv
# # from db import create_tables, insert_data_from_csv
# app = Flask(__name__)
# # Configuration de Flask-Mail pour utiliser Gmail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'lacapacitee@gmail.com'  # Remplace avec ton adresse Gmail
# app.config['MAIL_PASSWORD'] = '#Bac,2@21'  # Remplace avec ton mot de passe Gmail
# app.config['MAIL_DEFAULT_SENDER'] = ('VEENGE-MAAN-CHATBOT-JURIDIQUE', 'lacapacitee@gmail.com')  # Remplace avec ton nom d'application
# app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_ASCII_ATTACHMENTS'] = False

# mail = Mail(app)

# socketio = SocketIO(app)

# # Route to get notifications
# @app.route('/notifications', methods=['GET'])
# def get_notifications():
#     # Simulation de données de notification, remplace ça par tes données réelles
#     notifications = [{"message": "Nouvelle notification", "created_at": "2023-09-26"}]
#     return jsonify(notifications)

# # Route to add notification
# @app.route('/add_notification', methods=['POST'])
# def add_notification():
#     data = request.json
#     message = data.get('message')
    
#     # Émettre une notification via WebSocket à tous les clients connectés
#     socketio.emit('new_notification', {'message': message})
    
#     return jsonify({"status": "Notification envoyée"}), 200


# # Enregistrement du blueprint
# app.register_blueprint(main_routes)


# if __name__ == '__main__':
#     create_tables()  # Créer les tables si elles n'existent pas
#     # Insérer des données depuis le fichier CSV
#     insert_data_from_csv('QUESTIONS_CHATBOT_JURIDIQUE.csv')

#     socketio.run(app, debug=True)



# from flask import Flask
# from database import create_tables
# from routes.routes import main_routes  
# app = Flask(__name__)

# # Enregistrer le blueprint
# app.register_blueprint(main_routes)

# if __name__ == '__main__':
#     create_tables()  # Créer les tables si elles n'existent pas
#     app.run(debug=True)
