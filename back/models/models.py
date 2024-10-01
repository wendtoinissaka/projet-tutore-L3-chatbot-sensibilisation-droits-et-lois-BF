# app/models/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Article(db.Model):
#     __tablename__ = 'articles'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<Article {self.title}>'

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Notification {self.message[:20]}>'  # Affiche les 20 premiers caractères du message
