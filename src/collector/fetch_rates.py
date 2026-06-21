import requests
from config.settings import BLUELYTICS_URL, EXCHANGERATE_URL

AWESOMEAPI_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL,BTC-BRL,USDT-BRL"


def get_awesomeapi_prices() -> dict:
    response = requests.get(AWESOMEAPI_URL, timeout=10)

    print("STATUS AWESOME:", response.status_code)
    print("BODY AWESOME:", response.text[:500])

    response.raise_for_status()

    data = response.json()

    return {
        "usdt_brl": float(data["USDTBRL"]["bid"]),
        "btc_brl": float(data["BTCBRL"]["bid"]),
    }


def get_blue_usd_ars() -> float:
    """Retorna a cotação do dólar blue em pesos argentinos via Bluelytics."""
    response = requests.get(BLUELYTICS_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    buy  = data["blue"]["value_buy"]
    sell = data["blue"]["value_sell"]
    return (buy + sell) / 2


def get_direct_brl_ars() -> float:
    """Retorna a cotação direta BRL → ARS via ExchangeRate API."""
    response = requests.get(EXCHANGERATE_URL, timeout=10)
    response.raise_for_status()
    return float(response.json()["rates"]["ARS"])


def fetch_all_rates() -> dict:
    try:
        prices         = get_awesomeapi_prices()
        blue_usd_ars   = get_blue_usd_ars()
        direct_brl_ars = get_direct_brl_ars()

        return {
            "usdt_brl":       prices["usdt_brl"],
            "btc_brl":        prices["btc_brl"],
            "blue_usd_ars":   blue_usd_ars,
            "direct_brl_ars": direct_brl_ars,
        }
    except Exception as e:
        print(f"Erro ao buscar cotações: {e}")
        return None