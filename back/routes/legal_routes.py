from flask import Blueprint, jsonify
from models import LegalInfo

legal_bp = Blueprint('legal', __name__)

@legal_bp.route('/legal-info', methods=['GET'])
def get_legal_info():
    legal_info = LegalInfo.query.all()
    results = [
        {
            "id": info.id,
            "title": info.title,
            "content": info.content,
            "category": info.category
        } for info in legal_info
    ]
    return jsonify(results), 200
