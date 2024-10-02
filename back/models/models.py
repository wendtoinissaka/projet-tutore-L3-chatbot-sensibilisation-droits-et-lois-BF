# app/models/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    sous_categorie = db.Column(db.Text)
    question = db.Column(db.Text, nullable=False, unique=True)  # Rendre la question unique
    reponse = db.Column(db.Text, nullable=False)
    article_reference = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<FAQ {self.question[:20]}>'  # Affiche les 20 premiers caractères de la question



# class FAQ(db.Model):
#     __tablename__ = 'faq'

#     id = db.Column(db.Integer, primary_key=True)
#     categorie = db.Column(db.Text, nullable=False)
#     tag = db.Column(db.Text)
#     sous_categorie = db.Column(db.Text)
#     question = db.Column(db.Text, nullable=False)
#     reponse = db.Column(db.Text, nullable=False)
#     article_reference = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<FAQ {self.question[:20]}>'  # Affiche les 20 premiers caractères de la question

class Abonnee(db.Model):
    __tablename__ = 'abonnee'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    numero = db.Column(db.String(20), unique=True)
    date_abonnement = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Abonnee {self.email}>'  # Affiche l'email de l'abonné








# # app/models/models.py
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# # class Article(db.Model):
# #     __tablename__ = 'articles'

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String(100), nullable=False)
# #     content = db.Column(db.Text, nullable=False)
# #     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# #     def __repr__(self):
# #         return f'<Article {self.title}>'

# class Notification(db.Model):
#     __tablename__ = 'notifications'

#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     is_read = db.Column(db.Boolean, default=False)

#     def __repr__(self):
#         return f'<Notification {self.message[:20]}>'  # Affiche les 20 premiers caractères du message
