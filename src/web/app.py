from flask import Flask, render_template, jsonify, request
from src.collector.fetch_rates import fetch_all_rates
from src.calculator.arbitrage import calculate_routes
from src.storage.save_history import save_to_s3, load_today_history

app = Flask(__name__)

# cache simples em memória para não chamar a API a cada clique
_cache = {"data": None}


def get_fresh_data(amount_brl: float = 100.0) -> dict:
    rates = fetch_all_rates()
    if not rates:
        return None
    return calculate_routes(rates, amount_brl)


@app.route("/")
def index():
    """Página principal — carrega com dados de R$ 100."""
    data = get_fresh_data(100.0)
    _cache["data"] = data
    return render_template("index.html", data=data)


@app.route("/api/rates")
def api_rates():
    """Retorna cotações frescas em JSON para o botão Atualizar."""
    amount = float(request.args.get("amount", 100))
    data = get_fresh_data(amount)
    if not data:
        return jsonify({"error": "Falha ao buscar cotações"}), 500
    _cache["data"] = data
    return jsonify(data)


@app.route("/api/calculate")
def api_calculate():
    """Recalcula para um valor customizado sem chamar as APIs novamente."""
    amount = float(request.args.get("amount", 100))
    if not _cache["data"]:
        return jsonify({"error": "Nenhuma cotação em cache"}), 400
    rates = _cache["data"]["rates"]
    result = calculate_routes(rates, amount)
    return jsonify(result)


@app.route("/api/history")
def api_history():
    """Retorna o histórico do dia atual do S3."""
    history = load_today_history()
    return jsonify(history)


@app.route("/api/save", methods=["POST"])
def api_save():
    """Salva o snapshot atual no S3 (chamado pelo cron a cada hora)."""
    data = get_fresh_data(100.0)
    if not data:
        return jsonify({"error": "Falha ao buscar cotações"}), 500
    save_to_s3(data)
    return jsonify({"status": "ok", "timestamp": data["timestamp"]})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
