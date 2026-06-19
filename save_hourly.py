"""
Script chamado pelo cron a cada hora para salvar o snapshot no S3.

Adicione ao crontab:
0 * * * * cd /caminho/para/arbitrage-brl-ars && source venv/bin/activate && python save_hourly.py
"""
from src.collector.fetch_rates import fetch_all_rates
from src.calculator.arbitrage import calculate_routes
from src.storage.save_history import save_to_s3

if __name__ == "__main__":
    print("Coletando cotações...")
    rates = fetch_all_rates()
    if not rates:
        print("Falha ao buscar cotações.")
        exit(1)

    data = calculate_routes(rates, amount_brl=100.0)
    save_to_s3(data)
    print(f"Snapshot salvo. Melhor rota: {data['best_route'].upper()}")
