from flask import Flask
from src.routes.rotas import rotas_bp

app = Flask(__name__)

app.register_blueprint(rotas_bp)
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    