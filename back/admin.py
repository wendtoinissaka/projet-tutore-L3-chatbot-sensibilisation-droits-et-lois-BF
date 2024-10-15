from flask import Blueprint, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.models import FAQ, Abonnee, ChatHistory, Notification, Procedure, User, UserAdmin

# Initialisation de Flask-Login
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserAdmin.query.get(int(user_id))

# Vue d'administration sécurisée
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated  # Vérifie si l'utilisateur est authentifié

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_routes.login', next=request.url))  # Mettez à jour le nom ici

class ProcedureView(SecureModelView):
    column_default_sort = ('created_at', False)  # Tri par défaut sur 'created_at' par ordre croissant

class ChatHistoryView(SecureModelView):
    column_default_sort = ('created_at', False)  # Tri par défaut sur 'created_at' par ordre croissant


class NotificationView(SecureModelView):
    column_default_sort = ('created_at', False)  # Tri par défaut sur 'created_at' par ordre croissant

# Créer un Blueprint pour les routes d'administration
admin_blueprint = Blueprint('admin_routes', __name__)

# Routes de connexion et déconnexion
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Variable pour stocker les messages d'erreur
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserAdmin.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))  # Redirige vers la page d'administration
        else:
            error = 'Nom d’utilisateur ou mot de passe incorrect.'  # Message d'erreur

    return render_template('login.html', error=error)  # Passer l'erreur au template

@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_routes.login'))  # Mettez à jour le nom ici

def create_admin(app):
    # Configurer Flask-Login avec l'application
    login_manager.init_app(app)

    # Créer une instance de l'interface d'administration
    admin = Admin(app, name='VEENGE MAAN CHATBOT', template_mode='bootstrap3')

    # Ajouter les modèles à l'interface d'administration
    admin.add_view(ProcedureView(Procedure, db.session))
    admin.add_view(ChatHistoryView(ChatHistory, db.session))
    admin.add_view(NotificationView(Notification, db.session))
    admin.add_view(SecureModelView(FAQ, db.session))
    admin.add_view(SecureModelView(Abonnee, db.session))
    admin.add_view(ModelView(User, db.session))

    # Enregistrer le Blueprint
    app.register_blueprint(admin_blueprint)

def create_admin_user(app):
    with app.app_context():
        if not UserAdmin.query.filter_by(username='admin').first():  # Vérifie si l'utilisateur existe déjà
            admin = UserAdmin(username='admin', password=generate_password_hash('admin_password'))  # Hachage du mot de passe
            db.session.add(admin)
            db.session.commit()
            print("Administrateur créé avec succès.")
        else:
            print("L'utilisateur administrateur existe déjà.")



