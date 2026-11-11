from flask import jsonify
from src.analytics import processar_analise_besst

def get_acoes():
    
    """
    Controlador que executa a varredura das empresas
    nos setores BESST já filtradas conforme os critérios
    previamente definidos
    """
    
    try:
        df_resultado = processar_analise_besst(limite_testes=5)
        
        if df_resultado.empty:
            return(
                jsonify({
                    "status": "success",
                    "total": 0,
                    "data": [],
                    "message": (
                        """
                        Nenhuma ação atendeu simultaneamente aos critérios de
                        de lucros de (10 anos) e DY > 6%.
                        """
                    ),
                }),
                200,
            )
        
        dados_json = df_resultado.to_dict(orient="records")
        
        return jsonify({"status": "success", "total": len(dados_json), "data": dados_json}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500 