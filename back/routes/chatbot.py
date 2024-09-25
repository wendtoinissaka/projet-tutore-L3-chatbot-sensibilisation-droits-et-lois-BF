from flask import Blueprint, request, jsonify
from database.db import get_db_connection

chatbot_blueprint = Blueprint('chatbot', __name__)

@chatbot_blueprint.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_question = data.get('question')

    # Simuler une réponse basique
    if "droit" in user_question.lower():
        response = "Vous pouvez poser des questions sur le droit civil, le droit du travail, ou des procédures légales."
    else:
        response = "Je ne suis pas sûr de comprendre votre question."

    return jsonify({'response': response})
