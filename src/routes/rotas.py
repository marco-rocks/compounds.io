from flask import Blueprint, render_template
from src.controllers.analytics_controller import(
    get_acoes_besst,
    get_ativo_unico
)

rotas_bp = Blueprint("rotas_bp", __name__)

@rotas_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@rotas_bp.route('/analise-besst', methods=['GET', 'POST'])
def analise_besst():

    # Rota responsável por acionar o controlador de varredura das ações.
    return get_acoes_besst()

@rotas_bp.route('/analise-ativo-unico', methods=['GET', 'POST'])
def analise_ativo_unico():
    
    # Rota responsável por acionar o controlador de varredura de ativos únicos
    return get_ativo_unico()