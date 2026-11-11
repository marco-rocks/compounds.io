from flask import Flask, jsonify
from src.routes.rotas import rotas_bp

app = Flask(__name__)

app.register_blueprint(rotas_bp, url_prefix="/api")

@app.route("/", methods=['GET'])
def index():
    """
    Rota raiz informando o status da API do compounds.io
    """
    
    return jsonify({
        "project": "compounds.io",
        "description": (
            """
            API quantitativa para seleção de ações
            da B3 baseada na metodologia Buy and Hold
            e setores BESST
            """
        ),
        "status": "online",
        "endpoints": {"analise": "/api/analise"}
    })
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    