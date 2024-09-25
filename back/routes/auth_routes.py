from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from database.models import User, db
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
from config import Config

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

auth_bp = Blueprint('auth_bp', __name__)

# Google OAuth setup
google_bp = make_google_blueprint(
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    redirect_to="auth_bp.google_login"
)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/google-login')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    info = resp.json()
    user = User.query.filter_by(email=info["email"]).first()

    if user is None:
        user = User(email=info["email"], google_id=info["id"])
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return jsonify({"message": "Login with Google successful"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
