import os
from dotenv import load_dotenv
from flask import Flask, session
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_session import Session  # Importer Flask-Session
from admin import create_admin, create_admin_user
from config import Config
from database import create_tables, insert_avocats_from_csv, insert_data_from_csv, insert_precedure_data_from_csv
from routes.notification_listener import start_notification_listener
from routes.routes import init_routes
from stockage_nettoyage_donnees.insertion_article_civil import load_and_insert_articles_civil
from stockage_nettoyage_donnees.insertion_article_code_famille import load_and_insert_articles_famille
from stockage_nettoyage_donnees.insertion_article_code_penale import load_and_insert_articles_penale
from stockage_nettoyage_donnees.insertion_article_code_travail import load_and_insert_articles_travail
# from stockage_nettoyage_donnees.insertion_article_code_famille import load_and_insert_articles_famille
# from stockage_nettoyage_donnees.insertion_article_code_famille import load_and_insert_articles_famille

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)


mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialiser l'interface d'administration
create_admin(app)

# Initialiser les routes
init_routes(app, socketio)


if __name__ == '__main__':
    create_tables(app)  # Crée les tables de la base de données
    # Insérez les données après la création des tables
    # insert_data_from_csv('faq_chatbot.csv')
    # insert_precedure_data_from_csv('procedures_juridiques_administratives.csv')
    # insert_avocats_from_csv("contacts_avocats.csv")
    # load_and_insert_articles_civil('stockage_nettoyage_donnees/test_code_civil_apres_traitement1.json', app)
    # load_and_insert_articles_famille('stockage_nettoyage_donnees/articles_code_personnes_et_famille1.json', app.app_context())
    # load_and_insert_articles_penale('stockage_nettoyage_donnees/articles_code_penale.json', app.app_context())
    # load_and_insert_articles_travail('stockage_nettoyage_donnees/test_code_du_travail_apres_traitement.json', app.app_context())

    start_notification_listener(app)  # Démarre le listener en passant l'application
    create_admin_user(app)
    
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
