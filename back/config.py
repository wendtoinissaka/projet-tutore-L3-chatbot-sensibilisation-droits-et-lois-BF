import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_for_development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://issaka:issaka@localhost/legal_chatbot'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ajoutez les variables d'environnement pour Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
