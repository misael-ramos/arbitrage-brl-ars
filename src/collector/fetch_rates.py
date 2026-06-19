import requests
from config.settings import BLUELYTICS_URL, EXCHANGERATE_URL

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_coingecko_prices() -> dict:
    """Retorna preços de USDT e BTC em BRL via CoinGecko."""
    response = requests.get(
        COINGECKO_URL,
        params={
            "ids": "tether,bitcoin",
            "vs_currencies": "brl"
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return {
        "usdt_brl": float(data["tether"]["brl"]),
        "btc_brl":  float(data["bitcoin"]["brl"]),
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
        prices         = get_coingecko_prices()
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