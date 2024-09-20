from flask_migrate import Migrate
from models import db
from config import Config
from flask import Flask
from routes.chatbot_routes import chatbot_bp
from routes.auth_routes import auth_bp
from routes.legal_routes import legal_bp
from flask_cors import CORS  # Pour gérer les requêtes cross-origin

# Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Activer CORS pour permettre au frontend de communiquer avec le backend
CORS(app)

# Initialisation de la base de données
db.init_app(app)

# Ajouter la gestion des migrations
migrate = Migrate(app, db)

# Enregistrement des routes
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(legal_bp, url_prefix='/api/legal')

if __name__ == '__main__':
    app.run(debug=True)
