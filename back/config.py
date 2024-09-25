import os

class Config:
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'projet_chatbot')
    DB_USER = os.environ.get('DB_USER', 'issaka')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'issaka')


# import os
#
# DB_HOST = os.environ.get('DB_HOST', 'localhost')
# DB_NAME = os.environ.get('DB_NAME', 'projet_chatbot')
# DB_USER = os.environ.get('DB_USER', 'issaka')
# DB_PASSWORD = os.environ.get('DB_PASSWORD', 'issaka')
#
# SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# import os
#
# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_for_development'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://issaka:issaka@localhost/projet_chatbot'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     # Ajoutez les variables d'environnement pour Google OAuth
#     GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
#     GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
