from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from models import Procedure, ChatHistory  # Importer les modèles
from database import db
from models.models import FAQ, Abonnee, ChatHistory, Notification, Procedure  # Importer l'instance de ta base de données

class ProcedureView(ModelView):
    # Tri par défaut sur la colonne 'date' par ordre décroissant
    column_default_sort = ('created_at', True)  # True pour tri descendant, False pour ascendant
class ChatbHisoryView(ModelView):
    # Tri par défaut sur la colonne 'date' par ordre décroissant
    column_default_sort = ('created_at', True)  # True pour tri descendant, False pour ascendant

class NotificationView(ModelView):
    # Tri par défaut sur 'created_at' par ordre croissant
    column_default_sort = ('created_at', False)

def create_admin(app):
    # Créer une instance de l'interface d'administration
    admin = Admin(app, name='VEENGE MAAN CHATBOT', template_mode='bootstrap3')


def create_admin(app):
    # Créer une instance de l'interface d'administration
    admin = Admin(app, name='VEENGE MAAN CHATBOT', template_mode='bootstrap3')

    # Ajouter les modèles à l'interface d'administration
    admin.add_view(ProcedureView(Procedure, db.session))
    admin.add_view(ChatbHisoryView(ChatHistory, db.session))  # Sans tri spécifique
    admin.add_view(NotificationView(Notification, db.session))
    admin.add_view(ModelView(FAQ, db.session))
    admin.add_view(ModelView(Abonnee, db.session))

