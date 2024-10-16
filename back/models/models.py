import uuid
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin  # Import UserMixin for user management

db = SQLAlchemy()



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(36), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<ChatHistory {self.question[:20]}>'  # Affiche les 20 premiers caractères de la question


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Notification {self.message[:20]}>'  # Affiche les 20 premiers caractères du message


class FAQ(db.Model):
    __tablename__ = 'faq'

    id = db.Column(db.Integer, primary_key=True)
    categorie = db.Column(db.Text, nullable=False)
    tag = db.Column(db.Text)
    question = db.Column(db.Text, nullable=False, unique=True)  # Rendre la question unique
    reponse = db.Column(db.Text, nullable=False)
    article_reference = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<FAQ {self.question[:20]}>'  # Affiche les 20 premiers caractères de la question


class Abonnee(db.Model):
    __tablename__ = 'abonnee'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    numero = db.Column(db.String(20), unique=True)
    date_abonnement = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Abonnee {self.email}>'  # Affiche l'email de l'abonné


# Modèle pour les procédures juridiques
class Procedure(db.Model):
    __tablename__ = 'procedures'  # Nom de la table dans la base de données

    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique
    # type = db.Column(db.String(50))  # Type de la procédure
    titre = db.Column(db.String(255), nullable=False)  # Titre de la procédure
    description_texte = db.Column(db.Text)  # Description textuelle
    description_pieces_a_fournir = db.Column(db.Text)  # Pièces à fournir
    description_cout = db.Column(db.Text)  # Coût associé
    description_conditions_acces = db.Column(db.Text)  # Conditions d'accès
    source = db.Column(db.String(255))  # Source de la procédure
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __repr__(self):
        return f'<Procedure {self.titre}>'


class Avocat(db.Model):
    __tablename__ = 'avocats'

    id = db.Column(db.Integer, primary_key=True)
    nom_prenom = db.Column(db.String(100), nullable=False)
    specialisation = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Avocat {self.nom_prenom}>'


class UserContext(db.Model):
    __tablename__ = 'user_context'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)  # identifiant unique pour chaque utilisateur
    step = db.Column(db.String(50), nullable=False)     # état actuel de la conversation ("waiting_specialisation", "waiting_quartier", etc.)
    specialisation = db.Column(db.String(100), nullable=True)  # stocker la spécialisation une fois fournie
    ville = db.Column(db.String(100), nullable=True)        # stocker le quartier une fois fourni


class UserAdmin(db.Model, UserMixin):  # Inherit from UserMixin
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Updated length

    def __repr__(self):
        return f'<User {self.username}>'


class CodeCivil1(db.Model):
    __tablename__ = 'code_civil1'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # L'identifiant auto-incrémenté
    article_num = db.Column(db.Integer, unique=True, nullable=False)  # Le numéro de l'article
    texte = db.Column(db.Text, nullable=False)  # Le texte de l'article

    def __repr__(self):
        return f'<CodeCivil1 {self.article_num}>'


class CodeFamille1(db.Model):
    __tablename__ = 'code_famille1'

    id = db.Column(db.Integer, primary_key=True)
    article_num = db.Column(db.Integer, unique=True, nullable=False)
    texte = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<CodeFamille1 {self.article_num}>'


class CodePenal1(db.Model):
    __tablename__ = 'code_penale1'

    id = db.Column(db.Integer, primary_key=True)
    article_num = db.Column(db.Integer, unique=True, nullable=False)
    texte = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<CodePenal1 {self.article_num}>'
    

class CodeTravail1(db.Model):
    __tablename__ = 'code_travail1'

    id = db.Column(db.Integer, primary_key=True)
    article_num = db.Column(db.Integer, unique=True, nullable=False)
    texte = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<CodeTravail1 {self.article_num}>'