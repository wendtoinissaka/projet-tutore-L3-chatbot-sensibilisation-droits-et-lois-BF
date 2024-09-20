from flask import Blueprint, request, jsonify
# from chatbot import generate_response  # Hypothétique fonction pour générer des réponses du bot

from services.chatbot_service import process_question

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/ask', methods=['POST'])
def ask_question():
    user_input = request.json.get('question')
    if not user_input:
        return jsonify({"error": "No question provided"}), 400

    # Appelle du modèle (qu'on intégrera plus tard)
    bot_response = process_question(user_input)
    return jsonify({"response": bot_response})
