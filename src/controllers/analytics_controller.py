from flask import jsonify, render_template, request
from src.analytics import processar_analise_besst, processar_ativo_individual


def render_home_controller():
  """Renderiza a página HTML inicial (GET)."""
  return render_template("index.html")


def get_acoes_besst():
  """Controlador que executa a varredura das empresas

  nos setores BESST já filtradas conforme os critérios
  previamente definidos
  """
  if request.method == "POST":
    try:
      df_resultado = processar_analise_besst()

      if df_resultado.empty:
        return (
            jsonify({
                "status": "success",
                "total": 0,
                "data": [],
                "message": (
                    "Nenhuma ação atendeu simultaneamente aos critérios de"
                    " lucros de (10 anos) e DY > 6%."
                ),
            }),
            200,
        )

      dados_json = df_resultado.to_dict(orient="records")

      return jsonify({"status": "success", "total": len(dados_json), "data": dados_json}), 200

    except Exception as e:
      return jsonify({"status": "error", "message": str(e)}), 500

  return jsonify({"status": "error", "message": "Método não permitido"}), 405


def get_ativo_unico():
  if request.method == "POST":
    # Tenta ler do corpo JSON/Form, e se não achar, busca na URL (request.args)
    data = request.get_json(silent=True, force=True) or request.form
    ticker_input = data.get("ticker") or request.args.get("ticker", "")
    ticker_input = ticker_input.strip()

    # Controlador para analisar um ticker único enviado via formulário ou URL
    if not ticker_input:
      return (
          jsonify({
              "status": "error",
              "message": "Parâmetro 'ticker' não informado",
          }),
          400,
      )

    resultado = processar_ativo_individual(ticker_input)

    if "erro" in resultado:
      return (
          jsonify({
              "status": "fail",
              "ticker": ticker_input.upper(),
              "message": resultado["erro"],
          }),
          404,
      )

    return jsonify({"status": "success", "data": resultado}), 200

  return jsonify({"status": "error", "message": "Método não permitido"}), 405