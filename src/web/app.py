import json
import time
from flask import Flask, render_template, jsonify, request
from src.collector.fetch_rates import fetch_all_rates
from src.calculator.arbitrage import calculate_routes
from src.storage.save_history import save_to_s3, load_today_history

app = Flask(__name__)

# cache com TTL de 20 minutos
_cache = {"data": None, "fetched_at": 0}
CACHE_TTL = 1200

# popula o cache na inicialização
import time
print("Inicializando cache...")
_rates = fetch_all_rates()
if _rates:
    _cache["data"] = calculate_routes(_rates, 100.0)
    _cache["fetched_at"] = time.time()
    print("Cache inicializado com sucesso.")
else:
    print("Falha ao inicializar cache.")

def get_fresh_data(amount_brl: float = 100.0) -> dict:
    now = time.time()
    # só chama a API se o cache estiver vazio ou expirado
    if not _cache["data"] or (now - _cache["fetched_at"]) > CACHE_TTL:
        rates = fetch_all_rates()
        if not rates:
            return None
        _cache["data"] = calculate_routes(rates, 100.0)
        _cache["fetched_at"] = now

    # recalcula para o valor solicitado sem chamar a API
    rates = _cache["data"]["rates"]
    return calculate_routes(rates, amount_brl)


@app.route("/")
def index():
    data = get_fresh_data(100.0)
    print("DEBUG data:", data)
    data_json = json.dumps(data) if data else "null"
    print("DEBUG data_json:", data_json[:100] if data_json else "null")
    return render_template("index.html", data_json=data_json)


@app.route("/api/rates")
def api_rates():
    amount = float(request.args.get("amount", 100))
    data = get_fresh_data(amount)
    if not data:
        return jsonify({"error": "Falha ao buscar cotações"}), 500
    return jsonify(data)


@app.route("/api/calculate")
def api_calculate():
    amount = float(request.args.get("amount", 100))
    if not _cache["data"]:
        return jsonify({"error": "Nenhuma cotação em cache"}), 400
    rates = _cache["data"]["rates"]
    result = calculate_routes(rates, amount)
    return jsonify(result)


@app.route("/api/history")
def api_history():
    history = load_today_history()
    return jsonify(history)


@app.route("/api/save", methods=["POST"])
def api_save():
    data = get_fresh_data(100.0)
    if not data:
        return jsonify({"error": "Falha ao buscar cotações"}), 500
    save_to_s3(data)
    return jsonify({"status": "ok", "timestamp": data["timestamp"]})


if __name__ == "__main__":
    app.run(debug=True, port=5000)