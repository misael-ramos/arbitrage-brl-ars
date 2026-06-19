import requests
from config.settings import BINANCE_URL, BLUELYTICS_URL, EXCHANGERATE_URL


def get_binance_price(symbol: str) -> float:
    """Retorna o preço spot de um par na Binance. Ex: USDTBRL, BTCBRL."""
    response = requests.get(BINANCE_URL, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return float(response.json()["price"])


def get_blue_usd_ars() -> float:
    """Retorna a cotação do dólar blue em pesos argentinos via Bluelytics."""
    response = requests.get(BLUELYTICS_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    # média entre compra e venda do dólar blue
    buy  = data["blue"]["value_buy"]
    sell = data["blue"]["value_sell"]
    return (buy + sell) / 2


def get_direct_brl_ars() -> float:
    """Retorna a cotação direta BRL → ARS via ExchangeRate API."""
    response = requests.get(EXCHANGERATE_URL, timeout=10)
    response.raise_for_status()
    return float(response.json()["rates"]["ARS"])


def fetch_all_rates() -> dict:
    """
    Coleta todas as cotações necessárias e retorna um dicionário com os valores.
    Retorna None em caso de falha em qualquer uma das APIs.
    """
    try:
        usdt_brl    = get_binance_price("USDTBRL")   # quantos BRL por 1 USDT
        btc_brl     = get_binance_price("BTCBRL")    # quantos BRL por 1 BTC
        blue_usd_ars = get_blue_usd_ars()            # quantos ARS por 1 USD (blue)
        direct_brl_ars = get_direct_brl_ars()        # quantos ARS por 1 BRL (oficial)

        return {
            "usdt_brl":       usdt_brl,
            "btc_brl":        btc_brl,
            "blue_usd_ars":   blue_usd_ars,
            "direct_brl_ars": direct_brl_ars,
        }
    except Exception as e:
        print(f"Erro ao buscar cotações: {e}")
        return None
