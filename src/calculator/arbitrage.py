from datetime import datetime, timezone


def calculate_routes(rates: dict, amount_brl: float = 100.0) -> dict:
    """
    Calcula quanto ARS o usuário recebe nas 3 rotas para um valor em BRL.

    Rotas:
      1. BRL → USDT → ARS (via dólar blue argentino)
      2. BRL → BTC  → ARS (via dólar blue argentino)
      3. BRL → ARS  direto (câmbio oficial)

    Lógica:
      - USDT é pareado 1:1 com o dólar americano
      - Então: BRL / usdt_brl = USD → USD * blue_usd_ars = ARS
      - Mesmo raciocínio para BTC (btc_brl / usdt_brl = valor em USD)
    """
    usdt_brl      = rates["usdt_brl"]
    btc_brl       = rates["btc_brl"]
    blue_usd_ars  = rates["blue_usd_ars"]
    direct_brl_ars = rates["direct_brl_ars"]

    # rota 1: BRL → USDT → ARS
    usdt_amount    = amount_brl / usdt_brl          # quantos USDT compramos
    ars_via_usdt   = usdt_amount * blue_usd_ars     # USDT ≈ USD, convertemos para ARS

    # rota 2: BRL → BTC → ARS
    btc_amount     = amount_brl / btc_brl           # quanto BTC compramos
    btc_in_usd     = btc_amount * (btc_brl / usdt_brl)  # valor do BTC em USD
    ars_via_btc    = btc_in_usd * blue_usd_ars      # convertemos para ARS

    # rota 3: direto
    ars_direto     = amount_brl * direct_brl_ars

    # melhor rota
    results = {
        "usdt": ars_via_usdt,
        "btc":  ars_via_btc,
        "direto": ars_direto,
    }
    best_route = max(results, key=results.get)

    return {
        "timestamp":    datetime.now(timezone.utc).isoformat(),
        "amount_brl":   amount_brl,
        "rates":        rates,
        "results": {
            "via_usdt":   round(ars_via_usdt, 2),
            "via_btc":    round(ars_via_btc, 2),
            "direto":     round(ars_direto, 2),
        },
        "best_route":   best_route,
        "gain_vs_direct": {
            "usdt": round(ars_via_usdt - ars_direto, 2),
            "btc":  round(ars_via_btc  - ars_direto, 2),
        },
        "rate_per_brl": {
            "usdt":   round(ars_via_usdt   / amount_brl, 4),
            "btc":    round(ars_via_btc    / amount_brl, 4),
            "direto": round(ars_direto     / amount_brl, 4),
        }
    }
