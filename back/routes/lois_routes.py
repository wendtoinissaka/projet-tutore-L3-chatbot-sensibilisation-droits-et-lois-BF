from flask import Blueprint, jsonify

from services.lois_services import get_all_lois

# from services.loi_service import get_all_lois

lois_bp = Blueprint('lois', __name__)

@lois_bp.route('/api/lois/travail', methods=['GET'])
def get_lois_travail():
    lois = get_all_lois()
    return jsonify([{'id': loi.id, 'titre': loi.titre, 'contenu': loi.contenu} for loi in lois])

def register_routes(app):
    app.register_blueprint(lois_bp)
