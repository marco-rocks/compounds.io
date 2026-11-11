from flask import Blueprint
from src.controllers.analytics_controller import get_acoes

rotas_bp = Blueprint("rotas_bp", __name__)

@rotas_bp.route('/analise', methods=['GET'])
def analise():
    """
    Rota responsável por acionar o controlador de varredura das ações.
    """
    return get_acoes()
    